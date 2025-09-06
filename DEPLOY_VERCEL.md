# 🚀 Deploy na Vercel - Gemini AI Agent

Este guia mostra como fazer deploy do **Gemini AI Agent** na Vercel como uma API web.

## 📋 Pré-requisitos

- Conta na [Vercel](https://vercel.com)
- [Vercel CLI](https://vercel.com/cli) instalado
- Chave da API do Google Gemini

## 🔧 Configuração

### 1. Instalar Vercel CLI
```bash
npm i -g vercel
```

### 2. Configurar Variáveis de Ambiente
Na Vercel, adicione as seguintes variáveis de ambiente:

| Variável | Valor | Descrição |
|----------|-------|-----------|
| `GOOGLE_API_KEY` | sua_chave_api | Chave da API do Google Gemini |
| `GEMINI_MODEL` | gemini-1.5-pro | Modelo do Gemini |

### 3. Deploy
```bash
# Login na Vercel
vercel login

# Deploy do projeto
vercel

# Deploy para produção
vercel --prod
```

## 🌐 Endpoints da API

### **GET** `/`
- **Descrição**: Health check básico
- **Resposta**: Status da API

### **GET** `/health`
- **Descrição**: Verificação de saúde da API
- **Resposta**: Status detalhado

### **POST** `/chat`
- **Descrição**: Enviar mensagem para o agente
- **Body**:
  ```json
  {
    "message": "Sua mensagem aqui",
    "session_id": "opcional"
  }
  ```
- **Resposta**:
  ```json
  {
    "response": "Resposta do agente",
    "used_tool": true/false,
    "tool_name": "nome_da_ferramenta",
    "session_id": "id_da_sessao"
  }
  ```

### **GET** `/sessions`
- **Descrição**: Listar sessões ativas
- **Resposta**: Lista de IDs de sessão

### **DELETE** `/sessions/{session_id}`
- **Descrição**: Limpar sessão específica
- **Resposta**: Confirmação de remoção

## 🧪 Testando a API

### Exemplo com cURL
```bash
# Health check
curl https://seu-projeto.vercel.app/health

# Enviar mensagem
curl -X POST https://seu-projeto.vercel.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá, como você está?"}'

# Usar sessão específica
curl -X POST https://seu-projeto.vercel.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Qual é a capital da França?", "session_id": "user123"}'
```

### Exemplo com JavaScript
```javascript
// Enviar mensagem
const response = await fetch('https://seu-projeto.vercel.app/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Pesquise no Google sobre inteligência artificial',
    session_id: 'user123'
  })
});

const data = await response.json();
console.log(data.response);
```

## 🔧 Ferramentas Disponíveis

A API suporta as mesmas ferramentas do agente CLI:

- **search_web(query)**: Busca na web
- **read_file(path)**: Leitura de arquivos
- **run_command(command)**: Execução de comandos

## 📊 Monitoramento

- **Logs**: Acesse os logs na dashboard da Vercel
- **Métricas**: Monitore uso e performance
- **Erros**: Verifique logs de erro em tempo real

## 🚨 Limitações da Vercel

- **Timeout**: 10 segundos para funções serverless
- **Memória**: Limitada para sessões longas
- **Arquivos**: Não persiste arquivos localmente
- **Comandos**: `run_command` pode ter limitações

## 🔄 Atualizações

Para atualizar o deploy:
```bash
# Deploy automático
git push origin main

# Deploy manual
vercel --prod
```

## 🆘 Solução de Problemas

### Erro de Timeout
- Reduza o tamanho das respostas
- Use sessões menores

### Erro de Memória
- Limpe sessões antigas regularmente
- Use `/sessions` para gerenciar

### Erro de API Key
- Verifique se `GOOGLE_API_KEY` está configurada
- Confirme se a chave é válida

## 📞 Suporte

Para problemas específicos da Vercel:
- [Documentação Vercel](https://vercel.com/docs)
- [Suporte Vercel](https://vercel.com/support)

---

**Deploy realizado com sucesso! 🎉**
