# H024 Read-Only Observer No-Console Launcher Runbook

The local Windows scheduled observer can be launched through:

`scripts/run_h024_read_only_vps_observer_scheduled_hidden.vbs`

This launcher exists only to suppress the visible PowerShell window created by Windows Task Scheduler. It delegates to the existing read-only scheduled wrapper:

`scripts/run_h024_read_only_vps_observer_scheduled.ps1`

Safety boundary:

- no `order_check`
- no `order_send`
- no `symbol_select`
- no broker mutation
- no live broker request construction
- no executable trade request construction
- no entries
- no close/modify
- no SL/TP changes
- no trading loop

The launcher preserves the wrapper exit code. A nonzero exit remains nonzero and must still fail closed.

Recommended scheduled task action:

```powershell
wscript.exe "C:\Users\equin\Documents\institutional-ea\scripts\run_h024_read_only_vps_observer_scheduled_hidden.vbs"

This changes only local Windows launch behavior. It does not change broker safety, trading authorization, or evidence rules.

If healthcheck reports black_swan:UPSTREAM_NOT_PASS, do not suppress it. Refresh upstream read-only evidence and rerun the observer.
