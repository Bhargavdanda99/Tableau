#This code will pickup the latest workbook either it is added or any changes

$sourceDir = "$env:BUILD_SOURCESDIRECTORY"
$targetDir = "$env:BUILD_ARTIFACTSTAGINGDIRECTORY"

Set-Location $sourceDir

# Check if HEAD^ revision exists
$hasParent = $false
try {
    $parent = git rev-parse HEAD^ 2>$null
    if ($parent) {
        $hasParent = $true
    }
} catch {
    $hasParent = $false
}

if ($hasParent) {
    $diffRange = "HEAD^ HEAD"
    $diffCmd = "git diff --name-only $diffRange --"
    $changedFiles = Invoke-Expression $diffCmd | Where-Object { $_ -match '\.twb(x)?$' }
} else {
    # In shallow clone or single commit scenario, list all workbook files in HEAD
    $changedFiles = git ls-tree -r --name-only HEAD | Where-Object { $_ -match '\.twb(x)?$' }
    Write-Host "Single commit or shallow clone detected. Listing all workbook files."
}

if (-not $changedFiles) {
    Write-Host "No changed workbook files detected in latest commit."
} else {
    foreach ($file in $changedFiles) {
        $filePath = Join-Path $sourceDir $file.TrimStart('/')
        if (Test-Path $filePath) {
            Copy-Item -Path $filePath -Destination $targetDir -Force
            Write-Host "Copied changed workbook: $file"
        } else {
            Write-Warning "File not found: $filePath"
        }
    }
}
