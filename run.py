from app import create_app, db
from flask_migrate import Migrate
from livereload import Server

app = create_app("default")
migrate = Migrate(app, db)


@app.cli.command()
def initdb():
    """Initialize the database."""
    from flask_migrate import upgrade

    # migrate database to latest revision
    upgrade()


if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.serve()
    # app.run(host="127.0.0.1", port=os.environ.get("PORT"))