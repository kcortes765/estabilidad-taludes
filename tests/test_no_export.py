import os
import pytest
import customtkinter as ctk

from gui_components import ToolsPanel
from gui_dialogs import AppUtils


def test_export_button_removed():
    if os.environ.get("DISPLAY", "") == "":
        pytest.skip("No display available for Tkinter")
    root = ctk.CTk()
    panel = ToolsPanel(root, app_instance=None)
    assert not hasattr(panel, "export_btn")
    assert not hasattr(panel, "export_results")
    root.destroy()


def test_export_function_removed():
    assert not hasattr(AppUtils, "export_results")
