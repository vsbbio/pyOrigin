Powershell.exe;^
$CurrentPath = Get-Location;^
$Action = ([string]$CurrentPath + '\venv\Scripts\activate.ps1');^
. $Action;^
python "([string]$CurrentPath + '/app.py')"
pause