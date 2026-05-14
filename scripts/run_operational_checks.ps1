$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$tmpDir = Join-Path $repoRoot ".tmp"
if (!(Test-Path $tmpDir)) {
    New-Item -ItemType Directory -Path $tmpDir | Out-Null
}

$reportsDir = Join-Path $repoRoot "reports"
if (!(Test-Path $reportsDir)) {
    New-Item -ItemType Directory -Path $reportsDir | Out-Null
}

$env:TEMP = $tmpDir
$env:TMP = $tmpDir
$env:PYTHONUTF8 = "1"

$labsRoot = Join-Path $repoRoot "labs"
if (!(Test-Path $labsRoot)) {
    throw "No existe la carpeta labs en $repoRoot"
}

Write-Host "=== CONTRATOS JSON ==="
& python "scripts/validate_json_contracts.py"
if ($LASTEXITCODE -ne 0) {
    throw "Fallo en validacion de contratos JSON."
}

$withDemo = $env:RUN_DEMOS -eq "1"
$runAllArgs = @("scripts/run_all.py")
if ($withDemo) {
    $runAllArgs += "--with-demo"
}

$labDirs = Get-ChildItem -Path $labsRoot -Directory | Sort-Object Name
$results = @()

foreach ($lab in $labDirs) {
    $runAll = Join-Path $lab.FullName "scripts/run_all.py"
    if (!(Test-Path $runAll)) {
        continue
    }

    Write-Host "=== RUN_ALL: $($lab.Name) ==="
    $start = Get-Date
    $prevArtifacts = $env:ARTIFACTS_DIR
    $env:ARTIFACTS_DIR = (Join-Path $repoRoot ("artifacts\" + $lab.Name))
    Push-Location $lab.FullName
    try {
        & python @runAllArgs
        $code = $LASTEXITCODE
    }
    finally {
        Pop-Location
        $env:ARTIFACTS_DIR = $prevArtifacts
    }
    $duration = [Math]::Round(((Get-Date) - $start).TotalSeconds, 3)
    $status = if ($code -eq 0) { "PASS" } else { "FAIL" }

    $results += [PSCustomObject]@{
        laboratorio = $lab.Name
        estado = $status
        duracion_segundos = $duration
        demo_habilitada = $withDemo
    }
}

Write-Host ""
Write-Host "=== RESUMEN OPERATIVO ==="
$results | Format-Table -AutoSize

$summaryPath = Join-Path $reportsDir "operational_summary.json"
$payload = [PSCustomObject]@{
    generated_at = (Get-Date).ToString("o")
    with_demo = $withDemo
    total_labs = $results.Count
    failed_labs = @($results | Where-Object { $_.estado -eq "FAIL" }).Count
    results = $results
}
$payload | ConvertTo-Json -Depth 5 | Set-Content -Path $summaryPath -Encoding utf8
Write-Host "Resumen JSON: $summaryPath"

$fails = @($results | Where-Object { $_.estado -eq "FAIL" })
if ($fails.Count -gt 0) {
    Write-Error "Hay $($fails.Count) laboratorio(s) con fallos."
    exit 1
}

Write-Host "Todos los laboratorios con run_all han pasado."
exit 0
