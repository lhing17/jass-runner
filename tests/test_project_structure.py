"""Test project structure and basic imports."""

def test_package_can_be_imported():
    """Test that the jass_runner package can be imported."""
    import jass_runner
    assert jass_runner.__version__ == "0.1.0"