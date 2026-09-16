"""
main.py
-------
Entry point CLI untuk mendemonstrasikan baseline search Del-MaintOps
Copilot Milestone 1.

Jalankan dengan:
    uv run python src/main.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from search import build_del_maintops_graph, uniform_cost_search  # noqa: E402


def print_result(title: str, start: str, goal: str, result) -> None:
    print("=" * 70)
    print(title)
    print(f"Start : {start}")
    print(f"Goal  : {goal}")
    print("-" * 70)
    if not result.found:
        print("Hasil : GOAL TIDAK DITEMUKAN (no path)")
    else:
        print(f"Path  : {' -> '.join(result.path)}")
        print(f"Cost  : {result.total_cost}")
        print("Aksi yang diambil di sepanjang jalur:")
        for i, action in enumerate(result.actions, start=1):
            print(f"  {i}. {action}")
    print(f"Node yang di-expand: {result.nodes_expanded}")
    print("=" * 70)
    print()


def main() -> None:
    graph = build_del_maintops_graph()

    # Test Case 1 - Normal: laporan kerusakan listrik biasa
    r1 = uniform_cost_search(graph, "LAPORAN", "SELESAI_ELEC")
    print_result("Test Case 1 (Normal) - Laporan Kerusakan Listrik", "LAPORAN", "SELESAI_ELEC", r1)

    # Test Case 2 - Jalur alternatif: HVAC punya banyak jalur menuju goal,
    # algoritma harus memilih total cost termurah.
    r2 = uniform_cost_search(graph, "LAPORAN", "SELESAI_HVAC")
    print_result("Test Case 2 (Jalur Alternatif) - Laporan Kerusakan HVAC/AC", "LAPORAN", "SELESAI_HVAC", r2)

    # Test Case 3 - Edge case: goal berada pada komponen graf yang terisolasi,
    # tidak terjangkau dari LAPORAN.
    r3 = uniform_cost_search(graph, "LAPORAN", "SELESAI_ARSIP")
    print_result("Test Case 3 (Edge Case) - Goal Tidak Terjangkau", "LAPORAN", "SELESAI_ARSIP", r3)


if __name__ == "__main__":
    main()
