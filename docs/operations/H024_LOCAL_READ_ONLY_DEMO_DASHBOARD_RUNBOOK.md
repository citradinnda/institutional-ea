# H024 Local Read-Only Demo Dashboard Runbook

## Purpose

This is the local one-click operator console for the H024 free local Windows read-only demo.

It is a UX layer over the already committed demo deployment readiness verifier. It is not another governance packet.

It generates a static local HTML dashboard under:

```text
reports/demo/
Launch command
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\start_h024_local_read_only_demo_dashboard.ps1

The script refreshes the existing H024 free local read-only demo deployment readiness verifier, generates the dashboard, and opens it in the default browser.

To generate without opening the browser:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\start_h024_local_read_only_demo_dashboard.ps1 -NoOpen
Dashboard contents

The dashboard shows:

read-only demo readiness verdict
no-console scheduled task action
5-minute cadence status
latest scheduled run status and exit code
upstream packet summary
canary/account observation summary if already available from existing reports
READ-ONLY DEMO ONLY - NO TRADING AUTHORIZED banner

The generated HTML uses a Unicode em dash in the banner. The PowerShell source keeps this ASCII-safe via [char]0x2014 to avoid Windows PowerShell parsing issues.

Safety boundary

This dashboard is for status/demo observation only.

It does not authorize trading.

It does not authorize broker mutation.

It does not authorize request construction.

It does not authorize entries.

It does not authorize close/modify.

It does not authorize any order-capable execution path.

Infrastructure boundary

This remains free local Windows only.

No Oracle VPS.

No paid VPS.

No Linux migration.

No SSH workflow.

No live trading EA deployment.

Generated files

Generated dashboard files live under:

reports/demo/

Do not commit reports/.

reports/ remains generated runtime/demo evidence only.