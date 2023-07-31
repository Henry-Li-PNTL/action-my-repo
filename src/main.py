from typer import Typer

from application.cli import mavis_helm_update_action_app

app = Typer()
app.add_typer(
    mavis_helm_update_action_app,
    name="mavis-helm-update-action",
)


if __name__ == "__main__":
    app()  # pragma: no cover
