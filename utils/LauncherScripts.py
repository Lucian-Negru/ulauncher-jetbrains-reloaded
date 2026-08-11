""" Contains lookup for JetBrains Toolbox shell scripts """
from __future__ import annotations

import os
from typing import List


# pylint: disable=too-few-public-methods
class LauncherScripts:
    """ Resolves the shell script launching a given IDE """

    @staticmethod
    def find(scripts_path: str, prefixes: List[str], app_dirs: List[str]) -> str | None:
        """
        Finds the launcher script by name, falling back to a lookup by app directory
        :param scripts_path: Path to the shell scripts directory
        :param prefixes: Expected script names
        :param app_dirs: Toolbox app directory names of the IDE
        :return: Path to the launcher script
        """

        for prefix in prefixes:
            path = os.path.join(scripts_path, prefix)
            if os.path.isfile(path):
                return path

        return LauncherScripts.find_by_app_dir(scripts_path, app_dirs)

    @staticmethod
    def find_by_app_dir(scripts_path: str, app_dirs: List[str]) -> str | None:
        """
        Finds the launcher script pointing at one of the given Toolbox app directories,
        which is what tells apart IDEs whose scripts Toolbox had to number
        :param scripts_path: Path to the shell scripts directory
        :param app_dirs: Toolbox app directory names of the IDE
        :return: Path to the launcher script
        """

        if len(app_dirs) == 0:
            return None

        for name in sorted(os.listdir(scripts_path)):
            path = os.path.join(scripts_path, name)
            if not os.path.isfile(path):
                continue

            try:
                with open(path, "r", encoding="utf8") as script:
                    content = script.read()
            except (OSError, UnicodeDecodeError):
                continue

            if any(f"/{app_dir}/bin/" in content for app_dir in app_dirs):
                return path

        return None
