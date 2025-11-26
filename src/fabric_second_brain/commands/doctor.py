"""System diagnostics and health checks.

This module provides the doctor command to verify system setup,
check dependencies, and diagnose configuration issues.
"""

from __future__ import annotations

from fabric_second_brain.color import error, info, success
from fabric_second_brain.config import SBConfig
from fabric_second_brain.utils import check_command_exists, check_lmstudio_server


def cmd_doctor(cfg: SBConfig, lm_host: str, lm_port: int) -> int:
    """Run system diagnostics and check component availability.

    Verifies Fabric installation, vault path, and server connectivity.

    Args:
        cfg: Configuration instance.
        lm_host: LM Studio server host.
        lm_port: LM Studio server port.

    Returns:
        Number of problems found (0 if all OK).
    """
    print(info("🩺 Running Second-Brain Doctor"))
    print("-----------------------------------")

    problems = 0

    if not check_command_exists(cfg.fabric_cmd):
        print(error(f"❌ {cfg.fabric_cmd} not installed or not in PATH"))
        problems += 1
    else:
        print(success(f"✅ {cfg.fabric_cmd} found in PATH"))

    if not cfg.vault_path.exists():
        print(error(f"❌ vault path does not exist: {cfg.vault_path}"))
        problems += 1
    else:
        print(success(f"✅ vault path exists: {cfg.vault_path}"))

    if cfg.vendor == "lmstudio":
        if check_lmstudio_server(lm_host, lm_port):
            print(success(f"✅ LM Studio server reachable at {lm_host}:{lm_port}"))
        else:
            print(
                error(
                    f"❌ LM Studio server not reachable at {lm_host}:{lm_port} – "
                    "please start server mode"
                )
            )
            problems += 1

    if cfg.vendor == "ollama":
        if check_command_exists("ollama"):
            print(success("✅ ollama CLI found"))
        else:
            print(error("❌ ollama CLI not found in PATH"))
            problems += 1

    if problems == 0:
        print(success("🎉 System OK – everything looks good!"))
    else:
        print(error(f"⚠ Found {problems} problem(s)."))

    return problems
