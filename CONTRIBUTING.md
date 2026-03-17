# Contributing to RainGod Comfy Studio

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful, collaborative, and constructive in all interactions.

---

## Getting Started

### Fork & Clone

```bash
git clone https://github.com/<your-username>/raingod-studio-v4.git
cd raingod-studio-v4
git remote add upstream https://github.com/POWDER-RANGER/raingod-studio-v4.git
```

### Setup Development Environment

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

pip install -r requirements.txt
pip install -r requirements-dev.txt  # (pytest, black, mypy, etc.)
```

---

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming:
- `feature/` — New features
- `bugfix/` — Bug fixes
- `docs/` — Documentation
- `test/` — Test additions
- `refactor/` — Code improvements

### 2. Make Changes

Write code following the style guide (below).

### 3. Write Tests

All new code requires tests:

```bash
# Add tests in tests/test_*.py
pytest tests/test_your_feature.py -v
```

Minimum coverage: **90%**

### 4. Format & Lint

```bash
# Auto-format with Black
black backend/ tests/

# Sort imports with isort
isort backend/ tests/

# Type check with mypy
mypy backend/

# Lint with ruff
ruff check backend/ tests/
```

### 5. Commit with Conventional Commits

```bash
git commit -m "feat(dispatcher): add task type routing logic"
git commit -m "fix(circuit-breaker): reset failure count on recovery"
git commit -m "test(api): add endpoint validation tests"
git commit -m "docs(readme): update architecture diagram"
```

Format: `type(scope): message`

**Types:**
- `feat` — New feature
- `fix` — Bug fix
- `test` — Test additions
- `docs` — Documentation
- `refactor` — Code refactoring
- `perf` — Performance improvement
- `ci` — CI/CD changes
- `chore` — Maintenance

### 6. Push & Create PR

```bash
git push origin feature/your-feature-name
```

Then open a PR on GitHub.

---

## Code Style Guide

### Python

**Black formatter** (line length: 100)

```python
# ✅ Good
def process_request(
    payload: dict, model: str, quality_tier: str = "standard"
) -> dict:
    """Process a generation request.
    
    Args:
        payload: Request data
        model: Target model name
        quality_tier: Quality level (draft/standard/final)
        
    Returns:
        Response dictionary
    """
    pass


# ❌ Bad
def process_request(payload, model, quality_tier="standard"):
    # Process it
    pass
```

### Type Hints (mypy)

**All functions require type hints:**

```python
from typing import Optional, List, Dict, Any, AsyncIterator

# ✅ Good
async def get_queue_status(client_pool: int = 5) -> Dict[str, Any]:
    pending: List[str] = []
    running: Optional[str] = None
    return {"pending": pending, "running": running}


# ❌ Bad
async def get_queue_status(client_pool=5):
    return {}
```

### Docstrings (Google style)

```python
def calculate_strength(
    lora_name: str, base_strength: float = 0.75
) -> float:
    """Calculate effective LoRA strength with validation.
    
    Args:
        lora_name: Name of LoRA to apply
        base_strength: Base strength value (0.0-1.0)
        
    Returns:
        Calculated strength clamped to [0.0, 1.0]
        
    Raises:
        ValueError: If lora_name not found
        
    Example:
        >>> strength = calculate_strength("synthwave", 0.8)
        >>> assert 0 <= strength <= 1
    """
    pass
```

### Async/Await

```python
# ✅ Use async for I/O-bound operations
async def dispatch_request(task: Dict[str, Any]) -> dict:
    """Dispatch to appropriate adapter asynchronously."""
    result = await ollama_adapter.generate(task)
    return result


# ✅ Proper error handling
try:
    result = await adapter.call()
except asyncio.TimeoutError:
    logger.error("Request timeout, falling back to secondary")
except ValueError as e:
    logger.error(f"Validation error: {e}")
```

---

## Testing Requirements

### Test Structure

```python
import pytest
from unittest.mock import patch, AsyncMock


class TestMyFeature:
    """Tests for my_feature module."""

    @pytest.fixture
    def sample_data(self):
        """Setup sample data."""
        return {"key": "value"}

    def test_function_success(self, sample_data):
        """Test successful case."""
        result = process(sample_data)
        assert result is not None

    def test_function_error(self, sample_data):
        """Test error handling."""
        with pytest.raises(ValueError):
            process(None)

    @pytest.mark.asyncio
    async def test_async_function(self, sample_data):
        """Test async function."""
        result = await async_process(sample_data)
        assert result is not None
```

### Coverage Requirements

```bash
# Must maintain >90% coverage
pytest --cov=backend --cov-fail-under=90
```

---

## Documentation

### Markdown

- Use clear, concise language
- Include examples
- Link to related docs
- Keep README focused on quick start
- Add detailed guides to `/docs` folder

### Docstrings

- Google-style format
- Describe all parameters
- Document return values
- Include examples for public APIs
- List raised exceptions

---

## PR Checklist

Before submitting:

- [ ] Code follows style guide (Black, mypy, ruff)
- [ ] Tests added (>90% coverage)
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] No breaking changes (or clearly documented)
- [ ] CI/CD passes

---

## Issues & Discussions

### Report Bugs

Include:
- Reproduction steps
- Expected vs actual behavior
- Python version and OS
- Error trace

### Feature Requests

Include:
- Use case / motivation
- Proposed solution (if any)
- Alternative approaches considered

---

## Questions?

- Start a Discussion: https://github.com/POWDER-RANGER/raingod-studio-v4/discussions
- Open an Issue: https://github.com/POWDER-RANGER/raingod-studio-v4/issues

---

**Thank you for contributing! 🙏**
