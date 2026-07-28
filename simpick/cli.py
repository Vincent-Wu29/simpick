import argparse
from pathlib import Path

def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument(
        "--set",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Override a dotted config value; may be repected"
    )
    parser.add_argument("--verbose", action="store_true")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="simpick",
        description="SimPick visual manipulation and behavior cloning toolkit",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate = subparsers.add_parser("evaluate", help="Evaluate policies with shared metrics")
    _add_common(evaluate)
    evaluate.add_argument(
        "--methods",
        nargs="+",
        choices=["random", "oracle", "vision", "bc"],
        default=None
    )
    evaluate.add_argument("--checkpoint", type=Path, default=None)
    evaluate.add_argument("--output", type=Path, default=None)
    evaluate.add_argument("--task", choices=["pick", "reach"], default="pick")
    return parser

def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args()

    return 0