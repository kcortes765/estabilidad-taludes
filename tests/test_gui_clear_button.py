import os
import pytest
import customtkinter as ctk

from gui_app import SlopeStabilityApp


def test_clear_button_resets_state():
    if os.environ.get("DISPLAY", "") == "":
        pytest.skip("No display available for Tkinter")

    app = SlopeStabilityApp()

    # Cambiar algunos valores para simular uso
    app.parameter_panel.altura_var.set(15.0)
    app.results_panel.fs_bishop_label.configure(text="1.23")
    app.plotting_panel.current_perfil = [(0, 0), (1, 1)]

    # Ejecutar limpieza
    app.clear_results()

    # Verificaciones
    assert app.parameter_panel.altura_var.get() == 8.0
    assert app.results_panel.fs_bishop_label.cget("text") == "---"
    assert app.plotting_panel.current_perfil is None

    app.root.destroy()
