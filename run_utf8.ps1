$ErrorActionPreference = "Stop"

# Force this PowerShell session and child processes to use UTF-8.
chcp 65001 | Out-Null
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:LC_ALL = "C.UTF-8"
$env:LANG = "C.UTF-8"
$env:NODE_OPTIONS = "--enable-source-maps"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

python -m streamlit run app.py @args
