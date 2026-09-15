"""Tests for container-aware CLI routing (NixOS container mode).

When container.enable = true in the NixOS module, the activation script
writes a .container-mode metadata file. The host CLI detects this and
execs into the container instead of running locally.
"""
import os
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from xiuqo_cli.config import (
    get_container_exec_info,
)


# =============================================================================
# get_container_exec_info
# =============================================================================


@pytest.fixture
def container_env(tmp_path, monkeypatch):
    """Set up a fake XIUQO_HOME with .container-mode file."""
    xiuqo_home = tmp_path / ".xiuqo"
    xiuqo_home.mkdir()
    monkeypatch.setenv("XIUQO_HOME", str(xiuqo_home))
    monkeypatch.delenv("XIUQO_DEV", raising=False)

    container_mode = xiuqo_home / ".container-mode"
    container_mode.write_text(
        "# Written by NixOS activation script. Do not edit manually.\n"
        "backend=podman\n"
        "container_name=xiuqo\n"
        "exec_user=xiuqo\n"
        "xiuqo_bin=/data/current-package/bin/xiuqo\n"
    )
    return xiuqo_home


def test_get_container_exec_info_returns_metadata(container_env):
    """Reads .container-mode and returns all fields including exec_user."""
    with patch("xiuqo_constants.is_container", return_value=False):
        info = get_container_exec_info()

    assert info is not None
    assert info["backend"] == "podman"
    assert info["container_name"] == "xiuqo"
    assert info["exec_user"] == "xiuqo"
    assert info["xiuqo_bin"] == "/data/current-package/bin/xiuqo"








# =============================================================================
# _exec_in_container
# =============================================================================


@pytest.fixture
def docker_container_info():
    return {
        "backend": "docker",
        "container_name": "xiuqo",
        "exec_user": "xiuqo",
        "xiuqo_bin": "/data/current-package/bin/xiuqo",
    }


@pytest.fixture
def podman_container_info():
    return {
        "backend": "podman",
        "container_name": "xiuqo",
        "exec_user": "xiuqo",
        "xiuqo_bin": "/data/current-package/bin/xiuqo",
    }


def test_exec_in_container_calls_execvp(docker_container_info):
    """Verifies os.execvp is called with correct args: runtime, tty flags,
    user, env vars, container name, binary, and CLI args."""
    from xiuqo_cli.main import _exec_in_container

    with patch("shutil.which", return_value="/usr/bin/docker"), \
         patch("subprocess.run") as mock_run, \
         patch("sys.stdin") as mock_stdin, \
         patch("os.execvp") as mock_execvp, \
         patch.dict(os.environ, {"TERM": "xterm-256color", "LANG": "en_US.UTF-8"},
                    clear=False):
        mock_stdin.isatty.return_value = True
        mock_run.return_value = MagicMock(returncode=0)

        _exec_in_container(docker_container_info, ["chat", "-m", "opus"])

    mock_execvp.assert_called_once()
    cmd = mock_execvp.call_args[0][1]
    assert cmd[0] == "/usr/bin/docker"
    assert cmd[1] == "exec"
    assert "-it" in cmd
    idx_u = cmd.index("-u")
    assert cmd[idx_u + 1] == "xiuqo"
    e_indices = [i for i, v in enumerate(cmd) if v == "-e"]
    e_values = [cmd[i + 1] for i in e_indices]
    assert "TERM=xterm-256color" in e_values
    assert "LANG=en_US.UTF-8" in e_values
    assert "xiuqo" in cmd
    assert "/data/current-package/bin/xiuqo" in cmd
    assert "chat" in cmd


