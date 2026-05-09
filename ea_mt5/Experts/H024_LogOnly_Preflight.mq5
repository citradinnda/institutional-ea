#property strict
#property version   "0.1"
#property description "H024 log-only runtime preflight. Research only."

input bool   InpKillSwitchBlocked = true;
input string InpRunLabel = "H024_LOG_ONLY_PREFLIGHT";
input string InpOutputFile = "h024_ea_log_only_preflight.csv";

int g_file_handle = INVALID_HANDLE;

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

int OnInit()
{
   if(!OpenLogFile())
   {
      return INIT_FAILED;
   }

   WritePreflightRow("INIT", InpKillSwitchBlocked ? "blocked_by_default" : "not_blocked");
   return INIT_SUCCEEDED;
}

void OnTick()
{
   WritePreflightRow("TICK", InpKillSwitchBlocked ? "no_action_blocked" : "no_action_unblocked");
}

void OnDeinit(const int reason)
{
   WritePreflightRow("DEINIT", IntegerToString(reason));

   if(g_file_handle != INVALID_HANDLE)
   {
      FileClose(g_file_handle);
      g_file_handle = INVALID_HANDLE;
   }
}
