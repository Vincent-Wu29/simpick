from pathlib import Path
from typing import Any, Iterable
from xml.etree.ElementInclude import include
from typeguard import value
import yaml
import copy

class ConfigError(ValueError):
    """Raised when a configuration file or override is invalid."""

def _read_yaml(path: Path) -> dict[str, Any]:
    if not Path.exists(path):
        raise ConfigError(f"Configuration file do not exist: {path}")
    with path.open('r', encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ConfigError(f"Top-level YAML value must be a mapping: {path}")
    return data

def _deep_merge(base: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in update.items():
        if isinstance(value, dict) and isinstance(merged[key], dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged

def _set_dotted(config: dict[str, Any], dotted_key: str, value: Any) -> None:
    keys = dotted_key.split('.')
    if any(not key for key in keys):
        raise ConfigError(f"Invalid override key: {dotted_key!r}")
    cursor = config
    for key in keys[:-1]:
        current = cursor.get(key)
        if current is None:
            current = {}
            cursor[key] = current
        if not isinstance(current, dict):
            raise ConfigError(f"Cannot descend through non-mapping key: {key}")
        cursor = current
    cursor[keys[-1]] = value

def parse_overrides(items: Iterable[str] | None) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for item in items or []:
        if '=' not in item:
            raise ConfigError(f"overrides must use key=value syntax: {item!r}")
        key, raw_value = item.split('=', 1)
        _set_dotted(result, key.strip(), yaml.safe_load(raw_value))
    return result



def load_config(
    path: str | Path | None = None,
    overrides: Iterable[str] | None = None
) -> dict[str, Any]:
    root = Path(__file__).resolve().parents[2]
    default_path = root / "configs" / "default.yaml"
    config = _read_yaml(default_path)

    if path is not None:
        selected = Path(path).expanduser().resolve()
        if selected != default_path.resolve():
            config = _deep_merge(config, _read_yaml(selected))

    return _deep_merge(config, parse_overrides(overrides))