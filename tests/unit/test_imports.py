"""Package import smoke tests."""


def test_package_imports() -> None:
    import handicraft_export_intelligence

    assert handicraft_export_intelligence.__all__ == ["Settings", "load_settings"]
