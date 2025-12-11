const views = document.querySelectorAll(".view");
const navButtons = document.querySelectorAll(".nav-btn");

navButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    const target = btn.dataset.target;
    if (!target) return;
    views.forEach(v => v.classList.toggle("active", v.id === target));
  });
});

// JPEG Compression
const jpegFile = document.getElementById("jpeg-file");
const jpegOriginal = document.getElementById("jpeg-original");
const jpegOutput = document.getElementById("jpeg-output");
const jpegRun = document.getElementById("jpeg-run");
const jpegMetrics = document.getElementById("jpeg-metrics");
let jpegCurrentFile = null;

jpegFile.addEventListener("change", (e) => {
  jpegCurrentFile = e.target.files?.[0];
  if (jpegCurrentFile) {
    const reader = new FileReader();
    reader.onload = (event) => {
      jpegOriginal.innerHTML = `<img src="${event.target.result}" style="max-width: 100%; object-fit: contain;"/>`;
    };
    reader.readAsDataURL(jpegCurrentFile);
    jpegRun.disabled = false;
    jpegOutput.innerHTML = `<p style="color: #5b6c63;">Ready</p>`;
  }
});

jpegRun.addEventListener("click", () => {
  if (!jpegCurrentFile) return;
  jpegOutput.innerHTML = `<p style="color: #5b6c63;">Compressing...</p>`;
  
  const fd = new FormData();
  fd.append("file", jpegCurrentFile);
  fd.append("quality", 50);
  
  fetch("http://127.0.0.1:5000/compress", { method: "POST", body: fd })
    .then(r => r.json())
    .then(data => {
      if (data.error) {
        jpegOutput.innerHTML = `<p style="color: red;">${data.error}</p>`;
        return;
      }
      jpegOutput.innerHTML = `<img src="${data.compressed_image}" style="max-width: 100%; object-fit: contain;"/>`;
      if (jpegMetrics) {
        document.getElementById("original-size").textContent = (data.original_size / 1024).toFixed(2) + " KB";
        document.getElementById("compressed-size").textContent = (data.compressed_size / 1024).toFixed(2) + " KB";
        document.getElementById("compression-ratio").textContent = data.compression_percentage + "%";
        jpegMetrics.style.display = "grid";
      }
    })
    .catch(() => jpegOutput.innerHTML = `<p style="color: red;">Start Flask: python app.py</p>`);
});

// Noise Reduction
const noiseFile = document.getElementById("noise-file");
const noiseOriginal = document.getElementById("noise-original");
const noiseOutput = document.getElementById("noise-output");
const noiseRun = document.getElementById("noise-run");
const filterType = document.getElementById("filter-type");
const intensity = document.getElementById("intensity");
const method = document.getElementById("method");
let noiseCurrentFile = null;

noiseFile.addEventListener("change", (e) => {
  noiseCurrentFile = e.target.files?.[0];
  if (noiseCurrentFile) {
    const reader = new FileReader();
    reader.onload = (event) => {
      noiseOriginal.innerHTML = `<img src="${event.target.result}" style="max-width: 100%; object-fit: contain;"/>`;
    };
    reader.readAsDataURL(noiseCurrentFile);
    noiseRun.disabled = false;
    noiseOutput.innerHTML = `<p style="color: #5b6c63;">Ready</p>`;
  }
});

noiseRun.addEventListener("click", () => {
  if (!noiseCurrentFile) return;
  
  const filter = filterType.value;
  
  // Check if filter is implemented
  if (filter === "Min-Max Filter" || filter === "Gaussian Filter") {
    noiseOutput.innerHTML = `<p style="color: orange;">TODO: ${filter} not yet implemented</p>`;
    return;
  }
  
  noiseOutput.innerHTML = `<p style="color: #5b6c63;">Filtering...</p>`;
  
  const fd = new FormData();
  fd.append("file", noiseCurrentFile);
  fd.append("filter_type", filter);
  fd.append("kernel_size", intensity.value);
  fd.append("method", method.value);
  
  fetch("http://127.0.0.1:5000/filter", { method: "POST", body: fd })
    .then(r => r.json())
    .then(data => {
      if (data.error) {
        noiseOutput.innerHTML = `<p style="color: red;">${data.error}</p>`;
        return;
      }
      noiseOutput.innerHTML = `<img src="${data.filtered_image}" style="max-width: 100%; object-fit: contain;"/>`;
    })
    .catch(() => noiseOutput.innerHTML = `<p style="color: red;">Start Flask: python app.py</p>`);
});
