import os
import pytest
import customtkinter as ctk

from gui_plotting import PlottingPanel
from gui_components import ParameterPanel


def test_gui_components():
    if os.environ.get("DISPLAY", "") == "":
        pytest.skip("No display available for Tkinter")

    root = ctk.CTk()
    plot = PlottingPanel(root)
    param = ParameterPanel(root, callback=None)

    param.update_circle_entries(1.0, 2.0, 3.0)
    assert abs(param.centro_x_var.get() - 1.0) < 1e-6
    assert abs(param.centro_y_var.get() - 2.0) < 1e-6
    assert abs(param.radio_var.get() - 3.0) < 1e-6

    root.destroy()
