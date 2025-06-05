import os
import pytest
import customtkinter as ctk

from gui_components import ToolsPanel
from gui_dialogs import AppUtils


def test_tools_panel_no_export_button():
    if os.environ.get("DISPLAY", "") == "":
        pytest.skip("No display available for Tkinter")
    root = ctk.CTk()
    panel = ToolsPanel(root, app_instance=None)
    assert not hasattr(panel, "export_btn")
    root.destroy()


def test_clear_results_utilities():
    class DummyApp:
        def __init__(self):
            self.current_bishop_result = 1
            self.current_fellenius_result = 2
            self.updated = False
            self.cleared = False
            class DummyResults:
                def update_results(self_inner, *args, **kwargs):
                    self.updated = True
            class DummyPlot:
                def clear_all_plots(self_inner):
                    self.cleared = True
            self.results_panel = DummyResults()
            self.plotting_panel = DummyPlot()
        def update_status(self, msg):
            self.status = msg
    dummy = DummyApp()
    AppUtils.clear_results(dummy)
    assert dummy.current_bishop_result is None
    assert dummy.current_fellenius_result is None
    assert dummy.updated
    assert dummy.cleared
