from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .catalog import CONNECTORS, for_target

DOMAIN = re.compile(r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[A-Za-z]{2,63}$")
USERNAME = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")


def home() -> Path:
    return Path(os.environ.get("FLIPX2_HOME", Path.home() / ".local/share/flipx2"))


def clean_case(value: str) -> str:
    result = re.sub(r"[^A-Za-z0-9_-]", "-", value).strip("-_")
    if not result:
        raise ValueError("El nombre del caso debe contener letras o números.")
    return result[:80]


def validate(kind: str, value: str) -> None:
    pattern = DOMAIN if kind == "domain" else USERNAME
    if not pattern.fullmatch(value):
        raise ValueError(f"{kind} inválido: {value!r}")


def tool_status() -> list[dict]:
    return [{**asdict(c), "available": bool(shutil.which(c.binary))} for c in CONNECTORS]


def run(case: str, kind: str, target: str) -> dict:
    validate(kind, target)
    case_dir = home() / "cases" / clean_case(case)
    raw_dir = case_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    records = []
    for connector in for_target(kind):
        command = [connector.binary, *[part.format(**{kind: target}) for part in connector.args]]
        binary = shutil.which(connector.binary)
        record = {"connector": connector.name, "command": command, "level": connector.level}
        if not binary:
            record.update(status="skipped", reason=f"No está instalado: {connector.binary}")
        else:
            completed = subprocess.run(command, capture_output=True, text=True, timeout=180, shell=False)
            output = completed.stdout + ("\n[stderr]\n" + completed.stderr if completed.stderr else "")
            (raw_dir / f"{connector.name}.txt").write_text(output, encoding="utf-8")
            record.update(status="completed" if completed.returncode == 0 else "failed", exit_code=completed.returncode,
                          artifact=f"raw/{connector.name}.txt")
        records.append(record)
    report = {"case": clean_case(case), "target_type": kind, "target": target, "started_at": started,
              "finished_at": datetime.now(timezone.utc).isoformat(), "connectors": records}
    (case_dir / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def read_report(case: str) -> dict:
    path = home() / "cases" / clean_case(case) / "report.json"
    if not path.exists():
        raise FileNotFoundError(f"No existe el caso: {case}")
    return json.loads(path.read_text(encoding="utf-8"))
