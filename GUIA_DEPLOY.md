# 🚀 Guia Passo-a-Passo para Deploy na Vercel

## 📋 Pré-requisitos

### 1. Conta na Vercel
- Acesse [vercel.com](https://vercel.com)
- Crie uma conta gratuita
- Conecte com GitHub (recomendado)

### 2. Chave da API do Google Gemini
- Acesse [Google AI Studio](https://aistudio.google.com)
- Crie uma chave de API
- Copie a chave (começa com `AIza...`)

## 🔧 Deploy Automático (Recomendado)

### Opção 1: Via GitHub (Mais Fácil)
1. **Conecte o repositório na Vercel:**
   - Acesse [vercel.com/new](https://vercel.com/new)
   - Clique em "Import Git Repository"
   - Selecione `Thiago-Martins05/agent-ia`
   - Clique em "Import"

2. **Configure as variáveis de ambiente:**
   - Na tela de configuração, vá em "Environment Variables"
   - Adicione:
     - `GOOGLE_API_KEY` = sua chave da API
     - `GEMINI_MODEL` = `gemini-1.5-pro`
   - Clique em "Deploy"

3. **Pronto!** Sua API estará disponível em `https://seu-projeto.vercel.app`

### Opção 2: Via Vercel CLI

#### Windows:
```cmd
# Execute o script automático
deploy.bat
```

#### Linux/Mac:
```bash
# Execute o script automático
chmod +x deploy.sh
./deploy.sh
```

#### Manual:
```bash
# 1. Instalar Vercel CLI
npm install -g vercel

# 2. Login na Vercel
vercel login

# 3. Deploy
vercel

# 4. Deploy para produção
vercel --prod
```

## ⚙️ Configuração das Variáveis de Ambiente

### Na Dashboard da Vercel:
1. Acesse seu projeto
2. Vá em "Settings" → "Environment Variables"
3. Adicione:

| Nome | Valor | Ambiente |
|------|-------|----------|
| `GOOGLE_API_KEY` | `AIzaSy...` | Production, Preview, Development |
| `GEMINI_MODEL` | `gemini-1.5-pro` | Production, Preview, Development |

## 🧪 Testando o Deploy

### 1. Health Check
```bash
curl https://seu-projeto.vercel.app/health
```

**Resposta esperada:**
```json
{
  "status": "success",
  "message": "API saudável e pronta para uso"
}
```

### 2. Teste de Chat
```bash
curl -X POST https://seu-projeto.vercel.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá, como você está?"}'
```

### 3. Teste com Ferramenta
```bash
curl -X POST https://seu-projeto.vercel.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Pesquise no Google sobre inteligência artificial"}'
```

## 🌐 Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Health check básico |
| GET | `/health` | Verificação de saúde |
| POST | `/chat` | Enviar mensagem |
| GET | `/sessions` | Listar sessões |
| DELETE | `/sessions/{id}` | Limpar sessão |

## 📱 Exemplo de Uso com Frontend

### JavaScript/React:
```javascript
const chatWithAgent = async (message) => {
  const response = await fetch('https://seu-projeto.vercel.app/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      session_id: 'user123'
    })
  });
  
  const data = await response.json();
  return data.response;
};

// Uso
chatWithAgent('Qual é a capital da França?')
  .then(response => console.log(response));
```

### Python:
```python
import requests

def chat_with_agent(message, session_id="default"):
    url = "https://seu-projeto.vercel.app/chat"
    data = {
        "message": message,
        "session_id": session_id
    }
    
    response = requests.post(url, json=data)
    return response.json()

# Uso
result = chat_with_agent("Pesquise no Google sobre Python")
print(result["response"])
```

## 🔄 Atualizações

### Deploy Automático:
- Faça push para o GitHub
- A Vercel fará deploy automático

### Deploy Manual:
```bash
vercel --prod
```

## 🚨 Solução de Problemas

### Erro 500 - Internal Server Error
- Verifique se `GOOGLE_API_KEY` está configurada
- Confirme se a chave é válida

### Timeout
- Reduza o tamanho das mensagens
- Use sessões menores

### CORS Error
- A API já tem CORS habilitado
- Verifique se está usando HTTPS

## 📊 Monitoramento

### Logs:
- Acesse a dashboard da Vercel
- Vá em "Functions" → "View Function Logs"

### Métricas:
- Monitore uso e performance
- Verifique tempo de resposta

## 🎉 Pronto!

Sua API estará funcionando em:
**https://seu-projeto.vercel.app**

### Teste Rápido:
```bash
curl https://seu-projeto.vercel.app/health
```

---

**Deploy realizado com sucesso! 🚀**
