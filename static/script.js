const API_VIDEOS = "/api/videos";
const UPLOAD_ENDPOINT = "/upload";
const container = document.getElementById("reelsContainer");
const fileInput = document.getElementById("fileInput");
const toast = document.getElementById("toast");

function showToast(t) {
  toast.hidden = false;
  toast.textContent = t;
  setTimeout(()=> toast.hidden=true, 3000);
}

async function fetchVideos() {
  const res = await fetch(API_VIDEOS);
  if (!res.ok) return [];
  return await res.json();
}

function buildReel(video) {
  const reel = document.createElement("section");
  reel.className = "reel";
  const vid = document.createElement("video");
  vid.src = video.url;
  vid.controls = false;
  vid.playsInline = true;
  vid.loop = false;
  vid.preload = "metadata";
  vid.setAttribute("muted", "true");
  vid.style.cursor = "pointer";
  // toggle play/pause on click
  vid.addEventListener("click", () => {
    if (vid.paused) vid.play(); else vid.pause();
  });
  reel.appendChild(vid);
  const overlay = document.createElement("div");
  overlay.className = "overlay";
  overlay.innerHTML = `<div class="icon">❤</div><div class="icon">💬</div>`;
  reel.appendChild(overlay);

  return {reel, vid};
}

async function loadAndRender() {
  const videos = await fetchVideos();
  container.innerHTML = "";
  const observers = [];
  const items = videos.map(v => buildReel(v));
  items.forEach(({reel}) => container.appendChild(reel));

  const options = { root: container, threshold: [0.6] };
  const obs = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      const vid = e.target.querySelector("video");
      if (!vid) return;
      if (e.intersectionRatio >= 0.6) {
        // play
        vid.play().catch(()=>{});
      } else {
        vid.pause();
        vid.currentTime = vid.currentTime; // keep position
      }
    });
  }, options);

  document.querySelectorAll(".reel").forEach(r => obs.observe(r));
}

fileInput.addEventListener("change", async (ev)=>{
  const f = ev.target.files[0];
  if (!f) return;
  if (f.size > 200 * 1024 * 1024) { showToast("File too large"); return; }

  const fd = new FormData();
  fd.append("video", f);
  showToast("Uploading...");
  try {
    const res = await fetch(UPLOAD_ENDPOINT, { method: "POST", body: fd });
    const json = await res.json();
    if (res.ok && json.success) {
      showToast("Uploaded!");
      await loadAndRender();
    } else {
      showToast("Upload failed");
      console.error(json);
    }
  } catch (err) {
    console.error(err);
    showToast("Upload error");
  } finally {
    fileInput.value = "";
  }
});

loadAndRender();
