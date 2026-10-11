param([string]$Repo = (Split-Path -Parent $PSScriptRoot))
$ErrorActionPreference = 'Stop'
$cfg = Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $Repo 'config\higgsfield-typecast.json') | ConvertFrom-Json
function Require([bool]$Condition, [string]$Message) { if (-not $Condition) { throw "Mandatory layout v5: $Message" } }
Require ($cfg.layout.version -eq 5) 'global version must be 5'
Require ($cfg.layout.title_band_center_y -eq 260 -and $cfg.layout.title.center_y -eq 260) 'headline center must be y=260'
Require ($cfg.layout.title.font_pixels -eq 108 -and $cfg.layout.title.max_lines -eq 2 -and $cfg.layout.title.max_width_fraction -eq 0.87) 'headline size/lines/width changed'
Require ($cfg.layout.title.outline_pixels -eq 14) 'headline outline must be 14px'
Require ($cfg.layout.caption.center_y -eq 1306 -and $cfg.layout.caption.font_pixels -eq 64) 'caption center/size changed'
Require (($cfg.layout.title_band_pixels -join ',') -eq '0,100,1080,440') 'headline band changed'
Require (($cfg.layout.caption_zone_pixels -join ',') -eq '0,1180,1080,1430') 'caption band changed'
foreach ($name in 'captions','captions_en') {
    $cap = $cfg.$name
    Require ($cap.layout_version -eq 5 -and $cap.font_pixels -eq 64 -and $cap.max_width_fraction -eq 0.74 -and $cap.max_lines -eq 2) "$name size/version/width changed"
    Require ([math]::Abs($cap.fontsize_fraction * 1920 - 64) -lt 0.001) "$name normalized font differs"
    Require (($cap.text_zone_pixels -join ',') -eq '0,1180,1080,1430' -and $cap.background -eq 'none') "$name band/background changed"
}
foreach ($file in Get-ChildItem -LiteralPath (Join-Path $Repo 'topics') -Filter topic.json -Recurse -File) {
    $topic = Get-Content -Raw -Encoding UTF8 -LiteralPath $file.FullName | ConvertFrom-Json
    Require ($topic.layout_policy.version -eq 5 -and $topic.layout_policy.inherit_global -eq $true -and $topic.layout_policy.override_allowed -eq $false) "topic $($topic.slug) must inherit v5"
    Require ($null -eq $topic.layout -and $null -eq $topic.captions -and $null -eq $topic.captions_en) "topic $($topic.slug) has a forbidden local overlay override"
}
Write-Host '[ OK ] Mandatory layout v5: all topics, template, Korean and English inherit the approved proportions.'
