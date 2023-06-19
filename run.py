"""Flask CLI/Application entry point."""
import os

from dealflow import create_app, db
from dealflow.models.freelancer import Freelancer

application = app = create_app(os.getenv("FLASK_ENV", "production"))


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "User": Freelancer,
    }


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
