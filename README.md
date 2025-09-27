# My Favorite Places

An interactive map that highlights a few favorite destinations using Flask on the backend and Leaflet on the frontend. The app is intentionally lightweight so it can be deployed quickly on Replit (or any other simple hosting platform).

## Features

* **Leaflet-powered map:** Visualize saved locations with popups and a detail sidebar.
* **File-backed storage:** Favorite places are stored in `data/places.json` for easy editing and portability.
* **JSON API:** `/api/places` exposes the saved places so the frontend—and other clients—can consume them.
* **Extensible backend:** A POST endpoint (`/api/places`) lets you add new locations programmatically.

## Running Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app
```

Then open http://127.0.0.1:5000/ in your browser.

## Project Structure

```
app/
  __init__.py       # Flask application factory and API routes
  __main__.py       # Allows `python -m app` execution
  templates/
    index.html      # Leaflet map layout
  static/
    css/styles.css  # Page styling
    js/map.js       # Leaflet initialization script
data/
  places.json       # Seed data with example locations
docs/
  ARCHITECTURE.md   # Design and technology rationale
```

## Extending the App

* Build a simple HTML form that posts to `/api/places` so new locations can be added from the browser.
* Swap `load_places`/`save_places` for a database-backed implementation when you outgrow flat files.
* Introduce categories or tags to filter markers (e.g., cafes, museums, nature).
