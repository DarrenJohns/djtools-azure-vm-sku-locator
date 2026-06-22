#requires -Version 5
# Static verification for toptrumps-webgl.html
# Runs from repo root. Reports PASS / FAIL for each check.
$ErrorActionPreference = 'Stop'

$f = 'toptrumps-webgl.html'
$h = Get-Content $f -Raw
Write-Host "=== File size: $((Get-Item $f).Length) bytes ==="

$v = 'vendor/three.module.min.js'
if (!(Test-Path $v)) {
    Write-Host "FAIL: vendor missing"
} else {
    $vsize = (Get-Item $v).Length
    Write-Host "Vendor: $v ($vsize bytes, $([Math]::Round($vsize/1024)) KB)"
}

if ($h -match '<script type="importmap">[\s\S]*?"three":\s*"\./vendor/three\.module\.min\.js"') {
    Write-Host "PASS: import map present"
} else {
    Write-Host "FAIL: import map missing"
}

$cdn = [Regex]::Matches($h, '<script[^>]+src=["''](https?:|//)[^"'']+')
if ($cdn.Count -eq 0) {
    Write-Host "PASS: no CDN <script src>"
} else {
    Write-Host "FAIL: $($cdn.Count) CDN script srcs found"
    $cdn | ForEach-Object { Write-Host "  $($_.Value)" }
}

$globals = @('window.globeBurst', 'window.runCanvas2DGlobe', 'window.__attachFoilOverlay', 'window.__webglConfetti')
foreach ($g in $globals) {
    $count = ([Regex]::Matches($h, [Regex]::Escape($g))).Count
    $tag = if ($count -ge 1) { "PASS" } else { "FAIL" }
    Write-Host "$tag : '$g' x$count"
}

if ($h -match 'function markFallback[\s\S]{0,500}runCanvas2DGlobe\(\)') {
    Write-Host "PASS: markFallback -> runCanvas2DGlobe"
} else {
    Write-Host "FAIL: markFallback->runCanvas2DGlobe linkage missing"
}

$rmCount = ([Regex]::Matches($h, 'prefers-reduced-motion|reducedMotion\(\)')).Count
Write-Host "INFO: reduced-motion references: $rmCount"

@('.foil-webgl', '.meta-chip-link', '.beta-chip') | ForEach-Object {
    $p = $_
    if ($h -match [Regex]::Escape($p)) {
        Write-Host "PASS: CSS $p present"
    } else {
        Write-Host "FAIL: CSS $p missing"
    }
}

if ($h -match 'mountFlipCard[\s\S]{0,2000}__attachFoilOverlay') {
    Write-Host "PASS: mountFlipCard wired to __attachFoilOverlay"
} else {
    Write-Host "FAIL: mountFlipCard not wired to __attachFoilOverlay"
}

if ($h -match 'triggerVictoryFx[\s\S]{0,1500}__webglConfetti') {
    Write-Host "PASS: triggerVictoryFx wired to __webglConfetti"
} else {
    Write-Host "FAIL: triggerVictoryFx not wired to __webglConfetti"
}

$g = Get-Content 'toptrumps.html' -Raw
if ($g -match 'href="\./toptrumps-webgl\.html"') {
    Write-Host "PASS: discovery link in toptrumps.html"
} else {
    Write-Host "FAIL: discovery link missing in toptrumps.html"
}

if ($h -match 'href="\./toptrumps\.html"') {
    Write-Host "PASS: reciprocal link in toptrumps-webgl.html"
} else {
    Write-Host "FAIL: reciprocal link missing"
}

$dy = Get-Content '.github/workflows/deploy.yml' -Raw
$webgl = $dy -match 'toptrumps-webgl\.html'
$ven = $dy -match 'vendor'
Write-Host ("PASS check: deploy includes webgl=" + $webgl + ", vendor=" + $ven)

Write-Host "`n=== Verification complete ==="
