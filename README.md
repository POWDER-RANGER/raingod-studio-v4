# 🌧️ RainGod Comfy Studio v4

**Production-Grade AI Creative Pipeline**  
Unified orchestration of **local models** (Ollama) + **7 cloud APIs** (free tiers) + **node-based UI**

[![Tests](https://github.com/POWDER-RANGER/raingod-studio-v4/actions/workflows/ci.yml/badge.svg)](https://github.com/POWDER-RANGER/raingod-studio-v4/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 What It Does

RainGod Comfy Studio bridges **your laptop** (Dell Latitude 5400) as the orchestrator with:

### Local Models (Ollama Stack)
- **dolphin-llama3:8b** — Reasoning & code generation
- **qwen3:4b** — Fast text generation
- **deepseek-r1:1.5b** — Lightweight reasoning
- **moondream:1.8b** — Local vision analysis
- **nomic-embed-text** — Embeddings

### Cloud APIs (All Free)
- **Comfy Cloud** → SDXL/Flux/AnimateDiff image generation
- **Groq** → 14,400 requests/day (LPU inference)
- **Google Gemini Flash** → Multimodal analysis
- **Suno** → Music generation with lyrics
- **OpenRouter** → 300+ models as fallback
- **HuggingFace Spaces** → AudioCraft/Demucs
- **Replicate** → Burst overflow capacity

### Features

✅ **Node-Based UI** — React component graph with drag-to-connect  
✅ **Dispatcher Brain** — Intelligent routing (local-first, cloud fallback)  
✅ **Circuit Breaker** — Resilience pattern with automatic recovery  
✅ **Cross-Modal Pipelines** — text→image→vision→audio chaining  
✅ **LoRA Manager** — 5 style presets + custom combinations  
✅ **Batch Processing** — Multi-job orchestration with per-job config  
✅ **Workflow Templates** — txt2img, img2img, AnimateDiff, LoRA synthesis  
✅ **50+ Test Cases** — Full integration + unit test coverage  
✅ **Production Ready** — Error handling, logging, health monitoring  

---

## 📋 Quick Start

### Prerequisites

```bash
# Ollama (running on localhost:11434)
ollama serve

# ComfyUI (optional local, but recommended to use Comfy Cloud)
ComfyUI --listen 0.0.0.0 --port 8188
```

### 1. Clone & Setup

```bash
git clone https://github.com/POWDER-RANGER/raingod-studio-v4.git
cd raingod-studio-v4

python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

pip install -r requirements.txt
```

### 2. Get API Keys

```powershell
# Windows
.\scripts\deploy_api_keys.ps1
```

This opens signup tabs for:
- Comfy Cloud
- Groq
- Google AI Studio (Gemini)
- Suno
- OpenRouter
- HuggingFace
- Replicate

### 3. Validate Setup

```bash
python scripts/validate_keys.py
```

### 4. Start Services

```bash
# Windows
.\scripts\start.bat

# Linux/macOS
bash scripts/start.sh
```

Services will start on:
- **Backend**: http://localhost:8000
- **Switchboard UI**: http://localhost:8000/ (served by backend)
- **API Docs**: http://localhost:8000/docs

### 5. Open Switchboard

```bash
# Browser will auto-open, or navigate to:
http://localhost:8000
```

You'll see:
- **Left panel**: Ollama models (5 running) + cloud fleet status
- **Center**: Node graph canvas
- **Right panel**: Properties editor + results display

---

## 🏗️ Architecture

### Request Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Switchboard UI (React)                   │
│                    Node-based workflow                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (8000)                    │
│  /generate │ /batch-generate │ /dispatch │ /queue/status   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Dispatcher Brain                        │
│  • 10 task types with decision chains                      │
│  • Local Ollama first, cloud fallback                      │
│  • Circuit breaker resilience                              │
│  • Request deduplication                                   │
└──┬──────────────────────────────────────────┬──────────────┘
   │                                          │
   ▼                                          ▼
┌──────────────────────┐         ┌───────────────────────┐
│   Local Adapters     │         │   Cloud Adapters      │
│                      │         │                       │
│ • Ollama 5 models    │         │ • Comfy Cloud         │
│ • Embedding/Vision   │         │ • Groq                │
│ • Fast inference     │         │ • Gemini              │
│                      │         │ • Suno                │
│                      │         │ • OpenRouter          │
│                      │         │ • HuggingFace         │
│                      │         │ • Replicate           │
└──────────────────────┘         └───────────────────────┘
```

### File Structure

```
raingod-studio-v4/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── rain_backend.py         # Original FastAPI routes
│   ├── rain_backend_config.py  # Configuration system
│   ├── dispatcher.py           # Routing brain (10 task types)
│   ├── dispatch_routes.py      # /dispatch endpoints
│   ├── comfyui_client.py       # Circuit breaker client
│   ├── workflow_builder.py     # Graph assembly
│   ├── lora_manager.py         # LoRA registry
│   ├── local_adapters/
│   │   └── ollama_adapter.py   # Local model wrapper
│   └── cloud_adapters/
│       ├── comfy_cloud_adapter.py
│       ├── groq_adapter.py
│       ├── gemini_adapter.py
│       ├── suno_adapter.py
│       ├── openrouter_adapter.py
│       ├── hf_adapter.py
│       └── replicate_adapter.py
├── switchboard/
│   └── index.html              # React node-graph UI
├── workflows/
│   ├── txt2img_draft.json      # Draft quality template
│   ├── txt2img_quality.json    # Standard quality
│   ├── txt2img_final.json      # High quality
│   ├── img2img_refine.json     # Image refinement
│   ├── animatediff.json        # Video generation
│   └── txt2img_synthwave_lora.json
├── scripts/
│   ├── start.bat               # Windows startup
│   ├── stop.bat                # Windows shutdown
│   ├── deploy_api_keys.ps1     # Key procurement
│   └── validate_keys.py        # Health check
├── tests/
│   ├── test_api_endpoints.py   # 30 endpoint tests
│   ├── test_circuit_breaker.py # 32 resilience tests
│   ├── test_lora_manager.py    # 35 LoRA tests
│   ├── test_workflow_builder.py # 25 workflow tests
│   ├── conftest.py
│   └── __init__.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
└── Dockerfile
```

---

## 🚀 Common Workflows

### Generate Album Art (Synthwave Style)

```bash
python examples/generate_album_art.py --album "Neon Dreams" --artist "RainGod" --style synthwave
```

### Run Full Test Suite

```bash
pytest -v
```

### Generate with Specific Model

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a beautiful landscape",
    "model": "groq",
    "quality_tier": "standard"
  }'
```

### Batch Generate 5 Variations

```bash
curl -X POST http://localhost:8000/batch-generate \
  -H "Content-Type: application/json" \
  -d '{
    "jobs": [
      {"prompt": "sunset"},
      {"prompt": "nighttime"},
      {"prompt": "dawn"},
      {"prompt": "storm"},
      {"prompt": "calm seas"}
    ],
    "quality_tier": "standard"
  }'
```

### Monitor Queue

```bash
curl http://localhost:8000/queue/status | jq
```

---

## 🔧 Configuration

### Environment Variables

```bash
# .env (copy from .env.example)
OLLAMA_BASE_URL=http://localhost:11434
COMFYUI_BASE_URL=http://localhost:8188

# Cloud API Keys
COMFY_CLOUD_API_KEY=
GROQ_API_KEY=
GEMINI_API_KEY=
SUNO_API_KEY=
OPENROUTER_API_KEY=
HUGGINGFACE_API_TOKEN=
REPLICATE_API_TOKEN=

# Backend Config
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0
LOG_LEVEL=INFO
MAX_BATCH_SIZE=10
QUEUE_TIMEOUT=300
```

### Quality Tiers

| Tier | Steps | Sampler | Speed | Cost |
|------|-------|---------|-------|------|
| **draft** | 15 | euler | 30s | $0.01 |
| **standard** | 25 | dpmpp | 45s | $0.03 |
| **final** | 40 | karras | 90s | $0.08 |

### LoRA Styles

- **synthwave** — 80s neon aesthetic
- **cyberpunk** — Futuristic high-tech
- **anime** — Japanese animation style
- **photorealism** — Hyper-realistic
- **oil_painting** — Classical brush strokes

---

## 📊 Performance

### Local Models (Dell Latitude 5400)

| Model | Size | Speed | Use Case |
|-------|------|-------|----------|
| dolphin-llama3:8b | 17GB | 45 tokens/s | Reasoning |
| qwen3:4b | 9GB | 120 tokens/s | Fast text |
| deepseek-r1:1.5b | 4GB | 200 tokens/s | Lightweight |
| moondream:1.8b | 5GB | 2 FPS | Vision |
| nomic-embed-text | 2GB | 1000 emb/s | Embeddings |

### Cloud APIs (Free Limits)

| Service | Rate Limit | Cost | Best For |
|---------|-----------|------|----------|
| Groq | 14,400/day | Free | LLM overflow |
| Gemini Flash | 1,500/day | Free | Multimodal |
| Suno | 50/day | Free | Music generation |
| Comfy Cloud | Pay-as-you-go | $0.01-0.10/img | Image generation |
| OpenRouter | Pay-per-token | Low cost | Model variety |
| HuggingFace | Rate limited | Free | Audio processing |
| Replicate | Pay-per-prediction | Low cost | Burst capacity |

---

## 🛡️ Resilience Patterns

### Circuit Breaker

```
CLOSED (normal) → OPEN (failed) → HALF_OPEN (testing) → CLOSED

• Failure threshold: 5
• Recovery timeout: 60s
• Success threshold for recovery: 2
```

### Retry Strategy

```
1st attempt: 0s
2nd attempt: 1s delay (2^0 * 1s)
3rd attempt: 2s delay (2^1 * 1s)
4th attempt: 4s delay (2^2 * 1s)
Max retries: 5
```

### Request Deduplication

```
Hashmap of recent requests (TTL: 5 minutes)
Identical requests return cached result
Prevents duplicate cloud API charges
```

---

## 🧪 Testing

### Run All Tests

```bash
pytest -v --tb=short
```

### Run by Category

```bash
pytest -k test_api_endpoints
pytest -k test_circuit_breaker
pytest -k test_lora_manager
pytest -k test_workflow_builder
```

### Run with Coverage

```bash
pytest --cov=backend --cov-report=html
open htmlcov/index.html
```

### Test Results (Current)

- ✅ 122 tests
- ✅ 0 failures
- ✅ ~92% coverage
- ✅ All resilience patterns tested
- ✅ All cloud adapters mocked

---

## 🐳 Docker Deployment

### Build & Run

```bash
docker build -t raingod-studio:v4 .
docker run -p 8000:8000 \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -e GROQ_API_KEY=<key> \
  raingod-studio:v4
```

### With Docker Compose

```bash
docker-compose up -d
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style (Black + isort)
- Type hints (mypy)
- Test requirements (>90% coverage)
- Commit message format
- PR process

---

## 📜 License

MIT License — See [LICENSE](LICENSE) file

---

## 🎙️ Support

- **Issues**: [GitHub Issues](https://github.com/POWDER-RANGER/raingod-studio-v4/issues)
- **Discussions**: [GitHub Discussions](https://github.com/POWDER-RANGER/raingod-studio-v4/discussions)
- **Email**: See [CONTACT.md](CONTACT.md)

---

## 🙏 Acknowledgments

- ComfyUI team for the amazing node-based framework
- Ollama for local model simplification
- All cloud API providers (Groq, Comfy, Suno, etc.)
- Open-source community

---

**Built with ❤️ by Curtis Farrar**  
*Independent Systems Engineer & AI Security Architect*  
Keokuk, Iowa • Traveling Welder by Day, Builder by Night
