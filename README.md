# LevAI

Assistente pessoal com inteligência artificial integrada. Aplicação web construída com Django que oferece chat com IA, conversão de documentos, ferramentas de vídeo, gerenciamento de tarefas e extração de texto.

## Funcionalidades

- **Chat com IA** — Conversas com modelos locais via Ollama (deepseek-r1:8b para texto, gemma3:27b para imagens). Suporte a envio de documentos, imagens, áudio e vídeo no chat.
- **Conversor de documentos** — Converte arquivos Markdown para PDF com estilo ABNT usando WeasyPrint. Suporte a blocos de código, tabelas, fórmulas matemáticas e notas de rodapé.
- **Ferramentas de vídeo** — Download de vídeos via yt-dlp, conversão de formatos para MP4 e extração de áudio MP3 com MoviePy.
- **Gerenciamento de tarefas** — Calendário mensal interativo com criação, edição e exclusão de tarefas. Suporte a prioridades (baixa, média, alta) e status (pendente, em progresso, concluída).
- **Extração de texto** — Extrai texto de PDFs (pypdf), imagens via OCR (Tesseract) e transcrição de áudio (Google Speech Recognition).
- **Autenticação** — Sistema de login e registro de usuários com modelo customizado.

## Tech Stack

| Componente | Tecnologia |
| --- | --- |
| Framework | Django 5.2 |
| Linguagem | Python 3.13 |
| Banco de dados (produção) | PostgreSQL 17.4 |
| Banco de dados (desenvolvimento) | SQLite3 |
| IA | Ollama (deepseek-r1:8b, gemma3:27b) |
| Validação | Pydantic v2 |
| PDF | WeasyPrint, ReportLab |
| Vídeo/Áudio | MoviePy, FFmpeg, pydub |
| OCR | Tesseract + pytesseract |
| Deploy | Docker + Docker Compose |

## Pré-requisitos

### Dependências do sistema (Linux Ubuntu 24.04 LTS)

#### NVIDIA Container Toolkit

Necessário para executar modelos de IA com aceleração GPU via Docker.

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

```bash
sudo apt-get update
```

```bash
sudo apt-get install -y nvidia-container-toolkit
```

```bash
sudo nvidia-ctk runtime configure --runtime=docker
```

```bash
sudo systemctl restart docker
```

#### Ollama

Servidor local para execução dos modelos de IA.

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull  deepseek-r1:8b
ollama pull gemma3:27b
```

#### Tesseract OCR

Necessário para extração de texto de imagens e PDFs escaneados.

```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-por
tesseract --version
sudo apt install libtesseract-dev libleptonica-dev pkg-config
sudo apt install libpng-dev libjpeg-dev libtiff-dev
which tesseract
```

#### FFmpeg

Necessário para processamento de vídeo e áudio (MoviePy e pydub).

```bash
sudo apt install ffmpeg
```

#### Poppler

Necessário para conversão de PDF em imagens (pdf2image).

```bash
sudo apt install poppler-utils
```

### Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```bash
DB_URL="postgresql+asyncpg://user:password@database:5432/db"
DB_USER="user"
DB_PASSWORD="password"
DB_HOST="database"
DB_PORT="5432"
DB_NAME="db"
TEST_DB_URL="sqlite+aiosqlite:///:memory:"
```

| Variável | Descrição |
| --- | --- |
| `DB_URL` | URL de conexão completa do banco PostgreSQL |
| `DB_USER` | Usuário do banco de dados |
| `DB_PASSWORD` | Senha do banco de dados |
| `DB_HOST` | Host do banco (use `levai-database` para Docker) |
| `DB_PORT` | Porta do banco (padrão: `5432`) |
| `DB_NAME` | Nome do banco de dados |
| `TEST_DB_URL` | URL do banco para testes (SQLite em memória) |

## Dependências Python

Todas as dependências estão definidas em `pyproject.toml`.

### Produção

| Categoria | Pacotes |
| --- | --- |
| Framework | django, pydantic, pydantic-settings |
| IA | ollama |
| Documento/PDF | markdown, weasyprint, reportlab, pypdf, pdf2image, pymdown-extensions, python-markdown-math, pygments, mathjax |
| Vídeo/Áudio | moviepy, ffmpeg, pydub, yt-dlp, pytube, speechrecognition |
| OCR | pytesseract |

### Desenvolvimento

| Pacote | Uso |
| --- | --- |
| black | Formatação de código |
| ruff | Linter |
| pytest | Testes |
| gtts | Texto para fala (experimentação) |
| numpy | Computação numérica |
| pygame | Reprodução de áudio (experimentação) |

## Como executar

### Docker (produção)

```bash
docker compose up -d --build
```

Acesse a aplicação em: `http://localhost:8040`

O comando `make start` automatiza todo o processo: sobe os containers, baixa os modelos do Ollama e executa as migrations.

```bash
make start
```

### Local (desenvolvimento)

Instale as dependências:

```bash
uv sync
```

Ou, usando pip:

```bash
pip install -r requirements.txt
```

Para gerar o `requirements.txt` a partir do `pyproject.toml`:

```bash
make generate-dependencies
```

Aplique as migrations e inicie o servidor:

```bash
python manage.py migrate
python manage.py runserver
```

Acesse em: `http://localhost:8000`

## Comandos úteis (Makefile)

| Comando | Descrição |
| --- | --- |
| `make start` | Sobe containers Docker, baixa modelos Ollama e roda migrations |
| `make lint-fix` | Formata código com black e ruff |
| `make generate-dependencies` | Gera `requirements.txt` a partir do `pyproject.toml` |
| `make create-migrations` | Cria migrations do Django |
| `make run-migrations` | Aplica migrations no banco de dados |
| `make create-app app_name=nome` | Cria um novo app Django |
| `make reset-db` | Remove o banco SQLite e limpa arquivos de migrations |
| `make kabum` | Remove todos os containers, volumes, redes e imagens Docker |

## Estrutura do projeto

```
levai/
├── settings.py              # Configurações do Django
├── urls.py                  # Rotas principais
├── views.py                 # Views de erro customizadas (400, 403, 404, 500)
├── static/                  # CSS, JS e imagens globais
├── templates/               # Templates base e partials
├── apps/
│   ├── home/                # Página inicial
│   ├── chat/                # Chat com IA (listagem + detalhes)
│   ├── document/            # Conversor Markdown para PDF
│   ├── video/               # Ferramentas de vídeo (download, conversão)
│   ├── task/                # Gerenciamento de tarefas (calendário)
│   └── user/                # Autenticação (login, registro)
└── core/
    ├── services/            # Lógica de negócio (AIService, ExtractService)
    ├── repositories/        # Camada de acesso a dados
    ├── schemas/             # Schemas Pydantic (validação)
    ├── utils/               # Utilitários compartilhados
    ├── messages/            # Mensagens de erro/sucesso
    ├── constants.py         # Constantes da aplicação
    └── settings.py          # Configurações Pydantic (variáveis de ambiente)
```

## Referências

- [GitHub Ollama](https://github.com/ollama/ollama)
- [DockerHub Ollama](https://hub.docker.com/r/ollama/ollama)
- [REST API Ollama](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Ollama Python Library](https://github.com/ollama/ollama-python)

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](./LICENCE.txt) para mais detalhes.
