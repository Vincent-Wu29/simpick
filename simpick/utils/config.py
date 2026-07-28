from pathlib import Path
from typing import Any, Iterable
import yaml

class ConfigError(ValueError):
    """Raised when a configuration file or override is invalid."""

def _read_yaml(path: Path) -> dict[str, Any]:
    if not Path.exists(path):
        raise ConfigError(f"Configuration file do not exist: {path}")
    with path.open('r', encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not is

def load_config(
    path: str | Path | None = None,
    overrides: Iterable[str] | None = None
) -> dict[str, Any]:
    root = Path(__file__).resolve().parents[2]
    default_path = root / "configs" / "default.yaml"
    config = _read_yaml(default_path)