# 🎨 KDPEasy Cover Studio

A free VIP gift tool from KDPEasy Studio.

Turns your book idea into a print-ready KDP cover in two moves:
1. **Prompt Builder** — pick your book type, genre, style, mood → get
   a ready-to-paste prompt for ChatGPT Image / Midjourney / DALL-E.
2. **Cover Composer** — upload the resulting art, add title,
   subtitle & author with professional font pairings, download a
   300 DPI PNG with KDP bleed.

**Live app:** https://kdpeasy-cover-studio.streamlit.app

---

## 🇻🇳 Hướng dẫn deploy (dành cho anh chủ tool)

### Bước 1 — Tạo repo mới trên GitHub
1. Mở https://github.com/new
2. **Repository name:** `kdpeasy-cover-studio`
3. **Public** ✅
4. ✅ Tick "Add a README file"
5. Bấm **Create repository**

### Bước 2 — Upload 4 file vào repo
Trong repo vừa tạo, bấm **Add file → Upload files**, kéo cả 4 file
trong thư mục `C:\Users\Admin\Downloads\KDPEasy-Cover-Studio\`:

- `app.py`
- `requirements.txt`
- `runtime.txt`
- `README.md`

Bấm **Commit changes**.

### Bước 3 — Deploy lên Streamlit Cloud
1. Mở https://share.streamlit.io
2. Bấm **Create app → Deploy a public app from GitHub**
3. **Repository:** `daodinhthe1989-blip/kdpeasy-cover-studio`
4. **Branch:** `main`
5. **Main file path:** `app.py`
6. **App URL:** `kdpeasy-cover-studio`
7. Bấm **Deploy**

Đợi ~2 phút. Mật khẩu vào tool: **`KDPGIFT2026`**

> ⚠️ Lần đầu deploy sẽ mất thêm ~30 giây để tải font Google. Sau đó cache.

---

## 🇺🇸 How customers use it

### The workflow
Amazon buyers scroll past covers that look generic in 0.3 seconds.
Making a cover that stands out used to take design skills, Photoshop,
and hours in Canva. This tool turns it into two clicks.

### Step-by-step

**1. Go to the Prompt Builder tab.**
Pick:
- Book type (Picture book, Coloring book, Novel, Journal…)
- Genre (Fantasy, Bedtime, Adventure, SEL…)
- Illustration style (Watercolor, Vintage, Bold graphic…)
- Mood (Warm, Cool, Dramatic, Cozy…)
- Age group (3-5, 6-8, 9-12, Teen, Adult)
- Special elements to include

Copy the generated prompt.

**2. Paste it into ChatGPT Image** (or Midjourney / DALL-E / Leonardo).
Generate your art.

**3. Come back to the Cover Composer tab.**
Upload your art. Type your Title, Subtitle, and Author name.

**4. Choose your fonts.**
The tool includes 8 professionally paired font choices — Cinzel for
fairy tales, Fredoka for kids books, Caveat for handwritten journals,
Bangers for adventure, and more.

**5. Pick title position** (Top, Center, or Bottom).

**6. Auto-contrast picks the right text colour** based on your art —
white on dark scenes, dark on bright scenes.

**7. Download a 300 DPI PNG** with KDP bleed included, ready to
upload straight to Amazon KDP.

### Pro tips
- Peek at the **Template Gallery** tab first — 10 curated combos
  of position + font pairing for common genres
- The prompt tells ChatGPT / Midjourney *not* to include text in
  the art — because the tool adds professional text later
- Auto-contrast is on by default, but you can override with a
  custom colour if you want a specific brand tone
- 300 DPI + bleed enabled = uploads cleanly to KDP with zero
  formatting issues

---

## 🛠️ Tech stack
- **Streamlit** — UI
- **Pillow** — image compositing, text rendering
- **requests** — downloads 8 Google Fonts at first run
  (Cinzel, Fredoka, Cormorant, Quicksand, Caveat, Lora, Bangers,
  Merriweather — all OFL licence, free for commercial use)

No paid APIs. Runs free on Streamlit Cloud.

---

Made with ❤️ by **KDPEasy Studio** as a thank-you to our VIP list.
