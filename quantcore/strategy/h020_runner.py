import pandas as pd
from quantcore.strategy.h017 import H017Result
from quantcore.strategy.h019 import run_h019
from quantcore.strategy.h020 import H020SizingConfig, generate_h020_intent_panel

def run_h020_bridge_shim(
    *,
    usdjpy_ohlcv: pd.DataFrame,
    xauusd_ohlcv: pd.DataFrame,
    config: H020SizingConfig | None = None,
) -> H017Result:
    """Run H019, apply H020 sizing, and return an H017-compatible bridge shim."""
    h019_result = run_h019(usdjpy_ohlcv=usdjpy_ohlcv, xauusd_ohlcv=xauusd_ohlcv)
    
    panels = generate_h020_intent_panel(
        positions=h019_result.positions,
        stops_long=h019_result.stops_long,
        stops_short=h019_result.stops_short,
        h4_by_symbol={"USDJPY": usdjpy_ohlcv, "XAUUSD": xauusd_ohlcv},
        equity_usd=10000.0,
        config=config,
    )
    
    new_positions = pd.DataFrame(
        0.0, 
        index=h019_result.positions.index, 
        columns=h019_result.positions.columns
    )
    
    for panel in panels:
        t = panel.decision_time
        for symbol, intent in panel.intents.items():
            if not intent.suppressed:
                new_positions.at[t, symbol] = intent.final_signed_risk_fraction
                
    return H017Result(
        positions=new_positions,
        stops_long=h019_result.stops_long,
        stops_short=h019_result.stops_short,
        signals=h019_result.signals,
        vol_multipliers=h019_result.vol_multipliers,
        heat_multipliers=h019_result.heat_multipliers,
        heat_pre=h019_result.heat_pre,
        heat_post=h019_result.heat_post,
        heat_binding=h019_result.heat_binding,
    )
