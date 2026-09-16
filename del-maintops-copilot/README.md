# Del-MaintOps Copilot

**Enterprise AI Copilot untuk manajemen fasilitas & infrastruktur kampus Institut Teknologi Del.**

> Mata Kuliah: 10S3001 - Artificial Intelligence / Kecerdasan Buatan
> Milestone 1 (W02): Problem Framing, Spesifikasi PEAS, & Baseline Search
> Program Studi Sarjana Sistem Informasi, Institut Teknologi Del

## Tentang Proyek

Del-MaintOps Copilot adalah rancangan Enterprise AI Copilot yang ditujukan untuk
membantu tim sarana dan prasarana kampus dalam menganalisis laporan kerusakan
fasilitas (listrik, HVAC/AC, jaringan, dan fasilitas pendukung akademik
lainnya), menentukan tingkat urgensi, mencocokkan laporan dengan SOP internal,
dan memberikan rekomendasi tindakan.

**Fokus Milestone 1** (dokumen ini) *hanya* mencakup:

1. Problem framing & spesifikasi PEAS.
2. Formulasi ruang keadaan (state space) masalah triase laporan sebagai
   masalah pencarian graf.
3. Implementasi baseline search — **Uniform Cost Search (UCS)** — menggunakan
   `heapq`.
4. Inisialisasi repositori & environment proyek dengan Astral `uv`.

Fitur Generative AI, RAG, ChromaDB, FastMCP, dan dashboard Gradio yang
disebutkan pada roadmap besar proyek **belum** diimplementasikan pada
Milestone 1 — akan dibangun bertahap pada Milestone 2–5.

Dokumen laporan lengkap Milestone 1 (problem framing, PEAS, formulasi
X/A/T/G/C, analisis kompleksitas, dan self-review rubrik) tersedia di
`docs/milestone1.md` (atau berkas PDF/DOCX yang dikumpulkan terpisah).

## Struktur Repositori

```
del-maintops-copilot/
│
├── src/
│   ├── search/
│   │   ├── __init__.py
│   │   ├── graph.py      # Representasi graf masalah (state, action, cost)
│   │   └── ucs.py        # Implementasi Uniform Cost Search (heapq)
│   │
│   └── main.py           # CLI demo: menjalankan 3 test case
│
├── tests/
│   └── test_search.py    # Test otomatis (pytest): normal, alternatif, edge case
│
├── docs/
│   └── milestone1.md      # Ringkasan laporan Milestone 1
│
├── README.md
├── pyproject.toml
├── .gitignore
└── LICENSE
```

## Menjalankan Proyek (dengan Astral `uv`)

```bash
# 1. Inisialisasi & sinkronisasi environment
uv sync

# 2. Jalankan demo pencarian (3 test case)
uv run python src/main.py

# 3. Jalankan test otomatis
uv run pytest -v
```

Jika `uv` belum terpasang, environment juga dapat dijalankan dengan Python
standar (>=3.10) dan `pip install -e ".[dev]"` sebagai alternatif, karena
proyek ini tidak memiliki dependency eksternal di luar `pytest` untuk testing.

## Ringkasan Algoritma

Masalah triase laporan kerusakan diformulasikan sebagai graf berbobot searah
(directed weighted graph), dengan node merepresentasikan tahap penanganan
(klasifikasi → diagnosis → pencocokan SOP → alokasi teknisi → selesai) dan
bobot edge merepresentasikan estimasi waktu/effort. **Uniform Cost Search**
dipilih sebagai baseline karena graf ini tidak memiliki heuristik jarak yang
admissible secara alami (lihat penjelasan lengkap di dokumen Milestone 1,
Bab 5.1) — UCS menjamin solusi optimal untuk graf berbobot non-negatif tanpa
perlu mengarang fungsi heuristik.

## Status Data

Seluruh nilai bobot (cost) pada `src/search/graph.py` adalah **asumsi desain**
untuk kebutuhan pengujian algoritma pada Milestone 1, bukan data historis
nyata dari operasional IT Del. Bagian mana pun dalam dokumentasi yang memuat
data spesifik IT Del yang belum terverifikasi ditandai secara eksplisit
sebagai asumsi desain.

## Tim

| Nama | NIM | Peran |
|---|---|---|
| Lucas Pardede | 12S24015 | [DATA YANG PERLU DIKONFIRMASI] |
| [NAMA ANGGOTA 2] | [NIM] | [DATA YANG PERLU DIKONFIRMASI] |
| [NAMA ANGGOTA 3] | [NIM] | [DATA YANG PERLU DIKONFIRMASI] |
| [NAMA ANGGOTA 4 - opsional] | [NIM] | [DATA YANG PERLU DIKONFIRMASI] |

## Lisensi

Proyek ini menggunakan lisensi MIT — lihat berkas [LICENSE](LICENSE).
