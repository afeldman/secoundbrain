"""Debug information display.

This module provides the debug command to display system configuration
and diagnostic information.
"""

from __future__ import annotations

from fabric_second_brain.color import info
from fabric_second_brain.config import SBConfig
from fabric_second_brain.utils import check_command_exists, check_lmstudio_server


def cmd_debug(cfg: SBConfig, lm_host: str, lm_port: int) -> int:
    """Display debug information about system setup.

    Args:
        cfg: Configuration instance.
        lm_host: LM Studio server host.
        lm_port: LM Studio server port.

    Returns:
        Always returns 0 (success).
    """
    print(info("🔧 Second-Brain Debug Information"))
    print("-----------------------------------")
    print(f"Fabric command:     {cfg.fabric_cmd}")
    print(f"Fabric installed:   {'✅' if check_command_exists(cfg.fabric_cmd) else '❌'}")
    print(f"Vendor:             {cfg.vendor}")
    print(f"Model:              {cfg.model}")
    print(f"Vault path:         {cfg.vault_path}")
    print(f"LM Studio host:     {lm_host}")
    print(f"LM Studio port:     {lm_port}")

    if cfg.vendor == "lmstudio":
        print(
            f"LM Studio server:   "
            f"{'✅ reachable' if check_lmstudio_server(lm_host, lm_port) else '❌ not reachable'}"
        )

    if cfg.vendor == "ollama":
        print("Ollama:             (no active HTTP check implemented, vendor=ollama)")

    return 0
