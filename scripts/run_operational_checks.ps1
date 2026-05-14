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
    $labOk = $true
    $checks = @()

    $healthScript = Join-Path $lab.FullName "scripts\comprobar_salud.py"
    if (Test-Path $healthScript) {
        Write-Host "=== SALUD: $($lab.Name) ==="
        Push-Location $lab.FullName
        try {
            & python "scripts/comprobar_salud.py"
            $healthCode = $LASTEXITCODE
        }
        finally {
            Pop-Location
        }
        $healthStatus = if ($healthCode -eq 0) { "PASS" } else { "FAIL" }
        $checks += "salud=$healthStatus"
        if ($healthCode -ne 0) {
            $labOk = $false
        }
    }

    $testsPath = Join-Path $lab.FullName "tests"
    if (Test-Path $testsPath) {
        Write-Host "=== TESTS: $($lab.Name) ==="
        Push-Location $lab.FullName
        try {
            & python -m unittest discover tests -v
            $testsCode = $LASTEXITCODE
        }
        finally {
            Pop-Location
        }
        $testsStatus = if ($testsCode -eq 0) { "PASS" } else { "FAIL" }
        $checks += "tests=$testsStatus"
        if ($testsCode -ne 0) {
            $labOk = $false
        }
    }

    if ($checks.Count -eq 0) {
        continue
    }

    $status = if ($labOk) { "PASS" } else { "FAIL" }
    $results += [PSCustomObject]@{
        laboratorio = $lab.Name
        estado = $status
        detalle = ($checks -join ", ")
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

Write-Host "Todos los laboratorios con checks han pasado."
exit 0
