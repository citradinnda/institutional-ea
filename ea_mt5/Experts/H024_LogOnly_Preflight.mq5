#property strict
#property version   "0.600"
#property description "H024 log-only runtime preflight. Research only."

input bool   InpKillSwitchBlocked = true;
input string InpRunLabel = "H024_LOG_ONLY_PREFLIGHT";
input string InpSchemaVersion = "h024_ea_log_only_preflight_v2";
input string InpEaVersion = "0.6";
input string InpSourceVersion = "manual";
input string InpRuntimeMode = "log_only_preflight";
input double InpRiskFraction = 0.01;
input string InpOutputFile = "h024_ea_log_only_preflight.csv";
input int    InpTimerSeconds = 1;
input int    InpH024ClosedShift = 1;

int g_file_handle = INVALID_HANDLE;

int H024EffectiveClosedShift()
{
   if(InpH024ClosedShift < 1)
   {
      return 1;
   }
   if(InpH024ClosedShift > 240)
   {
      return 240;
   }
   return InpH024ClosedShift;
}

string BoolText(const bool value)
{
   return value ? "true" : "false";
}

string LongText(const long value)
{
   return IntegerToString(value);
}

bool OpenLogFile()
{
   g_file_handle = FileOpen(
      InpOutputFile,
      FILE_READ | FILE_WRITE | FILE_CSV | FILE_ANSI | FILE_SHARE_READ,
      ','
   );

   if(g_file_handle == INVALID_HANDLE)
   {
      Print("H024 log-only preflight failed to open log file: ", InpOutputFile);
      return false;
   }

   if(FileSize(g_file_handle) == 0)
   {
      FileWrite(
         g_file_handle,
         "generated_at_server",
         "schema_version",
         "ea_version",
         "source_version",
         "timer_seconds",
         "runtime_mode",
         "run_label",
         "event",
         "kill_switch_blocked",
         "symbol",
         "account_company",
         "account_server",
         "account_currency",
         "account_balance",
         "account_equity",
         "account_leverage",
         "account_trade_allowed",
         "account_trade_expert",
         "terminal_connected",
         "terminal_trade_allowed",
         "mql_trade_allowed",
         "bid",
         "ask",
         "spread_points",
         "volume_min",
         "volume_max",
         "volume_step",
         "stops_level",
         "freeze_level",
         "point",
         "digits",
         "detail"
      );
   }

   FileSeek(g_file_handle, 0, SEEK_END);
   return true;
}

void WritePreflightRow(const string event_name, const string detail)
{
   if(g_file_handle == INVALID_HANDLE)
   {
      return;
   }

   MqlTick tick;
   bool tick_ok = SymbolInfoTick(_Symbol, tick);

   FileWrite(
      g_file_handle,
      TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS),
      InpSchemaVersion,
      InpEaVersion,
      InpSourceVersion,
      IntegerToString(InpTimerSeconds),
      InpRuntimeMode,
      InpRunLabel,
      event_name,
      BoolText(InpKillSwitchBlocked),
      _Symbol,
      AccountInfoString(ACCOUNT_COMPANY),
      AccountInfoString(ACCOUNT_SERVER),
      AccountInfoString(ACCOUNT_CURRENCY),
      DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE), 2),
      DoubleToString(AccountInfoDouble(ACCOUNT_EQUITY), 2),
      LongText(AccountInfoInteger(ACCOUNT_LEVERAGE)),
      BoolText((bool)AccountInfoInteger(ACCOUNT_TRADE_ALLOWED)),
      BoolText((bool)AccountInfoInteger(ACCOUNT_TRADE_EXPERT)),
      BoolText((bool)TerminalInfoInteger(TERMINAL_CONNECTED)),
      BoolText((bool)TerminalInfoInteger(TERMINAL_TRADE_ALLOWED)),
      BoolText((bool)MQLInfoInteger(MQL_TRADE_ALLOWED)),
      tick_ok ? DoubleToString(tick.bid, (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS)) : "",
      tick_ok ? DoubleToString(tick.ask, (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS)) : "",
      LongText(SymbolInfoInteger(_Symbol, SYMBOL_SPREAD)),
      DoubleToString(SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN), 2),
      DoubleToString(SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX), 2),
      DoubleToString(SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP), 2),
      LongText(SymbolInfoInteger(_Symbol, SYMBOL_TRADE_STOPS_LEVEL)),
      LongText(SymbolInfoInteger(_Symbol, SYMBOL_TRADE_FREEZE_LEVEL)),
      DoubleToString(SymbolInfoDouble(_Symbol, SYMBOL_POINT), 10),
      LongText(SymbolInfoInteger(_Symbol, SYMBOL_DIGITS)),
      detail
   );

   FileFlush(g_file_handle);
}

void WriteIntentRow()
{
   string intent_detail = InpKillSwitchBlocked ? "NO_ACTION:kill_switch_blocked" : "NO_ACTION:log_only_unblocked";
   WritePreflightRow("INTENT", intent_detail);
}

string H024StrategyIntentDetail()
{
   MqlRates rates[];
   ArraySetAsSeries(rates, true);

   const int copied = CopyRates(_Symbol, PERIOD_H4, 0, 256, rates);
   if(copied < 10)
   {
      return "NO_ACTION:strategy_unavailable_insufficient_h4_warmup";
   }

   const int closed_shift = H024EffectiveClosedShift();
   const int slow_window = 5;
   const int slope_lag = 2;
   const int atr_window = 3;
   const int pullback_window = 3;
   const double min_pullback_atr = 0.25;
   const double max_pullback_atr = 3.0;
   const double min_slope_atr = 0.05;

   const double slow_ma = SimpleMeanClose(rates, closed_shift, slow_window);
   const double slow_ma_lag = SimpleMeanClose(rates, closed_shift + slope_lag, slow_window);
   const double atr = WilderAtrForClosedBar(rates, closed_shift, atr_window);
   const double previous_atr = WilderAtrForClosedBar(rates, closed_shift + 1, atr_window);

   const double slope = slow_ma - slow_ma_lag;
   const double slope_threshold = atr * min_slope_atr;

   const bool trend_up = rates[closed_shift].close > slow_ma && slope > slope_threshold;
   const bool trend_down = rates[closed_shift].close < slow_ma && slope < -slope_threshold;

   const bool previous_bearish = rates[closed_shift + 1].close < rates[closed_shift + 1].open;
   const bool previous_bullish = rates[closed_shift + 1].close > rates[closed_shift + 1].open;

   const double recent_high_before_signal = HighestHighBeforeSignal(rates, closed_shift, pullback_window);
   const double recent_low_before_signal = LowestLowBeforeSignal(rates, closed_shift, pullback_window);

   double long_pullback_depth_atr = EMPTY_VALUE;
   double short_pullback_depth_atr = EMPTY_VALUE;
   if(previous_atr > 0.0 && previous_atr != EMPTY_VALUE)
   {
      long_pullback_depth_atr = (recent_high_before_signal - rates[closed_shift + 1].low) / previous_atr;
      short_pullback_depth_atr = (rates[closed_shift + 1].high - recent_low_before_signal) / previous_atr;
   }

   const bool long_pullback_ok = (
      long_pullback_depth_atr != EMPTY_VALUE &&
      long_pullback_depth_atr >= min_pullback_atr &&
      long_pullback_depth_atr <= max_pullback_atr
   );
   const bool short_pullback_ok = (
      short_pullback_depth_atr != EMPTY_VALUE &&
      short_pullback_depth_atr >= min_pullback_atr &&
      short_pullback_depth_atr <= max_pullback_atr
   );

   const bool long_resumption = rates[closed_shift].close > rates[closed_shift + 1].high;
   const bool short_resumption = rates[closed_shift].close < rates[closed_shift + 1].low;

   const bool long_signal_observed = trend_up && previous_bearish && long_pullback_ok && long_resumption;
   const bool short_signal_observed = trend_down && previous_bullish && short_pullback_ok && short_resumption;

   if(long_signal_observed && short_signal_observed)
   {
      return "BLOCKED:strategy_conflict_log_only";
   }
   if(long_signal_observed)
   {
      return StringFormat(
         "WOULD_OPEN:side=long;closed_h4_time=%s;source=H024_STATE_OBSERVATION;mode=log_only_no_execution",
         TimeToString(rates[closed_shift].time, TIME_DATE | TIME_SECONDS)
      );
   }
   if(short_signal_observed)
   {
      return StringFormat(
         "WOULD_OPEN:side=short;closed_h4_time=%s;source=H024_STATE_OBSERVATION;mode=log_only_no_execution",
         TimeToString(rates[closed_shift].time, TIME_DATE | TIME_SECONDS)
      );
   }

   return StringFormat(
      "NO_ACTION:strategy_no_signal;closed_h4_time=%s;mode=log_only_no_execution",
      TimeToString(rates[closed_shift].time, TIME_DATE | TIME_SECONDS)
   );
}

void WriteH024StrategyIntentRow()
{
   WritePreflightRow("INTENT", H024StrategyIntentDetail());
}

//+------------------------------------------------------------------+
//| Pure Math Position Sizing (H020 Contract)                        |
//| Isolated from execution state for strict testability              |
//+------------------------------------------------------------------+
double ComputeH024LotSize(
   const double account_balance_usd,
   const double risk_fraction,
   const double entry_price,
   const double stop_price,
   const double tick_size,
   const double tick_value_usd_per_lot,
   const double volume_step,
   const double min_volume,
   const double max_volume,
   const int volume_digits = 2
)
{
   if(account_balance_usd <= 0.0 ||
      risk_fraction <= 0.0 ||
      risk_fraction > 1.0 ||
      entry_price <= 0.0 ||
      stop_price <= 0.0 ||
      tick_size <= 0.0 ||
      tick_value_usd_per_lot <= 0.0 ||
      volume_step <= 0.0 ||
      min_volume < 0.0 ||
      max_volume <= 0.0 ||
      max_volume < min_volume)
   {
      return 0.0;
   }

   const double stop_distance_price = MathAbs(entry_price - stop_price);
   if(stop_distance_price <= 0.0)
   {
      return 0.0;
   }

   const double risk_usd = account_balance_usd * risk_fraction;
   const double stop_distance_ticks = stop_distance_price / tick_size;
   const double loss_usd_per_lot = stop_distance_ticks * tick_value_usd_per_lot;
   if(loss_usd_per_lot <= 0.0)
   {
      return 0.0;
   }

   const double raw_lots = risk_usd / loss_usd_per_lot;
   const double capped_lots = MathMin(raw_lots, max_volume);
   const double stepped_lots = MathFloor((capped_lots + 0.000000000001) / volume_step) * volume_step;

   if(stepped_lots < min_volume)
   {
      return 0.0;
   }

   return NormalizeDouble(stepped_lots, volume_digits);
}
const string H024_INTENDED_ACTION_LOG_SCHEMA_VERSION = "h024_intended_action_log_v1";

string BuildH024IntendedActionLogHeader()
{
   return "timestamp,schema_version,ea_version,symbol,normalized_symbol,timeframe,decision,direction,entry_price,stop_price,stop_distance_price,tick_size,tick_value_usd_per_lot,account_balance_usd,risk_fraction,risk_usd,raw_lots,lots,min_volume,max_volume,volume_step,volume_digits,reason";
}

string BuildH024IntendedActionLogRow(
   const string timestamp,
   const string ea_version,
   const string symbol,
   const string normalized_symbol,
   const string timeframe,
   const string decision,
   const string direction,
   const double entry_price,
   const double stop_price,
   const double tick_size,
   const double tick_value_usd_per_lot,
   const double account_balance_usd,
   const double risk_fraction,
   const double min_volume,
   const double max_volume,
   const double volume_step,
   const int volume_digits,
   const string reason
)
{
   double stop_distance_price = 0.0;
   double risk_usd = account_balance_usd * risk_fraction;
   double raw_lots = 0.0;
   double lots = 0.0;

   if(entry_price > 0.0 && stop_price > 0.0)
   {
      stop_distance_price = MathAbs(entry_price - stop_price);
   }

   if(entry_price > 0.0 &&
      stop_price > 0.0 &&
      stop_distance_price > 0.0 &&
      tick_size > 0.0 &&
      tick_value_usd_per_lot > 0.0 &&
      account_balance_usd > 0.0 &&
      risk_fraction > 0.0 &&
      min_volume > 0.0 &&
      max_volume > 0.0 &&
      volume_step > 0.0 &&
      volume_digits >= 0)
   {
      double stop_distance_ticks = stop_distance_price / tick_size;
      double loss_usd_per_lot = stop_distance_ticks * tick_value_usd_per_lot;

      if(loss_usd_per_lot > 0.0)
      {
         raw_lots = risk_usd / loss_usd_per_lot;

         if(decision == "WOULD_OPEN")
         {
            lots = ComputeH024LotSize(
               account_balance_usd,
               risk_fraction,
               entry_price,
               stop_price,
               tick_size,
               tick_value_usd_per_lot,
               volume_step,
               min_volume,
               max_volume,
               volume_digits
            );
         }
      }
   }

   return StringFormat(
      "%s,%s,%s,%s,%s,%s,%s,%s,%.10f,%.10f,%.10f,%.10f,%.10f,%.2f,%.8f,%.2f,%.10f,%.10f,%.10f,%.10f,%.10f,%d,%s",
      timestamp,
      H024_INTENDED_ACTION_LOG_SCHEMA_VERSION,
      ea_version,
      symbol,
      normalized_symbol,
      timeframe,
      decision,
      direction,
      entry_price,
      stop_price,
      stop_distance_price,
      tick_size,
      tick_value_usd_per_lot,
      account_balance_usd,
      risk_fraction,
      risk_usd,
      raw_lots,
      lots,
      min_volume,
      max_volume,
      volume_step,
      volume_digits,
      reason
   );
}

string H024NormalizedSymbolName(const string symbol)
{
   if(StringFind(symbol, "USDJPY") == 0)
   {
      return "USDJPY";
   }
   if(StringFind(symbol, "XAUUSD") == 0)
   {
      return "XAUUSD";
   }
   return symbol;
}

string H024DecisionFromIntentDetail(const string intent_detail)
{
   if(StringFind(intent_detail, "WOULD_OPEN:") == 0)
   {
      return "WOULD_OPEN";
   }
   if(StringFind(intent_detail, "BLOCKED:") == 0)
   {
      return "BLOCKED";
   }
   return "NO_ACTION";
}

string H024DirectionFromIntentDetail(const string intent_detail)
{
   if(StringFind(intent_detail, "side=long") >= 0)
   {
      return "long";
   }
   if(StringFind(intent_detail, "side=short") >= 0)
   {
      return "short";
   }
   return "";
}

void WriteH024IntendedActionHeaderRow()
{
   WritePreflightRow("H024_INTENDED_ACTION_HEADER", BuildH024IntendedActionLogHeader());
}


int H024RuntimeVolumeDigits(const double volume_step)
{
   if(volume_step <= 0.0)
   {
      return 2;
   }

   int digits = 0;
   double scaled_step = volume_step;

   while(digits < 8 && MathAbs(scaled_step - MathRound(scaled_step)) > 0.00000001)
   {
      scaled_step *= 10.0;
      digits++;
   }

   return digits;
}


bool H024RuntimeEntryStopPrices(
   const string direction,
   double &entry_price,
   double &stop_price
)
{
   entry_price = 0.0;
   stop_price = 0.0;

   if(direction != "long" && direction != "short")
   {
      return false;
   }

   MqlRates rates[];
   ArraySetAsSeries(rates, true);

   const int closed_shift = H024EffectiveClosedShift();
   const int atr_window = 3;
   const double stop_atr_multiple = 2.0;
   const int required_bars = closed_shift + 64;

   const int copied = CopyRates(_Symbol, PERIOD_H4, 0, required_bars, rates);
   if(copied < closed_shift + atr_window + 1)
   {
      return false;
   }

   const double atr = WilderAtrForClosedBar(rates, closed_shift, atr_window);
   if(atr == EMPTY_VALUE || atr <= 0.0)
   {
      return false;
   }

   const int price_digits = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);
   entry_price = NormalizeDouble(rates[closed_shift].close, price_digits);

   if(direction == "long")
   {
      stop_price = NormalizeDouble(entry_price - (atr * stop_atr_multiple), price_digits);
   }
   else
   {
      stop_price = NormalizeDouble(entry_price + (atr * stop_atr_multiple), price_digits);
   }

   return (
      entry_price > 0.0 &&
      stop_price > 0.0 &&
      MathAbs(entry_price - stop_price) > 0.0
   );
}

void WriteH024IntendedActionRuntimeRow()
{
   const string intent_detail = H024StrategyIntentDetail();
   const string decision = H024DecisionFromIntentDetail(intent_detail);
   const string direction = H024DirectionFromIntentDetail(intent_detail);

   const double tick_size = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   const double tick_value = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   const double min_volume = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   const double max_volume = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   const double volume_step = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   const int volume_digits = H024RuntimeVolumeDigits(volume_step);

   double entry_price = 0.0;
   double stop_price = 0.0;
   string intended_decision = decision;
   string intended_reason = intent_detail;

   if(decision == "WOULD_OPEN")
   {
      if(!H024RuntimeEntryStopPrices(direction, entry_price, stop_price))
      {
         intended_decision = "BLOCKED";
         intended_reason = "BLOCKED:invalid_entry_stop_for_would_open;" + intent_detail;
      }
      else
      {
         const double preview_lots = ComputeH024LotSize(
            AccountInfoDouble(ACCOUNT_BALANCE),
            InpRiskFraction,
            entry_price,
            stop_price,
            tick_size,
            tick_value,
            volume_step,
            min_volume,
            max_volume,
            volume_digits
         );

         if(preview_lots <= 0.0)
         {
            intended_decision = "BLOCKED";
            intended_reason = "BLOCKED:volume_below_min_for_would_open;" + intent_detail;
         }
      }
   }

   const string intended_action_row = BuildH024IntendedActionLogRow(
      TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS),
      InpEaVersion,
      _Symbol,
      H024NormalizedSymbolName(_Symbol),
      "H4",
      intended_decision,
      direction,
      entry_price,
      stop_price,
      tick_size,
      tick_value,
      AccountInfoDouble(ACCOUNT_BALANCE),
      InpRiskFraction,
      min_volume,
      max_volume,
      volume_step,
      volume_digits,
      intended_reason
   );

   WritePreflightRow("H024_INTENDED_ACTION_ROW", intended_action_row);
}


string BarObservationDetail(const ENUM_TIMEFRAMES timeframe, const string label)
{
   int digits = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);
   datetime bar_time = iTime(_Symbol, timeframe, 0);

   if(bar_time <= 0)
   {
      return label + ":unavailable";
   }

   return label
      + ":time=" + TimeToString(bar_time, TIME_DATE | TIME_SECONDS)
      + ";open=" + DoubleToString(iOpen(_Symbol, timeframe, 0), digits)
      + ";high=" + DoubleToString(iHigh(_Symbol, timeframe, 0), digits)
      + ";low=" + DoubleToString(iLow(_Symbol, timeframe, 0), digits)
      + ";close=" + DoubleToString(iClose(_Symbol, timeframe, 0), digits)
      + ";tick_volume=" + LongText(iVolume(_Symbol, timeframe, 0));
}

void WriteMarketStateRow()
{
   string detail = BarObservationDetail(PERIOD_H4, "H4") + "|" + BarObservationDetail(PERIOD_M1, "M1");
   WritePreflightRow("MARKET_STATE", detail);
}

string ClosedBarObservationDetail(const ENUM_TIMEFRAMES timeframe, const string label)
{
   MqlRates rates[];
   ArraySetAsSeries(rates, true);
   const int copied = CopyRates(_Symbol, timeframe, 1, 1, rates);
   if(copied < 1)
   {
      return label + "_closed:unavailable";
   }

   return StringFormat(
      "%s_closed:time=%s;open=%.10f;high=%.10f;low=%.10f;close=%.10f;tick_volume=%I64d",
      label,
      TimeToString(rates[0].time, TIME_DATE | TIME_SECONDS),
      rates[0].open,
      rates[0].high,
      rates[0].low,
      rates[0].close,
      rates[0].tick_volume
   );
}

void WriteBarObservationRow()
{
   string detail = ClosedBarObservationDetail(PERIOD_H4, "H4") + "|" + ClosedBarObservationDetail(PERIOD_M1, "M1");
   WritePreflightRow("BAR_OBSERVATION", detail);
}

double TrueRangeAt(MqlRates &rates[], const int index)
{
   const double range_high_low = rates[index].high - rates[index].low;
   if(index + 1 >= ArraySize(rates))
   {
      return range_high_low;
   }

   const double previous_close = rates[index + 1].close;
   const double range_high_close = MathAbs(rates[index].high - previous_close);
   const double range_low_close = MathAbs(rates[index].low - previous_close);

   return MathMax(range_high_low, MathMax(range_high_close, range_low_close));
}

double WilderAtrForClosedBar(MqlRates &rates[], const int closed_shift, const int window)
{
   const int count = ArraySize(rates);
   if(count < closed_shift + window)
   {
      return EMPTY_VALUE;
   }

   // rates[] is series-indexed: 0 is forming/current, larger indices are older.
   // Compute a bounded Wilder ATR chronologically from the oldest copied bars
   // toward the requested closed bar. This mirrors the Python recurrence over
   // the available runtime warmup window.
   const int oldest = count - 1;
   if(oldest - window + 1 < closed_shift)
   {
      return EMPTY_VALUE;
   }

   double atr = 0.0;
   for(int offset = oldest; offset >= oldest - window + 1; --offset)
   {
      atr += TrueRangeAt(rates, offset);
   }
   atr /= window;

   for(int offset = oldest - window; offset >= closed_shift; --offset)
   {
      atr = ((atr * (window - 1)) + TrueRangeAt(rates, offset)) / window;
   }

   return atr;
}

double SimpleMeanClose(MqlRates &rates[], const int closed_shift, const int window)
{
   if(ArraySize(rates) < closed_shift + window)
   {
      return EMPTY_VALUE;
   }

   double total = 0.0;
   for(int offset = closed_shift; offset < closed_shift + window; ++offset)
   {
      total += rates[offset].close;
   }
   return total / window;
}

double HighestHighBeforeSignal(MqlRates &rates[], const int closed_shift, const int window)
{
   if(ArraySize(rates) < closed_shift + 1 + window)
   {
      return EMPTY_VALUE;
   }

   double value = rates[closed_shift + 1].high;
   for(int offset = closed_shift + 2; offset <= closed_shift + window; ++offset)
   {
      value = MathMax(value, rates[offset].high);
   }
   return value;
}

double LowestLowBeforeSignal(MqlRates &rates[], const int closed_shift, const int window)
{
   if(ArraySize(rates) < closed_shift + 1 + window)
   {
      return EMPTY_VALUE;
   }

   double value = rates[closed_shift + 1].low;
   for(int offset = closed_shift + 2; offset <= closed_shift + window; ++offset)
   {
      value = MathMin(value, rates[offset].low);
   }
   return value;
}

string DoubleText(const double value)
{
   if(value == EMPTY_VALUE || !MathIsValidNumber(value))
   {
      return "nan";
   }
   return DoubleToString(value, 10);
}

void WriteH024StateObservationRow()
{
   MqlRates rates[];
   ArraySetAsSeries(rates, true);

   const int copied = CopyRates(_Symbol, PERIOD_H4, 0, 256, rates);
   if(copied < 10)
   {
      WritePreflightRow("H024_STATE_OBSERVATION", "unavailable:insufficient_h4_warmup_bars");
      return;
   }

   const int closed_shift = H024EffectiveClosedShift();
   const int slow_window = 5;
   const int slope_lag = 2;
   const int atr_window = 3;
   const int pullback_window = 3;
   const double min_pullback_atr = 0.25;
   const double max_pullback_atr = 3.0;
   const double min_slope_atr = 0.05;

   const double slow_ma = SimpleMeanClose(rates, closed_shift, slow_window);
   const double slow_ma_lag = SimpleMeanClose(rates, closed_shift + slope_lag, slow_window);
   const double atr = WilderAtrForClosedBar(rates, closed_shift, atr_window);
   const double previous_atr = WilderAtrForClosedBar(rates, closed_shift + 1, atr_window);

   const double slope = slow_ma - slow_ma_lag;
   const double slope_threshold = atr * min_slope_atr;

   const bool trend_up = rates[closed_shift].close > slow_ma && slope > slope_threshold;
   const bool trend_down = rates[closed_shift].close < slow_ma && slope < -slope_threshold;

   const bool previous_bearish = rates[closed_shift + 1].close < rates[closed_shift + 1].open;
   const bool previous_bullish = rates[closed_shift + 1].close > rates[closed_shift + 1].open;

   const double recent_high_before_signal = HighestHighBeforeSignal(rates, closed_shift, pullback_window);
   const double recent_low_before_signal = LowestLowBeforeSignal(rates, closed_shift, pullback_window);

   double long_pullback_depth_atr = EMPTY_VALUE;
   double short_pullback_depth_atr = EMPTY_VALUE;
   if(previous_atr > 0.0 && previous_atr != EMPTY_VALUE)
   {
      long_pullback_depth_atr = (recent_high_before_signal - rates[closed_shift + 1].low) / previous_atr;
      short_pullback_depth_atr = (rates[closed_shift + 1].high - recent_low_before_signal) / previous_atr;
   }

   const bool long_pullback_ok = (
      long_pullback_depth_atr != EMPTY_VALUE &&
      long_pullback_depth_atr >= min_pullback_atr &&
      long_pullback_depth_atr <= max_pullback_atr
   );
   const bool short_pullback_ok = (
      short_pullback_depth_atr != EMPTY_VALUE &&
      short_pullback_depth_atr >= min_pullback_atr &&
      short_pullback_depth_atr <= max_pullback_atr
   );

   const bool long_resumption = rates[closed_shift].close > rates[closed_shift + 1].high;
   const bool short_resumption = rates[closed_shift].close < rates[closed_shift + 1].low;

   const bool long_signal_observed = trend_up && previous_bearish && long_pullback_ok && long_resumption;
   const bool short_signal_observed = trend_down && previous_bullish && short_pullback_ok && short_resumption;

   string detail = StringFormat(
      "closed_h4_time=%s;h4_warmup_bars=%d;slow_window=%d;slope_lag=%d;atr_window=%d;pullback_window=%d;slow_ma=%s;slow_ma_lag=%s;atr=%s;previous_atr=%s;slope=%s;slope_threshold=%s;trend_up=%s;trend_down=%s;previous_bearish=%s;previous_bullish=%s;recent_high_before_signal=%s;recent_low_before_signal=%s;long_pullback_depth_atr=%s;short_pullback_depth_atr=%s;long_pullback_ok=%s;short_pullback_ok=%s;long_resumption=%s;short_resumption=%s;long_signal_observed=%s;short_signal_observed=%s;action=NO_ACTION:state_observation_only",
      TimeToString(rates[closed_shift].time, TIME_DATE | TIME_SECONDS),
      copied,
      slow_window,
      slope_lag,
      atr_window,
      pullback_window,
      DoubleText(slow_ma),
      DoubleText(slow_ma_lag),
      DoubleText(atr),
      DoubleText(previous_atr),
      DoubleText(slope),
      DoubleText(slope_threshold),
      BoolText(trend_up),
      BoolText(trend_down),
      BoolText(previous_bearish),
      BoolText(previous_bullish),
      DoubleText(recent_high_before_signal),
      DoubleText(recent_low_before_signal),
      DoubleText(long_pullback_depth_atr),
      DoubleText(short_pullback_depth_atr),
      BoolText(long_pullback_ok),
      BoolText(short_pullback_ok),
      BoolText(long_resumption),
      BoolText(short_resumption),
      BoolText(long_signal_observed),
      BoolText(short_signal_observed)
   );

   WritePreflightRow("H024_STATE_OBSERVATION", detail);
}

int OnInit()
{
   if(!OpenLogFile())
   {
      return INIT_FAILED;
   }

   EventSetTimer(InpTimerSeconds);
   WritePreflightRow("INIT", InpKillSwitchBlocked ? "blocked_by_default" : "not_blocked");
   WriteIntentRow();
   WriteMarketStateRow();
   WriteBarObservationRow();
   WriteH024StateObservationRow();
   WriteH024StrategyIntentRow();
   WriteH024IntendedActionHeaderRow();
   WriteH024IntendedActionRuntimeRow();
   return INIT_SUCCEEDED;
}

void OnTick()
{
   WritePreflightRow("TICK", InpKillSwitchBlocked ? "no_action_blocked" : "no_action_unblocked");
   WriteIntentRow();
   WriteMarketStateRow();
   WriteBarObservationRow();
   WriteH024StateObservationRow();
   WriteH024StrategyIntentRow();
   WriteH024IntendedActionRuntimeRow();
}

void OnTimer()
{
   WriteIntentRow();
   WriteMarketStateRow();
   WriteBarObservationRow();
   WriteH024StateObservationRow();
   WriteH024StrategyIntentRow();
   WriteH024IntendedActionRuntimeRow();
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   WritePreflightRow("DEINIT", IntegerToString(reason));

   if(g_file_handle != INVALID_HANDLE)
   {
      FileClose(g_file_handle);
      g_file_handle = INVALID_HANDLE;
   }
}
