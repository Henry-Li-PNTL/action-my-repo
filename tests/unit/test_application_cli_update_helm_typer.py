from typer.testing import CliRunner

from src.main import app

runner = CliRunner()


def test_app_help():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "mavis-helm-update-action" in result.output


def test_app_subcommand__mavis_helm_update_action_help():
    result = runner.invoke(app, ["mavis-helm-update-action", "--help"])

    assert result.exit_code == 0
    assert "pull-request" in result.output


def test_app_subcommand__mavis_helm_update_action___pull_request_help():
    result = runner.invoke(app, ["mavis-helm-update-action", "pull-request", "--help"])

    assert result.exit_code == 0
    assert "base" in result.output
    assert "head" in result.output
    assert "target_repo" in result.output
    assert "target_repo_app_version" in result.output
