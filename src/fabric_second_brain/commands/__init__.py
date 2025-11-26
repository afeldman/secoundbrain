"""Command implementations for Fabric Second Brain CLI.

This submodule contains the implementation of all CLI commands,
with each command in its own dedicated file for better organization.

Modules:
    classify: Auto-classify notes in vault
    config: Configuration management
    debug: Debug information
    doctor: System diagnostics
    ingest: Document and media ingestion
    init: Initialize Obsidian vault
    organize: AI-powered vault organization
    search: Semantic search
    summary: File summarization
    vision: Vision analysis
    wisdom: Extract wisdom from sources
"""

from fabric_second_brain.commands.classify import cmd_classify
from fabric_second_brain.commands.config import (
    cmd_config_set_fabric,
    cmd_config_set_model,
    cmd_config_set_vault,
    cmd_config_show,
)
from fabric_second_brain.commands.debug import cmd_debug
from fabric_second_brain.commands.doctor import cmd_doctor
from fabric_second_brain.commands.ingest import cmd_ingest
from fabric_second_brain.commands.init import cmd_init
from fabric_second_brain.commands.organize import cmd_organize
from fabric_second_brain.commands.search import cmd_search
from fabric_second_brain.commands.summary import cmd_summary
from fabric_second_brain.commands.vision import cmd_vision
from fabric_second_brain.commands.wisdom import cmd_wisdom, cmd_wisdom_summary

__all__ = [
    "cmd_classify",
    "cmd_config_set_fabric",
    "cmd_config_set_model",
    "cmd_config_set_vault",
    "cmd_config_show",
    "cmd_debug",
    "cmd_doctor",
    "cmd_ingest",
    "cmd_init",
    "cmd_organize",
    "cmd_search",
    "cmd_summary",
    "cmd_vision",
    "cmd_wisdom",
    "cmd_wisdom_summary",
]
