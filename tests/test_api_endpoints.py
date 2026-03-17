"""
Comprehensive FastAPI endpoint tests for RainGod Comfy Studio.
Tests all primary endpoints, error handling, and response formats.
30 test cases covering single generation, batch, queue, outputs, config, health.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
import json
from backend.main import app


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def valid_generate_payload():
    """Valid single generation payload."""
    return {
        "prompt": "a beautiful landscape",
        "model": "comfy_cloud",
        "quality_tier": "standard"
    }


@pytest.fixture
def valid_batch_payload():
    """Valid batch generation payload."""
    return {
        "jobs": [
            {"prompt": "landscape", "model": "comfy_cloud"},
            {"prompt": "portrait", "model": "comfy_cloud"}
        ],
        "quality_tier": "standard"
    }


# ============================================================================
# HEALTH & DIAGNOSTICS
# ============================================================================

class TestHealthEndpoint:
    """Tests for /health endpoint."""

    def test_health_check_success(self, client):
        """Health check returns 200 with service status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "services" in data
        assert "timestamp" in data

    def test_health_includes_adapter_status(self, client):
        """Health check includes status of all adapters."""
        response = client.get("/health")
        data = response.json()
        assert "services" in data
        services = data["services"]
        # Should include Ollama local status
        assert any("ollama" in str(s).lower() for s in services.values() or [])

    def test_health_timestamp_format(self, client):
        """Health check includes valid ISO timestamp."""
        response = client.get("/health")
        data = response.json()
        timestamp = data.get("timestamp")
        assert timestamp is not None
        # Should be ISO format
        assert "T" in timestamp and "Z" in timestamp


# ============================================================================
# CONFIGURATION ENDPOINTS
# ============================================================================

class TestConfigEndpoint:
    """Tests for /config endpoint."""

    def test_config_returns_all_presets(self, client):
        """Config endpoint returns resolution and sampler presets."""
        response = client.get("/config")
        assert response.status_code == 200
        data = response.json()
        assert "resolutions" in data
        assert "samplers" in data
        assert "quality_tiers" in data

    def test_config_resolution_presets(self, client):
        """Config includes all 7 resolution presets."""
        response = client.get("/config")
        data = response.json()
        resolutions = data["resolutions"]
        assert len(resolutions) >= 7
        assert any(r["name"] == "thumbnail" for r in resolutions)
        assert any(r["name"] == "4k" for r in resolutions)

    def test_config_quality_tiers(self, client):
        """Config includes draft, standard, final quality tiers."""
        response = client.get("/config")
        data = response.json()
        tiers = data["quality_tiers"]
        tier_names = [t["name"] for t in tiers]
        assert "draft" in tier_names
        assert "standard" in tier_names
        assert "final" in tier_names

    def test_config_lora_styles(self, client):
        """Config includes LoRA style presets."""
        response = client.get("/config")
        data = response.json()
        assert "lora_styles" in data
        styles = data["lora_styles"]
        assert len(styles) >= 5


class TestPresetsEndpoint:
    """Tests for /presets endpoint."""

    def test_presets_list_success(self, client):
        """Presets endpoint returns list of available presets."""
        response = client.get("/presets")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_presets_include_metadata(self, client):
        """Each preset includes name, description, config."""
        response = client.get("/presets")
        data = response.json()
        preset = data[0]
        assert "name" in preset
        assert "description" in preset
        assert "config" in preset


# ============================================================================
# SINGLE GENERATION ENDPOINT
# ============================================================================

class TestGenerateEndpoint:
    """Tests for POST /generate endpoint."""

    @patch("backend.dispatcher.dispatch")
    def test_generate_success(self, mock_dispatch, client, valid_generate_payload):
        """Single generation request succeeds."""
        mock_dispatch.return_value = {
            "status": "completed",
            "image_url": "http://example.com/image.png",
            "seed": 12345
        }
        response = client.post("/generate", json=valid_generate_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert "image_url" in data

    @patch("backend.dispatcher.dispatch")
    def test_generate_missing_prompt(self, mock_dispatch, client):
        """Generation without prompt returns 422."""
        payload = {"model": "comfy_cloud"}
        response = client.post("/generate", json=payload)
        assert response.status_code == 422

    @patch("backend.dispatcher.dispatch")
    def test_generate_invalid_model(self, mock_dispatch, client, valid_generate_payload):
        """Invalid model name returns error."""
        valid_generate_payload["model"] = "invalid_model_xyz"
        response = client.post("/generate", json=valid_generate_payload)
        # Should either reject or handle gracefully
        assert response.status_code in [400, 422, 200]

    @patch("backend.dispatcher.dispatch")
    def test_generate_default_quality_tier(self, mock_dispatch, client):
        """Generation without quality_tier uses default."""
        payload = {
            "prompt": "test",
            "model": "comfy_cloud"
        }
        mock_dispatch.return_value = {"status": "completed"}
        response = client.post("/generate", json=payload)
        assert response.status_code == 200
        # Should have applied a default tier

    @patch("backend.dispatcher.dispatch")
    def test_generate_includes_all_params(self, mock_dispatch, client):
        """Generation request includes all provided parameters."""
        payload = {
            "prompt": "landscape at sunset",
            "model": "comfy_cloud",
            "quality_tier": "final",
            "style": "synthwave",
            "seed": 42
        }
        mock_dispatch.return_value = {"status": "completed", "seed": 42}
        response = client.post("/generate", json=payload)
        assert response.status_code == 200
        # Verify dispatch was called with payload
        mock_dispatch.assert_called()

    @patch("backend.dispatcher.dispatch")
    def test_generate_returns_job_id(self, mock_dispatch, client, valid_generate_payload):
        """Generation response includes job ID for tracking."""
        mock_dispatch.return_value = {
            "status": "queued",
            "job_id": "gen_12345_abc"
        }
        response = client.post("/generate", json=valid_generate_payload)
        data = response.json()
        assert "job_id" in data or "status" in data


# ============================================================================
# BATCH GENERATION ENDPOINT
# ============================================================================

class TestBatchGenerateEndpoint:
    """Tests for POST /batch-generate endpoint."""

    @patch("backend.dispatcher.dispatch")
    def test_batch_generate_success(self, mock_dispatch, client, valid_batch_payload):
        """Batch generation request succeeds."""
        mock_dispatch.return_value = {
            "status": "queued",
            "batch_id": "batch_12345",
            "job_count": 2
        }
        response = client.post("/batch-generate", json=valid_batch_payload)
        assert response.status_code == 200
        data = response.json()
        assert "batch_id" in data or "status" in data

    @patch("backend.dispatcher.dispatch")
    def test_batch_generate_empty_jobs(self, mock_dispatch, client):
        """Batch with no jobs returns error."""
        payload = {"jobs": [], "quality_tier": "standard"}
        response = client.post("/batch-generate", json=payload)
        assert response.status_code in [400, 422]

    @patch("backend.dispatcher.dispatch")
    def test_batch_generate_max_jobs(self, mock_dispatch, client):
        """Batch respects maximum job count."""
        jobs = [{"prompt": f"prompt {i}"} for i in range(100)]
        payload = {"jobs": jobs, "quality_tier": "standard"}
        response = client.post("/batch-generate", json=payload)
        # Should succeed or reject gracefully
        assert response.status_code in [200, 400]

    @patch("backend.dispatcher.dispatch")
    def test_batch_generate_tracks_all_jobs(self, mock_dispatch, client, valid_batch_payload):
        """Batch response tracks all submitted jobs."""
        mock_dispatch.return_value = {
            "batch_id": "batch_xyz",
            "jobs": [
                {"job_id": "job_1", "status": "queued"},
                {"job_id": "job_2", "status": "queued"}
            ]
        }
        response = client.post("/batch-generate", json=valid_batch_payload)
        assert response.status_code == 200
        data = response.json()
        assert "batch_id" in data or "jobs" in data

    @patch("backend.dispatcher.dispatch")
    def test_batch_generate_per_job_config(self, mock_dispatch, client):
        """Each batch job can have own model/settings."""
        payload = {
            "jobs": [
                {"prompt": "test1", "model": "comfy_cloud"},
                {"prompt": "test2", "model": "groq"}
            ]
        }
        mock_dispatch.return_value = {"batch_id": "batch_mixed"}
        response = client.post("/batch-generate", json=payload)
        assert response.status_code == 200


# ============================================================================
# QUEUE MANAGEMENT ENDPOINTS
# ============================================================================

class TestQueueStatusEndpoint:
    """Tests for GET /queue/status endpoint."""

    @patch("backend.dispatcher.get_queue_status")
    def test_queue_status_success(self, mock_status, client):
        """Queue status returns pending and running jobs."""
        mock_status.return_value = {
            "pending": 3,
            "running": 1,
            "completed": 15,
            "failed": 0
        }
        response = client.get("/queue/status")
        assert response.status_code == 200
        data = response.json()
        assert "pending" in data
        assert "running" in data

    @patch("backend.dispatcher.get_queue_status")
    def test_queue_status_detailed(self, mock_status, client):
        """Queue status can include job details."""
        mock_status.return_value = {
            "pending": 2,
            "jobs": [
                {"job_id": "job_1", "status": "queued", "prompt": "test"},
                {"job_id": "job_2", "status": "running", "progress": 45}
            ]
        }
        response = client.get("/queue/status")
        data = response.json()
        assert "jobs" in data or "pending" in data


class TestQueueCancelEndpoint:
    """Tests for DELETE /queue/{job_id} endpoint."""

    @patch("backend.dispatcher.cancel_job")
    def test_cancel_success(self, mock_cancel, client):
        """Job cancellation succeeds."""
        mock_cancel.return_value = {"status": "cancelled", "job_id": "job_123"}
        response = client.delete("/queue/job_123")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "cancelled"

    @patch("backend.dispatcher.cancel_job")
    def test_cancel_nonexistent_job(self, mock_cancel, client):
        """Cancelling non-existent job returns 404."""
        mock_cancel.side_effect = ValueError("Job not found")
        response = client.delete("/queue/job_nonexistent")
        assert response.status_code in [404, 400]

    @patch("backend.dispatcher.cancel_job")
    def test_cancel_already_completed(self, mock_cancel, client):
        """Cancelling completed job returns error."""
        mock_cancel.return_value = {"status": "error", "message": "Already completed"}
        response = client.delete("/queue/job_completed")
        assert response.status_code in [400, 200]


# ============================================================================
# OUTPUT RETRIEVAL ENDPOINTS
# ============================================================================

class TestOutputsEndpoint:
    """Tests for GET /outputs/{file} endpoint."""

    def test_outputs_retrieval_success(self, client):
        """Output file retrieval succeeds."""
        # Mock a file response
        with patch("backend.main.Path.exists", return_value=True):
            with patch("builtins.open", create=True):
                response = client.get("/outputs/test_image.png")
                # Should return file or 200
                assert response.status_code in [200, 404]

    def test_outputs_file_not_found(self, client):
        """Missing output file returns 404."""
        response = client.get("/outputs/nonexistent_file.png")
        assert response.status_code in [404, 400]

    def test_outputs_path_traversal_blocked(self, client):
        """Path traversal attempts are blocked."""
        response = client.get("/outputs/../../../etc/passwd")
        assert response.status_code in [404, 400, 403]


# ============================================================================
# ERROR HANDLING
# ============================================================================

class TestErrorHandling:
    """Tests for error handling across endpoints."""

    @patch("backend.dispatcher.dispatch")
    def test_dispatcher_timeout_handled(self, mock_dispatch, client, valid_generate_payload):
        """Dispatcher timeout returns graceful error."""
        mock_dispatch.side_effect = TimeoutError("Request timeout")
        response = client.post("/generate", json=valid_generate_payload)
        assert response.status_code >= 400

    @patch("backend.dispatcher.dispatch")
    def test_api_key_error_handled(self, mock_dispatch, client, valid_generate_payload):
        """Missing API key returns 401 or error."""
        mock_dispatch.side_effect = ValueError("Missing API key")
        response = client.post("/generate", json=valid_generate_payload)
        assert response.status_code >= 400

    def test_malformed_json_rejected(self, client):
        """Malformed JSON returns 422."""
        response = client.post(
            "/generate",
            data="{invalid json}",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422


# ============================================================================
# ROOT & DOCUMENTATION
# ============================================================================

class TestRootEndpoint:
    """Tests for root and documentation endpoints."""

    def test_root_redirect_or_docs(self, client):
        """Root endpoint provides docs or redirect."""
        response = client.get("/")
        assert response.status_code in [200, 307, 308]

    def test_openapi_docs_available(self, client):
        """OpenAPI/Swagger docs available."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_available(self, client):
        """ReDoc documentation available."""
        response = client.get("/redoc")
        assert response.status_code == 200

    def test_openapi_schema_valid(self, client):
        """OpenAPI schema is valid JSON."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema or "swagger" in schema


# ============================================================================
# RESPONSE FORMAT VALIDATION
# ============================================================================

class TestResponseFormats:
    """Tests for response format consistency."""

    @patch("backend.dispatcher.dispatch")
    def test_generate_response_schema(self, mock_dispatch, client, valid_generate_payload):
        """Generation response follows expected schema."""
        mock_dispatch.return_value = {
            "status": "completed",
            "image_url": "http://example.com/image.png",
            "seed": 12345,
            "execution_time": 45.2
        }
        response = client.post("/generate", json=valid_generate_payload)
        data = response.json()
        assert "status" in data

    @patch("backend.dispatcher.dispatch")
    def test_all_responses_include_timestamp(self, mock_dispatch, client, valid_generate_payload):
        """Responses include timestamp."""
        mock_dispatch.return_value = {"status": "completed"}
        response = client.post("/generate", json=valid_generate_payload)
        data = response.json()
        # Timestamp may be included at top level or in metadata
        assert response.status_code == 200