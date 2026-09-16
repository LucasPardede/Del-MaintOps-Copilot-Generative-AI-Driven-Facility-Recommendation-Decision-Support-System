"""
graph.py
--------
Representasi graf masalah untuk Del-MaintOps Copilot (Milestone 1).

Graf ini memodelkan alur penanganan laporan kerusakan fasilitas kampus
sebagai masalah pencarian (search problem):

    Node  -> merepresentasikan sebuah STATE (X): kombinasi antara
             kategori kerusakan dan tahap penanganan yang sudah dicapai.
    Edge  -> merepresentasikan sebuah ACTION (A) yang membawa sistem
             dari satu state ke state berikutnya (TRANSITION / T).
    Bobot -> merepresentasikan COST (C): estimasi waktu (dalam satuan
             menit, skala relatif) yang dibutuhkan untuk menjalankan
             action tersebut. Nilai bobot pada file ini adalah
             ASUMSI DESAIN untuk kebutuhan pengujian algoritma,
             BUKAN data historis nyata dari IT Del.

Catatan penting:
- Graf ini SENGAJA dibuat generik (bukan hardcoded jawaban akhir),
  sehingga algoritma pencarian pada ucs.py benar-benar melakukan
  eksplorasi graf, bukan sekadar mengembalikan jawaban yang ditanam.
- Terdapat lebih dari satu jalur (multi-path) menuju sebagian besar
  goal, untuk menguji kemampuan algoritma memilih jalur berbiaya
  minimum (lihat Test Case 2 pada tests/test_search.py).
- Terdapat pula komponen graf yang terisolasi (LAPORAN_ARSIP ->
  SELESAI_ARSIP) yang tidak terhubung ke komponen utama, digunakan
  untuk menguji edge case "goal tidak ditemukan" (lihat Test Case 3).
"""

from typing import Dict, List, Tuple

# Tipe: setiap node memetakan ke daftar (neighbor, cost, label_action)
Edge = Tuple[str, float, str]
AdjacencyList = Dict[str, List[Edge]]


class Graph:
    """Graf berbobot, terarah (directed weighted graph) untuk masalah
    routing/triase laporan kerusakan fasilitas Del-MaintOps."""

    def __init__(self, adjacency: AdjacencyList):
        self._adjacency = adjacency

    def nodes(self) -> List[str]:
        """Mengembalikan seluruh node yang dikenal (baik sebagai
        sumber maupun tujuan edge)."""
        all_nodes = set(self._adjacency.keys())
        for edges in self._adjacency.values():
            for neighbor, _cost, _label in edges:
                all_nodes.add(neighbor)
        return sorted(all_nodes)

    def neighbors(self, node: str) -> List[Edge]:
        """Mengembalikan daftar (neighbor, cost, label_action) dari
        sebuah node. Node tanpa outgoing edge (dead end) mengembalikan
        list kosong."""
        return self._adjacency.get(node, [])

    def has_node(self, node: str) -> bool:
        return node in self.nodes()


def build_del_maintops_graph() -> Graph:
    """Membangun instance graf Del-MaintOps yang dipakai pada Milestone 1.

    Struktur tahapan (layer) untuk setiap kategori kerusakan
    (Electrical / HVAC / Network):

        LAPORAN
           |
           v
        KLASIFIKASI (klasifikasi kategori kerusakan)
           |
           v
        DIAGNOSIS (diagnosis awal oleh teknisi/sistem)
           |
           v
        PENCOCOKAN SOP (SOP ditemukan vs eskalasi)
           |
           v
        ALOKASI TEKNISI (lokal vs eksternal/vendor)
           |
           v
        SELESAI (goal: laporan tertangani)
    """
    adjacency: AdjacencyList = {
        # --- Tahap awal: laporan masuk, lalu diklasifikasi ---
        "LAPORAN": [
            ("KLAS_ELEC", 2, "Klasifikasikan sebagai kerusakan listrik"),
            ("KLAS_HVAC", 2, "Klasifikasikan sebagai kerusakan HVAC/AC"),
            ("KLAS_NET", 2, "Klasifikasikan sebagai gangguan jaringan"),
        ],

        # ================= Kategori: ELECTRICAL =================
        "KLAS_ELEC": [
            ("DIAG_ELEC", 4, "Diagnosis awal kerusakan listrik"),
        ],
        "DIAG_ELEC": [
            ("SOP_ELEC_OK", 3, "SOP ditemukan: prosedur standar panel listrik"),
            ("SOP_ELEC_ESK", 9, "SOP tidak ditemukan: eskalasi ke teknisi senior"),
        ],
        "SOP_ELEC_OK": [
            ("TEK_ELEC_LOKAL", 5, "Alokasikan teknisi listrik lokal"),
            ("TEK_ELEC_LUAR", 14, "Teknisi lokal penuh: kontrak vendor eksternal"),
        ],
        "SOP_ELEC_ESK": [
            ("TEK_ELEC_LOKAL", 8, "Setelah eskalasi, alokasikan teknisi senior lokal"),
        ],
        "TEK_ELEC_LOKAL": [
            ("SELESAI_ELEC", 10, "Teknisi lokal menyelesaikan & menutup tiket"),
        ],
        "TEK_ELEC_LUAR": [
            ("SELESAI_ELEC", 18, "Vendor eksternal menyelesaikan & menutup tiket"),
        ],

        # ================= Kategori: HVAC / AC =================
        "KLAS_HVAC": [
            ("DIAG_HVAC", 4, "Diagnosis awal kerusakan HVAC/AC"),
        ],
        "DIAG_HVAC": [
            ("SOP_HVAC_OK", 3, "SOP ditemukan: prosedur pendinginan standar"),
            ("SOP_HVAC_ESK", 7, "SOP tidak ditemukan: eskalasi ke vendor AC"),
        ],
        "SOP_HVAC_OK": [
            ("TEK_HVAC_LOKAL", 6, "Alokasikan teknisi HVAC lokal"),
            ("TEK_HVAC_LUAR", 16, "Teknisi lokal penuh: kontrak vendor AC eksternal"),
        ],
        "SOP_HVAC_ESK": [
            ("TEK_HVAC_LUAR", 10, "Eskalasi langsung ke vendor AC (kasus kompleks)"),
        ],
        "TEK_HVAC_LOKAL": [
            ("SELESAI_HVAC", 12, "Teknisi lokal menyelesaikan & menutup tiket"),
        ],
        "TEK_HVAC_LUAR": [
            ("SELESAI_HVAC", 20, "Vendor AC eksternal menyelesaikan & menutup tiket"),
        ],

        # ================= Kategori: NETWORK =================
        "KLAS_NET": [
            ("DIAG_NET", 4, "Diagnosis awal gangguan jaringan"),
        ],
        "DIAG_NET": [
            ("SOP_NET_OK", 3, "SOP ditemukan: prosedur reset perangkat jaringan"),
            ("ISOLATED_NET", 5, "Kerusakan pada infrastruktur inti: belum ada SOP terdaftar"),
        ],
        "SOP_NET_OK": [
            ("TEK_NET_LOKAL", 4, "Alokasikan teknisi jaringan lokal"),
        ],
        "TEK_NET_LOKAL": [
            ("SELESAI_NET", 8, "Teknisi jaringan menyelesaikan & menutup tiket"),
        ],
        # ISOLATED_NET sengaja tidak memiliki outgoing edge (dead end):
        # merepresentasikan laporan yang mandek karena belum ada SOP,
        # menunggu tindak lanjut manual di luar cakupan Milestone 1.
        "ISOLATED_NET": [],

        # ================= Komponen terisolasi (untuk edge case) =================
        # Merepresentasikan domain laporan lain (mis. arsip administrasi)
        # yang TIDAK terhubung ke alur triase fasilitas di atas.
        # Dipakai untuk menguji perilaku algoritma saat goal tidak
        # dapat dijangkau dari start node manapun pada komponen utama.
        "LAPORAN_ARSIP": [
            ("SELESAI_ARSIP", 3, "Proses administrasi arsip (di luar domain fasilitas)"),
        ],
        "SELESAI_ARSIP": [],
    }
    return Graph(adjacency)
