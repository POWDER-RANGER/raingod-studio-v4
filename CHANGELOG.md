# Changelog

All notable changes to RainGod Comfy Studio will be documented in this file.

## [4.0.0] - 2026-03-16

### Added
- **Unified Repository** — Merged RAINGOD-ComfyUI-Integration backend into studio
- **Dispatcher Brain** — Intelligent routing across 10 task types with local-first fallback
- **Local Models** — Ollama integration (5 models)
- **Cloud APIs** — 7 cloud adapter implementations (Comfy Cloud, Groq, Gemini, Suno, OpenRouter, HuggingFace, Replicate)
- **Switchboard UI** — React node-based interface with drag-to-connect workflows
- **Circuit Breaker** — Resilience pattern with automatic recovery
- **Request Deduplication** — Prevent duplicate API calls via hashing
- **Connection Pooling** — Concurrent request handling
- **Cross-Modal Pipelines** — Text→Image→Vision→Audio chaining
- **LoRA Manager** — 5 style presets + custom combinations
- **Workflow Builder** — Graph assembly with validation and serialization
- **Batch Processing** — Multi-job orchestration
- **122 Tests** — Comprehensive test coverage (30 API, 32 resilience, 35 LoRA, 25 workflow)
- **Docker Support** — Multi-stage Dockerfile + docker-compose
- **CI/CD** — GitHub Actions with Black/mypy/ruff/pytest
- **Documentation** — README, CONTRIBUTING, CHANGELOG, architecture guide

### Features

#### Backend
- FastAPI application with 9 REST endpoints
- Health checks and diagnostics
- Configuration system with 7 resolution presets, 3 quality tiers
- Error handling with graceful degradation
- Structured logging
- Request validation with Pydantic

#### Adapters
- **Ollama** — Local inference for 5 models
- **Comfy Cloud** — SDXL, Flux, AnimateDiff workflows
- **Groq** — 14,400 requests/day LPU inference
- **Gemini Flash** — Multimodal analysis
- **Suno** — Music generation with lyrics
- **OpenRouter** — 300+ model fallback
- **HuggingFace Spaces** — AudioCraft, Demucs
- **Replicate** — Burst capacity, SDXL-Lightning

#### UI
- 11 node types (text, image, sampler, decoder, etc.)
- Drag-to-connect workflow building
- Cubic bezier SVG connections
- Live adapter status indicators
- Per-node run buttons
- Result panel with metadata

### Configuration
- 7 resolution presets (thumbnail → 4K)
- 5 sampler presets (fast/quality/ultra)
- 3 quality tiers (draft/standard/final)
- 5 LoRA style presets
- Batch processing configuration
- Cache & optimization settings

### Testing
- 122 comprehensive tests
- AsyncMock for cloud adapter mocking
- Fixture-based test setup
- Coverage >90%
- Async test support with pytest

### Quality
- Black code formatting
- isort import sorting
- mypy type checking
- ruff linting
- 90%+ test coverage requirement

### Documentation
- Comprehensive README with quick start
- Architecture documentation
- Contributing guidelines
- API documentation (FastAPI /docs)
- Inline docstrings (Google style)

## [3.0.0] - Previous (Integration Repo)

### Build Progress
- Phase 1: 40% complete (15/50+ files)
- All critical backend infrastructure production-ready
- Core FastAPI, ComfyUI client, configuration system complete
- Quickstart automation and documentation complete

---

## Versioning

This project follows [Semantic Versioning](https://semver.org/)

## Roadmap

### Planned (v4.1)
- Web-based file upload interface
- Advanced prompt engineering UI
- Model fine-tuning integration
- Real-time queue visualization
- WebSocket push updates

### Planned (v4.2)
- Multi-user authentication
- Workflow history & versioning
- Custom node types
- GPU VRAM monitoring
- Cost tracking across cloud APIs

### Planned (v5.0)
- Distributed processing
- Plugin architecture
- Advanced analytics
- Performance profiling
- Mobile app
