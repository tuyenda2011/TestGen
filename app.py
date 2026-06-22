from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"


def _bootstrap_src_path() -> None:
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))


_bootstrap_src_path()

print("APP_BOOTSTRAP importing testgen.streamlit_app", flush=True)

# Streamlit executes this file as the app script. Importing the package module
# renders the real UI while keeping `streamlit run app.py` as the public command.
if "testgen.streamlit_app" in sys.modules:
    del sys.modules["testgen.streamlit_app"]
import testgen.streamlit_app  # noqa: E402,F401

print("APP_BOOTSTRAP imported testgen.streamlit_app", flush=True)
