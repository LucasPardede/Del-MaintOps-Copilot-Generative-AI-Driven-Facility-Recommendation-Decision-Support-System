"""
test_search.py
---------------
Test case untuk baseline UCS Del-MaintOps Copilot (Milestone 1).

Jalankan dengan:
    uv run pytest

Catatan: nilai expected_cost pada file ini dihitung manual dari bobot
yang didefinisikan di src/search/graph.py (lihat dokumen Milestone 1,
Bab 5.5, tabel test case, untuk perhitungan lengkapnya). Nilai-nilai
ini BUKAN hasil karangan — bisa diverifikasi ulang dengan menjumlahkan
bobot edge di sepanjang path yang diharapkan.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from search import build_del_maintops_graph, uniform_cost_search  # noqa: E402


def test_case_1_normal_electrical_report():
    """Test Case 1 - Normal: laporan kerusakan listrik biasa.

    Jalur termurah yang diharapkan:
    LAPORAN -> KLAS_ELEC -> DIAG_ELEC -> SOP_ELEC_OK -> TEK_ELEC_LOKAL -> SELESAI_ELEC
    Cost = 2 + 4 + 3 + 5 + 10 = 24
    """
    graph = build_del_maintops_graph()
    result = uniform_cost_search(graph, "LAPORAN", "SELESAI_ELEC")

    assert result.found is True
    assert result.path == [
        "LAPORAN",
        "KLAS_ELEC",
        "DIAG_ELEC",
        "SOP_ELEC_OK",
        "TEK_ELEC_LOKAL",
        "SELESAI_ELEC",
    ]
    assert result.total_cost == 24


def test_case_2_alternative_path_hvac_report():
    """Test Case 2 - Jalur Alternatif: laporan HVAC memiliki >1 jalur
    menuju goal (via SOP_HVAC_OK/TEK_HVAC_LOKAL, via TEK_HVAC_LUAR,
    atau via eskalasi SOP_HVAC_ESK). Algoritma harus memilih cost
    terendah.

    Jalur termurah yang diharapkan:
    LAPORAN -> KLAS_HVAC -> DIAG_HVAC -> SOP_HVAC_OK -> TEK_HVAC_LOKAL -> SELESAI_HVAC
    Cost = 2 + 4 + 3 + 6 + 12 = 27

    Jalur alternatif yang harus DIHINDARI karena lebih mahal:
    - via TEK_HVAC_LUAR: 2+4+3+16+20 = 45
    - via SOP_HVAC_ESK -> TEK_HVAC_LUAR: 2+4+7+10+20 = 43
    """
    graph = build_del_maintops_graph()
    result = uniform_cost_search(graph, "LAPORAN", "SELESAI_HVAC")

    assert result.found is True
    assert result.path == [
        "LAPORAN",
        "KLAS_HVAC",
        "DIAG_HVAC",
        "SOP_HVAC_OK",
        "TEK_HVAC_LOKAL",
        "SELESAI_HVAC",
    ]
    assert result.total_cost == 27
    # Pastikan algoritma benar-benar membandingkan, bukan kebetulan cocok:
    assert result.total_cost < 45
    assert result.total_cost < 43


def test_case_3_edge_case_unreachable_goal():
    """Test Case 3 - Edge Case: goal berada pada komponen graf yang
    terisolasi (LAPORAN_ARSIP -> SELESAI_ARSIP), tidak terhubung dari
    LAPORAN. Algoritma harus mengembalikan found=False, bukan error
    atau path yang salah."""
    graph = build_del_maintops_graph()
    result = uniform_cost_search(graph, "LAPORAN", "SELESAI_ARSIP")

    assert result.found is False
    assert result.path is None
    assert result.total_cost == float("inf")


def test_case_3b_edge_case_dead_end_no_sop():
    """Edge case tambahan: ISOLATED_NET adalah dead end (tidak punya
    outgoing edge) karena belum ada SOP terdaftar. Mencari goal
    SELESAI_NET dari LAPORAN tetap harus berhasil lewat jalur SOP_NET_OK,
    membuktikan algoritma tidak "terjebak" di dead end."""
    graph = build_del_maintops_graph()
    result = uniform_cost_search(graph, "LAPORAN", "SELESAI_NET")

    assert result.found is True
    assert "ISOLATED_NET" not in result.path
    assert result.total_cost == 2 + 4 + 3 + 4 + 8  # = 21


def test_unknown_node_returns_not_found():
    """Edge case: start atau goal yang tidak dikenal graf sama sekali
    harus ditangani dengan anggun (found=False), bukan exception."""
    graph = build_del_maintops_graph()
    result = uniform_cost_search(graph, "LAPORAN", "NODE_TIDAK_ADA")

    assert result.found is False
    assert result.nodes_expanded == 0
