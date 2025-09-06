@echo off
echo 🚀 Deploy do Gemini AI Agent para Vercel
echo ========================================

REM Verificar se Vercel CLI está instalado
where vercel >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Vercel CLI não encontrado!
    echo 📦 Instalando Vercel CLI...
    npm install -g vercel
    echo ✅ Vercel CLI instalado!
) else (
    echo ✅ Vercel CLI encontrado!
)

REM Verificar se está logado
echo 🔐 Verificando login na Vercel...
vercel whoami >nul 2>nul
if %errorlevel% neq 0 (
    echo 🔑 Faça login na Vercel:
    vercel login
) else (
    echo ✅ Já está logado na Vercel!
)

REM Deploy
echo 🚀 Iniciando deploy...
vercel

echo ✅ Deploy concluído!
echo 🌐 Sua API estará disponível em: https://seu-projeto.vercel.app
echo.
echo 📋 Próximos passos:
echo 1. Configure as variáveis de ambiente na Vercel:
echo    - GOOGLE_API_KEY: sua_chave_api
echo    - GEMINI_MODEL: gemini-1.5-pro
echo 2. Teste a API:
echo    curl https://seu-projeto.vercel.app/health

pause
