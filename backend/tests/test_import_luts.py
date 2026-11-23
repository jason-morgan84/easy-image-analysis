from core.frontend_operations import import_luts, project_root_dir
import pytest
import os

def test_import_luts_not_png():
    logger = []
    lut_list = import_luts(logger)
    for item in logger:
        print(f"{item.identifier}: {item.message}")
        if item.identifier == "test_not_png.txt":
            assert "lut file not imported as not .png" in item.message

def test_import_luts_not_valid_png():
    test_lut_path = os.path.join(project_root_dir, "frontend", "luts", "test_luts")
    logger = []
    lut_list = import_luts(logger, test_lut_path)
    assert "test_invalid_png.png" in [item.identifier for item in logger]
    for item in logger:
        print(f"{item.identifier}: {item.message}")
        if item.identifier == "test_invalid_png.png":
            assert "lut file could not be opened" in item.message

def test_import_luts_wrong_mode():
    test_lut_path = os.path.join(project_root_dir, "frontend", "luts", "test_luts")
    logger = []
    lut_list = import_luts(logger, test_lut_path)
    assert "test_wrong_mode.png" in [item.identifier for item in logger]
    for item in logger:
        print(f"{item.identifier}: {item.message}")
        if item.identifier == "test_wrong_mode.png":
            assert "lut file not 8-bit RGB image" in item.message

def test_import_luts_short_lut():
    test_lut_path = os.path.join(project_root_dir, "frontend", "luts", "test_luts")
    logger = []
    lut_list = import_luts(logger, test_lut_path)
    assert "test_short_lut.png" in [item.identifier for item in logger]
    for item in logger:
        print(f"{item.identifier}: {item.message}")
        if item.identifier == "test_short_lut.png":
            assert "discarded as not correct shape" in item.message

def test_import_luts():
    logger = []
    lut_list = import_luts(logger)
    for item in logger:
        print(f"{item.identifier}: {item.message}")
    assert len(lut_list) == 10