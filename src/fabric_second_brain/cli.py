"""Main CLI entry point for Fabric Second Brain.

This module provides the argument parser and routes commands to their
respective implementations in the commands submodule.
"""

from __future__ import annotations

import argparse
import sys

from fabric_second_brain.banner import print_banner
from fabric_second_brain.commands import (
    cmd_classify,
    cmd_config_set_fabric,
    cmd_config_set_model,
    cmd_config_set_vault,
    cmd_config_show,
    cmd_debug,
    cmd_doctor,
    cmd_ingest,
    cmd_init,
    cmd_organize,
    cmd_search,
    cmd_summary,
    cmd_vision,
    cmd_wisdom,
    cmd_wisdom_summary,
)
from fabric_second_brain.config import load_config


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the CLI.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="second-brain",
        description="Second Brain CLI around Fabric AI + Obsidian + LM Studio/Ollama",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init
    subparsers.add_parser("init", help="Initialize Second Brain vault structure")

    # config
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_sub = config_parser.add_subparsers(dest="config_cmd", help="Config commands")

    config_sub.add_parser("show", help="Show current configuration")

    set_model = config_sub.add_parser("set-model", help="Set AI model")
    set_model.add_argument("model", help="Model name (e.g., openai/gpt-4)")

    set_vault = config_sub.add_parser("set-vault", help="Set vault path")
    set_vault.add_argument("vault", help="Path to Obsidian vault")

    set_fabric = config_sub.add_parser("set-fabric-cmd", help="Set Fabric command path")
    set_fabric.add_argument("fabric_cmd", help="Path to fabric command")

    # classify
    classify_parser = subparsers.add_parser("classify", help="Auto-classify notes in vault")
    classify_parser.add_argument("--path", help="Override vault path")

    # search
    search_parser = subparsers.add_parser("search", help="Semantic search in vault")
    search_parser.add_argument("query", help="Search query")

    # organize
    organize_parser = subparsers.add_parser("organize", help="Organize vault with AI")
    organize_parser.add_argument("--path", help="Override vault path")

    # vision
    vision_parser = subparsers.add_parser("vision", help="Vision analysis for images")
    vision_parser.add_argument("image", help="Path to image file")

    # summary
    summary_parser = subparsers.add_parser("summary", help="Summarize a file")
    summary_parser.add_argument("file", help="File to summarize")

    # wisdom
    wisdom_parser = subparsers.add_parser("wisdom", help="Extract wisdom from PDF or YouTube")
    wisdom_parser.add_argument("--pdf", help="Path to PDF file")
    wisdom_parser.add_argument("--youtube", help="YouTube URL")
    wisdom_parser.add_argument("--into-vault", action="store_true", help="Save to vault")
    wisdom_parser.add_argument("--model", help="Override model")
    wisdom_parser.add_argument("--vendor", help="Override vendor")
    wisdom_parser.add_argument("--tags", help="Comma-separated tags")
    wisdom_parser.add_argument("--category", help="Vault category (default: Wisdom)")
    wisdom_parser.add_argument("--title", help="Custom title")

    # wisdom-summary
    wisdom_summary_parser = subparsers.add_parser(
        "wisdom-summary", help="Create wisdom note + second-level summary"
    )
    wisdom_summary_parser.add_argument("--pdf", help="Path to PDF file")
    wisdom_summary_parser.add_argument("--youtube", help="YouTube URL")
    wisdom_summary_parser.add_argument("--into-vault", action="store_true", help="Save to vault")
    wisdom_summary_parser.add_argument("--model", help="Override model")
    wisdom_summary_parser.add_argument("--vendor", help="Override vendor")
    wisdom_summary_parser.add_argument("--tags", help="Comma-separated tags")
    wisdom_summary_parser.add_argument("--category", help="Vault category (default: Wisdom)")
    wisdom_summary_parser.add_argument("--title", help="Custom title for both notes")

    # ingest
    ingest_parser = subparsers.add_parser("ingest", help="Ingest documents and media files")
    ingest_parser.add_argument("file", help="File to ingest")
    ingest_parser.add_argument("--into-vault", action="store_true", help="Save to vault")
    ingest_parser.add_argument("--model", help="Override model")
    ingest_parser.add_argument("--vendor", help="Override vendor")
    ingest_parser.add_argument("--tags", help="Comma-separated tags")
    ingest_parser.add_argument(
        "--category", help="Vault category (Literature/Media, auto-detected if not set)"
    )
    ingest_parser.add_argument("--title", help="Custom title")

    # debug
    debug_parser = subparsers.add_parser("debug", help="Show debug information")
    debug_parser.add_argument("--lm-host", default="localhost", help="LM Studio host")
    debug_parser.add_argument("--lm-port", type=int, default=1234, help="LM Studio port")

    # doctor
    doctor_parser = subparsers.add_parser("doctor", help="Run system diagnostics")
    doctor_parser.add_argument("--lm-host", default="localhost", help="LM Studio host")
    doctor_parser.add_argument("--lm-port", type=int, default=1234, help="LM Studio port")

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the CLI.

    Args:
        argv: Command-line arguments. Uses sys.argv[1:] if None.

    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    print_banner()

    argv = argv or sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    # Load configuration
    cfg = load_config()

    # Route to commands
    if args.command == "init":
        return cmd_init(cfg)

    elif args.command == "config":
        if args.config_cmd == "show":
            return cmd_config_show(cfg)
        elif args.config_cmd == "set-model":
            return cmd_config_set_model(cfg, args.model)
        elif args.config_cmd == "set-vault":
            return cmd_config_set_vault(cfg, args.vault)
        elif args.config_cmd == "set-fabric-cmd":
            return cmd_config_set_fabric(cfg, args.fabric_cmd)
        else:
            parser.parse_args(["config", "--help"])
            return 1

    elif args.command == "classify":
        return cmd_classify(cfg, args.path)

    elif args.command == "search":
        return cmd_search(cfg, args.query)

    elif args.command == "organize":
        return cmd_organize(cfg, args.path)

    elif args.command == "vision":
        return cmd_vision(cfg, args.image)

    elif args.command == "summary":
        return cmd_summary(cfg, args.file)

    elif args.command == "wisdom":
        # Update cfg with model/vendor if provided
        if args.model:
            cfg.model = args.model
        if args.vendor:
            cfg.vendor = args.vendor
        return cmd_wisdom(
            cfg=cfg,
            pdf=args.pdf,
            youtube=args.youtube,
            into_vault=args.into_vault,
            output_file=None,
            title=args.title,
            tags_raw=args.tags,
        )

    elif args.command == "wisdom-summary":
        # Update cfg with model/vendor if provided
        if args.model:
            cfg.model = args.model
        if args.vendor:
            cfg.vendor = args.vendor
        return cmd_wisdom_summary(
            cfg=cfg,
            pdf=args.pdf,
            youtube=args.youtube,
            into_vault=args.into_vault,
            output_file=None,
            title=args.title,
            tags_raw=args.tags,
        )

    elif args.command == "ingest":
        # Update cfg with model/vendor if provided
        if args.model:
            cfg.model = args.model
        if args.vendor:
            cfg.vendor = args.vendor
        return cmd_ingest(
            cfg=cfg,
            file_path=args.file,
            into_vault=args.into_vault,
            output_file=None,
            title=args.title,
            tags_raw=args.tags,
            category=args.category,
        )

    elif args.command == "debug":
        return cmd_debug(cfg, args.lm_host, args.lm_port)

    elif args.command == "doctor":
        return cmd_doctor(cfg, args.lm_host, args.lm_port)

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
