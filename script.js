const CONFIG = {
  WEATHER_API_KEY: "82ef7eb8c710a4d63f28712218fd2b3e",
  FALLBACK_CITY: "New York"
};

const elements = {
  form: document.getElementById("cityForm"),
  input: document.getElementById("cityInput"),
  location: document.getElementById("location"),
  weather: document.getElementById("weather"),
  trends: document.getElementById("trends"),
  videos: document.getElementById("videos"),
  loader: document.getElementById("loader")
};

document.addEventListener("DOMContentLoaded", initApp);

async function initApp() {
  elements.form.addEventListener("submit", handleFormSubmit);
  try {
    const city = await detectLocation();
    await updateDashboard(city);
  } catch {
    await updateDashboard(CONFIG.FALLBACK_CITY);
  }
}

async function handleFormSubmit(e) {
  e.preventDefault();
  const city = elements.input.value.trim();
  if (!city) return;
  await updateDashboard(city);
}

async function updateDashboard(city) {
  showLoader(true);
  try {
    elements.location.textContent = `📍 ${city}`;
    const weather = await fetchWeather(city);
   const trend = await getLocalTrend(city);
    elements.trends.textContent = `🔥 Local Trend: ${trend}`;
    showRecommendations(weather, trend, city);
  } catch (error) {
    console.error("Error:", error);
    showErrorState();
  } finally {
    showLoader(false);
  }
}

async function fetchWeather(city) {
  const res = await fetch(
    `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${CONFIG.WEATHER_API_KEY}&units=metric`
  );
  const data = await res.json();
  if (data.cod !== 200) throw new Error("Weather fetch failed");

  elements.weather.textContent = `🌦 ${data.weather[0].description}, ${data.main.temp}°C`;
  updateBackground(data.weather[0].main);
  return {
    condition: data.weather[0].main,
    temp: data.main.temp
  };
}

function updateBackground(condition) {
  document.body.className = "";
  if (condition.includes("Rain")) document.body.classList.add("rainy");
  else if (condition.includes("Snow")) document.body.classList.add("snowy");
  else if (condition.includes("Clear")) document.body.classList.add("sunny");
  else document.body.classList.add("cloudy");
}

async function getLocalTrend(city) {
  try {
    const res = await fetch(`http://localhost:5000/trends?city=${encodeURIComponent(city)}`);
    const data = await res.json();
    return data.trend || "local culture";
  } catch (err) {
    console.error("Backend trend fetch failed:", err);
    return "local culture";
  }
}

  };
  const options = trends[city] || ["Local culture"];
  return options[Math.floor(Math.random() * options.length)];
}

function showRecommendations(weather, trend, city) {
  elements.videos.innerHTML = "";
  const theme = generateThemes(weather.condition);

  const suggestions = [
    {
      title: `${trend} in ${city}`,
      description: "Trending in your area",
      searchQuery: `${trend} ${city}`
    },
    {
      title: `${weather.condition} Day Ideas`,
      description: theme,
      searchQuery: `${theme} ${city}`
    }
  ];

  suggestions.forEach(item => {
    const card = document.createElement("div");
    card.className = "recommendation-card";
    const thumbUrl = `https://img.youtube.com/vi/${getRandomId()}/0.jpg`;

    card.innerHTML = `
      <img src="${thumbUrl}" alt="${item.title}">
      <h3>${item.title}</h3>
      <p>${item.description}</p>
      <a href="https://www.youtube.com/results?search_query=${encodeURIComponent(item.searchQuery)}"
         target="_blank" class="search-button">Search Videos</a>
    `;
    elements.videos.appendChild(card);
  });
}

function getRandomId() {
  const chars = "abcdefghijklmnopqrstuvwxyz0123456789";
  return Array.from({ length: 11 }, () => chars[Math.floor(Math.random() * chars.length)]).join("");
}

function generateThemes(condition) {
  const themes = {
    Rain: "Indoor activities",
    Snow: "Hot drinks & cozy spots",
    Clear: "Outdoor adventures",
    Clouds: "Chill day ideas"
  };
  return themes[condition] || "Explore nearby";
}

function showLoader(show) {
  elements.loader.style.display = show ? "block" : "none";
}

function showErrorState() {
  elements.weather.textContent = "❗ Unable to fetch weather.";
  elements.trends.textContent = "❗ Trend data unavailable.";
  elements.videos.innerHTML = `<p style="color:red;">Failed to load recommendations.</p>`;
}

async function detectLocation() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) return reject();
    navigator.geolocation.getCurrentPosition(async pos => {
      try {
        const city = await reverseGeocode(pos.coords.latitude, pos.coords.longitude);
        resolve(city);
      } catch {
        reject();
      }
    }, reject);
  });
}

async function reverseGeocode(lat, lon) {
  const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`);
  const data = await res.json();
  return data.address.city || data.address.town || CONFIG.FALLBACK_CITY;
}
