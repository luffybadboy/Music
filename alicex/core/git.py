# THIS CODE FULLY MODIFIED AND RE-WRITED BY @Mobarak46
import asyncio
import shlex
from typing import Tuple

# Keep imports to avoid breaking other files
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

import config
from ..logging import LOGGER


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())


def git():
    """
    Git updater disabled for Docker / Render deployments.
    This project was originally made for VPS/Heroku auto-updates,
    which do NOT work on Render containers.
    """
    LOGGER(__name__).info("Git updater disabled (Render deployment)")
    return
