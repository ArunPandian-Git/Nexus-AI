from pathlib import Path

Path("/content/backend/core").mkdir(
    parents=True,
    exist_ok=True
)

Path("/content/backend/core/__init__.py").touch()
