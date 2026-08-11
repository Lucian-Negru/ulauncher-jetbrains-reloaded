""" Tests for the JetBrains Toolbox shell scripts lookup """

# pylint: disable=missing-function-docstring

from utils.LauncherScripts import LauncherScripts

PHPSTORM_SCRIPT = "phpstorm"
NUMBERED_SCRIPT = "phpstorm2"
LIGHT_SCRIPT = "phpstorm-light"
PHPSTORM_APP_DIR = "phpstorm"
LIGHT_APP_DIR = "phpstorm-light"


def test_finds_script_matching_the_expected_name(tmp_path):
    scripts = make_scripts_dir(tmp_path, {LIGHT_SCRIPT: LIGHT_APP_DIR})

    found = LauncherScripts.find(scripts, [LIGHT_SCRIPT], [LIGHT_APP_DIR])

    assert found == str(tmp_path / LIGHT_SCRIPT)


def test_prefers_the_expected_name_over_the_app_directory(tmp_path):
    scripts = make_scripts_dir(
        tmp_path, {LIGHT_SCRIPT: LIGHT_APP_DIR, NUMBERED_SCRIPT: LIGHT_APP_DIR}
    )

    found = LauncherScripts.find(scripts, [LIGHT_SCRIPT], [LIGHT_APP_DIR])

    assert found == str(tmp_path / LIGHT_SCRIPT)


def test_falls_back_to_the_script_pointing_at_the_app_directory(tmp_path):
    scripts = make_scripts_dir(
        tmp_path, {PHPSTORM_SCRIPT: PHPSTORM_APP_DIR, NUMBERED_SCRIPT: LIGHT_APP_DIR}
    )

    found = LauncherScripts.find(scripts, [LIGHT_SCRIPT], [LIGHT_APP_DIR])

    assert found == str(tmp_path / NUMBERED_SCRIPT)


def test_ignores_scripts_of_an_ide_whose_app_directory_shares_a_prefix(tmp_path):
    scripts = make_scripts_dir(tmp_path, {NUMBERED_SCRIPT: LIGHT_APP_DIR})

    found = LauncherScripts.find(scripts, [PHPSTORM_SCRIPT], [PHPSTORM_APP_DIR])

    assert found is None


def test_returns_nothing_when_the_ide_declares_no_app_directory(tmp_path):
    scripts = make_scripts_dir(tmp_path, {NUMBERED_SCRIPT: LIGHT_APP_DIR})

    found = LauncherScripts.find(scripts, [LIGHT_SCRIPT], [])

    assert found is None


def make_scripts_dir(tmp_path, scripts: dict) -> str:
    """
    Writes Toolbox-style launcher scripts, each pointing at the given app directory
    :param tmp_path: Directory to write the scripts to
    :param scripts: Script names mapped to their Toolbox app directory
    :return: Path to the scripts directory
    """

    for name, app_dir in scripts.items():
        script = tmp_path / name
        script.write_text(
            "#!/bin/bash\n"
            f'"/home/user/.local/share/JetBrains/Toolbox/apps/{app_dir}/bin/phpstorm" "$@"\n',
            encoding="utf8"
        )
        script.chmod(0o755)

    return str(tmp_path)
