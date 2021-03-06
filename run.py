from app import app
from livereload import Server


if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.serve()
    # app.run(host="127.0.0.1", port=os.environ.get("PORT"))