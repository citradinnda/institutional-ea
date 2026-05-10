cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

$handoffPath = "docs\operations\handoffs\HANDOFF_74.md"
New-Item -ItemType Directory -Force -Path (Split-Path $handoffPath) | Out-Null

# Writes whatever is currently copied to clipboard into the handoff file
Get-Clipboard | Set-Content -Path $handoffPath -Encoding UTF8

Write-Host "`n=== Verify handoff header ==="
Get-Content $handoffPath -First 5

Write-Host "`n=== Docs-only checks ==="
git diff --check
if ($LASTEXITCODE -ne 0) { throw "git diff --check failed" }

git diff --stat

git add $handoffPath

git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw "git diff --cached --check failed" }

git diff --cached --stat

git commit -m "Add handoff document #74"

git push

git status

git ls-files $handoffPath
