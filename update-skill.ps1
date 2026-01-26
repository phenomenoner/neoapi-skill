param(
    [string]$Repo = "phenomenoner/neoapi-skill",
    [string]$Branch = "main",
    [string]$SkillSubdir = "skills/neoapi-python",
    [string]$InstallDir = "$env:USERPROFILE\.codex\skills\public\neoapi-python",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

if ($Repo -eq "OWNER/REPO") {
    throw "Set -Repo to your GitHub repo, for example: -Repo yourorg/neoapi-skill"
}

$rawBase = "https://raw.githubusercontent.com/$Repo/$Branch/$SkillSubdir"
$remoteVersionUrl = "$rawBase/VERSION"
$remoteVersion = (Invoke-WebRequest -UseBasicParsing $remoteVersionUrl).Content.Trim()

$localVersion = ""
$localVersionPath = Join-Path $InstallDir "VERSION"
if (Test-Path $localVersionPath) {
    $localVersion = (Get-Content -Raw -LiteralPath $localVersionPath).Trim()
}

if (-not $Force -and $localVersion -and $localVersion -eq $remoteVersion) {
    Write-Host "Already up to date ($localVersion)."
    exit 0
}

$repoZip = "https://github.com/$Repo/archive/refs/heads/$Branch.zip"
$tempRoot = Join-Path $env:TEMP ("neoapi-skill-" + [guid]::NewGuid().ToString())
New-Item -ItemType Directory -Force -Path $tempRoot | Out-Null

$zipPath = Join-Path $tempRoot "repo.zip"
Invoke-WebRequest -UseBasicParsing $repoZip -OutFile $zipPath
Expand-Archive -Force $zipPath $tempRoot

$repoName = ($Repo -split "/")[-1]
$extractedRoot = Join-Path $tempRoot "$repoName-$Branch"
$source = Join-Path $extractedRoot $SkillSubdir
if (-not (Test-Path $source)) {
    throw "Skill subdir not found: $source"
}

New-Item -ItemType Directory -Force (Split-Path $InstallDir -Parent) | Out-Null
if (Test-Path $InstallDir) {
    Remove-Item -Recurse -Force $InstallDir
}
Copy-Item -Recurse -Force $source $InstallDir

Write-Host "Installed $remoteVersion to $InstallDir"
