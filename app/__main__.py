"""Application entrypoint for local runs and platforms like Render."""

from __future__ import annotations

import os

from . import create_app


app = create_app()


if __name__ == "__main__":
    # Render injects the port in the PORT env var and expects the server to
    # listen on all interfaces. Fall back to Flask defaults for local runs.
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
