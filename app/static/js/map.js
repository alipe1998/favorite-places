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

  const detailsElement = document.getElementById("place-details");
  const form = document.getElementById("add-place-form");
  const statusElement = document.getElementById("form-status");

  const renderDetails = (place) => {
    if (!detailsElement) return;

    const { latitude, longitude } = place;
    const latitudeText = Number.isFinite(latitude)
      ? latitude.toFixed(4)
      : String(latitude);
    const longitudeText = Number.isFinite(longitude)
      ? longitude.toFixed(4)
      : String(longitude);

    detailsElement.innerHTML = `
      <div class="place-details">
        <h3>${place.name}</h3>
        <p>${place.description}</p>
        <p class="coordinates">${latitudeText}, ${longitudeText}</p>
      </div>
    `;
  };

  const addMarkerForPlace = (place) => {
    const marker = L.marker([place.latitude, place.longitude]).addTo(map);
    marker.bindPopup(`
      <h3>${place.name}</h3>
      <p>${place.description}</p>
    `);

    marker.on("click", () => {
      renderDetails(place);
    });

    return marker;
  };

  try {
    const response = await fetch("/api/places");
    if (!response.ok) {
      throw new Error(`Failed to fetch places: ${response.status}`);
    }

    const places = await response.json();
    places.forEach((place) => addMarkerForPlace(place));
  } catch (error) {
    console.error(error);
    if (detailsElement) {
      detailsElement.innerHTML = `
        <p role="alert">Unable to load favorite places right now. Please try again later.</p>
      `;
    }
  }

  const setStatusMessage = (message, type = "") => {
    if (!statusElement) return;
    statusElement.textContent = message;
    statusElement.classList.remove("success", "error");
    if (type) {
      statusElement.classList.add(type);
    }
  };

  form?.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const name = formData.get("name").toString().trim();
    const description = formData.get("description").toString().trim();
    const latitudeValue = formData.get("latitude").toString().trim();
    const longitudeValue = formData.get("longitude").toString().trim();

    if (!name || !description || !latitudeValue || !longitudeValue) {
      setStatusMessage("Please fill out all fields before submitting.", "error");
      return;
    }

    const latitude = Number.parseFloat(latitudeValue);
    const longitude = Number.parseFloat(longitudeValue);

    if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
      setStatusMessage("Latitude and longitude must be valid numbers.", "error");
      return;
    }

    const payload = { name, description, latitude, longitude };

    try {
      setStatusMessage("Saving place...");

      const response = await fetch("/api/places", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorBody = await response.json().catch(() => ({}));
        const errorMessage = errorBody.error || "Unable to save the place.";
        throw new Error(errorMessage);
      }

      const savedPlace = await response.json();
      addMarkerForPlace(savedPlace).openPopup();
      map.setView(
        [savedPlace.latitude, savedPlace.longitude],
        Math.max(map.getZoom(), 6)
      );
      renderDetails(savedPlace);
      form.reset();
      setStatusMessage(`Added '${savedPlace.name}' to your map!`, "success");
    } catch (error) {
      console.error(error);
      setStatusMessage(
        error instanceof Error ? error.message : "Unable to save the place.",
        "error"
      );
    }
  });
});
