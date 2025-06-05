import os
import pytest
import customtkinter as ctk

from gui_app import SlopeStabilityApp


def has_display():
    return os.environ.get("DISPLAY", "") != ""


@pytest.mark.skipif(not has_display(), reason="No display available for Tkinter")
def test_app_initialization_and_closure():
    app = SlopeStabilityApp()
    app.root.update()
    app.root.destroy()


@pytest.mark.skipif(not has_display(), reason="No display available for Tkinter")
def test_app_help_about():
    app = SlopeStabilityApp()
    app.show_help()
    app.show_about()
    app.root.destroy()
