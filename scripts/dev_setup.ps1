# dev_setup.ps1
# Configura el entorno de desarrollo local (Windows + VS Code)

Write-Host "=== Configuracion del entorno de desarrollo ===" -ForegroundColor Green
Write-Host ""

# 1. Crear entorno virtual
if (-not (Test-Path ".venv")) {
    Write-Host "[1/4] Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "  OK" -ForegroundColor Green
} else {
    Write-Host "[1/4] Entorno virtual ya existe" -ForegroundColor Cyan
}

# 2. Activar e instalar paquete
Write-Host "[2/4] Instalando paquete en modo editable..." -ForegroundColor Yellow
& ".\.venv\Scripts\pip.exe" install -e . 2>&1 | Out-Null
Write-Host "  OK" -ForegroundColor Green

# 3. Instalar dependencias de desarrollo
Write-Host "[3/4] Instalando dependencias de desarrollo..." -ForegroundColor Yellow
& ".\.venv\Scripts\pip.exe" install black ruff pytest 2>&1 | Out-Null
Write-Host "  OK" -ForegroundColor Green

# 4. Verificar
Write-Host "[4/4] Verificando instalacion..." -ForegroundColor Yellow
& ".\.venv\Scripts\python.exe" -c "from libreria_analisismolecular import colab; print('  Paquete importado OK')"
Write-Host "  OK" -ForegroundColor Green

Write-Host ""
Write-Host "Entorno listo! Activalo con:" -ForegroundColor Green
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
