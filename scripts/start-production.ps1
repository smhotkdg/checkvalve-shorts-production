<#
Start a Shorts production run in Claude Code.

Usage (from anywhere):
  powershell -ExecutionPolicy Bypass -File <repo>\scripts\start-production.ps1 -Slug tower-crane

What it does:
  1. git pull (fast-forward only) in this repository
  2. checks the topic package and local tools (Typecast key, Python, Blender, FFmpeg, Claude Code)
  3. builds work\<slug>\claude-prompt.txt from docs\claude-code-prompt.md
  4. opens Claude Code in this repository with that prompt (skip with -NoLaunch)
#>
param(
    [string]$Slug = '',
    [switch]$NoLaunch,
    [switch]$SkipPull,
    [string]$BlenderPath = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
)
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repo

function Write-Ok([string]$m)   { Write-Host "[ OK ] $m" -ForegroundColor Green }
function Write-Warn([string]$m) { Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Write-Step([string]$m) { Write-Host "`n== $m" -ForegroundColor Cyan }

Write-Step 'Repository'
Write-Ok $repo
if (-not $SkipPull) {
    git pull --ff-only
    if ($LASTEXITCODE -ne 0) { throw 'git pull failed. Commit or stash local changes, then run again.' }
}
Write-Ok ("HEAD " + (git log --oneline -1))

$config = Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $repo 'config\higgsfield-typecast.json') | ConvertFrom-Json
if (-not $Slug) { $Slug = $config.active_topic }
if ($Slug -notmatch '^[a-z0-9][a-z0-9-]*$') { throw "Invalid slug: $Slug" }

Write-Step "Topic: $Slug"
$topicDir = Join-Path $repo (Join-Path 'topics' $Slug)
foreach ($f in 'brief.md', 'narration.txt', 'title-description.txt', 'topic.json') {
    $p = Join-Path $topicDir $f
    if (-not (Test-Path -LiteralPath $p)) { throw "Missing topics\$Slug\$f" }
    if ((Get-Item -LiteralPath $p).Length -eq 0) { throw "Empty topics\$Slug\$f" }
}
Write-Ok 'brief.md, narration.txt, title-description.txt, topic.json'
if ($config.active_topic -ne $Slug) {
    Write-Warn "config active_topic is '$($config.active_topic)'; Claude Code will be told to use '$Slug'."
}

Write-Step 'Local tools'
if (Test-Path -LiteralPath (Join-Path $repo 'work\typecast-key.xml')) { Write-Ok 'Typecast key (work\typecast-key.xml)' }
else { Write-Warn 'No work\typecast-key.xml: connect-typecast.ps1 will ask for the key (hidden input) on first use.' }

$py = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (-not (Test-Path -LiteralPath $py)) { $py = (Get-Command python, python3 -ErrorAction SilentlyContinue | Select-Object -First 1).Source }
if ($py) { Write-Ok "Python: $py" } else { Write-Warn 'Python 3 not found.' }

if (Test-Path -LiteralPath $BlenderPath) { Write-Ok "Blender: $BlenderPath" }
elseif (Get-Command blender -ErrorAction SilentlyContinue) { Write-Ok 'Blender: on PATH' }
else { Write-Warn "Blender not found at $BlenderPath (pass -BlenderPath)." }

foreach ($tool in 'ffmpeg', 'ffprobe') {
    if (Get-Command $tool -ErrorAction SilentlyContinue) { Write-Ok $tool } else { Write-Warn "$tool not on PATH." }
}
$claude = Get-Command claude -ErrorAction SilentlyContinue
if ($claude) { Write-Ok "Claude Code: $($claude.Source)" }
elseif (-not $NoLaunch) { throw 'Claude Code (claude) not on PATH. Install it or open this folder in Claude Code manually.' }

Write-Step 'Prompt'
$work = Join-Path $repo (Join-Path 'work' $Slug)
New-Item -ItemType Directory -Force -Path $work | Out-Null
$doc = Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $repo 'docs\claude-code-prompt.md')
$m = [regex]::Match($doc, '(?s)```text\r?\n(.*?)\r?\n```')
if (-not $m.Success) { throw 'No ```text block found in docs\claude-code-prompt.md' }
$prompt = $m.Groups[1].Value.Replace('<slug>', $Slug)
$promptPath = Join-Path $work 'claude-prompt.txt'
[IO.File]::WriteAllText($promptPath, $prompt, (New-Object Text.UTF8Encoding($false)))
Write-Ok "work\$Slug\claude-prompt.txt ($($prompt.Length) chars)"

$instruction = "Read work/$Slug/claude-prompt.txt and carry out every instruction in it for topic '$Slug', in order, stopping where it asks for my approval. The repository is already pulled. Reply in Korean."
if ($NoLaunch) {
    Write-Step 'Ready (not launched)'
    Write-Host "claude `"$instruction`""
    return
}
Write-Step 'Launching Claude Code'
& claude $instruction
