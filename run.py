from app import create_app, db
from flask_migrate import Migrate
from livereload import Server
from flask_ngrok import run_with_ngrok


app = create_app("default")
run_with_ngrok(app)
migrate = Migrate(app, db)


@app.cli.command()
def initdb():
    """Initialize the database."""
    from flask_migrate import upgrade

    # migrate database to latest revision
    upgrade()


if __name__ == "__main__":
    # server = Server(app.wsgi_app)
    # server.serve()
    app.run()
