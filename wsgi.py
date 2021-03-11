from app import create_app, db
from flask_migrate import Migrate

app = create_app("default")
migrate = Migrate(app, db)


@app.cli.command()
def initdb():
    """Initialize the database."""
    from flask_migrate import upgrade

    # migrate database to latest revision
    upgrade()


if __name__ == "__main__":
    app.run()