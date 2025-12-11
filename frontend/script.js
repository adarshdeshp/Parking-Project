AOS.init();

const BACKEND_URL = "http://10.173.184.189:5000";

const spinner = document.getElementById("spinner");
const gallery = document.getElementById("gallery");

async function loadImages() {
  try {
    const res = await fetch(`${BACKEND_URL}/violations`);
    const images = await res.json();
    spinner.style.display = "none";
    gallery.style.display = "grid";
    gallery.innerHTML = "";

    if (images.length === 0) {
      gallery.innerHTML = "<h2>No violations detected yet 🚘</h2>";
      return;
    }

    images.reverse().forEach((src, i) => {
      const card = document.createElement("div");
      card.className = "card";
      card.setAttribute("data-aos", "zoom-in");

      const img = document.createElement("img");
      img.src = src;
      const caption = document.createElement("p");
      caption.textContent = `Detected #${i + 1}`;

      card.appendChild(img);
      card.appendChild(caption);
      gallery.appendChild(card);
    });

    updateChart(images.length);
  } catch (err) {
    console.error("Error loading images:", err);
  }
}

function updateChart(count) {
  const ctx = document.getElementById("violationChart").getContext("2d");
  const chartData = {
    labels: Array.from({ length: count }, (_, i) => `Car ${i + 1}`),
    datasets: [
      {
        label: "Violations Detected",
        data: Array.from({ length: count }, () => Math.floor(Math.random() * 5) + 1),
        backgroundColor: "rgba(0, 198, 255, 0.4)",
        borderColor: "#00c6ff",
        borderWidth: 2,
      },
    ],
  };
  new Chart(ctx, {
    type: "bar",
    data: chartData,
    options: {
      plugins: { legend: { labels: { color: "#fff" } } },
      scales: {
        x: { ticks: { color: "#aaa" }, grid: { color: "#333" } },
        y: { ticks: { color: "#aaa" }, grid: { color: "#333" } },
      },
    },
  });
}

loadImages();
setInterval(loadImages, 6000);