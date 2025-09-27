from __future__ import annotations

import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, List

from flask import Flask, jsonify, render_template, request

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "places.json"
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_FILE = LOG_DIR / "app.log"


def load_places() -> List[Dict[str, Any]]:
    """Load saved places from the JSON file."""
    if not DATA_FILE.exists():
        logging.getLogger(__name__).warning("Places data file not found at %s", DATA_FILE)
        return []

    with DATA_FILE.open("r", encoding="utf-8") as fh:
        places = json.load(fh)

    logging.getLogger(__name__).info("Loaded %d places from data file", len(places))
    return places


def save_places(places: List[Dict[str, Any]]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as fh:
        json.dump(places, fh, indent=2)
    logging.getLogger(__name__).info("Persisted %d places to data file", len(places))


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    if not any(isinstance(handler, RotatingFileHandler) for handler in app.logger.handlers):
        file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=5)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)

    @app.get("/")
    def index() -> str:
        app.logger.info("Rendering index page")
        return render_template("index.html")

    @app.get("/api/places")
    def get_places() -> Any:
        app.logger.info("Fetching stored places")
        return jsonify(load_places())

    @app.post("/api/places")
    def add_place() -> Any:
        payload = request.get_json(force=True, silent=True)
        if not payload:
            app.logger.warning("Received empty payload when creating a place")
            return jsonify({"error": "Invalid JSON payload"}), 400

        required_fields = {"name", "description", "latitude", "longitude"}
        if not required_fields.issubset(payload):
            app.logger.warning(
                "Missing required fields when creating a place: provided keys=%s",
                sorted(payload.keys()) if hasattr(payload, "keys") else payload,
            )
            return (
                jsonify(
                    {
                        "error": "Missing required fields",
                        "required": sorted(required_fields),
                    }
                ),
                400,
            )

        try:
            latitude = float(payload["latitude"])
            longitude = float(payload["longitude"])
        except (TypeError, ValueError):
            app.logger.warning(
                "Invalid latitude/longitude provided: lat=%s lon=%s",
                payload.get("latitude"),
                payload.get("longitude"),
            )
            return (
                jsonify({"error": "Latitude and longitude must be numeric."}),
                400,
            )

        place = {
            "name": str(payload["name"]),
            "description": str(payload["description"]),
            "latitude": latitude,
            "longitude": longitude,
        }

        places = load_places()
        places.append(place)
        save_places(places)
        app.logger.info("Added new place '%s'", place["name"])
        return jsonify(place), 201

    return app
