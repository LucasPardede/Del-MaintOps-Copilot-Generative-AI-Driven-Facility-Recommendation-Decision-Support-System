"""
ucs.py
------
Implementasi Uniform Cost Search (UCS) untuk baseline Milestone 1
Del-MaintOps Copilot.

Mengapa UCS, bukan A*?
Dijelaskan lengkap pada laporan Milestone 1 (Bab 5.1), ringkasnya:
graf Del-MaintOps bersifat kategorikal/simbolik (tahap penanganan,
bukan koordinat spasial), sehingga tidak tersedia fungsi heuristik
h(n) yang admissible secara alami tanpa mengarang angka estimasi.
Daripada memaksakan heuristik yang tidak dapat dipertanggungjawabkan,
Milestone 1 memilih UCS sebagai baseline yang correct dan optimal
untuk graf berbobot non-negatif, sekaligus jujur terhadap keterbatasan
data yang tersedia saat ini.

UCS mengembangkan node berdasarkan cumulative path cost g(n) terkecil
menggunakan priority queue (heapq). Karena seluruh bobot pada graph.py
bernilai non-negatif, UCS dijamin menemukan jalur dengan total cost
minimum (optimal), setara dengan Dijkstra's algorithm dari satu
sumber (single-source shortest path).
"""

import heapq
import itertools
from typing import List, Optional, Tuple

from .graph import Graph


class SearchResult:
    """Struktur hasil pencarian, memuat path, total cost, dan
    jumlah node yang di-expand (untuk analisis kompleksitas)."""

    def __init__(
        self,
        path: Optional[List[str]],
        total_cost: float,
        actions: Optional[List[str]],
        nodes_expanded: int,
        found: bool,
    ):
        self.path = path
        self.total_cost = total_cost
        self.actions = actions
        self.nodes_expanded = nodes_expanded
        self.found = found

    def __repr__(self) -> str:
        if not self.found:
            return (
                f"SearchResult(found=False, nodes_expanded={self.nodes_expanded})"
            )
        return (
            f"SearchResult(path={self.path}, total_cost={self.total_cost}, "
            f"nodes_expanded={self.nodes_expanded})"
        )


def uniform_cost_search(
    graph: Graph, start: str, goal: str, verbose: bool = False
) -> SearchResult:
    """Menjalankan Uniform Cost Search dari `start` menuju `goal`.

    Parameters
    ----------
    graph : Graph
        Instance graf masalah (lihat graph.py).
    start : str
        Node awal (state awal / initial state).
    goal : str
        Node tujuan (goal state).
    verbose : bool
        Jika True, mencetak proses expand setiap node ke stdout
        (berguna untuk demonstrasi/debugging, bukan untuk assertion test).

    Returns
    -------
    SearchResult
        found=False jika goal tidak dapat dijangkau dari start
        (mis. graf tidak terhubung / goal tidak eksis).
    """
    nodes_expanded = 0

    if not graph.has_node(start) or not graph.has_node(goal):
        # Start atau goal tidak dikenal sama sekali oleh graf.
        return SearchResult(None, float("inf"), None, nodes_expanded, False)

    # Priority queue berisi tuple (cumulative_cost, tie_breaker, node, path, actions)
    # tie_breaker (counter) mencegah heapq membandingkan list/tuple saat cost sama.
    counter = itertools.count()
    frontier: List[Tuple[float, int, str, List[str], List[str]]] = []
    heapq.heappush(frontier, (0.0, next(counter), start, [start], []))

    # best_cost menyimpan cost termurah yang PERNAH ditemukan menuju suatu
    # node saat node itu di-*pop* dari frontier (bukan saat di-push),
    # agar node dengan multiple entry di frontier ditangani dengan benar.
    visited_with_cost = {}

    while frontier:
        cost_so_far, _, node, path, actions = heapq.heappop(frontier)

        # Lazy deletion: abaikan entry usang jika sudah pernah di-visit
        # dengan cost yang sama atau lebih murah.
        if node in visited_with_cost and visited_with_cost[node] <= cost_so_far:
            continue
        visited_with_cost[node] = cost_so_far
        nodes_expanded += 1

        if verbose:
            print(f"[expand #{nodes_expanded}] node={node} g(n)={cost_so_far}")

        if node == goal:
            return SearchResult(path, cost_so_far, actions, nodes_expanded, True)

        for neighbor, edge_cost, label in graph.neighbors(node):
            new_cost = cost_so_far + edge_cost
            if neighbor in visited_with_cost and visited_with_cost[neighbor] <= new_cost:
                continue
            heapq.heappush(
                frontier,
                (new_cost, next(counter), neighbor, path + [neighbor], actions + [label]),
            )

    # Frontier habis tanpa menemukan goal -> goal tidak dapat dijangkau.
    return SearchResult(None, float("inf"), None, nodes_expanded, False)
