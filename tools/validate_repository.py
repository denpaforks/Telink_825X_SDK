#!/usr/bin/env python3
"""Validate repository structure, bilingual docs, and safety invariants."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def paired_markdown(path: Path) -> Path:
    if path.name.endswith(".zh.md"):
        return path.with_name(path.name.removesuffix(".zh.md") + ".md")
    return path.with_name(path.stem + ".zh.md")


def validate_markdown(errors: list[str]) -> None:
    markdown = sorted(ROOT.rglob("*.md"))
    if not markdown:
        fail(errors, "no Markdown documents found")
        return

    for path in markdown:
        relative = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        first_line = text.splitlines()[0] if text.splitlines() else ""
        pair = paired_markdown(path)
        if not pair.is_file():
            fail(errors, f"missing bilingual pair for {relative}")

        is_chinese = path.name.endswith(".zh.md")
        is_root_readme = relative.as_posix() in {"README.md", "README.zh.md"}
        if is_chinese:
            expected = "English-README-green" if is_root_readme else "English-Docs-green"
        else:
            expected = "中文-README-blue" if is_root_readme else "中文-文档-blue"
        if expected not in first_line:
            fail(errors, f"incorrect first-line language badge in {relative}")

        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().split()[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            local = unquote(target.split("#", 1)[0])
            if local and not (path.parent / local).resolve().exists():
                fail(errors, f"broken local link in {relative}: {target}")


def validate_projects(errors: list[str]) -> None:
    projects = sorted(
        path.parent
        for base in (ROOT / "example", ROOT / "study")
        for path in base.rglob("makefile")
    )
    if len(projects) != 18:
        fail(errors, f"expected 18 Make projects, found {len(projects)}")

    build_helper = (ROOT / "tools" / "build_all.sh").read_text(encoding="utf-8")
    for token in ("make clean", "warnings=", "sha256sum", "failed"):
        if token not in build_helper:
            fail(errors, f"build helper is missing required behavior: {token}")


def validate_flash_tool(errors: list[str]) -> None:
    tool = ROOT / "make" / "Telink_Tools.py"
    source = tool.read_text(encoding="utf-8")
    ast.parse(source, filename=str(tool))
    required = {
        "FLASH_SIZE = 0x80000": "Flash size boundary",
        "MAX_FIRMWARE_SIZE = 0x2C000": "firmware size boundary",
        "time.monotonic()": "bounded read timeout",
        "[REDACTED]": "secret redaction",
        "def write_flash": "write command handler",
    }
    for token, description in required.items():
        if token not in source:
            fail(errors, f"flash tool is missing {description}")


def main() -> int:
    errors: list[str] = []
    validate_markdown(errors)
    validate_projects(errors)
    validate_flash_tool(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print("Repository validation passed: bilingual docs, 18 projects, and flash-tool invariants.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
