"""
MintYourAgent Unit Tests

Run with: pytest tests/ -v
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add parent to path for import
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestConstants:
    """Test constants and configuration."""
    
    def test_version_format(self):
        """Version should be semver format."""
        from mya import Constants
        parts = Constants.VERSION.split('.')
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)
    
    def test_rpc_endpoints_defined(self):
        """All networks should have RPC endpoints."""
        from mya import Constants, Network
        for network in Network:
            assert network in Constants.RPC_ENDPOINTS
    
    def test_command_aliases_valid(self):
        """Command aliases should be strings."""
        from mya import Constants
        for alias, cmd in Constants.COMMAND_ALIASES.items():
            assert isinstance(alias, str)
            assert isinstance(cmd, str)


class TestBase58:
    """Test base58 encoding/decoding."""
    
    def test_encode_decode_roundtrip(self):
        """Encoding then decoding should return original."""
        from mya import b58_encode, b58_decode
        
        test_data = b'\x00\x01\x02\x03\x04'
        encoded = b58_encode(test_data)
        decoded = b58_decode(encoded)
        assert decoded == test_data
    
    def test_encode_empty(self):
        """Empty bytes should encode to '1'."""
        from mya import b58_encode
        assert b58_encode(b'') == '1'
    
    def test_decode_invalid_char(self):
        """Invalid characters should raise ValueError."""
        from mya import b58_decode
        with pytest.raises(ValueError):
            b58_decode('0OIl')  # 0, O, I, l are not in base58
    
    def test_decode_leading_ones(self):
        """Leading 1s should decode to leading zeros."""
        from mya import b58_decode
        result = b58_decode('111')
        assert result.startswith(b'\x00\x00\x00')


class TestSanitization:
    """Test input sanitization."""
    
    def test_sanitize_removes_control_chars(self):
        """Control characters should be removed."""
        from mya import sanitize_input
        result = sanitize_input("hello\x00world\x1f")
        assert '\x00' not in result
        assert '\x1f' not in result
        assert 'helloworld' == result
    
    def test_sanitize_preserves_normal_text(self):
        """Normal text should be preserved."""
        from mya import sanitize_input
        text = "Hello, World! 123"
        assert sanitize_input(text) == text
    
    def test_sanitize_truncates_long_input(self):
        """Very long input should be truncated."""
        from mya import sanitize_input
        long_text = "x" * 20000
        result = sanitize_input(long_text)
        assert len(result) == 10000


class TestPathSafety:
    """Test path validation."""
    
    def test_rejects_path_traversal(self):
        """Path traversal should be rejected."""
        from mya import validate_path_safety
        with pytest.raises(ValueError, match="traversal"):
            validate_path_safety("../../../etc/passwd")
    
    def test_accepts_normal_path(self):
        """Normal paths should be accepted."""
        from mya import validate_path_safety
        with tempfile.NamedTemporaryFile() as f:
            result = validate_path_safety(f.name)
            assert result.exists()


class TestWalletChecksum:
    """Test wallet integrity."""
    
    def test_checksum_consistent(self):
        """Same data should produce same checksum."""
        from mya import compute_wallet_checksum
        data = b'\x01\x02\x03\x04'
        c1 = compute_wallet_checksum(data)
        c2 = compute_wallet_checksum(data)
        assert c1 == c2
    
    def test_checksum_changes_with_data(self):
        """Different data should produce different checksums."""
        from mya import compute_wallet_checksum
        c1 = compute_wallet_checksum(b'\x01\x02\x03\x04')
        c2 = compute_wallet_checksum(b'\x01\x02\x03\x05')
        assert c1 != c2


class TestOutput:
    """Test output formatting."""
    
    def test_color_disabled_when_no_color(self):
        """Colors should be disabled with --no-color."""
        from mya import Output, RuntimeConfig, set_runtime
        
        rt = RuntimeConfig(no_color=True)
        set_runtime(rt)
        
        result = Output.color("test", "red")
        assert '\033[' not in result
    
    def test_emoji_disabled_when_no_emoji(self):
        """Emoji should be disabled with --no-emoji."""
        from mya import Output, RuntimeConfig, set_runtime, OutputFormat
        
        rt = RuntimeConfig(no_emoji=True, format=OutputFormat.TEXT)
        set_runtime(rt)
        
        result = Output._emoji('success')
        assert result == ''


class TestSuggestCommand:
    """Test command suggestions."""
    
    def test_suggests_similar_command(self):
        """Should suggest similar commands for typos."""
        from mya import suggest_command
        
        commands = ['launch', 'wallet', 'setup', 'config']
        
        assert suggest_command('launh', commands) == 'launch'
        assert suggest_command('walet', commands) == 'wallet'
        assert suggest_command('confg', commands) == 'config'
    
    def test_no_suggestion_for_unrelated(self):
        """Should return None for unrelated input."""
        from mya import suggest_command
        
        commands = ['launch', 'wallet']
        assert suggest_command('xyz123', commands) is None


class TestHistory:
    """Test history functionality."""
    
    def test_add_and_get_history(self):
        """Should be able to add and retrieve history."""
        from mya import add_to_history, get_history, get_data_dir
        
        # Use temp directory
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('mya.get_data_dir', return_value=Path(tmpdir)):
                with patch('mya.get_history_file', return_value=Path(tmpdir) / 'history.json'):
                    with patch('mya.ensure_data_dir'):
                        add_to_history("test", {"key": "value"})
                        # Note: In real test, would need to mock file operations


class TestExitCodes:
    """Test exit codes."""
    
    def test_exit_codes_are_integers(self):
        """All exit codes should be integers."""
        from mya import ExitCode
        for code in ExitCode:
            assert isinstance(code.value, int)
    
    def test_success_is_zero(self):
        """SUCCESS should be 0."""
        from mya import ExitCode
        assert ExitCode.SUCCESS == 0


class TestDotEnv:
    """Test .env file loading."""
    
    def test_loads_env_file(self):
        """Should load .env file."""
        from mya import load_dotenv
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("TEST_VAR=test_value\n")
            f.write("# Comment\n")
            f.write('QUOTED="with quotes"\n')
            f.flush()
            
            try:
                result = load_dotenv(Path(f.name))
                assert "TEST_VAR" in result
                assert result["TEST_VAR"] == "test_value"
                assert result.get("QUOTED") == "with quotes"
            finally:
                os.unlink(f.name)


# Integration tests would go here with mocked API calls

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
