# Del-MaintOps Copilot
## Milestone 1 — Business Problem Framing, Spesifikasi PEAS, & Inisialisasi Repositori GitHub

**Mata Kuliah:** 10S3001 – Kecerdasan Buatan / Artificial Intelligence
**Program Studi:** Sarjana Sistem Informasi, Institut Teknologi Del
**Kode Tugas:** Tugas 1 (Milestone 1 – W02)
**Kelompok:** [Kode Kelompok — DATA YANG PERLU DIKONFIRMASI]

| Nama | NIM |
|---|---|
| Lucas Pardede | 12S24015 |
| [NAMA ANGGOTA 2] | [NIM ANGGOTA 2] |
| [NAMA ANGGOTA 3] | [NIM ANGGOTA 3] |

**Repositori GitHub:** `[TAUTAN REPOSITORI GITHUB — DATA YANG PERLU DIKONFIRMASI]`

---

## 1. Pendahuluan

### 1.1 Latar Belakang

Institut Teknologi Del (IT Del) sebagaimana perguruan tinggi pada umumnya
mengoperasikan berbagai fasilitas fisik untuk mendukung kegiatan akademik:
laboratorium komputer, ruang kelas, asrama mahasiswa, jaringan komputer
kampus, sistem kelistrikan, serta perangkat pendingin ruangan (HVAC/AC) pada
ruang-ruang yang membutuhkannya. Fasilitas ini secara alami mengalami
kerusakan atau gangguan dari waktu ke waktu, dan penanganannya bergantung
pada proses pelaporan serta tindak lanjut oleh tim sarana dan prasarana.

**Asumsi Desain:** karena tim penyusun tidak memiliki akses terhadap data
operasional riil sistem pelaporan kerusakan fasilitas IT Del, seluruh
karakteristik proses (volume laporan, mekanisme triase saat ini, dsb.) pada
dokumen ini dirumuskan sebagai asumsi desain yang masuk akal berdasarkan pola
umum pengelolaan fasilitas kampus, bukan sebagai fakta operasional yang sudah
terverifikasi.

### 1.2 Identifikasi Masalah

Secara umum, pengelolaan laporan kerusakan fasilitas pada institusi dengan
skala kampus menghadapi beberapa tantangan berulang:

- Laporan kerusakan dapat menumpuk, terutama pada periode aktivitas akademik
  yang padat.
- Tidak selalu tersedia mekanisme triase (penentuan prioritas penanganan)
  yang konsisten antar laporan.
- Tingkat urgensi setiap laporan sulit ditentukan secara objektif — laporan
  dengan potensi bahaya berbeda (mis. korsleting listrik vs. AC yang kurang
  dingin) berisiko diperlakukan setara jika hanya diurutkan berdasarkan
  waktu masuk (first-in-first-out).
- Tim maintenance memerlukan alur keputusan yang jelas mengenai jalur
  penanganan mana yang paling efisien dari sisi waktu dan sumber daya.
- Pencocokan laporan dengan SOP (Standard Operating Procedure) internal yang
  relevan dapat memakan waktu apabila dilakukan sepenuhnya manual.

### 1.3 Problem Statement

**Current Condition:** Laporan kerusakan fasilitas kampus (listrik, HVAC,
jaringan, dan fasilitas pendukung akademik lain) saat ini — *dalam asumsi
desain proyek ini* — ditangani tanpa mekanisme triase otomatis yang
konsisten, sehingga prioritas penanganan bergantung pada penilaian manual
staf yang menerima laporan.

**Problem:** Tidak adanya alur keputusan terstruktur untuk (1) menentukan
prioritas penanganan berdasarkan tingkat urgensi dan kompleksitas, dan
(2) memilih jalur penanganan (SOP → alokasi teknisi) dengan total biaya
(waktu/effort) terendah, menyebabkan variasi kualitas dan kecepatan
penanganan antar laporan yang seharusnya dapat diperlakukan secara lebih
sistematis.

**Impact:** Potensi keterlambatan penanganan pada laporan yang sebenarnya
mendesak, penggunaan sumber daya teknisi yang kurang optimal (mis. eskalasi
ke vendor eksternal yang lebih mahal padahal teknisi lokal tersedia), serta
pengalaman pengguna fasilitas (mahasiswa, dosen, staf) yang menurun akibat
ketidakpastian waktu penyelesaian.

**AI Opportunity:** Sebagian dari proses ini — klasifikasi kategori
kerusakan, penentuan prioritas, pencocokan SOP, dan pemilihan jalur
penanganan optimal — dapat dimodelkan sebagai masalah pencarian keputusan
(search problem) maupun, pada milestone lanjutan, sebagai tugas berbasis
pengetahuan (RAG) dan generative reasoning. Pada Milestone 1, peluang ini
difokuskan pada pemodelan proses triase-dan-routing sebagai masalah pencarian
graf berbobot.

### 1.4 Tujuan

1. Merumuskan problem framing yang realistis untuk domain manajemen
   fasilitas kampus IT Del.
2. Menyusun spesifikasi PEAS (Performance measure, Environment, Actuators,
   Sensors) yang formal dan terukur.
3. Memformulasikan proses triase-dan-routing laporan kerusakan sebagai
   masalah pencarian graf (state space X, action A, transition T, goal G,
   cost C).
4. Mengimplementasikan baseline search (UCS) yang benar-benar dapat
   dieksekusi, lengkap dengan test case.
5. Menginisialisasi repositori GitHub dengan struktur dan environment
   (Astral `uv`) yang profesional sebagai fondasi milestone berikutnya.

### 1.5 Batasan

- Milestone 1 **tidak** mencakup implementasi Generative AI, RAG, ChromaDB,
  FastMCP, ataupun antarmuka Gradio — komponen-komponen tersebut merupakan
  cakupan Milestone 2–5.
- Data laporan kerusakan, SOP, dan bobot cost yang digunakan pada graf
  bersifat **asumsi desain** untuk kebutuhan pengujian algoritma, bukan data
  historis nyata IT Del.
- Sistem yang dirancang berperan sebagai *decision support*, bukan pengganti
  keputusan akhir teknisi/manusia, terutama untuk hal-hal yang menyangkut
  keselamatan.

---

## 2. Problem Framing

### 2.1 Business Context

Del-MaintOps Copilot beroperasi dalam konteks manajemen fasilitas dan
infrastruktur kampus IT Del, mencakup domain:

| Domain Fasilitas | Contoh Kerusakan/Gangguan |
|---|---|
| Laboratorium komputer | Perangkat tidak menyala, jaringan lab terputus |
| Ruang kelas | Lampu/proyektor rusak, AC tidak dingin |
| Asrama | Instalasi listrik bermasalah, air/sanitasi |
| Kelistrikan | Korsleting, panel listrik trip berulang |
| HVAC / AC | AC bocor, kompresor tidak berfungsi |
| Jaringan | Akses internet terputus, perangkat access point mati |
| Fasilitas pendukung akademik | Peralatan penunjang praktikum rusak |

### 2.2 Pain Points

- Volume laporan dapat menumpuk pada periode sibuk (mis. awal semester,
  masa ujian dengan penggunaan lab intensif). *(asumsi desain)*
- Ketiadaan mekanisme triase eksplisit membuat urutan penanganan bergantung
  pada siapa yang menerima laporan terlebih dahulu, bukan tingkat urgensi
  sebenarnya. *(asumsi desain)*
- Pencocokan laporan dengan SOP yang tepat memerlukan pengetahuan prosedural
  yang mungkin tidak dimiliki merata oleh seluruh staf penerima laporan.
  *(asumsi desain)*
- Keputusan mengenai apakah suatu kerusakan ditangani teknisi internal atau
  perlu eskalasi ke vendor eksternal seringkali bersifat ad-hoc, berpotensi
  menimbulkan biaya/waktu yang tidak efisien. *(asumsi desain)*

### 2.3 Stakeholder

| Stakeholder | Peran | Permasalahan | Kebutuhan |
|---|---|---|---|
| Mahasiswa | Pelapor & pengguna fasilitas | Fasilitas yang rusak mengganggu kegiatan akademik/harian | Kepastian dan kecepatan penanganan laporan |
| Dosen | Pelapor & pengguna fasilitas (ruang kelas, lab) | Gangguan fasilitas menghambat proses belajar-mengajar | Penanganan cepat untuk fasilitas kelas/lab |
| Staf/pengelola fasilitas | Penerima & pencatat laporan | Volume laporan tinggi, sulit menentukan prioritas manual | Alat bantu triase yang konsisten dan cepat |
| Teknisi | Eksekutor perbaikan | Instruksi penanganan tidak selalu disertai SOP yang jelas | Rekomendasi SOP & alur kerja yang jelas per laporan |
| Tim sarana dan prasarana | Pengelola & pengambil keputusan alokasi sumber daya | Perlu menyeimbangkan beban kerja teknisi internal vs. vendor eksternal | Rekomendasi jalur penanganan dengan biaya/waktu optimal |
| Administrator sistem | Pengelola platform Del-MaintOps Copilot | Perlu memastikan sistem berjalan andal & data tercatat rapi | Observabilitas dan kemudahan pemeliharaan sistem |

Hubungan stakeholder dengan sistem: mahasiswa/dosen berperan sebagai
pelapor (sumber input laporan); staf fasilitas dan tim sarana-prasarana
berperan sebagai pengguna utama hasil rekomendasi sistem (prioritas, SOP,
jalur penanganan); teknisi menjadi eksekutor akhir yang keputusannya tetap
final untuk aspek teknis dan keselamatan; administrator sistem menjaga
keberlangsungan operasional Del-MaintOps Copilot itu sendiri.

### 2.4 AI Opportunity — Perbandingan Pendekatan

| Aspek | Manual | Rule-based / Sistem Informasi Sederhana | AI-assisted (Del-MaintOps Copilot) |
|---|---|---|---|
| Penentuan prioritas | Bergantung penilaian individu staf, tidak konsisten | Konsisten tetapi kaku (if-else tetap), sulit menangani variasi kasus | Dapat mempertimbangkan banyak faktor & memberi rekomendasi jalur, tetap dapat dijelaskan (explainable) |
| Pencocokan SOP | Manual, bergantung pengetahuan staf | Terbatas pada aturan yang di-hardcode | Pencarian/pencocokan yang lebih fleksibel terhadap variasi deskripsi laporan (dikembangkan penuh pada Milestone 3 dengan RAG) |
| Pemilihan jalur penanganan optimal | Tidak terstruktur, sering berdasarkan kebiasaan | Bisa dihitung tetapi biasanya tidak otomatis dibandingkan seluruh alternatif | Algoritma pencarian (UCS/A*) dapat membandingkan seluruh jalur secara sistematis dan menemukan biaya minimum |
| Skalabilitas | Rendah saat volume tinggi | Sedang | Berpotensi tinggi, namun tetap perlu pengawasan manusia |

**Penting:** perbandingan di atas tidak menyimpulkan "AI pasti lebih baik".
Sistem rule-based sederhana bisa jadi sudah memadai untuk kasus-kasus rutin
dan sederhana; keunggulan pendekatan AI-assisted baru terasa signifikan pada
skenario dengan banyak variasi kasus dan kebutuhan mempertimbangkan banyak
faktor sekaligus. Del-MaintOps Copilot diposisikan sebagai **decision
support**, bukan pengganti keputusan teknisi:

- AI tidak melakukan perbaikan fisik terhadap fasilitas.
- AI tidak menggantikan keahlian dan penilaian teknisi di lapangan.
- AI memberikan rekomendasi prioritas, SOP, dan jalur penanganan.
- Keputusan yang menyangkut keselamatan tetap membutuhkan verifikasi
  manusia.
- Pada Milestone 1, komponen AI generatif **belum** diimplementasikan; yang
  dibangun adalah baseline symbolic search sebagai fondasi.

### 2.5 Karakteristik Environment

Dijelaskan secara formal pada Bagian 3.2 (PEAS – Environment).

---

## 3. PEAS

### 3.1 Performance Measure

| Performance Measure | Apa yang Diukur | Cara Mengukur | Mengapa Penting |
|---|---|---|---|
| Keberhasilan menemukan jalur solusi | Apakah sistem berhasil menemukan jalur penanganan yang valid dari laporan hingga status selesai | Rasio laporan yang menghasilkan path vs. yang gagal (found=True/False pada hasil search) | Menjamin setiap laporan yang valid selalu mendapat rekomendasi tindak lanjut |
| Total cost jalur keputusan | Estimasi total waktu/effort dari laporan hingga selesai | Nilai `total_cost` yang dikembalikan algoritma UCS | Merepresentasikan efisiensi rekomendasi — biaya lebih rendah berarti penanganan lebih cepat/hemat sumber daya *(target proyek, bukan angka yang sudah terbukti pada operasional nyata)* |
| Konsistensi keputusan | Apakah laporan dengan karakteristik serupa menghasilkan rekomendasi jalur yang serupa/prediktif | Membandingkan hasil search untuk beberapa laporan dengan kategori sama | Konsistensi penting agar staf/teknisi dapat mempercayai rekomendasi sistem |
| Waktu respons sistem | Waktu komputasi yang dibutuhkan algoritma untuk menghasilkan rekomendasi | Waktu eksekusi fungsi `uniform_cost_search` (dapat diukur dengan `time.perf_counter`) | Rekomendasi harus tersedia cukup cepat agar berguna secara praktis, walau pada Milestone 1 graf masih berskala kecil |
| Relevansi rekomendasi SOP | Kesesuaian SOP yang dipilih dengan kategori kerusakan yang dilaporkan | Pada Milestone 1 diverifikasi manual melalui review jalur/label aksi; pengukuran otomatis (mis. skor relevansi semantik) baru relevan pada Milestone 3+ | Rekomendasi yang tidak relevan akan menurunkan kepercayaan pengguna terhadap sistem |

*(Nilai ambang/target numerik spesifik seperti "akurasi ≥ 90%" belum
ditetapkan pada Milestone 1 karena belum tersedia data evaluasi nyata;
angka semacam itu akan menjadi **target proyek** pada milestone lanjutan
setelah data historis tersedia.)*

### 3.2 Environment

| Karakteristik | Status | Alasan | Contoh |
|---|---|---|---|
| Observability | **Partially Observable** | Sistem hanya mengetahui informasi yang dicantumkan pada laporan (deskripsi teks, lokasi, kategori); kondisi fisik sebenarnya di lapangan (tingkat keparahan riil, ketersediaan spare part) tidak sepenuhnya terlihat oleh sistem | Laporan menyebut "AC mati", tetapi sistem tidak mengetahui apakah penyebabnya kompresor rusak atau sekadar remote kehabisan baterai sebelum teknisi memeriksa langsung |
| Determinism | **Stochastic** | Ketersediaan teknisi, waktu tempuh ke lokasi, dan durasi perbaikan aktual dapat bervariasi dan tidak sepenuhnya dapat diprediksi sistem | Teknisi yang dijadwalkan bisa saja sedang menangani laporan lain sehingga waktu tunggu aktual berbeda dari estimasi |
| Sequential/Episodic | **Sequential** | Keputusan pada satu laporan (mis. alokasi teknisi tertentu) dapat memengaruhi ketersediaan sumber daya untuk laporan berikutnya | Jika teknisi listrik lokal dialokasikan untuk laporan A, laporan B dengan kategori sama mungkin harus menunggu atau dialihkan ke vendor eksternal |
| Dynamics | **Dynamic** | Status laporan lain, ketersediaan teknisi, dan kondisi fasilitas dapat berubah sementara sistem sedang memproses sebuah laporan | Teknisi yang semula tersedia bisa saja ditugaskan ke laporan darurat lain di tengah proses triase laporan yang sedang dievaluasi |
| Representasi | **Text-based Discrete** | State, action, dan kategori pada Milestone 1 direpresentasikan sebagai node/label diskrit (kategori kerusakan, tahap penanganan), bukan data kontinu seperti sensor fisik real-time | Kategori kerusakan dinyatakan sebagai label diskrit: "Electrical", "HVAC", "Network", bukan sinyal sensor analog |

### 3.3 Actuators

Actuator merepresentasikan **output/aksi sistem**, bukan tindakan fisik
teknisi:

- Menghasilkan rekomendasi jalur penanganan (urutan tahap dari laporan
  hingga selesai).
- Menentukan kategori prioritas penanganan (berdasarkan jalur/cost yang
  dipilih).
- Menyediakan referensi SOP yang cocok dengan kategori laporan (label aksi
  pada jalur hasil pencarian).
- Menampilkan hasil pencarian (path, total cost, dan daftar aksi) kepada
  staf/tim sarana dan prasarana untuk digunakan sebagai dasar keputusan.

Tindakan fisik seperti benar-benar memperbaiki panel listrik atau mengganti
komponen AC tetap sepenuhnya dilakukan oleh teknisi manusia — sistem hanya
memberi rekomendasi, bukan mengeksekusi perbaikan.

### 3.4 Sensors

Sensor merepresentasikan **input** yang diterima sistem dari laporan:

- Deskripsi teks kerusakan yang ditulis pelapor.
- Lokasi/gedung dan ruangan tempat kerusakan terjadi.
- Jenis/kategori fasilitas yang dilaporkan rusak.
- Waktu laporan dibuat (timestamp).
- Metadata tiket lain (mis. ID pelapor, status sebelumnya, jika tersedia).

Pada Milestone 1, seluruh sensor ini masih berupa input konseptual untuk
mendefinisikan `start state` pada graf pencarian; parsing otomatis dari teks
bebas (natural language) menjadi state terstruktur direncanakan sebagai
bagian dari pipeline RAG pada Milestone 3–4.

---

## 4. State Space Formulation

### 4.1 State (X)

**Definisi:** sebuah state merepresentasikan kombinasi antara *kategori
kerusakan* yang telah diklasifikasikan dan *tahap penanganan* yang telah
dicapai oleh laporan tersebut.

Representasi yang digunakan pada Milestone 1 (lihat implementasi pada
`src/search/graph.py`):

```
State = node bernama <TAHAP>_<KATEGORI>
```

Contoh: `DIAG_ELEC` berarti "laporan bertipe Electrical yang telah berada
pada tahap Diagnosis". Representasi berbasis label node dipilih (bukan
tuple `(lokasi, jenis_kerusakan, status_diagnosis, teknisi, tahap)` yang
lebih kompleks) karena pada Milestone 1 fokus utama adalah membuktikan
kebenaran algoritma pencarian graf pada baseline yang jelas dan dapat
diverifikasi; representasi state yang lebih kaya (menyertakan atribut
lokasi/gedung spesifik dan identitas teknisi individual) direncanakan pada
milestone lanjutan begitu data nyata tersedia.

### 4.2 Action (A)

Tindakan yang dapat "dilakukan" oleh agent pencarian pada ruang keadaan
(bukan tindakan fisik teknisi, melainkan langkah logis dalam alur
keputusan):

- Mengklasifikasikan laporan ke kategori kerusakan (Electrical/HVAC/
  Network).
- Melakukan diagnosis awal terhadap kategori yang telah ditentukan.
- Mencocokkan hasil diagnosis dengan SOP (ditemukan vs. eskalasi manual).
- Mengalokasikan teknisi (lokal vs. vendor eksternal).
- Menyelesaikan/menutup laporan.

Setiap action direpresentasikan sebagai edge berlabel pada graf (lihat
`graph.py`), sehingga setiap action benar-benar dapat dieksekusi dalam
graph search — bukan hanya deskripsi naratif.

### 4.3 Transition (T)

Transisi menjelaskan bagaimana suatu action mengubah state. Contoh konkret:

```
State: KLAS_ELEC
Action: "Diagnosis awal kerusakan listrik"
-> State: DIAG_ELEC

State: DIAG_ELEC
Action: "SOP ditemukan: prosedur standar panel listrik"
-> State: SOP_ELEC_OK
```

Transisi bersifat deterministik pada level graf (satu action dari satu
state selalu menuju satu state tujuan yang sama), meskipun *durasi riil*
setiap transisi di dunia nyata bersifat stokastik (lihat Bagian 3.2).
Pemisahan ini disengaja: graf Milestone 1 memodelkan struktur keputusan
(decision structure), bukan simulasi stokastik penuh — simulasi stokastik
berada di luar cakupan Milestone 1.

### 4.4 Goal (G)

**Definisi goal:** "Laporan mencapai state `SELESAI_<KATEGORI>` yang
sesuai, melalui jalur penanganan yang valid (SOP tercocokkan dan teknisi
teralokasi)."

Evaluasi kecocokan dengan UCS/A*: definisi goal ini cocok digunakan dengan
UCS karena bersifat **goal-test sederhana** (pengecekan node == goal),
tanpa memerlukan goal predicate kompleks yang bergantung pada informasi di
luar state graf. Hal ini memenuhi prasyarat UCS/A* standar, yaitu goal
harus dapat diuji langsung dari representasi state.

### 4.5 Cost (C)

Cost pada setiap edge merepresentasikan **estimasi waktu/effort** (dalam
satuan menit, skala relatif) yang dibutuhkan untuk menjalankan satu action.
Pemilihan waktu sebagai basis cost (dibanding, misalnya, jarak fisik antar
lokasi) didasarkan pada pertimbangan bahwa tujuan utama performance measure
Del-MaintOps adalah kecepatan penyelesaian laporan (lihat Bagian 3.1).

**Asumsi Desain — seluruh angka cost pada `graph.py` adalah nilai rekaan
untuk kebutuhan pengujian algoritma**, dirancang dengan pola yang masuk
akal secara kualitatif (mis. eskalasi ke vendor eksternal selalu diberi
cost lebih tinggi daripada penanganan oleh teknisi lokal, karena melibatkan
proses administratif dan penjadwalan tambahan), namun bukan hasil
pengukuran waktu nyata di lapangan.

---

## 5. Baseline Search

### 5.1 Pemilihan Algoritma: UCS vs. A*

Milestone 1 memilih **Uniform Cost Search (UCS)** sebagai algoritma
baseline, dengan pertimbangan sebagai berikut:

- Graf Del-MaintOps bersifat **kategorikal/simbolik** — node
  merepresentasikan tahap proses (klasifikasi, diagnosis, SOP, alokasi),
  bukan koordinat spasial atau besaran fisik yang secara alami memiliki
  fungsi jarak.
- Untuk menggunakan A*, dibutuhkan fungsi heuristik h(n) yang **admissible**
  (tidak pernah overestimate biaya sebenarnya menuju goal). Pada domain ini,
  tidak tersedia data nyata (mis. rata-rata waktu penyelesaian historis per
  tahap) yang bisa dijadikan dasar heuristik yang valid — menciptakan angka
  heuristik tanpa dasar empiris berisiko justru **tidak admissible** dan
  menyesatkan analisis algoritma.
- UCS menjamin solusi optimal untuk graf berbobot **non-negatif** (seluruh
  cost pada `graph.py` bernilai positif), setara dengan algoritma Dijkstra
  dari satu sumber, tanpa memerlukan asumsi heuristik tambahan.
- UCS menggunakan **priority queue** (di sini diimplementasikan dengan
  `heapq`) yang selalu mengambil node dengan **cumulative path cost**
  (g(n)) terendah untuk di-expand berikutnya — sehingga node pertama yang
  mencapai goal dijamin merupakan node dengan total cost terendah (untuk
  bobot non-negatif).

Dengan pertimbangan tersebut, A* dapat menjadi arah pengembangan lanjutan
begitu data nyata (mis. waktu rata-rata historis per kategori kerusakan)
tersedia untuk menyusun heuristik yang benar-benar admissible dan
consistent — namun untuk Milestone 1, UCS dinilai sebagai pilihan yang
lebih jujur dan defensible dibandingkan memaksakan heuristik rekaan.

### 5.2 Representasi Graph

**Diagram ASCII** (disederhanakan, menampilkan struktur layer umum yang
berulang untuk tiap kategori — detail lengkap ada tiga kategori paralel:
Electrical, HVAC, Network):

```text
LAPORAN
  |
  +--(Klasifikasi)--> KLAS_ELEC --(Diagnosis)--> DIAG_ELEC
  |                                                  |
  |                                    +-------------+-------------+
  |                                    |                           |
  |                              SOP_ELEC_OK                 SOP_ELEC_ESK
  |                                    |                           |
  |                        +-----------+-----------+               |
  |                        |                       |               |
  |                  TEK_ELEC_LOKAL         TEK_ELEC_LUAR <---------+
  |                        |                       |
  |                        +----------+------------+
  |                                   v
  |                             SELESAI_ELEC
  |
  +--(Klasifikasi)--> KLAS_HVAC --(Diagnosis)--> DIAG_HVAC
  |                                                  |    (pola identik dengan Electrical:
  |                                                  |     SOP_HVAC_OK/ESK -> TEK_HVAC_LOKAL/LUAR -> SELESAI_HVAC)
  |
  +--(Klasifikasi)--> KLAS_NET --(Diagnosis)--> DIAG_NET
                                                     |
                                       +-------------+-------------+
                                       |                           |
                                 SOP_NET_OK                  ISOLATED_NET
                                       |                       (dead end -
                                 TEK_NET_LOKAL                  belum ada SOP)
                                       |
                                 SELESAI_NET

(Komponen terisolasi, tidak terhubung ke graf di atas — dipakai untuk
 menguji edge case "goal tidak ditemukan"):
LAPORAN_ARSIP --> SELESAI_ARSIP
```

**Adjacency List** (ringkas, nilai lengkap ada di `src/search/graph.py`):

```
LAPORAN        -> [(KLAS_ELEC, 2), (KLAS_HVAC, 2), (KLAS_NET, 2)]
KLAS_ELEC      -> [(DIAG_ELEC, 4)]
DIAG_ELEC      -> [(SOP_ELEC_OK, 3), (SOP_ELEC_ESK, 9)]
SOP_ELEC_OK    -> [(TEK_ELEC_LOKAL, 5), (TEK_ELEC_LUAR, 14)]
SOP_ELEC_ESK   -> [(TEK_ELEC_LOKAL, 8)]
TEK_ELEC_LOKAL -> [(SELESAI_ELEC, 10)]
TEK_ELEC_LUAR  -> [(SELESAI_ELEC, 18)]

KLAS_HVAC      -> [(DIAG_HVAC, 4)]
DIAG_HVAC      -> [(SOP_HVAC_OK, 3), (SOP_HVAC_ESK, 7)]
SOP_HVAC_OK    -> [(TEK_HVAC_LOKAL, 6), (TEK_HVAC_LUAR, 16)]
SOP_HVAC_ESK   -> [(TEK_HVAC_LUAR, 10)]
TEK_HVAC_LOKAL -> [(SELESAI_HVAC, 12)]
TEK_HVAC_LUAR  -> [(SELESAI_HVAC, 20)]

KLAS_NET       -> [(DIAG_NET, 4)]
DIAG_NET       -> [(SOP_NET_OK, 3), (ISOLATED_NET, 5)]
SOP_NET_OK     -> [(TEK_NET_LOKAL, 4)]
TEK_NET_LOKAL  -> [(SELESAI_NET, 8)]
ISOLATED_NET   -> []   (dead end)

LAPORAN_ARSIP  -> [(SELESAI_ARSIP, 3)]   (komponen terisolasi)
SELESAI_ARSIP  -> []
```

**Tabel Node dan Edge (kategori Electrical, sebagai contoh)**

| Dari | Ke | Cost | Aksi |
|---|---|---|---|
| LAPORAN | KLAS_ELEC | 2 | Klasifikasikan sebagai kerusakan listrik |
| KLAS_ELEC | DIAG_ELEC | 4 | Diagnosis awal kerusakan listrik |
| DIAG_ELEC | SOP_ELEC_OK | 3 | SOP ditemukan: prosedur standar panel listrik |
| DIAG_ELEC | SOP_ELEC_ESK | 9 | SOP tidak ditemukan: eskalasi ke teknisi senior |
| SOP_ELEC_OK | TEK_ELEC_LOKAL | 5 | Alokasikan teknisi listrik lokal |
| SOP_ELEC_OK | TEK_ELEC_LUAR | 14 | Teknisi lokal penuh: kontrak vendor eksternal |
| SOP_ELEC_ESK | TEK_ELEC_LOKAL | 8 | Setelah eskalasi, alokasikan teknisi senior lokal |
| TEK_ELEC_LOKAL | SELESAI_ELEC | 10 | Teknisi lokal menyelesaikan & menutup tiket |
| TEK_ELEC_LUAR | SELESAI_ELEC | 18 | Vendor eksternal menyelesaikan & menutup tiket |

*(Tabel lengkap untuk kategori HVAC dan Network mengikuti pola yang sama,
tersedia langsung pada kode `src/search/graph.py`.)*

### 5.3 Heuristic

Tidak digunakan pada Milestone 1 (lihat justifikasi pemilihan UCS pada
Bagian 5.1).

### 5.4 Implementasi

Implementasi lengkap tersedia pada `src/search/ucs.py` (algoritma) dan
`src/search/graph.py` (representasi graf). Poin-poin kunci implementasi:

- Menggunakan `heapq` sebagai priority queue murni (tanpa library search
  eksternal).
- Priority queue menyimpan tuple `(cumulative_cost, tie_breaker, node,
  path, actions)` — `tie_breaker` berupa counter untuk mencegah error
  perbandingan saat dua entri memiliki cost sama.
- Menggunakan strategi *lazy deletion*: entri usang pada frontier
  diabaikan saat di-pop jika node tersebut sudah pernah di-visit dengan
  cost yang sama atau lebih rendah — pola umum implementasi UCS/Dijkstra
  dengan `heapq` yang tidak mendukung `decrease-key` secara native.
- Mengembalikan objek `SearchResult` berisi `path`, `total_cost`,
  `actions` (daftar label aksi di sepanjang jalur), `nodes_expanded`
  (untuk analisis kompleksitas), dan `found` (boolean).
- Modular: fungsi `uniform_cost_search(graph, start, goal)` menerima graf,
  start state, dan goal state sebagai parameter — tidak ada jawaban yang
  di-hardcode.

### 5.5 Test Case

| Test | Input (start → goal) | Expected Path | Actual Path (hasil eksekusi nyata) | Cost | Status |
|---|---|---|---|---|---|
| 1 — Normal | LAPORAN → SELESAI_ELEC | LAPORAN→KLAS_ELEC→DIAG_ELEC→SOP_ELEC_OK→TEK_ELEC_LOKAL→SELESAI_ELEC | *(sama)* | 24 | ✅ PASSED |
| 2 — Jalur Alternatif | LAPORAN → SELESAI_HVAC | LAPORAN→KLAS_HVAC→DIAG_HVAC→SOP_HVAC_OK→TEK_HVAC_LOKAL→SELESAI_HVAC (cost 27, dari 3 kemungkinan jalur: 27 vs 45 vs 43) | *(sama, cost 27 terpilih sebagai termurah)* | 27 | ✅ PASSED |
| 3 — Edge Case | LAPORAN → SELESAI_ARSIP (komponen terisolasi) | Tidak ada path (found=False) | *(sama, found=False)* | ∞ | ✅ PASSED |

Kolom "Actual Path" di atas diambil langsung dari eksekusi nyata
`pytest tests/test_search.py -v` dan `python src/main.py` (bukan simulasi
atau karangan) — seluruh 5 test (termasuk 2 test tambahan untuk dead end
`ISOLATED_NET` dan node tidak dikenal) **PASSED** pada saat dokumen ini
disusun. Output lengkap eksekusi `main.py`:

```
Test Case 1 (Normal) - Laporan Kerusakan Listrik
Path  : LAPORAN -> KLAS_ELEC -> DIAG_ELEC -> SOP_ELEC_OK -> TEK_ELEC_LOKAL -> SELESAI_ELEC
Cost  : 24.0
Node yang di-expand: 20

Test Case 2 (Jalur Alternatif) - Laporan Kerusakan HVAC/AC
Path  : LAPORAN -> KLAS_HVAC -> DIAG_HVAC -> SOP_HVAC_OK -> TEK_HVAC_LOKAL -> SELESAI_HVAC
Cost  : 27.0
Node yang di-expand: 21

Test Case 3 (Edge Case) - Goal Tidak Terjangkau
Hasil : GOAL TIDAK DITEMUKAN (no path)
Node yang di-expand: 21
```

### 5.6 Hasil

UCS berhasil menemukan jalur optimal (biaya minimum) pada seluruh skenario
yang goal-nya terjangkau, dan mengembalikan status "tidak ditemukan" secara
anggun (tanpa error) pada skenario goal tidak terjangkau. Jumlah node yang
di-expand relatif kecil (20–21 dari total ±22 node pada graf), konsisten
dengan sifat UCS yang mengeksplorasi hampir seluruh ruang keadaan berbobot
rendah sebelum memastikan optimalitas — sesuai ekspektasi teoretis untuk
graf sekecil ini.

### 5.7 Analisis Kompleksitas

Dengan branching factor rata-rata $b$ dan kedalaman solusi optimal $d$
(dalam satuan langkah, bukan cost), kompleksitas UCS secara umum:

- **Waktu:** $O(b^{1 + \lfloor C^*/\epsilon \rfloor})$, dengan $C^*$ adalah
  cost solusi optimal dan $\epsilon$ adalah cost edge minimum — pada
  praktiknya untuk graf berhingga seperti Del-MaintOps, kompleksitas dapat
  didekati sebagai $O(E \log V)$ (mirip Dijkstra dengan binary heap), di
  mana $V$ = jumlah node dan $E$ = jumlah edge.
- **Ruang:** $O(b^{1 + \lfloor C^*/\epsilon \rfloor})$, karena UCS harus
  menyimpan seluruh node frontier di priority queue — sebanding dengan
  $O(V)$ untuk graf berhingga seperti pada Milestone 1.

Untuk graf Del-MaintOps saat ini ($V \approx 22$ node, $E \approx 22$
edge), kompleksitas ini masih sangat kecil dan pencarian selesai hampir
instan. **Keterbatasan:** jika jumlah kategori fasilitas dan tahap
penanganan bertambah signifikan (mis. puluhan kategori kerusakan × banyak
sub-tahap × banyak pilihan teknisi), ukuran graf akan tumbuh secara
kombinatorial, dan UCS — yang tidak memanfaatkan informasi arah menuju
goal seperti A* — akan mengeksplorasi node jauh lebih banyak dari yang
diperlukan. Ini menjadi salah satu alasan A* dengan heuristik yang baik
menjadi arah optimasi yang relevan pada milestone lanjutan, setelah data
untuk menyusun heuristik admissible tersedia.

---

## 6. Repository & Software Engineering

### 6.1 Struktur Repositori

```
del-maintops-copilot/
│
├── src/
│   ├── search/
│   │   ├── __init__.py
│   │   ├── graph.py       # Representasi graf (state, action, cost)
│   │   └── ucs.py         # Implementasi Uniform Cost Search
│   │
│   └── main.py            # CLI demo (3 test case)
│
├── tests/
│   └── test_search.py     # Test otomatis (pytest)
│
├── docs/
│   └── milestone1.md      # Dokumen ini
│
├── README.md
├── pyproject.toml
├── .gitignore
└── LICENSE
```

- `src/search/graph.py` — mendefinisikan struktur data graf dan instance
  graf Del-MaintOps.
- `src/search/ucs.py` — algoritma UCS murni menggunakan `heapq`.
- `src/main.py` — menjalankan demonstrasi 3 skenario pencarian.
- `tests/test_search.py` — 5 test otomatis (3 diminta rubrik + 2 tambahan)
  yang seluruhnya **PASSED** pada eksekusi nyata.

### 6.2 Environment dengan `uv`

```bash
uv init      # (jika repositori belum memiliki pyproject.toml)
uv sync      # menyiapkan virtual environment sesuai pyproject.toml
uv run python src/main.py
uv run pytest -v
```

`pyproject.toml` mendefinisikan dependency minimal (`pytest` untuk
development) — proyek Milestone 1 tidak membutuhkan dependency eksternal
untuk algoritma pencariannya sendiri, sesuai requirement "tidak
menggunakan library search eksternal".

### 6.3 README

Lihat `README.md` pada root repositori — memuat deskripsi proyek, struktur
folder, instruksi menjalankan dengan `uv`, ringkasan algoritma, dan status
data (asumsi desain vs. fakta).

### 6.4 Git Commit Strategy

**Asumsi Desain / Rekomendasi** (karena riwayat commit aktual bergantung
pada proses kerja tim yang sesungguhnya, belum dapat ditentukan dari sisi
dokumen ini):

- Gunakan commit message konvensional, mis. `feat: implement UCS baseline
  search`, `docs: add milestone 1 problem framing`, `test: add edge case
  for unreachable goal`.
- Setiap anggota tim melakukan commit atas bagian yang menjadi tanggung
  jawabnya (problem framing, PEAS, implementasi search, dokumentasi
  repositori) agar riwayat commit mencerminkan kontribusi seimbang, sesuai
  kriteria rubrik "Standar Repositori & Kualitas Kode".
- `[TAUTAN REPOSITORI GITHUB DAN RIWAYAT COMMIT — DATA YANG PERLU
  DIKONFIRMASI SETELAH REPOSITORI DIBUAT DAN DIISI OLEH TIM]`.

---

## 7. Kesimpulan

Pada Milestone 1, tim berhasil merumuskan problem framing yang realistis
untuk domain manajemen fasilitas kampus IT Del (dengan pemisahan jelas
antara fakta, asumsi desain, dan rancangan sistem), menyusun spesifikasi
PEAS yang formal dan terukur, memformulasikan proses triase-dan-routing
laporan kerusakan sebagai masalah pencarian graf (X, A, T, G, C), serta
mengimplementasikan dan menguji baseline Uniform Cost Search yang benar-
benar dapat dieksekusi (dibuktikan oleh 5 test otomatis yang seluruhnya
lulus). Repositori GitHub disiapkan dengan struktur modular dan environment
Astral `uv` sebagai fondasi pengembangan.

Hasil Milestone 1 ini menjadi fondasi bagi milestone berikutnya:

```text
Milestone 1: State Space + UCS (baseline symbolic search / decision path)
        |
        v
Milestone 2: Business Constraint Solver (CSP/GA)
        |
        v
Milestone 3: Enterprise Knowledge Base & Vector Search (ChromaDB/RAG)
        |
        v
Milestone 4: Enterprise AI Agent Pipeline (LLM + RAG + MCP)
        |
        v
Milestone 5: Purwarupa Web Interaktif (Gradio)
```

UCS/A* pada Milestone 1 berperan sebagai **baseline symbolic search /
decision path**, bukan sistem AI final — komponen Generative AI baru akan
diintegrasikan bertahap mulai Milestone 4, dengan tetap memanfaatkan
struktur keputusan (state space) yang telah dirumuskan pada milestone ini.

---

## 8. Self-Review Berdasarkan Rubrik Milestone 1

### Problem Framing & Karakteristik Bisnis (Bobot 30%)

| Checklist | Status |
|---|---|
| Masalah nyata jelas | ✅ Terpenuhi — dijelaskan pada Bab 1–2, dengan pemisahan tegas fakta vs. asumsi desain |
| Pain point jelas | ✅ Terpenuhi (Bab 2.2) |
| Stakeholder jelas | ✅ Terpenuhi, tabel lengkap dengan peran & kebutuhan (Bab 2.3) |
| Dampak masalah jelas | ✅ Terpenuhi (Bab 1.3 — Impact) |
| Alasan menggunakan AI jelas | ✅ Terpenuhi, termasuk perbandingan manual/rule-based/AI (Bab 2.4) |
| Environment dianalisis | ✅ Terpenuhi (Bab 3.2, tabel klasifikasi lengkap) |
| **Perlu dilengkapi tim** | Validasi/penyesuaian asumsi desain dengan kondisi riil IT Del jika data tersedia; identitas lengkap anggota kelompok |

### Formulasi Ruang Keadaan & Algoritma Search (Bobot 40%)

| Checklist | Status |
|---|---|
| X, A, T, G, C jelas | ✅ Terpenuhi (Bab 4) |
| Graph dapat direpresentasikan dalam kode | ✅ Terpenuhi — `src/search/graph.py`, diverifikasi lewat eksekusi nyata |
| UCS/A* benar | ✅ UCS diimplementasikan dan diverifikasi lewat 5 test otomatis (semua PASSED) |
| Menggunakan heapq | ✅ Terpenuhi (`src/search/ucs.py`) |
| Cost masuk akal | ✅ Terpenuhi, dengan pola kualitatif yang konsisten (eskalasi/vendor eksternal selalu lebih mahal); ditandai sebagai asumsi desain |
| Jika A*, heuristik admissible | N/A — tim memilih UCS dengan justifikasi eksplisit (Bab 5.1) |
| Minimal 3 test case | ✅ Terpenuhi (5 test case: normal, alternatif, 2 edge case, node tidak dikenal) |
| Edge case diuji | ✅ Terpenuhi (goal tidak terjangkau, dead end, node tidak dikenal) |
| Tidak ada hardcoded final answer | ✅ Algoritma generik menerima graph/start/goal sebagai parameter |
| **Perlu dilengkapi tim** | Pertimbangkan menambah heuristik A* pada milestone lanjutan setelah data waktu penanganan riil tersedia |

### Standar Repositori & Kualitas Kode (Bobot 30%)

| Checklist | Status |
|---|---|
| README | ✅ Tersedia (`README.md`) |
| pyproject.toml | ✅ Tersedia |
| .gitignore | ✅ Tersedia |
| LICENSE | ✅ Tersedia (MIT — nama pemegang hak cipta perlu diisi tim) |
| Source code | ✅ Tersedia dan telah diverifikasi berjalan |
| Test | ✅ Tersedia, seluruh test PASSED |
| Struktur folder rapi | ✅ Terpenuhi |
| Git commit profesional | ⚠️ **Perlu dilengkapi tim** — bergantung pada proses kerja aktual di GitHub, tidak dapat diverifikasi dari dokumen ini |

### Ringkasan Bagian yang Masih Perlu Dilengkapi Tim

1. Data identitas lengkap seluruh anggota kelompok (nama, NIM, kode
   kelompok) pada halaman judul dan `README.md`.
2. Membuat repositori GitHub sesungguhnya, melakukan commit sesuai struktur
   di atas, dan mencantumkan tautannya pada dokumen serahan.
3. Mengisi nama pemegang hak cipta pada `LICENSE`.
4. Jika tersedia data operasional nyata IT Del di kemudian hari (mis. dari
   unit sarana-prasarana), pertimbangkan menyesuaikan angka cost pada
   `graph.py` agar merepresentasikan estimasi waktu yang lebih akurat,
   bukan sekadar asumsi desain kualitatif.
