# 🤖 Gemini AI Agent

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini-4285F4.svg)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Um agente de IA inteligente construído com **Python** e **Google Gemini API**, equipado com ferramentas externas para busca na web, leitura de arquivos e execução de comandos.

## ✨ Características

- 🧠 **Memória de Conversa**: Mantém contexto da conversa usando ChatSession
- 🔄 **Histórico Persistente**: Lembra de interações anteriores
- 🤖 **Integração Gemini**: Usa a API do Google Gemini para respostas inteligentes
- 🛠️ **Ferramentas Externas**: Sistema modular de ferramentas
- ⚡ **Performance Otimizada**: Reutilização do modelo para eficiência
- 🛡️ **Tratamento de Erros**: Sistema robusto de tratamento de exceções
- 🌐 **Interface em Português**: Interface amigável e localizada
- 🔧 **Feedback Visual**: Indicações claras de execução de ferramentas
- 📋 **Instruções Inteligentes**: Prompt otimizado para uso de ferramentas
- 🎨 **Interface Sofisticada**: Feedback profissional e elegante

## 🛠️ Ferramentas Disponíveis

### 🔍 Busca na Web
- **Função**: `search_web(query)`
- **Descrição**: Busca informações na web usando DuckDuckGo API
- **Exemplo**: `TOOL: search_web: clima em Paris`

### 📄 Leitura de Arquivos
- **Função**: `read_file(path)`
- **Descrição**: Lê arquivos de texto locais
- **Exemplo**: `TOOL: read_file: exemplo.txt`

### ⚡ Execução de Comandos
- **Função**: `run_command(command)`
- **Descrição**: Executa comandos do sistema operacional
- **Exemplo**: `TOOL: run_command: dir`

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Chave da API do Google Gemini

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/gemini-agent.git
cd gemini-agent
```

### 2. Crie um ambiente virtual
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
# Gemini API Configuration
GOOGLE_API_KEY=sua_chave_api_aqui
GEMINI_MODEL=gemini-1.5-pro

# Agent Configuration
AGENT_NAME=GeminiAgent
AGENT_DESCRIPTION=An intelligent agent powered by Google Gemini

# Memory Configuration
MEMORY_TYPE=local
MEMORY_PATH=./memory

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=./logs/agent.log

# API Configuration (if using main_api.py)
DEBUG=True
HOST=localhost
PORT=8000
```

## 🎯 Uso

### Interface de Linha de Comando
```bash
python src/main.py
```

### Exemplo de Conversa
```
🤖 Olá! Eu sou seu agente de IA com ferramentas inteligentes. Digite 'sair' para encerrar.

Você: Qual é a capital da França?
Agente: A capital da França é Paris.

Você: Pesquise no Google quem é o atual presidente do Brasil.
🔧 O agente decidiu usar uma ferramenta...
Resultado da ferramenta:
Resultado da busca: Luiz Inácio Lula da Silva é o 39º e atual presidente do Brasil desde 1º de janeiro de 2023.

Você: Mostre o conteúdo do arquivo exemplo.txt
🔧 O agente decidiu usar uma ferramenta...
Resultado da ferramenta:
Este é um arquivo de exemplo.
Contém informações importantes para testar a ferramenta de leitura.
O agente pode ler este arquivo usando a ferramenta read_file.

Você: sair
👋 Até logo!
```

## 📁 Estrutura do Projeto

```
gemini-agent/
├── src/
│   ├── __init__.py
│   ├── agent.py              # Lógica principal do agente
│   ├── chat_session.py       # Gerenciamento de memória
│   ├── gemini_client.py      # Cliente da API Gemini
│   ├── main.py              # Ponto de entrada principal
│   ├── tool_executor.py     # Executor de ferramentas
│   └── tools.py             # Definições das ferramentas
├── .env                     # Variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
├── requirements.txt        # Dependências Python
├── settings.py            # Configurações do projeto
├── exemplo.txt           # Arquivo de exemplo para testes
└── README.md            # Este arquivo
```

## 🔧 Configuração

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|---------|
| `GOOGLE_API_KEY` | Chave da API do Google Gemini | **Obrigatório** |
| `GEMINI_MODEL` | Modelo do Gemini a usar | `gemini-1.5-pro` |
| `AGENT_NAME` | Nome do agente | `GeminiAgent` |
| `AGENT_DESCRIPTION` | Descrição do agente | `An intelligent agent powered by Google Gemini` |
| `MEMORY_TYPE` | Tipo de memória | `local` |
| `MEMORY_PATH` | Caminho da memória | `./memory` |
| `LOG_LEVEL` | Nível de log | `INFO` |
| `LOG_FILE` | Arquivo de log | `./logs/agent.log` |

### Dependências

```
google-generativeai==0.7.2
python-dotenv==1.0.1
fastapi==0.115.0
uvicorn==0.30.6
pydantic==2.8.2
requests==2.32.3
rich==13.7.1
```

## 🧪 Testes

### Teste das Ferramentas
```bash
# Teste individual das ferramentas
python -c "from src.tools import search_web, read_file, run_command; print('Testando ferramentas...')"

# Teste do executor de ferramentas
python -c "from src.tool_executor import execute_tool; print(execute_tool('TOOL: search_web: teste'))"
```

### Teste do Agente Completo
```bash
python src/main.py
```

## 🔒 Segurança

- **Chaves de API**: Nunca commite chaves de API no repositório
- **Arquivo .env**: Está no `.gitignore` para proteção
- **Validação**: Todas as entradas são validadas antes do processamento
- **Tratamento de Erros**: Sistema robusto de tratamento de exceções

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🙏 Agradecimentos

- [Google Gemini API](https://ai.google.dev) pela API de IA
- [DuckDuckGo](https://duckduckgo.com) pela API de busca
- Comunidade Python pelos pacotes utilizados

## 📞 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique se todas as dependências estão instaladas
2. Confirme se a chave da API está configurada corretamente
3. Verifique os logs para mais detalhes sobre erros
4. Abra uma issue no GitHub

---

**Desenvolvido com ❤️ usando Python e Google Gemini API**