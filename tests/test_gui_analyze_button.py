import os
import threading
import pytest
from unittest.mock import patch

from gui_app import SlopeStabilityApp


class DummyThread:
    def __init__(self, target=None, *args, **kwargs):
        self.target = target
    def start(self):
        if self.target:
            self.target()

def test_analyze_button_triggers_run(monkeypatch):
    if os.environ.get("DISPLAY", "") == "":
        pytest.skip("No display available for Tkinter")

    app = SlopeStabilityApp()
    called = False
    def dummy_run():
        nonlocal called
        called = True

    monkeypatch.setattr(threading, "Thread", lambda *a, **kw: DummyThread(*a, **kw))
    monkeypatch.setattr(app, "_run_analysis_thread", dummy_run)

    app.tools_panel.analyze_btn.invoke()

    assert called
    assert app.status_label.cget("text") == "Ejecutando análisis..."
    assert app.progress_bar.get() >= 0.1

    app.root.destroy()
