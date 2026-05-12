[CmdletBinding()]
param(
    [string]$TaskName = "H024 Read Only VPS Observer",
    [switch]$Preview
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($Preview) {
    [ordered]@{
        task_name = $TaskName
        preview_only = $true
        action = "unregister_if_present"
        read_only_observer_only = $true
        trading_authorized = $false
        broker_mutation_authorized = $false
        live_execution_authorized = $false
    } | ConvertTo-Json -Depth 4

    Write-Host "Preview only. No scheduled task was removed."
    return
}

$task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($null -eq $task) {
    Write-Host "No scheduled task found: $TaskName"
    return
}

Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
Write-Host "Removed scheduled task: $TaskName"
