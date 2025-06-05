import os
import pytest
import customtkinter as ctk

from gui_app import SlopeStabilityApp
from gui_components import ToolsPanel


def test_tools_panel_no_export_button():
    if os.environ.get("DISPLAY", "") == "":
        pytest.skip("No display available for Tkinter")
    root = ctk.CTk()
    panel = ToolsPanel(root, app_instance=None)
    assert not hasattr(panel, "export_btn")
    root.destroy()


def test_clear_results_resets_state():
    if os.environ.get("DISPLAY", "") == "":
        pytest.skip("No display available for Tkinter")
    app = SlopeStabilityApp()
    app.current_bishop_result = object()
    app.current_fellenius_result = object()
    app.clear_results()
    assert app.current_bishop_result is None
    assert app.current_fellenius_result is None
    app.root.destroy()
