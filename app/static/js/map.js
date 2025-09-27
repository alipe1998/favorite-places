document.addEventListener("DOMContentLoaded", async () => {
  const map = L.map("map", {
    center: [20, 0],
    zoom: 2,
    worldCopyJump: true,
  });

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19,
  }).addTo(map);

  try {
    const response = await fetch("/api/places");
    if (!response.ok) {
      throw new Error(`Failed to fetch places: ${response.status}`);
    }

    const places = await response.json();
    const detailsElement = document.getElementById("place-details");

    places.forEach((place) => {
      const marker = L.marker([place.latitude, place.longitude]).addTo(map);
      marker.bindPopup(`\n        <h3>${place.name}</h3>\n        <p>${place.description}</p>\n      `);

      marker.on("click", () => {
        detailsElement.innerHTML = `\n          <div class="place-details">\n            <h3>${place.name}</h3>\n            <p>${place.description}</p>\n            <p class="coordinates">${place.latitude.toFixed(4)}, ${place.longitude.toFixed(4)}</p>\n          </div>\n        `;
      });
    });
  } catch (error) {
    console.error(error);
    document.getElementById("place-details").innerHTML = `\n      <p role="alert">Unable to load favorite places right now. Please try again later.</p>\n    `;
  }
});
