from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional

from .errors import InputError


DEFAULT_STATE_PATH = os.path.expanduser("~/.gdk9/state.json")


def _ensure_parent(path: Path) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)


def load_state(path: Optional[str] = None) -> Dict[str, Any]:
  p = Path(path or DEFAULT_STATE_PATH)
  if not p.exists():
    return {"symbols": {}, "rules": {}}
  try:
    return json.loads(p.read_text(encoding="utf-8"))
  except Exception as exc:
    raise InputError(f"Failed to read state from {p}: {exc}")


def save_state(state: Dict[str, Any], path: Optional[str] = None) -> None:
  p = Path(path or DEFAULT_STATE_PATH)
  _ensure_parent(p)
  tmp = p.with_suffix(p.suffix + ".tmp")
  tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
  tmp.replace(p)


def get_symbol(state: Dict[str, Any], name: str) -> Optional[float]:
  return state.get("symbols", {}).get(name)


def set_symbol(state: Dict[str, Any], name: str, energy: float) -> None:
  if not math.isfinite(energy):
    raise InputError("Energy must be a finite float")
  state.setdefault("symbols", {})[name] = float(energy)


def list_symbols(state: Dict[str, Any]) -> Dict[str, float]:
  return dict(sorted(state.get("symbols", {}).items()))

