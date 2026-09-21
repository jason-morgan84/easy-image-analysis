import re
import pytest
import core

def test_version_attribute_exists():
    """Ensure backend.__version__ is declared and is a non-empty string."""
    assert hasattr(core, "__version__"), "backend module missing __version__ attribute"
    assert isinstance(core.__version__, str), "__version__ must be a string"
    assert len(core.__version__) > 0, "__version__ cannot be empty"

def test_version_follows_semver():
    """Validate __version__ against SemVer format (e.g. '0.1.0', '0.2.0-dev', '1.0.0-rc1')."""
    # Standard SemVer 2.0 regex matching MAJOR.MINOR.PATCH with optional -prerelease / +build info
    semver_pattern = r"^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$"
    
    current_version = core.__version__
    assert re.match(semver_pattern, current_version), (
        f"Version '{current_version}' does not comply with Semantic Versioning "
        f"(expected format like '0.1.0' or '0.2.0-dev')."
    )