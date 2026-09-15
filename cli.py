from __future__ import annotations

import argparse
import json
import sys

from .core import read_report, run, tool_status


def main() -> None:
    parser = argparse.ArgumentParser(prog="flipx2", description="Orquestador OSINT pasivo para Kali Linux")
    subs = parser.add_subparsers(dest="command", required=True)
    subs.add_parser("tools", help="lista conectores y dependencias")
    runner = subs.add_parser("run", help="ejecuta conectores pasivos autorizados")
    runner.add_argument("--case", required=True)
    target = runner.add_mutually_exclusive_group(required=True)
    target.add_argument("--domain")
    target.add_argument("--username")
    runner.add_argument("--authorized", action="store_true", help="confirma autorización para investigar el objetivo")
    reporter = subs.add_parser("report", help="muestra el reporte de un caso")
    reporter.add_argument("--case", required=True)
    args = parser.parse_args()
    try:
        if args.command == "tools":
            payload = tool_status()
        elif args.command == "report":
            payload = read_report(args.case)
        else:
            if not args.authorized:
                parser.error("Debes incluir --authorized para ejecutar una investigación.")
            kind, value = ("domain", args.domain) if args.domain else ("username", args.username)
            payload = run(args.case, kind, value)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    except (ValueError, FileNotFoundError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
