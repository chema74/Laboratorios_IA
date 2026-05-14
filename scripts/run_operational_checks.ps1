$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$tmpDir = Join-Path $repoRoot ".tmp"
if (!(Test-Path $tmpDir)) {
    New-Item -ItemType Directory -Path $tmpDir | Out-Null
}

$env:TEMP = $tmpDir
$env:TMP = $tmpDir
$env:PYTHONUTF8 = "1"

$labsRoot = Join-Path $repoRoot "labs"
if (!(Test-Path $labsRoot)) {
    throw "No existe la carpeta labs en $repoRoot"
}

$labDirs = Get-ChildItem -Path $labsRoot -Directory | Sort-Object Name
$results = @()

foreach ($lab in $labDirs) {
    $testsPath = Join-Path $lab.FullName "tests"
    if (!(Test-Path $testsPath)) {
        continue
    }

    Write-Host "=== TESTS: $($lab.Name) ==="
    Push-Location $lab.FullName
    try {
        & python -m unittest discover tests -v
        $code = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }

    $status = if ($code -eq 0) { "PASS" } else { "FAIL" }
    $results += [PSCustomObject]@{
        laboratorio = $lab.Name
        estado = $status
        exit_code = $code
    }
}

Write-Host ""
Write-Host "=== RESUMEN OPERATIVO ==="
$results | Format-Table -AutoSize

$fails = @($results | Where-Object { $_.estado -eq "FAIL" })
if ($fails.Count -gt 0) {
    Write-Error "Hay $($fails.Count) laboratorio(s) con fallos."
    exit 1
}

Write-Host "Todos los laboratorios con tests han pasado."
exit 0
