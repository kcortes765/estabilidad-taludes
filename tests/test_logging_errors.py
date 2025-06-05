import os
import pytest
from logging_utils import setup_logging
from utils.file_utils import load_text_file
from core.bishop import calcular_m_alpha
from data.models import Dovela


@pytest.fixture(autouse=True)
def _setup_logging(tmp_path):
    log_file = tmp_path / "test.log"
    setup_logging(str(log_file))
    yield


def test_load_text_file_logs_error(caplog):
    with pytest.raises(FileNotFoundError):
        load_text_file("non_existent.txt")
    assert any("Archivo no encontrado" in r.message for r in caplog.records)


def test_calcular_m_alpha_invalid_fs_logs(caplog):
    dovela = Dovela(
        x_centro=0.0,
        ancho=1.0,
        altura=1.0,
        angulo_alpha=0.0,
        cohesion=10.0,
        phi_grados=20.0,
        gamma=18.0,
        peso=1.0,
        presion_poros=0.0,
        longitud_arco=1.0,
        fuerza_normal_efectiva=1.0,
        tiene_traccion=False,
        y_base=0.0,
        y_superficie=1.0,
    )
    with pytest.raises(Exception):
        calcular_m_alpha(dovela, 0.0)
    assert any("Factor de seguridad" in r.message for r in caplog.records)


def test_gui_show_error_logs(caplog, monkeypatch):
    if os.environ.get("DISPLAY", "") == "":
        pytest.skip("No display available for Tkinter")

    from gui_app import SlopeStabilityApp

    messages = []
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: messages.append(a))

    app = SlopeStabilityApp()
    app._show_analysis_error("prueba")

    assert messages
    assert any("prueba" in m[1] for m in messages)
    assert any("prueba" in r.message for r in caplog.records)
    app.root.destroy()

