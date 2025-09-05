# ===============================
# Setup Projeto Python no Windows
# ===============================

# Versão do Python que você quer usar
$PythonVersion = "3.12.0"
$EnvName = "venv"
$ReqFile = "requirements.txt"

Write-Host "=============================="
Write-Host "1️ Configurando Python com pyenv-win"
Write-Host "=============================="

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
Write-Host "2️ Criando ambiente virtual"
Write-Host "=============================="

python -m venv $EnvName

Write-Host "=============================="
Write-Host "3️ Ativando ambiente virtual"
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

Write-Host "=============================="
Write-Host "4️ Instalando Taskipy"
Write-Host "=============================="

pip install --upgrade pip
pip install taskipy
python.exe -m pip install --upgrade pip

Write-Host "=============================="
Write-Host "5️ Gerando requirements.txt"
Write-Host "=============================="

pip freeze > $ReqFile
Write-Host "$ReqFile criado/atualizado com sucesso"

Write-Host "=============================="
Write-Host "Setup concluído!"
Write-Host "Para ativar o ambiente futuramente: .\$EnvName\Scripts\Activate.ps1"
