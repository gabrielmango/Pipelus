# ===============================
# Setup Projeto Python no Windows
# ===============================

# Versão do Python que você quer usar
$PythonVersion = "3.12.0"
$EnvName = "venv"
$ReqFile = "requirements.txt"

Write-Host "================================="
Write-Host "Configurando Python com pyenv-win"
Write-Host "================================="

# Verifica se a versão do Python já está instalada
$installed = pyenv versions | Select-String $PythonVersion
if (-not $installed) {
    Write-Host "Instalando Python $PythonVersion via pyenv..."
    pyenv install $PythonVersion
} else {
    Write-Host "Python $PythonVersion já instalado"
}

# Define a versão local do projeto
pyenv local $PythonVersion
Write-Host "Python ativo no projeto: $(python --version)"

Write-Host "=============================="
Write-Host "Criando ambiente virtual"
Write-Host "=============================="

if (-Not (Test-Path $EnvName)) {
    python -m venv $EnvName
    Write-Host "Ambiente virtual $EnvName criado com sucesso"
} else {
    Write-Host "Ambiente virtual $EnvName já existe"
}

Write-Host "=============================="
Write-Host "Ativando ambiente virtual"
Write-Host "=============================="

# Ativa o ambiente no terminal atual
$activatePath = ".\$EnvName\Scripts\Activate.ps1"
if (Test-Path $activatePath) {
    Write-Host "Ativando $EnvName..."
    & $activatePath
} else {
    Write-Host "Erro: arquivo de ativação não encontrado!"
    exit
}

Write-Host "=================================="
Write-Host "Instalando dependências existentes"
Write-Host "=================================="

if (Test-Path $ReqFile) {
    Write-Host "$ReqFile encontrado! Instalando dependências..."
    pip install -r $ReqFile
    Write-Host "Dependências instaladas com sucesso!"
} else {
    Write-Host "$ReqFile não encontrado!"
}

Write-Host "=============================="
Write-Host "Setup concluído!"
Write-Host "Para ativar o ambiente futuramente: .\$EnvName\Scripts\Activate.ps1"
