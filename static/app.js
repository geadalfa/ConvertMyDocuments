/**
 * app.js
 * Frontend controller for DocShield Converter.
 * Zero-Leakage Offline Document & OCR Suite.
 */

(function () {
  "use strict";

  // Application State
  const state = {
    currentMode: "pdf_to_word",
    selectedFiles: [], // Array of { name, size, type, data }
    outputDir: "C:\\Users\\Alfa\\Downloads",
    activeJobId: null,
    pollInterval: null,
    lastResult: null,
  };

  // DOM Elements
  const navTabs = document.getElementById("navTabs");
  const tabButtons = document.querySelectorAll(".tab-btn");
  const bannerTitle = document.getElementById("bannerTitle");
  const bannerDesc = document.getElementById("bannerDesc");
  const dropZone = document.getElementById("dropZone");
  const fileInput = document.getElementById("fileInput");
  const btnBrowse = document.getElementById("btnBrowse");
  const dropzoneAcceptText = document.getElementById("dropzoneAcceptText");

  const filesPreviewSection = document.getElementById("filesPreviewSection");
  const filesList = document.getElementById("filesList");
  const filesCount = document.getElementById("filesCount");
  const btnClearFiles = document.getElementById("btnClearFiles");

  const optOcrContainer = document.getElementById("optOcrContainer");
  const optAutoOcr = document.getElementById("optAutoOcr");
  const optWatermarkContainer = document.getElementById("optWatermarkContainer");
  const optBleachWm = document.getElementById("optBleachWm");
  const optThresholdRow = document.getElementById("optThresholdRow");
  const optWmThreshold = document.getElementById("optWmThreshold");
  const thresholdVal = document.getElementById("thresholdVal");
  const optUnlockContainer = document.getElementById("optUnlockContainer");
  const optUnlock = document.getElementById("optUnlock");
  const optPageSizeContainer = document.getElementById("optPageSizeContainer");
  const optPageSize = document.getElementById("optPageSize");
  const outputDirDisplay = document.getElementById("outputDirDisplay");

  const btnStartConvert = document.getElementById("btnStartConvert");
  const btnConvertText = document.getElementById("btnConvertText");

  const progressCard = document.getElementById("progressCard");
  const progressStatusText = document.getElementById("progressStatusText");
  const progressPercentBadge = document.getElementById("progressPercentBadge");
  const progressBarFill = document.getElementById("progressBarFill");

  const resultCard = document.getElementById("resultCard");
  const resultFilePath = document.getElementById("resultFilePath");
  const resModeBadge = document.getElementById("resModeBadge");
  const resPagesBadge = document.getElementById("resPagesBadge");
  const btnOpenFile = document.getElementById("btnOpenFile");
  const btnOpenFolder = document.getElementById("btnOpenFolder");
  const btnCopyText = document.getElementById("btnCopyText");
  const btnConvertAnother = document.getElementById("btnConvertAnother");

  const textPreviewContainer = document.getElementById("textPreviewContainer");
  const textPreviewBox = document.getElementById("textPreviewBox");
  const charCountLabel = document.getElementById("charCountLabel");
  const toast = document.getElementById("toast");
  const toastMsg = document.getElementById("toastMsg");

  // Mode Configuration Specs
  const MODE_CONFIGS = {
    pdf_to_word: {
      title: "1. Konversi PDF ke Dokumen Word (.docx)",
      desc: "Mengekstrak PDF digital atau halaman scan non-selectable dengan RapidOCR offline, pemutihan watermark, dan buka proteksi PDF.",
      accept: ".pdf",
      multiple: false,
      btnText: "Mulai Konversi PDF ke Word",
      showOcr: true,
      showUnlock: true,
      showPageSize: false,
    },
    pdf_to_text: {
      title: "2. Ekstraksi PDF ke File Teks (.txt)",
      desc: "Mengekstrak teks digital secara langsung atau menjalankan OCR otomatis untuk scanned PDF. Teks dapat langsung disalin ke clipboard.",
      accept: ".pdf",
      multiple: false,
      btnText: "Mulai Ekstraksi Teks dari PDF",
      showOcr: true,
      showUnlock: true,
      showPageSize: false,
    },
    jpg_to_pdf: {
      title: "3. Gabungkan Gambar / Foto ke Dokumen PDF (.pdf)",
      desc: "Menyatukan satu atau banyak foto / scan dokumen (JPG, PNG, WEBP, BMP) menjadi satu berkas PDF dengan kualitas tinggi.",
      accept: ".jpg,.jpeg,.png,.webp,.bmp,.tiff",
      multiple: true,
      btnText: "Mulai Gabungkan Gambar ke PDF",
      showOcr: false,
      showUnlock: false,
      showPageSize: true,
    },
    jpg_to_word: {
      title: "4. Ekstrak Teks Gambar / Foto ke Word (.docx)",
      desc: "Membaca teks dari gambar, kwitansi, foto dokumen atau buku ber-watermark menggunakan RapidOCR dan menyusunnya ke Word rapi.",
      accept: ".jpg,.jpeg,.png,.webp,.bmp,.tiff",
      multiple: true,
      btnText: "Mulai OCR Gambar ke Word",
      showOcr: false,
      showUnlock: false,
      showPageSize: false,
    },
  };

  // Initialize
  function init() {
    setupEventListeners();
    fetchSystemStatus();
    switchMode("pdf_to_word");
    startHeartbeat();
  }

  // System Status
  async function fetchSystemStatus() {
    try {
      const res = await fetch("/api/status");
      if (res.ok) {
        const data = await res.json();
        if (data.default_output_dir) {
          state.outputDir = data.default_output_dir;
          outputDirDisplay.textContent = state.outputDir;
        }
      }
    } catch (e) {
      console.warn("Status fetch failed:", e);
    }
  }

  // Switch Active Mode
  function switchMode(modeKey) {
    state.currentMode = modeKey;
    const config = MODE_CONFIGS[modeKey];
    if (!config) return;

    // Update Nav Tab Active States
    tabButtons.forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.mode === modeKey);
    });

    // Update Mode Banner
    bannerTitle.textContent = config.title;
    bannerDesc.textContent = config.desc;

    // Update File Input Constraints
    fileInput.accept = config.accept;
    fileInput.multiple = config.multiple;
    dropzoneAcceptText.textContent = `Mendukung format: ${config.accept.replace(/\./g, " ").toUpperCase()}`;

    // Toggle Specific Option Visibility
    optOcrContainer.classList.toggle("hidden", !config.showOcr);
    optUnlockContainer.classList.toggle("hidden", !config.showUnlock);
    optPageSizeContainer.classList.toggle("hidden", !config.showPageSize);

    // Reset Selected Files when switching modes
    state.selectedFiles = [];
    renderFilesList();
    resetResultViews();
    updateConvertButtonState();
  }

  // Format File Size
  function formatBytes(bytes) {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
  }

  // Handle Files Selected
  async function handleFilesSelected(fileList) {
    if (!fileList || fileList.length === 0) return;
    const config = MODE_CONFIGS[state.currentMode];

    const newFiles = Array.from(fileList);
    const filesToLoad = config.multiple ? newFiles : [newFiles[0]];

    for (const file of filesToLoad) {
      try {
        const dataUrl = await readFileAsDataUrl(file);
        // Avoid duplicate by name & size
        const exists = state.selectedFiles.some(
          (f) => f.name === file.name && f.size === file.size
        );
        if (!exists) {
          if (!config.multiple) {
            state.selectedFiles = [{ name: file.name, size: file.size, type: file.type, data: dataUrl }];
          } else {
            state.selectedFiles.push({ name: file.name, size: file.size, type: file.type, data: dataUrl });
          }
        }
      } catch (err) {
        console.error("Failed to read file:", err);
      }
    }

    renderFilesList();
    updateConvertButtonState();
  }

  function readFileAsDataUrl(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  // Render Selected Files
  function renderFilesList() {
    filesList.innerHTML = "";
    if (state.selectedFiles.length === 0) {
      filesPreviewSection.classList.add("hidden");
      filesCount.textContent = "0";
      return;
    }

    filesPreviewSection.classList.remove("hidden");
    filesCount.textContent = state.selectedFiles.length.toString();

    state.selectedFiles.forEach((file, index) => {
      const row = document.createElement("div");
      row.className = "file-row";
      row.innerHTML = `
        <div class="file-info">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
            <polyline points="14 2 14 8 20 8"/>
          </svg>
          <span class="file-name" title="${file.name}">${file.name}</span>
          <span class="file-size">${formatBytes(file.size)}</span>
        </div>
        <button type="button" class="btn-remove-file" data-index="${index}" title="Hapus berkas ini">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      `;

      row.querySelector(".btn-remove-file").addEventListener("click", () => {
        state.selectedFiles.splice(index, 1);
        renderFilesList();
        updateConvertButtonState();
      });

      filesList.appendChild(row);
    });
  }

  // Update Convert Button State
  function updateConvertButtonState() {
    const config = MODE_CONFIGS[state.currentMode];
    if (state.selectedFiles.length === 0) {
      btnStartConvert.disabled = true;
      btnConvertText.textContent = "Pilih Berkas Terlebih Dahulu";
    } else {
      btnStartConvert.disabled = false;
      const count = state.selectedFiles.length;
      if (count === 1) {
        btnConvertText.textContent = config.btnText;
      } else {
        btnConvertText.textContent = `${config.btnText} (${count} Berkas)`;
      }
    }
  }

  // Reset Result & Progress Views
  function resetResultViews() {
    progressCard.classList.add("hidden");
    resultCard.classList.add("hidden");
    textPreviewContainer.classList.add("hidden");
    btnCopyText.classList.add("hidden");
    if (state.pollInterval) {
      clearInterval(state.pollInterval);
      state.pollInterval = null;
    }
  }

  // Start Conversion Request
  async function startConversion() {
    if (state.selectedFiles.length === 0) return;

    resetResultViews();
    btnStartConvert.disabled = true;
    progressCard.classList.remove("hidden");
    progressBarFill.style.width = "5%";
    progressPercentBadge.textContent = "5%";
    progressStatusText.textContent = "Mengirim berkas ke memori pemrosesan lokal...";

    const jobId = "job_" + Date.now();
    state.activeJobId = jobId;

    // Gather conversion options
    const payload = {
      job_id: jobId,
      mode: state.currentMode,
      files: state.selectedFiles,
      output_dir: state.outputDir,
      options: {
        ocr_mode: optAutoOcr.checked ? "auto" : "direct_only",
        bleach_watermark: optBleachWm.checked,
        watermark_threshold: parseInt(optWmThreshold.value, 10),
        unlock: optUnlock.checked,
        page_size: optPageSize.value,
      },
    };

    try {
      const resp = await fetch("/api/convert", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!resp.ok) {
        throw new Error("Gagal memulai proses konversi.");
      }

      // Start Polling for Progress
      pollJobProgress(jobId);
    } catch (err) {
      alert("Terjadi kesalahan saat memulai konversi: " + err.message);
      progressCard.classList.add("hidden");
      btnStartConvert.disabled = false;
    }
  }

  // Poll Job Progress
  function pollJobProgress(jobId) {
    state.pollInterval = setInterval(async () => {
      try {
        const resp = await fetch(`/api/progress?job_id=${jobId}`);
        if (!resp.ok) return;

        const data = await resp.json();
        const pct = Math.max(5, Math.min(100, data.percent || 0));
        progressBarFill.style.width = `${pct}%`;
        progressPercentBadge.textContent = `${pct}%`;
        if (data.status) {
          progressStatusText.textContent = data.status;
        }

        if (data.done) {
          clearInterval(state.pollInterval);
          state.pollInterval = null;

          if (data.error) {
            alert("Gagal melakukan konversi: " + data.error);
            progressCard.classList.add("hidden");
            btnStartConvert.disabled = false;
            return;
          }

          // Handle Success
          handleConversionSuccess(data.result);
        }
      } catch (e) {
        console.warn("Poll error:", e);
      }
    }, 350);
  }

  // Conversion Success Handler
  function handleConversionSuccess(result) {
    progressCard.classList.add("hidden");
    resultCard.classList.remove("hidden");
    state.lastResult = result;

    const outPath = result.output_path || "";
    resultFilePath.textContent = outPath;

    // Badges
    resModeBadge.textContent = result.mode || "Hybrid Layout";
    let metaText = result.pages ? `${result.pages} Halaman` : `${result.images_count || 1} Berkas`;
    if (result.images_embedded) {
      metaText += ` (${result.images_embedded} Gambar`;
      if (result.tables_embedded) {
        metaText += `, ${result.tables_embedded} Tabel`;
      }
      metaText += `)`;
    }
    resPagesBadge.textContent = metaText;

    // Handle Text Mode Preview & Copy
    if (state.currentMode === "pdf_to_text" && result.text) {
      textPreviewContainer.classList.remove("hidden");
      textPreviewBox.value = result.text;
      charCountLabel.textContent = `${result.char_count || result.text.length} Karakter`;
      btnCopyText.classList.remove("hidden");
    } else {
      textPreviewContainer.classList.add("hidden");
      btnCopyText.classList.add("hidden");
    }

    btnStartConvert.disabled = false;
    showToast("Konversi berhasil diselesaikan 100% lokal!");
  }

  // Toast Notification
  function showToast(message) {
    toastMsg.textContent = message;
    toast.classList.remove("hidden");
    setTimeout(() => {
      toast.classList.add("hidden");
    }, 2500);
  }

  // Native Open File via Windows API
  async function openConvertedFile() {
    if (!state.lastResult || !state.lastResult.output_path) return;
    try {
      const resp = await fetch("/api/open-file", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_path: state.lastResult.output_path }),
      });
      const data = await resp.json();
      if (!data.success) {
        alert("Tidak dapat membuka file langsung: " + (data.error || ""));
      }
    } catch (e) {
      alert("Gagal menghubungi server lokal: " + e.message);
    }
  }

  // Native Open Folder Explorer via Windows API
  async function openConvertedFolder() {
    if (!state.lastResult || !state.lastResult.output_path) return;
    try {
      await fetch("/api/open-folder", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_path: state.lastResult.output_path }),
      });
    } catch (e) {
      console.warn("Folder open failed:", e);
    }
  }

  // Copy Extracted Text
  function copyTextToClipboard() {
    if (!textPreviewBox.value) return;
    navigator.clipboard.writeText(textPreviewBox.value).then(() => {
      showToast("Teks berhasil disalin ke clipboard!");
    });
  }

  // Setup Event Listeners
  function setupEventListeners() {
    // Nav Tab Clicks
    tabButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const mode = btn.dataset.mode;
        if (mode && mode !== state.currentMode) {
          switchMode(mode);
        }
      });
    });

    // File Input change
    fileInput.addEventListener("change", (e) => {
      handleFilesSelected(e.target.files);
    });

    // Browse Button
    btnBrowse.addEventListener("click", () => {
      fileInput.click();
    });

    // Dropzone Click
    dropZone.addEventListener("click", (e) => {
      if (e.target !== btnBrowse && !btnBrowse.contains(e.target)) {
        fileInput.click();
      }
    });

    // Drag & Drop
    ["dragenter", "dragover"].forEach((eventName) => {
      dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add("drag-over");
      });
    });

    ["dragleave", "drop"].forEach((eventName) => {
      dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove("drag-over");
      });
    });

    dropZone.addEventListener("drop", (e) => {
      const dt = e.dataTransfer;
      if (dt && dt.files && dt.files.length > 0) {
        handleFilesSelected(dt.files);
      }
    });

    // Clear All Files
    btnClearFiles.addEventListener("click", () => {
      state.selectedFiles = [];
      renderFilesList();
      updateConvertButtonState();
    });

    // Bleach Watermark Toggle
    optBleachWm.addEventListener("change", () => {
      optThresholdRow.classList.toggle("hidden", !optBleachWm.checked);
    });

    // Threshold Slider
    optWmThreshold.addEventListener("input", (e) => {
      thresholdVal.textContent = e.target.value;
    });

    // Start Convert Button
    btnStartConvert.addEventListener("click", startConversion);

    // Result Action Buttons
    btnOpenFile.addEventListener("click", openConvertedFile);
    btnOpenFolder.addEventListener("click", openConvertedFolder);
    btnCopyText.addEventListener("click", copyTextToClipboard);
    btnConvertAnother.addEventListener("click", () => {
      state.selectedFiles = [];
      renderFilesList();
      resetResultViews();
      updateConvertButtonState();
    });
  }

  // Heartbeat loop (every 4 seconds) to keep server alive while window is open
  function startHeartbeat() {
    setInterval(() => {
      fetch("/api/heartbeat", { method: "POST" }).catch(() => {});
    }, 4000);
  }

  // Boot up
  document.addEventListener("DOMContentLoaded", init);
})();
