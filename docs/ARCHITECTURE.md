# My Favorite Places — Architecture Notes

## High-Level Goals

* Provide a simple way to visualize a curated list of locations on an interactive web map.
* Keep the deployment lightweight for environments like Replit that excel at quick iterations.
* Demonstrate how Python + Flask can coordinate with Leaflet.js for client-side mapping.

## Key Design Decisions

### Deployment-First Mindset

The project targets platforms such as Replit where the goal is to have something deployable as quickly as possible. Flask was chosen because it:

* Has a tiny dependency footprint (only the Flask package is required).
* Offers a single-file bootstrap that plays nicely with Replit's default runner.
* Makes it trivial to serve both JSON APIs and server-rendered HTML.

### File-Based Storage Instead of a Database

Replit's persistent storage model favors small files over managed databases. Storing the places in `data/places.json` keeps the data portable, versionable, and easy to edit by hand. For a handful of favorite places, the performance overhead of reading and writing a JSON file is negligible.

If the dataset grows or concurrent writes become a concern, the code isolates file access in `load_places`/`save_places`, so the persistence layer can be swapped for a real database without touching the HTTP handlers.

### Separating Presentation From Data Delivery

The Flask backend renders a basic `index.html` template that bootstraps the Leaflet map. All place data is fetched via the `/api/places` endpoint. This approach keeps the HTML static, allowing the frontend to update dynamically without full page reloads and making it easier to reuse the API for other clients (e.g., mobile or CLI tools).

### Why Leaflet?

Leaflet is a lightweight open-source mapping library that works out of the box with OpenStreetMap tiles. It keeps the bundle small while still supporting markers, popups, and event handling. Compared with heavier platforms such as Google Maps, Leaflet requires no API keys or billing setup—perfect for quick deployments.

We rely on CDN-hosted Leaflet assets to simplify deployment. Replit automatically caches CDN assets, so the initial load is fast without bundling complexities.

### Progressive Enhancement & Accessibility

* The map markers are augmented with popups and an adjacent "Place details" panel that updates on marker click. Users who cannot interact with the map still receive location information via this panel.
* Errors from the API gracefully degrade with a message in the info panel instead of leaving the page blank.

## Future Extensions

* Add a POST form to submit new places from the UI rather than via API calls.
* Incorporate categories or tags to filter markers.
* Persist user-generated places per account once authentication is introduced.
