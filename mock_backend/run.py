import os

from mock_backend import create_app


app = create_app()


if __name__ == "__main__":
    host = os.environ.get("BACKEND_HOST", "0.0.0.0")
    port = int(os.environ.get("BACKEND_PORT", "5001"))
    debug = os.environ.get("BACKEND_DEBUG", "1") == "1"
    app.run(host=host, port=port, debug=debug)
