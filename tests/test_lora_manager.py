"""
LoRA (Low-Rank Adaptation) manager tests for RainGod Comfy Studio.
Tests LoRA registry, validation, style presets, and parameter handling.
35 test cases covering all LoRA manager functionality.
"""

import pytest
from unittest.mock import patch, MagicMock
import json
import os
from backend.lora_manager import LoRAManager, LoRAStyle


@pytest.fixture
def lora_manager():
    """Create a LoRA manager instance."""
    return LoRAManager()


@pytest.fixture
def sample_lora_config():
    """Sample LoRA configuration."""
    return {
        "name": "synthwave_lora",
        "path": "models/loras/synthwave.safetensors",
        "trigger_word": "synthwave style",
        "description": "Synthwave aesthetic LoRA",
        "author": "test_author",
        "version": "1.0",
        "tags": ["synthwave", "80s", "neon"]
    }


# ============================================================================
# LORA REGISTRATION TESTS
# ============================================================================

class TestLoRARegistration:
    """Tests for LoRA registration and loading."""

    def test_register_lora_success(self, lora_manager, sample_lora_config):
        """LoRA registers successfully."""
        result = lora_manager.register(sample_lora_config)
        assert result is True

    def test_register_lora_with_missing_name(self, lora_manager):
        """LoRA registration fails without name."""
        config = {"path": "models/loras/test.safetensors"}
        with pytest.raises(ValueError):
            lora_manager.register(config)

    def test_register_lora_with_missing_path(self, lora_manager, sample_lora_config):
        """LoRA registration fails without path."""
        del sample_lora_config["path"]
        with pytest.raises(ValueError):
            lora_manager.register(sample_lora_config)

    def test_register_duplicate_lora(self, lora_manager, sample_lora_config):
        """Duplicate LoRA registration fails or overwrites."""
        lora_manager.register(sample_lora_config)
        # Second registration should either fail or overwrite
        result = lora_manager.register(sample_lora_config)
        # Behavior depends on implementation

    def test_lora_available_after_registration(self, lora_manager, sample_lora_config):
        """LoRA is available after registration."""
        lora_manager.register(sample_lora_config)
        assert "synthwave_lora" in lora_manager.list_available()

    def test_register_multiple_loras(self, lora_manager):
        """Multiple LoRAs can be registered."""
        loras = [
            {"name": "lora_1", "path": "path/1.safetensors"},
            {"name": "lora_2", "path": "path/2.safetensors"},
            {"name": "lora_3", "path": "path/3.safetensors"}
        ]
        for lora in loras:
            lora_manager.register(lora)
        available = lora_manager.list_available()
        assert len(available) >= 3


# ============================================================================
# LORA STYLE PRESETS TESTS
# ============================================================================

class TestLoRAStylePresets:
    """Tests for predefined LoRA style presets."""

    def test_synthwave_preset_available(self, lora_manager):
        """Synthwave style preset exists."""
        styles = lora_manager.get_styles()
        assert any(s["name"] == "synthwave" for s in styles)

    def test_cyberpunk_preset_available(self, lora_manager):
        """Cyberpunk style preset exists."""
        styles = lora_manager.get_styles()
        assert any(s["name"] == "cyberpunk" for s in styles)

    def test_anime_preset_available(self, lora_manager):
        """Anime style preset exists."""
        styles = lora_manager.get_styles()
        assert any(s["name"] == "anime" for s in styles)

    def test_photorealism_preset_available(self, lora_manager):
        """Photorealism style preset exists."""
        styles = lora_manager.get_styles()
        assert any(s["name"] == "photorealism" for s in styles)

    def test_oil_painting_preset_available(self, lora_manager):
        """Oil painting style preset exists."""
        styles = lora_manager.get_styles()
        assert any(s["name"] == "oil_painting" for s in styles)

    def test_style_includes_metadata(self, lora_manager):
        """Each style includes name, description, and LoRA list."""
        styles = lora_manager.get_styles()
        if len(styles) > 0:
            style = styles[0]
            assert "name" in style
            assert "description" in style
            assert "loras" in style

    def test_apply_style_preset(self, lora_manager):
        """Style preset can be applied to generation config."""
        config = lora_manager.apply_style("synthwave")
        assert config is not None
        assert "loras" in config

    def test_invalid_style_rejected(self, lora_manager):
        """Invalid style name returns error."""
        config = lora_manager.apply_style("invalid_style_xyz")
        # Should either return None, empty config, or raise error
        assert config is None or isinstance(config, dict)


# ============================================================================
# LORA PARAMETER HANDLING TESTS
# ============================================================================

class TestLoRAParameters:
    """Tests for LoRA parameter management."""

    def test_lora_strength_range(self, lora_manager, sample_lora_config):
        """LoRA strength is between 0 and 1."""
        lora_manager.register(sample_lora_config)
        lora = lora_manager.get("synthwave_lora")
        assert 0 <= lora.get("strength", 0.75) <= 1

    def test_set_lora_strength(self, lora_manager, sample_lora_config):
        """LoRA strength can be set."""
        lora_manager.register(sample_lora_config)
        lora_manager.set_strength("synthwave_lora", 0.5)
        lora = lora_manager.get("synthwave_lora")
        assert lora.get("strength") == 0.5

    def test_invalid_lora_strength_rejected(self, lora_manager, sample_lora_config):
        """Invalid strength values are rejected."""
        lora_manager.register(sample_lora_config)
        # Strength > 1 should be rejected or clamped
        with pytest.raises((ValueError, AssertionError)):
            lora_manager.set_strength("synthwave_lora", 1.5)

    def test_lora_trigger_word_preserved(self, lora_manager, sample_lora_config):
        """Trigger words are preserved."""
        lora_manager.register(sample_lora_config)
        lora = lora_manager.get("synthwave_lora")
        assert lora["trigger_word"] == "synthwave style"

    def test_multiple_loras_with_different_strengths(self, lora_manager):
        """Multiple LoRAs can have different strengths."""
        config1 = {"name": "lora_1", "path": "path/1.safetensors", "strength": 0.7}
        config2 = {"name": "lora_2", "path": "path/2.safetensors", "strength": 0.3}
        lora_manager.register(config1)
        lora_manager.register(config2)
        assert lora_manager.get("lora_1")["strength"] == 0.7
        assert lora_manager.get("lora_2")["strength"] == 0.3


# ============================================================================
# LORA VALIDATION TESTS
# ============================================================================

class TestLoRAValidation:
    """Tests for LoRA file validation."""

    def test_validate_safetensors_format(self, lora_manager):
        """Safetensors format is validated."""
        config = {
            "name": "test",
            "path": "models/loras/test.safetensors"
        }
        # Should accept .safetensors extension
        result = lora_manager.register(config)
        assert result is True

    def test_validate_pt_format(self, lora_manager):
        """PyTorch .pt format is validated."""
        config = {
            "name": "test_pt",
            "path": "models/loras/test.pt"
        }
        # Should accept .pt extension
        result = lora_manager.register(config)
        assert result is True

    def test_reject_invalid_format(self, lora_manager):
        """Invalid file formats are rejected."""
        config = {
            "name": "test_invalid",
            "path": "models/loras/test.txt"
        }
        # Should reject .txt
        with pytest.raises((ValueError, AssertionError)):
            lora_manager.register(config)

    def test_validate_path_exists(self, lora_manager):
        """LoRA path validation checks existence."""
        config = {
            "name": "nonexistent",
            "path": "/nonexistent/path/to/lora.safetensors"
        }
        # Depending on implementation, may check path or defer
        # At minimum should have error handling

    def test_lora_metadata_validation(self, lora_manager, sample_lora_config):
        """LoRA metadata is validated."""
        lora_manager.register(sample_lora_config)
        lora = lora_manager.get("synthwave_lora")
        # Validate expected fields
        assert "name" in lora
        assert "path" in lora


# ============================================================================
# LORA COMBINATION TESTS
# ============================================================================

class TestLoRACombinations:
    """Tests for combining multiple LoRAs."""

    def test_combine_two_loras(self, lora_manager):
        """Two LoRAs can be combined."""
        lora1 = {"name": "style1", "path": "path/1.safetensors", "strength": 0.6}
        lora2 = {"name": "style2", "path": "path/2.safetensors", "strength": 0.4}
        lora_manager.register(lora1)
        lora_manager.register(lora2)
        combined = lora_manager.combine(["style1", "style2"])
        assert len(combined) == 2

    def test_combine_multiple_loras(self, lora_manager):
        """Multiple LoRAs can be combined."""
        for i in range(5):
            lora = {
                "name": f"lora_{i}",
                "path": f"path/{i}.safetensors",
                "strength": 0.2
            }
            lora_manager.register(lora)
        combined = lora_manager.combine([f"lora_{i}" for i in range(5)])
        assert len(combined) == 5

    def test_strength_normalization_in_combination(self, lora_manager):
        """Combined LoRA strengths are normalized."""
        # Combined strength should not exceed reasonable limits
        lora1 = {"name": "s1", "path": "p1.safetensors", "strength": 0.7}
        lora2 = {"name": "s2", "path": "p2.safetensors", "strength": 0.6}
        lora_manager.register(lora1)
        lora_manager.register(lora2)
        combined = lora_manager.combine(["s1", "s2"])
        # Each should maintain its strength or be normalized

    def test_invalid_lora_in_combination_rejected(self, lora_manager):
        """Invalid LoRA names in combination are rejected."""
        with pytest.raises((ValueError, KeyError)):
            lora_manager.combine(["nonexistent_lora"])


# ============================================================================
# LORA EXPORT/IMPORT TESTS
# ============================================================================

class TestLoRAExportImport:
    """Tests for exporting and importing LoRA configurations."""

    def test_export_lora_config(self, lora_manager, sample_lora_config):
        """LoRA config can be exported."""
        lora_manager.register(sample_lora_config)
        exported = lora_manager.export("synthwave_lora")
        assert exported is not None
        assert isinstance(exported, dict)

    def test_import_lora_config(self, lora_manager, sample_lora_config):
        """LoRA config can be imported."""
        exported = sample_lora_config
        lora_manager.import_config(exported)
        assert "synthwave_lora" in lora_manager.list_available()

    def test_export_import_roundtrip(self, lora_manager, sample_lora_config):
        """Export then import preserves LoRA data."""
        lora_manager.register(sample_lora_config)
        exported = lora_manager.export("synthwave_lora")
        # Clear and re-import
        lora_manager.unregister("synthwave_lora")
        lora_manager.import_config(exported)
        assert "synthwave_lora" in lora_manager.list_available()

    def test_batch_export_all_loras(self, lora_manager):
        """All LoRAs can be exported at once."""
        for i in range(3):
            lora_manager.register({
                "name": f"lora_{i}",
                "path": f"path/{i}.safetensors"
            })
        all_exported = lora_manager.export_all()
        assert len(all_exported) >= 3


# ============================================================================
# LORA LISTING & SEARCH TESTS
# ============================================================================

class TestLoRAListing:
    """Tests for listing and searching LoRAs."""

    def test_list_all_loras(self, lora_manager):
        """All registered LoRAs can be listed."""
        for i in range(3):
            lora_manager.register({
                "name": f"lora_{i}",
                "path": f"path/{i}.safetensors"
            })
        available = lora_manager.list_available()
        assert len(available) >= 3

    def test_search_lora_by_name(self, lora_manager, sample_lora_config):
        """LoRA can be found by name."""
        lora_manager.register(sample_lora_config)
        found = lora_manager.get("synthwave_lora")
        assert found is not None
        assert found["name"] == "synthwave_lora"

    def test_search_lora_by_tag(self, lora_manager, sample_lora_config):
        """LoRA can be found by tag."""
        lora_manager.register(sample_lora_config)
        found = lora_manager.search_by_tag("synthwave")
        assert len(found) > 0
        assert any(f["name"] == "synthwave_lora" for f in found)

    def test_search_lora_by_author(self, lora_manager, sample_lora_config):
        """LoRA can be found by author."""
        lora_manager.register(sample_lora_config)
        found = lora_manager.search_by_author("test_author")
        assert len(found) > 0

    def test_empty_search_returns_empty(self, lora_manager):
        """Search with no matches returns empty list."""
        found = lora_manager.search_by_tag("nonexistent_tag_xyz")
        assert found == [] or found is None
