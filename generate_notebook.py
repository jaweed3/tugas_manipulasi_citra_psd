import json

cells = []

def md(source):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [source]
    })

def code(source):
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "source": [source],
        "outputs": [],
        "execution_count": None
    })

# ============================================================
# TITLE
# ============================================================
md("""# Manipulasi Citra Digital dengan OpenCV

**Mata Kuliah:** Pengolahan Sinyal Digital
**Nama:** [Nama Mahasiswa]
**NIM:** [NIM]

""")

# ============================================================
# IMPORTS
# ============================================================
md("""## Persiapan Library""")

code("""import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

print(f"OpenCV version: {cv.__version__}")
print(f"NumPy version: {np.__version__}")""")

# ============================================================
# BAGIAN A: MEMBACA DAN MENAMPILKAN CITRA
# ============================================================
md("""---
# Bagian A: Membaca dan Menampilkan Citra""")

md("""### A.1 Membaca Citra
Saya menggunakan dua citra dari internet dengan ukuran dan konten berbeda.""")
code("""img1 = cv.imread('../images/image1.jpg')
img2 = cv.imread('../images/image2.jpg')

if img1 is None:
    raise FileNotFoundError("image1.jpg tidak ditemukan")
if img2 is None:
    raise FileNotFoundError("image2.jpg tidak ditemukan")

print(f"img1 shape: {img1.shape}, dtype: {img1.dtype}")
print(f"img2 shape: {img2.shape}, dtype: {img2.dtype}")
print(f"img1 min: {img1.min()}, max: {img1.max()}")
print(f"img2 min: {img2.min()}, max: {img2.max()}")""")

md("""### A.2 Konversi BGR ke RGB
OpenCV membaca gambar dalam format BGR, sedangkan Matplotlib menggunakan RGB. Jika langsung ditampilkan tanpa konversi, warnanya akan salah.""")
code("""img1_rgb = cv.cvtColor(img1, cv.COLOR_BGR2RGB)
img2_rgb = cv.cvtColor(img2, cv.COLOR_BGR2RGB)

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

axes[0, 0].imshow(cv.cvtColor(img1, cv.COLOR_BGR2RGB))
axes[0, 0].set_title("img1 (dibaca cv.imread, dikonversi ke RGB)")
axes[0, 0].axis("off")

axes[0, 1].imshow(img1)
axes[0, 1].set_title("img1 (langsung dari OpenCV, BGR)")
axes[0, 1].axis("off")

axes[1, 0].imshow(cv.cvtColor(img2, cv.COLOR_BGR2RGB))
axes[1, 0].set_title("img2 (dibaca cv.imread, dikonversi ke RGB)")
axes[1, 0].axis("off")

axes[1, 1].imshow(img2)
axes[1, 1].set_title("img2 (langsung dari OpenCV, BGR)")
axes[1, 1].axis("off")

plt.suptitle("Perbandingan BGR vs RGB", fontsize=14)
plt.tight_layout()
plt.show()""")

md("""**Analisis Bagian A:**

1. **Mengapa warna terlihat tidak sesuai jika langsung ditampilkan?**
   OpenCV membaca gambar dalam format BGR (Blue-Green-Red), sedangkan Matplotlib mengharapkan format RGB (Red-Green-Blue). Channel biru dan merah tertukar, sehingga warna tampak kebiruan atau tidak natural.

2. **Perbedaan BGR dan RGB?**
   BGR dan RGB sama-sama menggunakan tiga channel warna, tapi urutannya berbeda. BGR digunakan oleh OpenCV secara default, RGB digunakan oleh sebagian besar library lain (Matplotlib, PIL).

3. **Mengapa penting memahami format warna?**
   Kalau tidak paham format warna, hasil manipulasi dan visualisasi bisa salah. Misal kita pikir sudah memanipulasi channel merah tapi ternyata yang berubah adalah channel biru.""")

# ============================================================
# BAGIAN B: RESIZE CITRA
# ============================================================
md("""---
# Bagian B: Resize Citra""")

md("""### B.1 Resize Dua Citra
Agar bisa di-blend, kedua citra harus punya ukuran yang identik. Saya resize ke (600, 400) untuk semua.""")
code("""target_size = (600, 400)

img1_resize = cv.resize(img1_rgb, target_size)
img2_resize = cv.resize(img2_rgb, target_size)

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

axes[0, 0].imshow(img1_rgb)
axes[0, 0].set_title(f"img1 sebelum resize: {img1_rgb.shape[:2]}")
axes[0, 0].axis("off")

axes[0, 1].imshow(img1_resize)
axes[0, 1].set_title(f"img1 setelah resize: {img1_resize.shape[:2]}")
axes[0, 1].axis("off")

axes[1, 0].imshow(img2_rgb)
axes[1, 0].set_title(f"img2 sebelum resize: {img2_rgb.shape[:2]}")
axes[1, 0].axis("off")

axes[1, 1].imshow(img2_resize)
axes[1, 1].set_title(f"img2 setelah resize: {img2_resize.shape[:2]}")
axes[1, 1].axis("off")

plt.tight_layout()
plt.show()""")

md("""**Analisis Bagian B:**

1. **Mengapa harus sama ukurannya?**
   Image blending dilakukan per-pixel. Operasi `α * I1 + β * I2` hanya bisa kalau matriks kedua citra punya dimensi yang sama persis.

2. **Risiko resize terhadap kualitas?**
   Resize memperbesar atau memperkecil bisa menyebabkan informasi hilang (downscale) atau gambar jadi blur (upscale). Interpolasi yang digunakan juga berpengaruh.

3. **Resize mengubah proporsi?**
   Iya, kalau aspek ratio tidak dipertahankan. Di sini saya paksa ke (600, 400) tanpa menjaga rasio asli, jadi objek bisa terlihat memanjang atau melebar.""")

# ============================================================
# BAGIAN C: IMAGE BLENDING
# ============================================================
md("""---
# Bagian C: Image Blending""")

md("""### C.1 Melakukan Image Blending
Formula: `I_blend = α * I1 + β * I2`, dengan `α + β = 1`.""")
code("""alphas = [0.2, 0.5, 0.8]
betas = [0.8, 0.5, 0.2]

fig, axes = plt.subplots(2, 3, figsize=(15, 8))

# baris 1: citra asli
axes[0, 0].imshow(img1_resize)
axes[0, 0].set_title("Citra 1")
axes[0, 0].axis("off")

axes[0, 1].imshow(img2_resize)
axes[0, 1].set_title("Citra 2")
axes[0, 1].axis("off")

axes[0, 2].axis("off")  # kosong

# baris 2: hasil blending
for i, (a, b) in enumerate(zip(alphas, betas)):
    blend = cv.addWeighted(img1_resize, a, img2_resize, b, 0)
    axes[1, i].imshow(blend)
    axes[1, i].set_title(f"Blend: α={a}, β={b}")
    axes[1, i].axis("off")

plt.suptitle("Image Blending dengan Berbagai Bobot", fontsize=14)
plt.tight_layout()
plt.show()""")

md("""### C.2 Tabel Perbandingan Hasil Blending

| α | β | Analisis Hasil |
|---|---|----------------|
| 0.2 | 0.8 | Citra 2 lebih dominan. Detail dari citra 1 masih terlihat samar di beberapa area. Warna lebih condong ke citra 2. |
| 0.5 | 0.5 | Kedua citra tercampur seimbang. Tidak ada yang dominan, hasilnya seperti overlay transparan 50:50. |
| 0.8 | 0.2 | Citra 1 lebih dominan. Citra 2 hanya terlihat seperti lapisan tipis di atasnya. Kontras lebih mirip citra 1. |

**Analisis Bagian C:**

1. **Pengaruh α dan β?** α mengontrol kontribusi citra 1, β untuk citra 2. Semakin besar α, semakin terlihat citra 1. Jumlahnya harus 1 agar intensitas rata-rata tetap dalam rentang [0, 255].

2. **Citra dominan saat α besar?** Citra 1 lebih dominan karena bobotnya lebih besar.

3. **Kalau α + β > 1?** Intensitas pixel bisa overflow > 255, menyebabkan clipping atau saturasi pada pixel terang.

4. **Aplikasi nyata?** Transisi antar scene di video (crossfade), watermark transparan, efek superimpose.""")

# ============================================================
# BAGIAN D: IMAGE NEGATIVE
# ============================================================
md("""---
# Bagian D: Image Negative""")

md("""### D.1 Membuat Citra Negatif
Formula: `I_negatif = 255 - I`""")
code("""img_negative = 255 - img1_resize

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].imshow(img1_resize)
axes[0, 0].set_title("Citra Asli")
axes[0, 0].axis("off")

axes[0, 1].imshow(img_negative)
axes[0, 1].set_title("Citra Negatif")
axes[0, 1].axis("off")

# histogram
colors = ['r', 'g', 'b']
for i, color in enumerate(colors):
    hist_orig, _ = np.histogram(img1_resize[:,:,i], bins=256, range=(0,256))
    axes[1, 0].plot(hist_orig, color=color, alpha=0.7)
    hist_neg, _ = np.histogram(img_negative[:,:,i], bins=256, range=(0,256))
    axes[1, 1].plot(hist_neg, color=color, alpha=0.7)

axes[1, 0].set_title("Histogram Citra Asli")
axes[1, 0].set_xlabel("Intensitas Pixel")
axes[1, 0].set_ylabel("Frekuensi")

axes[1, 1].set_title("Histogram Citra Negatif")
axes[1, 1].set_xlabel("Intensitas Pixel")
axes[1, 1].set_ylabel("Frekuensi")

plt.tight_layout()
plt.show()""")

md("""**Analisis Bagian D:**

1. **Pixel terang setelah negatif?** Menjadi gelap. Misal pixel 200 jadi 55.

2. **Pixel gelap setelah negatif?** Menjadi terang. Misal pixel 30 jadi 225.

3. **Perubahan histogram?** Histogram tercermin (mirror) secara horizontal. Puncak yang tadinya di kanan (terang) pindah ke kiri (gelap) dan sebaliknya.

4. **Kapan image negative berguna?** Analisis citra medis (sinar-X), deteksi tepi, kadang untuk visualisasi pola yang sulit dilihat di citra asli.""")

# ============================================================
# BAGIAN E: TRANSFORMASI LOGARITMIK
# ============================================================
md("""---
# Bagian E: Transformasi Logaritmik""")

md("""### E.1 Menerapkan Transformasi Logaritmik
Formula: `s = c * log(1 + r)`, dengan `c = 255 / log(1 + r_max)`""")
code("""c = 255.0 / np.log10(1 + float(np.max(img1_resize)))
print(f"Konstanta skala (c): {c:.4f}")

img_log = c * np.log10(img1_resize.astype(np.float64) + 1)
img_log = np.clip(img_log, 0, 255).astype(np.uint8)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].imshow(img1_resize)
axes[0, 0].set_title("Citra Asli")
axes[0, 0].axis("off")

axes[0, 1].imshow(img_log)
axes[0, 1].set_title("Hasil Transformasi Logaritmik")
axes[0, 1].axis("off")

colors = ['r', 'g', 'b']
for i, color in enumerate(colors):
    hist_orig, _ = np.histogram(img1_resize[:,:,i], bins=256, range=(0,256))
    axes[1, 0].plot(hist_orig, color=color, alpha=0.7)
    hist_log, _ = np.histogram(img_log[:,:,i], bins=256, range=(0,256))
    axes[1, 1].plot(hist_log, color=color, alpha=0.7)

axes[1, 0].set_title("Histogram Citra Asli")
axes[1, 0].set_xlabel("Intensitas Pixel")
axes[1, 1].set_title("Histogram Citra Logaritmik")
axes[1, 1].set_xlabel("Intensitas Pixel")

plt.tight_layout()
plt.show()

print(f"\\nPerbandingan nilai pixel:")
print(f"  Asli  - min: {img1_resize.min()}, max: {img1_resize.max()}")
print(f"  Log   - min: {img_log.min()}, max: {img_log.max()}")""")

md("""**Analisis Bagian E:**

1. **Efek pada area gelap?** Area gelap ditingkatkan kontrasnya secara signifikan. Fungsi log punya slope curam di nilai rendah, jadi perubahan kecil di area gelap menghasilkan perubahan besar.

2. **Efek pada area terang?** Area terang kompresi, detailnya berkurang karena slope log melandai di nilai tinggi.

3. **Mengapa digunakan untuk area gelap?** Karena distribusi pixel gelap diregangkan (stretched), detail yang tadinya hampir tidak terlihat jadi lebih jelas.

4. **Risiko pada citra terang?** Kalau citra sudah terang, transformasi log justru bisa menghilangkan detail di area terang karena kompresi, dan gambar jadi flat.""")

# ============================================================
# BAGIAN F: TRANSFORMASI GAMMA
# ============================================================
md("""---
# Bagian F: Transformasi Gamma""")

md("""### F.1 Menerapkan Transformasi Gamma
Normalisasi dulu ke [0,1], lalu `s = r^γ`, kemudian dikembalikan ke [0,255].""")
code("""gamma_values = [0.5, 1.0, 2.0, 2.5]

img_normalized = img1_resize.astype(np.float64) / 255.0

fig, axes = plt.subplots(2, 4, figsize=(18, 8))

# baris 1: citra hasil gamma
for i, g in enumerate(gamma_values):
    img_gamma = (img_normalized ** g) * 255.0
    img_gamma = np.clip(img_gamma, 0, 255).astype(np.uint8)
    axes[0, i].imshow(img_gamma)
    axes[0, i].set_title(f"γ = {g}")
    axes[0, i].axis("off")

# baris 2: histogram
colors = ['r', 'g', 'b']
for i, g in enumerate(gamma_values):
    img_gamma = (img_normalized ** g) * 255.0
    img_gamma = np.clip(img_gamma, 0, 255).astype(np.uint8)
    for ch, color in enumerate(colors):
        hist, _ = np.histogram(img_gamma[:,:,ch], bins=256, range=(0,256))
        axes[1, i].plot(hist, color=color, alpha=0.7)
    axes[1, i].set_title(f"Histogram γ = {g}")
    axes[1, i].set_xlabel("Intensitas")

plt.suptitle("Transformasi Gamma dengan Berbagai Nilai γ", fontsize=14)
plt.tight_layout()
plt.show()""")

md("""### F.2 Tabel Perbandingan Efek Nilai γ

| Nilai γ | Efek terhadap Citra |
|---------|---------------------|
| 0.5 | Citra jadi lebih terang secara keseluruhan. Kontras area gelap meningkat, detail di bayangan lebih terlihat. Seperti koreksi underexposure. |
| 1.0 | Tidak ada perubahan (identik dengan citra asli). γ=1 menghasilkan transformasi identitas. |
| 2.0 | Citra jadi lebih gelap. Area terang mulai terkompresi, kontras berkurang. Efek seperti overexposure. |
| 2.5 | Citra jauh lebih gelap. Banyak detail hilang di area gelap karena pixel terkompresi ke nilai rendah. Hanya area paling terang yang masih terlihat. |

**Analisis Bagian F:**

1. **γ < 1?** Pixel nilai rendah (gelap) dinaikkan lebih banyak, sehingga citra terlihat lebih terang dengan detail bayangan lebih jelas.

2. **γ = 1?** Output = input, tidak ada perubahan.

3. **γ > 1?** Pixel nilai tinggi (terang) dipertahankan, pixel gelap semakin gelap. Citra jadi lebih gelap secara keseluruhan.

4. **Koreksi pencahayaan?** γ < 1 untuk mengoreksi citra underexposed (gelap), γ > 1 untuk mengoreksi citra overexposed (terang) atau untuk efek dramatIS.

5. **Kapan gamma lebih cocok dari log?** Gamma lebih fleksibel karena bisa menangani koreksi terang dan gelap tergantung nilai γ. Log transform lebih spesifik untuk memperkuat area gelap saja.""")

# ============================================================
# BAGIAN G: ANALISIS HOTS
# ============================================================
md("""---
# Bagian G: Analisis HOTS (Higher Order Thinking Skills)""")

md("""### G.1 Perbandingan Teknik Manipulasi Citra

| Teknik | Jenis Operasi | Efek Visual | Kapan Digunakan |
|--------|--------------|-------------|-----------------|
| Image blending | Aritmetika linier (weighted sum) | Dua citra digabung dengan transparansi sesuai bobot | Membuat efek transisi, watermark, superimpose dua gambar |
| Image negative | Aritmetika (255 - pixel) | Warna terbalik (seperti negatif film) | Analisis citra medis, deteksi pola, visualisasi kontras alternatif |
| Transformasi logaritmik | Logaritmik non-linier | Detail area gelap meningkat, area terang kompresi | Citra underexposed, citra medis dengan detail di bayangan |
| Transformasi gamma | Power-law non-linier | γ<1: cerah; γ>1: gelap; fleksibel | Koreksi pencahayaan, kalibrasi monitor, preprocessing computer vision |""")

md("""### G.2 Analisis Pengambilan Keputusan

**1. Citra terlalu gelap → teknik paling tepat?**
Transformasi gamma dengan γ < 1 (misal 0.5) atau transformasi logaritmik. Gamma lebih aman karena kita bisa mengontrol seberapa banyak koreksi. Logaritmik juga bisa tapi efeknya lebih tetap dan tidak bisa diatur sefleksibel gamma.

**2. Citra terlalu terang → teknik paling tepat?**
Transformasi gamma dengan γ > 1 (misal 2 atau 2.5). Ini akan meredam area terang dan membawa detail yang tadinya washout jadi lebih terlihat. Log transform tidak cocok karena dia justru mengkompresi area terang tanpa banyak membantu.

**3. Ingin menggabungkan dua citra → teknik?**
Image blending dengan `cv.addWeighted()`. Atur bobot α dan β sesuai kontribusi yang diinginkan. Ini adalah satu-satunya teknik dari empat yang dibahas yang memang dirancang untuk menggabungkan dua gambar.

**4. Menonjolkan detail area gelap → log transform atau gamma?**
Log transform lebih spesifik untuk ini karena slope-nya besar di area gelap dan kecil di area terang. Tapi gamma dengan γ < 1 juga bisa dan kadang lebih natural. Saya pribadi lebih pilih log transform untuk citra yang sangat gelap karena efeknya lebih agresif di area gelap.

**5. Apakah semua transformasi selalu memperbaiki kualitas?**
Tidak. Transformasi citra adalah operasi yang mengubah pixel, belum tentu jadi lebih baik. Image negative misalnya, secara teknis tidak memperbaiki apapun, hanya membalikkan intensitas. Transformasi gamma dengan nilai ekstrem bisa menghilangkan detail. Konteks dan tujuan menentukan apakah suatu transformasi "memperbaiki" atau justru merusak.""")

md("""### G.3 Studi Kasus (Pilih 2)

**Studi Kasus 1: Foto Malam Hari**

*Teknik yang digunakan:* Transformasi gamma dengan γ < 1, misal 0.3-0.5.

*Alasan:* Foto malam hari didominasi pixel gelap. Gamma correction dengan γ < 1 akan meregangkan area gelap sehingga detail yang tadinya hampir hitam menjadi lebih terlihat. Risikonya noise juga ikut diperkuat karena sensor kamera biasanya menghasilkan noise di area gelap. Alternatifnya bisa pakai transformasi logaritmik, tapi gamma memberi kontrol lebih baik.

**Studi Kasus 3: Efek Gabungan Foto dan Tekstur**

*Teknik yang sesuai:* Image blending.

*Pengaruh bobot:* Bobot menentukan seberapa transparan tekstur terhadap foto. α=0.8 (foto) dan β=0.2 (tekstur) akan membuat tekstur tampak samar sebagai efek overlay halus. α=0.5 dan β=0.5 membuat keduanya sama kuat. Kalau ingin tekstur dominan, balik bobotnya. Properti yang perlu diperhatikan adalah α + β harus = 1 agar intensitas tidak overflow.""")

# ============================================================
# BAGIAN H: REFLEKSI PRIBADI
# ============================================================
md("""---
# Bagian H: Refleksi Pribadi

1. **Teknik paling mudah dipahami?** Image negative. Logikanya paling sederhana, tinggal 255 - pixel. Hasilnya juga langsung terlihat dramatis jadi memuaskan.

2. **Teknik paling sulit dianalisis?** Transformasi gamma. Meskipun rumusnya sederhana (r^γ), efeknya tergantung pada distribusi pixel di citra. Dua citra berbeda bisa bereaksi berbeda terhadap nilai γ yang sama. Butuh eksperimen untuk benar-benar paham.

3. **Perbedaan log transform dan gamma?** Log transform selalu meningkatkan area gelap dan kompresi area terang, apapun citranya. Gamma lebih fleksibel: bisa terangin (γ<1) atau gelapin (γ>1) tergantung kebutuhan. Bentuk kurvanya juga berbeda.

4. **Hal baru tentang nilai pixel?** Saya baru sadar kalau operasi sederhana seperti pangkat atau log pada pixel bisa mengubah persepsi visual secara drastis. Pixel itu cuma angka 0-255, tapi cara kita memetakan ulang angka-angka itu sangat mempengaruhi bagaimana gambar dilihat manusia.

5. **Aplikasi peningkatan kualitas citra, teknik pertama?** Transformasi gamma. Karena fleksibel, bisa handle citra gelap dan terang. Implementasinya juga sederhana tapi efeknya besar.""")

# ============================================================
# KESIMPULAN
# ============================================================
md("""---
# Kesimpulan

Dari tugas ini saya belajar bahwa manipulasi citra digital bukan hanya tentang membuat gambar terlihat lebih bagus, tapi tentang memahami hubungan antara nilai pixel dengan persepsi visual. Empat teknik yang dipelajari (blending, negative, log transform, gamma transform) masing-masing punya karakteristik dan kegunaan yang berbeda. Tidak ada teknik yang universal lebih baik, semuanya tergantung pada kondisi citra dan tujuan yang ingin dicapai.""")
# ============================================================
# BUILD NOTEBOOK
# ============================================================
notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.10.0"
        }
    },
    "cells": cells
}

with open("notebook/image_manipulation.ipynb", "w") as f:
    json.dump(notebook, f, indent=1)

print("Notebook berhasil dibuat!")
print(f"Total cells: {len(cells)}")
