import pytest


def pytest_collection_modifyitems(items):
    for item in items:
        if "model" in item.name:
            item.add_marker(pytest.mark.model)
        if "model_structure" in item.name:
            item.add_marker(pytest.mark.model_structure)
