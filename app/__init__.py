from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from flask import Flask, jsonify, render_template, request

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "places.json"


def load_places() -> List[Dict[str, Any]]:
    """Load saved places from the JSON file."""
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save_places(places: List[Dict[str, Any]]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as fh:
        json.dump(places, fh, indent=2)


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")

    @app.get("/")
    def index() -> str:
        return render_template("index.html")

    @app.get("/api/places")
    def get_places() -> Any:
        return jsonify(load_places())

    @app.post("/api/places")
    def add_place() -> Any:
        payload = request.get_json(force=True, silent=True)
        if not payload:
            return jsonify({"error": "Invalid JSON payload"}), 400

        required_fields = {"name", "description", "latitude", "longitude"}
        if not required_fields.issubset(payload):
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
        return jsonify(place), 201

    return app
