param([string]$PythonCommand = '', [switch]$GenerateNarration, [string]$ScriptPath = '', [string]$OutputPath = '')
$ErrorActionPreference = 'Stop'
$typecastWorkspace = Split-Path -Parent $PSScriptRoot
$typecastWorkDirectory = Join-Path $typecastWorkspace 'work'
New-Item -ItemType Directory -Force -Path $typecastWorkDirectory | Out-Null
$typecastEncryptedPath = Join-Path $typecastWorkspace 'work\typecast-key.xml'
if (-not (Test-Path -LiteralPath $typecastEncryptedPath)) {
    $typecastSecret = Read-Host 'Typecast API key (input hidden)' -AsSecureString
    if ($typecastSecret.Length -eq 0) { throw 'No API key entered' }
    $typecastSecret | Export-Clixml -LiteralPath $typecastEncryptedPath
}
$typecastSecret = Import-Clixml -LiteralPath $typecastEncryptedPath
if (-not $PythonCommand) {
    $typecastBundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    if (Test-Path -LiteralPath $typecastBundledPython) { $PythonCommand = $typecastBundledPython }
    else {
        $typecastInstalledPython = Get-Command python,python3 -ErrorAction SilentlyContinue | Select-Object -First 1
        if (-not $typecastInstalledPython) { throw 'Install Python 3 or pass -PythonCommand with its path' }
        $PythonCommand = $typecastInstalledPython.Source
    }
}
$typecastPreviousKey = $env:TYPECAST_API_KEY
$typecastSecretPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($typecastSecret)
try {
    $env:TYPECAST_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($typecastSecretPointer)
    $typecastBridgeArguments = @((Join-Path $typecastWorkspace 'src\typecast_api_bridge.py'))
    if ($GenerateNarration) {
        if (-not $ScriptPath) { $ScriptPath = Join-Path $typecastWorkspace 'work\higgsfield-typecast\narration-script.txt' }
        if (-not $OutputPath) { $OutputPath = Join-Path $typecastWorkspace 'outputs\piljae.wav' }
        $typecastBridgeArguments += @('--generate', '--script', $ScriptPath, '--out', $OutputPath)
    }
    & $PythonCommand @typecastBridgeArguments
    if ($LASTEXITCODE -ne 0) { throw 'API operation incomplete; inspect its status before retrying a generation' }
    if ($GenerateNarration) { Write-Host 'Piljae narration generated.' }
    else { Write-Host 'Connected. Piljae voice verified. No audio generation requested.' }
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($typecastSecretPointer)
    if ($null -eq $typecastPreviousKey) { Remove-Item Env:\TYPECAST_API_KEY -ErrorAction SilentlyContinue }
    else { $env:TYPECAST_API_KEY = $typecastPreviousKey }
}
