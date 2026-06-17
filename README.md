# Manipulasi Citra Digital

| | |
|---|---|
| **Nama** | Fatih Jawwad Al Mumtaz |
| **NIM** | 452024611047 |
| **Kelas** | Teknik Informatika -- Semester 5 |
| **Mata Kuliah** | Pengolahan Sinyal Digital |
| **Dosen Pengampu** | Assoc. Prof. Dr. Oddy Virgantara Putra, S.Kom., M.T. |

## Deskripsi

Tugas individu implementasi teknik manipulasi citra digital menggunakan OpenCV. Mencakup empat teknik: image blending, image negative, transformasi logaritmik, dan transformasi gamma. Setiap teknik dianalisis efeknya terhadap tampilan citra dan distribusi pixel.

## Topik

- Membaca dan menampilkan citra (BGR vs RGB)
- Resize citra
- Image blending dengan variasi bobot
- Image negative dan analisis histogram
- Transformasi logaritmik
- Transformasi gamma
- Analisis HOTS dan studi kasus

## Library

| Library | Versi | Kegunaan |
|---------|-------|----------|
| OpenCV | 4.13.0 | Baca/manipulasi citra |
| NumPy | 2.4.6 | Operasi matriks & array |
| Matplotlib | 3.11.0 | Visualisasi citra & histogram |
| Jupyter | 1.1.1 | Notebook environment |

Dependensi lengkap ada di `pyproject.toml`.

## Repository Structure

```
manipulasi-citra-digital/
├── images/
│   ├── image1.jpg               # Citra 1 (600×800)
│   └── image2.jpg               # Citra 2 (768×1024)
├── notebook/
│   └── image_manipulation.ipynb # Notebook utama (35 cells, sudah dieksekusi)
├── report/
│   └── laporan.pdf              # Laporan PDF (7 halaman)
├── pyproject.toml               # Konfigurasi project & dependensi (uv)
├── generate_notebook.py         # Generator notebook
├── uv.lock                      # Lock file dependensi
└── README.md                    # File ini
```

## Cara Menjalankan

### Prerequisites
- Python >= 3.9
- uv (package manager)

### Setup & Run

```bash
# Install uv kalo belum punya
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone / masuk ke directory project
cd manipulasi-citra-digital

# Setup environment & install dependensi
uv sync

# Jalankan notebook
uv run jupyter notebook notebook/image_manipulation.ipynb
```

### Run langsung (tanpa GUI)

```bash
uv run jupyter nbconvert --to notebook \
  --execute notebook/image_manipulation.ipynb \
  --output-dir . \
  --ExecutePreprocessor.timeout=120
```

### Compile laporan (LaTeX → PDF)

```bash
# Install tectonic kalo belum punya
# Download dari https://github.com/tectonic-typesetting/tectonic/releases

tectonic report/laporan.tex --outdir report
```

## Citra yang Digunakan

| Citra | Ukuran Asli | Deskripsi |
|-------|-------------|-----------|
| `images/image1.jpg` | 600×800 px | Gambar dari picsum.photos, ukuran lebih portrait |
| `images/image2.jpg` | 768×1024 px | Gambar dari picsum.photos, resolusi lebih besar |

Keduanya format JPEG, 3 channel BGR, tipe data uint8, rentang intensitas 0--255.
Konten spesifik bisa dicek langsung di notebook (ada visualisasi).

## Ringkasan Hasil Eksperimen

### Image Blending
- 3 variasi bobot: (0.2,0.8), (0.5,0.5), (0.8,0.2)
- α + β harus = 1 biar intensitas ga overflow
- α > β → citra 1 dominan, β > α → citra 2 dominan

### Image Negative
- Rumus: 255 - pixel
- Histogram tercermin horizontal (mirror)
- Ga nambah/ilang informasi, cuma mindahin intensitas

### Transformasi Logaritmik
- Konstanta c = 105.89 (dari percobaan)
- Detail area gelap naik, area terang kompresi
- Ada bug teknis: overflow uint8 pas pake `np.max()` → solusi pake `float()`

### Transformasi Gamma
- 4 nilai γ: 0.5, 1.0, 2.0, 2.5
- γ < 1 → gambar terang, γ > 1 → gambar gelap
- Paling fleksibel dari semua teknik

### Bug yang Ditemukan
Pas implementasi log transform, `np.max(img1_resize)` baliknya uint8. Operasi `1 + 255` overflow ke 0, jadinya c = -0.00 dan gambar item semua. Fix: pake `float(np.max(...))`.

## Analisis HOTS

### Perbandingan Teknik

| Teknik | Operasi | Efek | Kapan Dipake |
|--------|---------|------|-------------|
| Blending | α×I₁ + β×I₂ | Overlay dua gambar | Transisi, watermark |
| Negative | 255 - I | Warna terbalik | Citra medis, pola |
| Log | c·log(1+r) | Detail gelap naik | Underexposed citra |
| Gamma | r^γ | Terang/gelap | Koreksi exposure |

### Keputusan Teknis
- **Citra gelap** → gamma correction (γ < 1)
- **Citra terang** → gamma correction (γ > 1)
- **Gabung citra** → image blending
- **Detail area gelap** → log transform (lebih spesifik)
- **Perbaikan kualitas** → tergantung konteks, ga semua transformasi otomatis bikin lebih baik

### Studi Kasus
1. **Foto malam** → gamma 0.3--0.5. Risiko noise naik.
2. **Citra medis** → log transform. Detail samar jadi kontras.
3. **Overlay tekstur** → image blending dengan bobot sesuai kebutuhan.

## Kesimpulan

Manipulasi citra digital bukan cuma soal kode jalan, tapi soal paham hubungan antara nilai pixel dengan persepsi visual. Setiap teknik punya karakteristik sendiri: blending buat gabung gambar, negative buat inversi, log buat stretch gelap, gamma buat koreksi dua arah. Ga ada teknik yang universal terbaik -- pemilihan tergantung kondisi citra dan tujuan.

## Referensi

- [OpenCV Documentation](https://docs.opencv.org/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Matplotlib Documentation](https://matplotlib.org/stable/)
- [picsum.photos](https://picsum.photos/) -- sumber gambar
- [Tectonic](https://tectonic-typesetting.github.io/) -- LaTeX engine
