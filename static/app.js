/**
 * app.js
 * Frontend controller for ConvertMyDocuments v1.1.2.
 * Zero-Leakage Offline Document & OCR Desktop Suite for Windows.
 * Supports Bilingual UI (English & Indonesian) with persistent session preferences.
 */

(function () {
  "use strict";

  // Bilingual Dictionary (English Default & Indonesian)
  const I18N = {
    en: {
      page_title: "ConvertMyDocuments v1.1.2 - Zero-Leakage Offline Document & OCR Suite",
      app_subtitle: "Zero-Leakage Local Document & OCR Suite",
      privacy_pill_tooltip: "All files processed 100% locally in your PC memory without internet.",
      privacy_pill_text: "100% Offline (Localhost)",

      // Nav Tabs
      tab_pdf_to_word: "1. PDF to Word",
      tab_pdf_to_text: "2. PDF to Text",
      tab_jpg_to_pdf: "3. JPG to PDF",
      tab_jpg_to_word: "4. JPG to Word (OCR)",

      // Mode Configs
      modes: {
        pdf_to_word: {
          title: "1. Convert PDF to Word Document (.docx)",
          desc: "Extract digital PDFs or scanned non-selectable pages with offline RapidOCR, watermark bleaching, and copy/print restriction unlocking.",
          btnText: "Start PDF to Word Conversion",
          acceptText: "Supports PDF files (No size limits, processed locally)",
        },
        pdf_to_text: {
          title: "2. Extract PDF to Plain Text (.txt)",
          desc: "Extract digital text instantly or run automated OCR for scanned PDFs. Text can be copied to clipboard with 1-click.",
          btnText: "Start Text Extraction from PDF",
          acceptText: "Supports PDF files (No size limits, processed locally)",
        },
        jpg_to_pdf: {
          title: "3. Merge Images / Photos to PDF (.pdf)",
          desc: "Combine single or multiple photos / document scans (JPG, PNG, WEBP, BMP, TIFF) into a single high-quality PDF document.",
          btnText: "Start Merging Images to PDF",
          acceptText: "Supports JPG, PNG, WEBP, BMP, TIFF (Multi-file batch merge)",
        },
        jpg_to_word: {
          title: "4. Extract Image / Photo Text to Word (.docx)",
          desc: "Extract text from images, receipts, document photos, or watermarked scans with RapidOCR and compile into editable Word format.",
          btnText: "Start Image OCR to Word",
          acceptText: "Supports JPG, PNG, WEBP, BMP, TIFF (Multi-file batch OCR)",
        },
      },

      // Dropzone & Selected Files
      dropzone_prompt: "Drag & Drop Files Here",
      btn_browse: "Choose Files from Computer",
      selected_files_title: "Selected Files",
      btn_clear_all: "Clear All",
      remove_file_title: "Remove this file",

      // Options Panel
      options_title: "Precision & Privacy Settings",
      options_tag: "Zero Cloud Leakage",
      opt_ocr_label: "Auto Scanned PDF Detection (RapidOCR)",
      opt_ocr_hint: "Recognize non-selectable text or scanned pages with offline AI OCR.",
      opt_wm_label: "Remove Watermarks & Transparent Stamps",
      opt_wm_hint: "Bleach background watermarks, stamps, or paper discoloration with OpenCV thresholding.",
      opt_threshold_label: "Bleach Threshold:",
      opt_threshold_hint: "Pixels brighter than this value are converted to clean pure white (#FFFFFF). Default: 185.",
      opt_unlock_label: "Unlock PDF Copy & Print Restrictions",
      opt_unlock_hint: "Automatically decrypts protected PDFs or permission locks without external password.",
      opt_pagesize_label: "PDF Page Layout Format",
      opt_pagesize_hint: "Choose page size ratio for the merged PDF document.",
      opt_pagesize_fit: "Original Image Size (Fit Resolution)",
      opt_pagesize_a4_p: "A4 Paper (Portrait)",
      opt_pagesize_a4_l: "A4 Paper (Landscape)",
      output_dir_label: "Output Destination Folder",
      output_dir_hint: "Converted documents will be saved directly on your computer.",

      // CTA Button
      btn_choose_first: "Choose File(s) First",
      files_suffix: "Files",
      file_suffix: "File",

      // Progress Card
      progress_title: "Converting Document Locally...",
      progress_status_sending: "Sending files to local processing memory...",
      progress_finished: "Conversion completed successfully!",

      // Result Card
      result_title: "Conversion Completed Successfully!",
      label_method: "Process Method",
      label_pages: "Pages / Files Count",
      label_security: "Data Security",
      security_value: "100% Offline (Localhost)",
      btn_open_file: "Open File Directly",
      btn_open_folder: "Show in Folder Explorer",
      btn_copy_text: "Copy Text to Clipboard",
      btn_convert_another: "Convert Another Document",
      text_preview_title: "Extracted Text Preview:",

      // Units & Plurals
      unit_page: "Page",
      unit_pages: "Pages",
      unit_files: "Files",
      unit_file: "File",
      unit_images: "Images",
      unit_image: "Image",
      unit_tables: "Tables",
      unit_table: "Table",
      unit_chars: "Characters",

      // Notifications
      toast_copied: "Text copied to clipboard!",
      toast_success: "Conversion completed 100% locally!",
      alert_open_fail: "Cannot open file directly: ",
      alert_server_fail: "Failed to connect to local server: ",
      alert_convert_fail: "Conversion failed: ",
      alert_start_fail: "Error occurred while starting conversion: ",

      // Settings & Updates
      settings_btn_title: "Settings & Updates",
      settings_modal_title: "Settings & Updates",
      setting_auto_update_label: "Automatic Updates from GitHub",
      setting_auto_update_hint: "Automatically check for newer releases and download the installer in background (Default ON).",
      setting_check_updates_btn: "Check for Updates Now",
      setting_checking: "Checking for updates...",
      setting_version_label: "Installed Version:",
      update_banner_available: "New Update Available:",
      update_banner_ready: "Update Ready to Install:",
      update_banner_downloading: "Downloading update from GitHub...",
      update_btn_update: "Update Now",
      update_btn_restart: "Restart & Install",
      update_toast_up_to_date: "ConvertMyDocuments is up to date (v1.1.2).",
      update_toast_installing: "Launching installer... ConvertMyDocuments will close.",
    },

    id: {
      page_title: "ConvertMyDocuments v1.1.2 - Suite Dokumen & OCR Offline Tanpa Bocor Data",
      app_subtitle: "Suite Dokumen & OCR Lokal Tanpa Bocor Data",
      privacy_pill_tooltip: "Semua berkas diproses 100% lokal di memori PC tanpa internet.",
      privacy_pill_text: "100% Offline (Localhost)",

      // Nav Tabs
      tab_pdf_to_word: "1. PDF ke Word",
      tab_pdf_to_text: "2. PDF ke Teks",
      tab_jpg_to_pdf: "3. JPG ke PDF",
      tab_jpg_to_word: "4. JPG ke Word (OCR)",

      // Mode Configs
      modes: {
        pdf_to_word: {
          title: "1. Konversi PDF ke Dokumen Word (.docx)",
          desc: "Mengekstrak PDF digital atau halaman scan non-selectable dengan RapidOCR offline, pemutihan watermark, dan pembukaan proteksi salin/cetak.",
          btnText: "Mulai Konversi PDF ke Word",
          acceptText: "Mendukung file PDF (Maks. bebas, diproses lokal)",
        },
        pdf_to_text: {
          title: "2. Ekstraksi PDF ke File Teks (.txt)",
          desc: "Mengekstrak teks digital secara langsung atau menjalankan OCR otomatis untuk scanned PDF. Teks dapat langsung disalin ke clipboard.",
          btnText: "Mulai Ekstraksi Teks dari PDF",
          acceptText: "Mendukung file PDF (Maks. bebas, diproses lokal)",
        },
        jpg_to_pdf: {
          title: "3. Gabungkan Gambar / Foto ke Dokumen PDF (.pdf)",
          desc: "Menyatukan satu atau banyak foto / scan dokumen (JPG, PNG, WEBP, BMP, TIFF) menjadi satu berkas PDF dengan kualitas tinggi.",
          btnText: "Mulai Gabungkan Gambar ke PDF",
          acceptText: "Mendukung JPG, PNG, WEBP, BMP, TIFF (Penggabungan multi-gambar)",
        },
        jpg_to_word: {
          title: "4. Ekstrak Teks Gambar / Foto ke Word (.docx)",
          desc: "Membaca teks dari gambar, kwitansi, foto dokumen atau buku ber-watermark menggunakan RapidOCR dan menyusunnya ke Word rapi.",
          btnText: "Mulai OCR Gambar ke Word",
          acceptText: "Mendukung JPG, PNG, WEBP, BMP, TIFF (Ekstraksi OCR multi-gambar)",
        },
      },

      // Dropzone & Selected Files
      dropzone_prompt: "Tarik & Lepaskan Berkas di Sini",
      btn_browse: "Pilih Berkas dari Komputer",
      selected_files_title: "Berkas Terpilih",
      btn_clear_all: "Hapus Semua",
      remove_file_title: "Hapus berkas ini",

      // Options Panel
      options_title: "Pengaturan Presisi & Privasi",
      options_tag: "Zero Cloud Leakage",
      opt_ocr_label: "Deteksi Scanned PDF Otomatis (RapidOCR)",
      opt_ocr_hint: "Mengenali teks gambar non-selectable atau halaman scan dengan AI OCR offline.",
      opt_wm_label: "Hapus Watermark & Cap Transparan",
      opt_wm_hint: "Memutihkan background cap air/stempel/diskolorasi kertas dengan OpenCV thresholding.",
      opt_threshold_label: "Ambang Batas Pemutihan (Threshold):",
      opt_threshold_hint: "Piksel lebih terang dari nilai ini diubah menjadi putih bersih (#FFFFFF). Standar: 185.",
      opt_unlock_label: "Buka Proteksi Salin & Cetak PDF",
      opt_unlock_hint: "Otomatis mendekripsi PDF terkunci atau pembatasan izin tanpa password eksternal.",
      opt_pagesize_label: "Format Tata Letak Halaman PDF",
      opt_pagesize_hint: "Pilih rasio ukuran halaman dokumen PDF hasil gabungan.",
      opt_pagesize_fit: "Ukuran Asli Gambar (Fit Resolution)",
      opt_pagesize_a4_p: "Kertas A4 Tegak (Portrait)",
      opt_pagesize_a4_l: "Kertas A4 Mendatar (Landscape)",
      output_dir_label: "Folder Penyimpanan Hasil",
      output_dir_hint: "Dokumen hasil konversi akan disimpan langsung di komputer Anda.",

      // CTA Button
      btn_choose_first: "Pilih Berkas Terlebih Dahulu",
      files_suffix: "Berkas",
      file_suffix: "Berkas",

      // Progress Card
      progress_title: "Sedang Mengonversi Dokumen Secara Lokal...",
      progress_status_sending: "Mengirim berkas ke memori pemrosesan lokal...",
      progress_finished: "Konversi selesai dengan sukses!",

      // Result Card
      result_title: "Konversi Berhasil Selesai!",
      label_method: "Metode Proses",
      label_pages: "Jumlah Halaman / Berkas",
      label_security: "Keamanan Data",
      security_value: "100% Offline (Localhost)",
      btn_open_file: "Buka File Langsung",
      btn_open_folder: "Tampilkan di Folder Explorer",
      btn_copy_text: "Salin Teks ke Clipboard",
      btn_convert_another: "Konversi Dokumen Lain",
      text_preview_title: "Pratinjau Teks yang Diekstrak:",

      // Units & Plurals
      unit_page: "Halaman",
      unit_pages: "Halaman",
      unit_files: "Berkas",
      unit_file: "Berkas",
      unit_images: "Gambar",
      unit_image: "Gambar",
      unit_tables: "Tabel",
      unit_table: "Tabel",
      unit_chars: "Karakter",

      // Notifications
      toast_copied: "Teks berhasil disalin ke clipboard!",
      toast_success: "Konversi berhasil diselesaikan 100% lokal!",
      alert_open_fail: "Tidak dapat membuka file langsung: ",
      alert_server_fail: "Gagal menghubungi server lokal: ",
      alert_convert_fail: "Gagal melakukan konversi: ",
      alert_start_fail: "Terjadi kesalahan saat memulai konversi: ",

      // Settings & Updates
      settings_btn_title: "Pengaturan & Pembaruan",
      settings_modal_title: "Pengaturan & Pembaruan",
      setting_auto_update_label: "Pembaruan Otomatis dari GitHub",
      setting_auto_update_hint: "Otomatis memeriksa rilis terbaru dan mengunduh installer di latar belakang (Default AKTIF).",
      setting_check_updates_btn: "Periksa Pembaruan Sekarang",
      setting_checking: "Memeriksa pembaruan...",
      setting_version_label: "Versi Terpasang:",
      update_banner_available: "Pembaruan Baru Tersedia:",
      update_banner_ready: "Pembaruan Siap Dipasang:",
      update_banner_downloading: "Mengunduh pembaruan dari GitHub...",
      update_btn_update: "Perbarui Sekarang",
      update_btn_restart: "Pasang & Mulai Ulang",
      update_toast_up_to_date: "ConvertMyDocuments sudah versi terbaru (v1.1.2).",
      update_toast_installing: "Menjalankan installer... ConvertMyDocuments akan ditutup.",
    },
  };

  // Base Mode Specifications (Non-localized specs)
  const MODE_SPECS = {
    pdf_to_word: {
      accept: ".pdf",
      multiple: false,
      showOcr: true,
      showUnlock: true,
      showPageSize: false,
    },
    pdf_to_text: {
      accept: ".pdf",
      multiple: false,
      showOcr: true,
      showUnlock: true,
      showPageSize: false,
    },
    jpg_to_pdf: {
      accept: ".jpg,.jpeg,.png,.webp,.bmp,.tiff",
      multiple: true,
      showOcr: false,
      showUnlock: false,
      showPageSize: true,
    },
    jpg_to_word: {
      accept: ".jpg,.jpeg,.png,.webp,.bmp,.tiff",
      multiple: true,
      showOcr: false,
      showUnlock: false,
      showPageSize: false,
    },
  };

  // Application State
  const state = {
    language: "en", // Default strictly English
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

  const langBtnEn = document.getElementById("langBtnEn");
  const langBtnId = document.getElementById("langBtnId");
  const privacyPill = document.getElementById("privacyPill");

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

  // Helper to get active dictionary
  function dict() {
    return I18N[state.language] || I18N.en;
  }

  // Switch Language & Persist across sessions
  function setLanguage(lang, persist = true) {
    if (lang !== "en" && lang !== "id") {
      lang = "en";
    }
    state.language = lang;

    // Update Language Toggle Buttons
    if (langBtnEn && langBtnId) {
      langBtnEn.classList.toggle("active", lang === "en");
      langBtnId.classList.toggle("active", lang === "id");
    }

    // Update document metadata
    document.documentElement.lang = lang;
    const currentDict = dict();
    document.title = currentDict.page_title;
    if (privacyPill) {
      privacyPill.title = currentDict.privacy_pill_tooltip;
    }

    // Update all elements with data-i18n
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.dataset.i18n;
      if (currentDict[key]) {
        el.textContent = currentDict[key];
      }
    });

    // Update mode banner & inputs
    updateModeBanner();
    updateConvertButtonState();

    // Update Settings Modal elements if present
    const settingsModalTitle = document.getElementById("settingsModalTitle");
    if (settingsModalTitle) settingsModalTitle.textContent = currentDict.settings_modal_title;
    const lblAutoUpdateSetting = document.getElementById("lblAutoUpdateSetting");
    if (lblAutoUpdateSetting) lblAutoUpdateSetting.textContent = currentDict.setting_auto_update_label;
    const hintAutoUpdateSetting = document.getElementById("hintAutoUpdateSetting");
    if (hintAutoUpdateSetting) hintAutoUpdateSetting.textContent = currentDict.setting_auto_update_hint;
    const lblInstalledVersion = document.getElementById("lblInstalledVersion");
    if (lblInstalledVersion) lblInstalledVersion.textContent = currentDict.setting_version_label;
    const txtCheckUpdateModal = document.getElementById("txtCheckUpdateModal");
    if (txtCheckUpdateModal) txtCheckUpdateModal.textContent = currentDict.setting_check_updates_btn;
    const btnOpenSettings = document.getElementById("btnOpenSettings");
    if (btnOpenSettings) btnOpenSettings.title = currentDict.settings_btn_title;

    // Re-render result badge if currently visible
    if (state.lastResult) {
      renderResultBadges(state.lastResult);
    }

    // Persist Language Settings
    if (persist) {
      try {
        localStorage.setItem("cmd_language", lang);
      } catch (e) {
        console.warn("Could not save to localStorage:", e);
      }
      fetch("/api/settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ language: lang }),
      }).catch((e) => console.warn("Could not persist language to server:", e));
    }
  }

  // Load Initial Settings & Language (localStorage -> /api/settings -> default "en")
  async function loadInitialSettings() {
    let savedLang = null;
    try {
      savedLang = localStorage.getItem("cmd_language");
    } catch (e) {
      savedLang = null;
    }

    try {
      const res = await fetch("/api/settings");
      if (res.ok) {
        const data = await res.json();
        if (!savedLang && (data.language === "en" || data.language === "id")) {
          savedLang = data.language;
        }
        if (data.auto_update !== undefined) {
          const chk = document.getElementById("chkAutoUpdate");
          if (chk) chk.checked = Boolean(data.auto_update);
        }
      }
    } catch (e) {
      // server offline or request failed
    }

    setLanguage(savedLang || "en", false);
  }

  // ==============================================================================
  // SETTINGS & AUTO-UPDATE ENGINE (ConvertMyDocuments)
  // ==============================================================================
  let currentUpdateData = null;
  let updatePollTimer = null;

  const btnOpenSettings = document.getElementById("btnOpenSettings");
  const btnCloseSettings = document.getElementById("btnCloseSettings");
  const settingsModal = document.getElementById("settingsModal");
  const chkAutoUpdate = document.getElementById("chkAutoUpdate");
  const btnCheckUpdateModal = document.getElementById("btnCheckUpdateModal");
  const versionStatusText = document.getElementById("versionStatusText");
  const settingsUpdateDot = document.getElementById("settingsUpdateDot");

  const updateBanner = document.getElementById("updateBanner");
  const updateBannerTitle = document.getElementById("updateBannerTitle");
  const updateBannerVersion = document.getElementById("updateBannerVersion");
  const updateBannerDesc = document.getElementById("updateBannerDesc");
  const updateMiniProgress = document.getElementById("updateMiniProgress");
  const updateMiniBar = document.getElementById("updateMiniBar");
  const updateMiniPct = document.getElementById("updateMiniPct");
  const btnUpdateAction = document.getElementById("btnUpdateAction");
  const txtUpdateAction = document.getElementById("txtUpdateAction");
  const btnDismissUpdate = document.getElementById("btnDismissUpdate");

  function openSettingsModal() {
    if (settingsModal) settingsModal.classList.remove("hidden");
  }

  function closeSettingsModal() {
    if (settingsModal) settingsModal.classList.add("hidden");
  }

  function toggleAutoUpdate(enable) {
    fetch("/api/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ auto_update: enable }),
    }).catch(() => {});
  }

  async function checkUpdates(manual = false) {
    const currentDict = dict();
    const txtModal = document.getElementById("txtCheckUpdateModal");
    const checkIcon = btnCheckUpdateModal ? btnCheckUpdateModal.querySelector(".check-icon") : null;

    if (checkIcon) checkIcon.classList.add("animate-spin");
    if (txtModal && manual) txtModal.textContent = currentDict.setting_checking;

    try {
      const res = await fetch("/api/update/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ force: manual }),
      });
      const data = await res.json();

      if (checkIcon) checkIcon.classList.remove("animate-spin");
      if (txtModal) txtModal.textContent = currentDict.setting_check_updates_btn;

      if (data.status === "available" || data.update_available) {
        currentUpdateData = data;
        renderUpdateNotification(data);
        if (versionStatusText) {
          versionStatusText.textContent = `${currentDict.update_banner_available} v${data.latest_version}`;
          versionStatusText.style.color = "var(--emerald-400)";
        }
        if (settingsUpdateDot) settingsUpdateDot.classList.remove("hidden");
      } else if (data.status === "ready_to_install") {
        currentUpdateData = data;
        renderUpdateNotification(data);
        if (versionStatusText) {
          versionStatusText.textContent = `${currentDict.update_banner_ready} v${data.latest_version}`;
          versionStatusText.style.color = "var(--emerald-400)";
        }
      } else if (data.status === "up_to_date") {
        if (settingsUpdateDot) settingsUpdateDot.classList.add("hidden");
        if (versionStatusText) {
          versionStatusText.textContent = currentDict.update_toast_up_to_date;
          versionStatusText.style.color = "var(--text-muted)";
        }
        if (manual) {
          showToast(currentDict.update_toast_up_to_date);
        }
      } else if (data.status === "error" && manual) {
        showToast(data.error || "Failed to check updates.");
      }
    } catch (err) {
      if (checkIcon) checkIcon.classList.remove("animate-spin");
      if (txtModal) txtModal.textContent = currentDict.setting_check_updates_btn;
      if (manual) showToast("Network error while checking updates.");
    }
  }

  function renderUpdateNotification(data) {
    if (!updateBanner) return;
    const currentDict = dict();
    const newVer = data.latest_version || "New";

    if (updateBannerVersion) updateBannerVersion.textContent = `v${newVer}`;

    if (data.status === "ready_to_install" || data.installer_ready) {
      if (updateBannerTitle) updateBannerTitle.textContent = currentDict.update_banner_ready;
      if (updateBannerDesc) updateBannerDesc.textContent = state.language === "en" ? "Installer downloaded. Restart to apply." : "Installer terunduh. Mulai ulang untuk memasang.";
      if (txtUpdateAction) txtUpdateAction.textContent = currentDict.update_btn_restart;
      if (updateMiniProgress) updateMiniProgress.classList.add("hidden");
      if (btnUpdateAction) {
        btnUpdateAction.classList.remove("hidden");
        btnUpdateAction.disabled = false;
      }
    } else if (data.status === "downloading") {
      if (updateBannerTitle) updateBannerTitle.textContent = currentDict.update_banner_downloading;
      if (updateBannerDesc) updateBannerDesc.textContent = `${data.progress || 0}%`;
      if (updateMiniProgress) updateMiniProgress.classList.remove("hidden");
      if (updateMiniBar) updateMiniBar.style.setProperty("--progress", `${data.progress || 0}%`);
      if (updateMiniPct) updateMiniPct.textContent = `${data.progress || 0}%`;
      if (btnUpdateAction) btnUpdateAction.classList.add("hidden");
    } else {
      // available
      if (updateBannerTitle) updateBannerTitle.textContent = currentDict.update_banner_available;
      if (updateBannerDesc) updateBannerDesc.textContent = state.language === "en" ? "New release ready on GitHub." : "Rilis baru tersedia di GitHub.";
      if (txtUpdateAction) txtUpdateAction.textContent = currentDict.update_btn_update;
      if (updateMiniProgress) updateMiniProgress.classList.add("hidden");
      if (btnUpdateAction) {
        btnUpdateAction.classList.remove("hidden");
        btnUpdateAction.disabled = false;
      }
    }

    updateBanner.classList.remove("hidden");
  }

  async function handleUpdate() {
    const currentDict = dict();
    if (!currentUpdateData) return;

    if (currentUpdateData.status === "ready_to_install" || currentUpdateData.installer_ready) {
      if (btnUpdateAction) btnUpdateAction.disabled = true;
      if (txtUpdateAction) txtUpdateAction.textContent = currentDict.update_toast_installing;
      try {
        await fetch("/api/update/apply", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ silent: false }),
        });
        showToast(currentDict.update_toast_installing);
      } catch (e) {
        showToast("Failed to apply update: " + e);
      }
      return;
    }

    // Trigger download
    if (btnUpdateAction) btnUpdateAction.disabled = true;
    if (txtUpdateAction) txtUpdateAction.textContent = currentDict.update_banner_downloading;
    try {
      const res = await fetch("/api/update/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      const data = await res.json();
      currentUpdateData = data;
      renderUpdateNotification(data);
      pollUpdateProgress();
    } catch (e) {
      showToast("Download failed: " + e);
    }
  }

  function pollUpdateProgress() {
    if (updatePollTimer) clearInterval(updatePollTimer);
    updatePollTimer = setInterval(async () => {
      try {
        const res = await fetch("/api/update/status");
        const data = await res.json();
        currentUpdateData = data;
        renderUpdateNotification(data);
        if (data.status === "ready_to_install" || data.installer_ready || data.status === "error") {
          clearInterval(updatePollTimer);
          updatePollTimer = null;
        }
      } catch (e) {
        clearInterval(updatePollTimer);
        updatePollTimer = null;
      }
    }, 800);
  }

  // Initialize Application
  async function init() {
    setupEventListeners();
    await loadInitialSettings();
    fetchSystemStatus();
    switchMode("pdf_to_word");
    startHeartbeat();

    // Auto-update check status polling after 2.5 seconds
    setTimeout(() => {
      fetch("/api/update/status")
        .then((r) => r.json())
        .then((data) => {
          if (data.update_available || data.status === "ready_to_install" || data.status === "downloading") {
            currentUpdateData = data;
            renderUpdateNotification(data);
            if (data.status === "downloading") {
              pollUpdateProgress();
            }
          }
        })
        .catch(() => {});
    }, 2500);
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
        // If localStorage had nothing, check if server has saved language
        const localSaved = localStorage.getItem("cmd_language");
        if (!localSaved && data.language && (data.language === "en" || data.language === "id")) {
          setLanguage(data.language, false);
        }
      }
    } catch (e) {
      console.warn("Status fetch failed:", e);
    }
  }

  // Update Mode Banner texts based on active mode & language
  function updateModeBanner() {
    const currentDict = dict();
    const modeInfo = currentDict.modes[state.currentMode];
    const spec = MODE_SPECS[state.currentMode];
    if (!modeInfo || !spec) return;

    bannerTitle.textContent = modeInfo.title;
    bannerDesc.textContent = modeInfo.desc;
    dropzoneAcceptText.textContent = modeInfo.acceptText;
  }

  // Switch Active Mode
  function switchMode(modeKey) {
    state.currentMode = modeKey;
    const spec = MODE_SPECS[modeKey];
    if (!spec) return;

    // Update Nav Tab Active States
    tabButtons.forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.mode === modeKey);
    });

    // Update Mode Banner & Text
    updateModeBanner();

    // Update File Input Constraints
    fileInput.accept = spec.accept;
    fileInput.multiple = spec.multiple;

    // Toggle Specific Option Visibility
    optOcrContainer.classList.toggle("hidden", !spec.showOcr);
    optUnlockContainer.classList.toggle("hidden", !spec.showUnlock);
    optPageSizeContainer.classList.toggle("hidden", !spec.showPageSize);

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
    const spec = MODE_SPECS[state.currentMode];

    const newFiles = Array.from(fileList);
    const filesToLoad = spec.multiple ? newFiles : [newFiles[0]];

    for (const file of filesToLoad) {
      try {
        const dataUrl = await readFileAsDataUrl(file);
        // Avoid duplicate by name & size
        const exists = state.selectedFiles.some(
          (f) => f.name === file.name && f.size === file.size
        );
        if (!exists) {
          if (!spec.multiple) {
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

    const currentDict = dict();
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
        <button type="button" class="btn-remove-file" data-index="${index}" title="${currentDict.remove_file_title}">
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
    const currentDict = dict();
    const modeInfo = currentDict.modes[state.currentMode];
    if (!modeInfo) return;

    if (state.selectedFiles.length === 0) {
      btnStartConvert.disabled = true;
      btnConvertText.textContent = currentDict.btn_choose_first;
    } else {
      btnStartConvert.disabled = false;
      const count = state.selectedFiles.length;
      if (count === 1) {
        btnConvertText.textContent = modeInfo.btnText;
      } else {
        const suffix = count > 1 ? currentDict.files_suffix : currentDict.file_suffix;
        btnConvertText.textContent = `${modeInfo.btnText} (${count} ${suffix})`;
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

    const currentDict = dict();
    resetResultViews();
    btnStartConvert.disabled = true;
    progressCard.classList.remove("hidden");
    progressBarFill.style.width = "5%";
    progressPercentBadge.textContent = "5%";
    progressStatusText.textContent = currentDict.progress_status_sending;

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
        throw new Error("Local conversion request failed to start.");
      }

      // Start Polling for Progress
      pollJobProgress(jobId);
    } catch (err) {
      alert(currentDict.alert_start_fail + err.message);
      progressCard.classList.add("hidden");
      btnStartConvert.disabled = false;
    }
  }

  // Poll Job Progress
  function pollJobProgress(jobId) {
    const currentDict = dict();
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
            alert(currentDict.alert_convert_fail + data.error);
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

  // Render Badges in Result View
  function renderResultBadges(result) {
    const currentDict = dict();
    resModeBadge.textContent = result.mode || "Hybrid Layout";

    let metaText = "";
    if (result.pages) {
      const pageUnit = result.pages > 1 ? currentDict.unit_pages : currentDict.unit_page;
      metaText = `${result.pages} ${pageUnit}`;
    } else {
      const count = result.images_count || 1;
      const fileUnit = count > 1 ? currentDict.unit_files : currentDict.unit_file;
      metaText = `${count} ${fileUnit}`;
    }

    if (result.images_embedded) {
      const imgUnit = result.images_embedded > 1 ? currentDict.unit_images : currentDict.unit_image;
      metaText += ` (${result.images_embedded} ${imgUnit}`;
      if (result.tables_embedded) {
        const tblUnit = result.tables_embedded > 1 ? currentDict.unit_tables : currentDict.unit_table;
        metaText += `, ${result.tables_embedded} ${tblUnit}`;
      }
      metaText += `)`;
    }
    resPagesBadge.textContent = metaText;
  }

  // Conversion Success Handler
  function handleConversionSuccess(result) {
    const currentDict = dict();
    progressCard.classList.add("hidden");
    resultCard.classList.remove("hidden");
    state.lastResult = result;

    const outPath = result.output_path || "";
    resultFilePath.textContent = outPath;

    renderResultBadges(result);

    // Handle Text Mode Preview & Copy
    if (state.currentMode === "pdf_to_text" && result.text) {
      textPreviewContainer.classList.remove("hidden");
      textPreviewBox.value = result.text;
      const count = result.char_count || result.text.length;
      charCountLabel.textContent = `${count} ${currentDict.unit_chars}`;
      btnCopyText.classList.remove("hidden");
    } else {
      textPreviewContainer.classList.add("hidden");
      btnCopyText.classList.add("hidden");
    }

    btnStartConvert.disabled = false;
    showToast(currentDict.toast_success);
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
    const currentDict = dict();
    if (!state.lastResult || !state.lastResult.output_path) return;
    try {
      const resp = await fetch("/api/open-file", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_path: state.lastResult.output_path }),
      });
      const data = await resp.json();
      if (!data.success) {
        alert(currentDict.alert_open_fail + (data.error || ""));
      }
    } catch (e) {
      alert(currentDict.alert_server_fail + e.message);
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
    const currentDict = dict();
    if (!textPreviewBox.value) return;
    navigator.clipboard.writeText(textPreviewBox.value).then(() => {
      showToast(currentDict.toast_copied);
    });
  }

  // Setup Event Listeners
  function setupEventListeners() {
    // Language Switch Buttons
    if (langBtnEn) {
      langBtnEn.addEventListener("click", () => setLanguage("en", true));
    }
    if (langBtnId) {
      langBtnId.addEventListener("click", () => setLanguage("id", true));
    }

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

    // Settings & Updates Modal and Buttons
    if (btnOpenSettings) {
      btnOpenSettings.addEventListener("click", openSettingsModal);
    }
    if (btnCloseSettings) {
      btnCloseSettings.addEventListener("click", closeSettingsModal);
    }
    if (settingsModal) {
      settingsModal.addEventListener("click", (e) => {
        if (e.target === settingsModal) closeSettingsModal();
      });
    }
    if (chkAutoUpdate) {
      chkAutoUpdate.addEventListener("change", (e) => {
        toggleAutoUpdate(e.target.checked);
      });
    }
    if (btnCheckUpdateModal) {
      btnCheckUpdateModal.addEventListener("click", () => checkUpdates(true));
    }
    if (btnUpdateAction) {
      btnUpdateAction.addEventListener("click", handleUpdate);
    }
    if (btnDismissUpdate) {
      btnDismissUpdate.addEventListener("click", () => {
        if (updateBanner) updateBanner.classList.add("hidden");
      });
    }
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
