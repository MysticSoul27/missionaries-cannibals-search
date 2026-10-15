
"""
MISSIONARIES AND CANNIBALS
BFS + Animated River Crossing + Graph Visualizations

Install:
    python -m pip install matplotlib networkx pillow

Run:
    python missionaries_cannibals_animated.py

Output folder:
    bfs_outputs/
        river_crossing.gif
        state_space_graph.png
        state_space_tree.png
        crossing_sequence.png
        solution_report.txt
"""

from collections import deque
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Reliable GIF/PNG generation on Windows

import matplotlib.pyplot as plt
import networkx as nx

from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle, Polygon, Rectangle
from matplotlib.lines import Line2D


# ============================================================
# 1. CONFIGURATION
# ============================================================

TOTAL_M = int(input("Enter number of missionaries: "))
TOTAL_C = int(input("Enter number of cannibals: "))
BOAT_CAPACITY = int(input("Enter boat capacity: "))

if TOTAL_M < 0 or TOTAL_C < 0 or BOAT_CAPACITY < 1:
    raise ValueError("Counts cannot be negative and boat capacity must be at least 1.")

# State = (missionaries on left, cannibals on left, boat side)
# Boat: 0 = left bank, 1 = right bank
START = (TOTAL_M, TOTAL_C, 0)
GOAL = (0, 0, 1)

OUTPUT = Path("bfs_outputs")
OUTPUT.mkdir(parents=True, exist_ok=True)

NAVY = "#14213D"
BLUE = "#2878B5"
ORANGE = "#F4A261"
GREEN = "#2A9D8F"
PALE = "#F4F7FB"
RIVER = "#B8E0F2"
BANK = "#DDEBD5"
WHITE = "#FFFFFF"
WOOD = "#8D5524"
GREY = "#64748B"

FPS = 12
FRAMES_PER_CROSSING = 12


# ============================================================
# 2. STATE REPRESENTATION AND VALIDATION
# ============================================================

def label(state):
    m, c, boat = state
    return f"({m},{c},{'L' if boat == 0 else 'R'})"


def description(state):
    m, c, boat = state
    return (
        f"Left: {m}M, {c}C | "
        f"Right: {TOTAL_M - m}M, {TOTAL_C - c}C | "
        f"Boat: {'Left' if boat == 0 else 'Right'}"
    )


def valid(state):
    m, c, boat = state

    if not (0 <= m <= TOTAL_M and 0 <= c <= TOTAL_C):
        return False

    if boat not in (0, 1):
        return False

    mr = TOTAL_M - m
    cr = TOTAL_C - c

    # Cannibals must not outnumber missionaries on either
    # bank whenever missionaries are present.
    left_safe = m == 0 or m >= c
    right_safe = mr == 0 or mr >= cr

    return left_safe and right_safe


# Every possible non-empty boat load of at most two people.
LOADS = sorted(
    [
        (m, c)
        for m in range(BOAT_CAPACITY + 1)
        for c in range(BOAT_CAPACITY + 1)
        if 1 <= m + c <= BOAT_CAPACITY
    ],
    key=lambda item: (sum(item), item[0]),
    reverse=True,
)


def successors(state):
    """Return every legal next state and its crossing description."""
    m, c, boat = state
    result = []

    for bm, bc in LOADS:

        if boat == 0:
            nxt = (m - bm, c - bc, 1)
            direction = "Left -> Right"
        else:
            nxt = (m + bm, c + bc, 0)
            direction = "Right -> Left"

        if valid(nxt):
            move = f"{bm}M + {bc}C | {direction}"
            result.append((nxt, move))

    return result


# ============================================================
# 3. BREADTH-FIRST SEARCH
# ============================================================

def bfs():
    queue = deque([START])
    visited = {START}

    parent = {START: None}
    move_used = {}
    depth = {START: 0}

    explored = []
    discovery = [START]

    while queue:
        current = queue.popleft()
        explored.append(current)

        if current == GOAL:
            break

        for nxt, move in successors(current):
            if nxt in visited:
                continue

            visited.add(nxt)
            parent[nxt] = current
            move_used[nxt] = move
            depth[nxt] = depth[current] + 1

            discovery.append(nxt)
            queue.append(nxt)

    if GOAL not in parent:
        raise RuntimeError("BFS could not find a solution.")

    # Reconstruct shortest path using parent pointers.
    path = []
    moves = []
    current = GOAL

    while current is not None:
        path.append(current)
        previous = parent[current]

        if previous is not None:
            moves.append(move_used[current])

        current = previous

    path.reverse()
    moves.reverse()

    return path, moves, explored, parent, discovery, depth


# ============================================================
# 4. GRAPH AND TREE CONSTRUCTION
# ============================================================

def make_graph(discovery):
    graph = nx.DiGraph()
    discovered = set(discovery)

    for state in discovery:
        graph.add_node(state)

        for nxt, move in successors(state):
            if nxt in discovered:
                graph.add_edge(state, nxt, move=move)

    return graph


def make_tree(parent):
    tree = nx.DiGraph()

    for state, previous in parent.items():
        tree.add_node(state)

        if previous is not None:
            tree.add_edge(previous, state)

    return tree


def layered_positions(graph, depth):
    """Arrange states in horizontal layers according to BFS depth."""
    layers = {}

    for node in graph.nodes:
        layers.setdefault(depth[node], []).append(node)

    pos = {}

    for level, nodes in sorted(layers.items()):
        nodes.sort(key=lambda s: (s[2], s[0], s[1]))
        width = max(2.5, (len(nodes) - 1) * 2.0)

        if len(nodes) == 1:
            xs = [0.0]
        else:
            xs = [
                -width / 2 + i * width / (len(nodes) - 1)
                for i in range(len(nodes))
            ]

        for x, node in zip(xs, nodes):
            pos[node] = (x, -level * 1.6)

    return pos


# ============================================================
# 5. STATE-SPACE GRAPH
# ============================================================

def draw_graph(graph, path, depth):
    pos = layered_positions(graph, depth)

    path_nodes = set(path)
    path_edges = list(zip(path[:-1], path[1:]))

    fig, ax = plt.subplots(figsize=(16, 10), facecolor=PALE)
    ax.set_facecolor(PALE)

    ax.set_title(
        "STATE-SPACE GRAPH | BFS SHORTEST PATH",
        fontsize=18,
        fontweight="bold",
        color=NAVY,
        pad=20,
    )

    normal = [n for n in graph if n not in path_nodes]
    middle = [n for n in path if n not in (START, GOAL)]

    nx.draw_networkx_edges(
        graph,
        pos,
        ax=ax,
        edge_color="#B7C2CE",
        width=1.1,
        arrows=True,
        arrowsize=13,
        connectionstyle="arc3,rad=0.05",
    )

    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=path_edges,
        ax=ax,
        edge_color=GREEN,
        width=3.2,
        arrows=True,
        arrowsize=18,
    )

    nx.draw_networkx_nodes(
        graph,
        pos,
        nodelist=normal,
        ax=ax,
        node_color="#DCE6F1",
        edgecolors="#7B8FA1",
        node_size=1250,
    )

    nx.draw_networkx_nodes(
        graph,
        pos,
        nodelist=middle,
        ax=ax,
        node_color="#B7E4C7",
        edgecolors=GREEN,
        node_size=1450,
        linewidths=2,
    )

    nx.draw_networkx_nodes(
        graph,
        pos,
        nodelist=[START],
        ax=ax,
        node_color=BLUE,
        edgecolors=NAVY,
        node_size=1650,
    )

    nx.draw_networkx_nodes(
        graph,
        pos,
        nodelist=[GOAL],
        ax=ax,
        node_color=ORANGE,
        edgecolors=NAVY,
        node_size=1650,
    )

    nx.draw_networkx_labels(
        graph,
        pos,
        labels={n: label(n) for n in graph},
        ax=ax,
        font_size=8,
        font_weight="bold",
        font_color=NAVY,
    )

    legend_items = [
        Line2D(
            [0], [0], marker="o", color="w",
            markerfacecolor=BLUE, markersize=12, label="Start"
        ),
        Line2D(
            [0], [0], marker="o", color="w",
            markerfacecolor=ORANGE, markersize=12, label="Goal"
        ),
        Line2D(
            [0], [0], color=GREEN, linewidth=3,
            label="Shortest path"
        ),
        Line2D(
            [0], [0], color="#B7C2CE", linewidth=2,
            label="Other legal transitions"
        ),
    ]

    ax.legend(handles=legend_items, loc="upper right")
    ax.text(
        0.01,
        0.02,
        "State = (missionaries left, cannibals left, boat side L/R)",
        transform=ax.transAxes,
        fontsize=10,
        color=NAVY,
    )

    ax.axis("off")
    fig.tight_layout()

    fig.savefig(
        OUTPUT / "state_space_graph.png",
        dpi=200,
        bbox_inches="tight",
        facecolor=PALE,
    )

    plt.close(fig)


# ============================================================
# 6. BFS STATE-SPACE TREE
# ============================================================

def draw_tree(parent, path, depth):
    tree = make_tree(parent)
    pos = layered_positions(tree, depth)

    path_nodes = set(path)
    path_edges = list(zip(path[:-1], path[1:]))

    fig, ax = plt.subplots(figsize=(16, 10), facecolor=PALE)
    ax.set_facecolor(PALE)

    ax.set_title(
        "BFS STATE-SPACE TREE | DISCOVERY ORDER",
        fontsize=18,
        fontweight="bold",
        color=NAVY,
        pad=20,
    )

    normal = [n for n in tree if n not in path_nodes]
    middle = [n for n in path if n not in (START, GOAL)]

    nx.draw_networkx_edges(
        tree, pos, ax=ax,
        edge_color="#AAB4C0", width=1.5, arrows=False
    )

    nx.draw_networkx_edges(
        tree, pos, edgelist=path_edges, ax=ax,
        edge_color=GREEN, width=3.2, arrows=False
    )

    nx.draw_networkx_nodes(
        tree, pos, nodelist=normal, ax=ax,
        node_color="#DCE6F1", edgecolors="#7B8FA1",
        node_size=1250
    )

    nx.draw_networkx_nodes(
        tree, pos, nodelist=middle, ax=ax,
        node_color="#B7E4C7", edgecolors=GREEN,
        node_size=1450, linewidths=2
    )

    nx.draw_networkx_nodes(
        tree, pos, nodelist=[START], ax=ax,
        node_color=BLUE, edgecolors=NAVY, node_size=1650
    )

    nx.draw_networkx_nodes(
        tree, pos, nodelist=[GOAL], ax=ax,
        node_color=ORANGE, edgecolors=NAVY, node_size=1650
    )

    nx.draw_networkx_labels(
        tree, pos,
        labels={n: label(n) for n in tree},
        ax=ax, font_size=8, font_weight="bold",
        font_color=NAVY
    )

    ax.text(
        0.01, 0.02,
        "Each edge represents a first-discovery parent relationship.",
        transform=ax.transAxes, fontsize=10, color=NAVY
    )

    ax.axis("off")
    fig.tight_layout()

    fig.savefig(
        OUTPUT / "state_space_tree.png",
        dpi=200,
        bbox_inches="tight",
        facecolor=PALE,
    )

    plt.close(fig)


# ============================================================
# 7. POPULATION CHANGE CHART
# ============================================================

def draw_crossing_chart(path):
    steps = list(range(len(path)))
    m_values = [s[0] for s in path]
    c_values = [s[1] for s in path]

    fig, ax = plt.subplots(figsize=(12, 5.5), facecolor=PALE)
    ax.set_facecolor(PALE)

    ax.plot(
        steps, m_values, marker="o", linewidth=2.8,
        color=BLUE, label="Missionaries on left bank"
    )

    ax.plot(
        steps, c_values, marker="s", linewidth=2.8,
        color=ORANGE, label="Cannibals on left bank"
    )

    ax.set_title(
        "POPULATION CHANGE DURING THE SHORTEST SOLUTION",
        fontsize=15, fontweight="bold", color=NAVY, pad=15
    )

    ax.set_xlabel("State / crossing number")
    ax.set_ylabel("People on left bank")
    ax.set_xticks(steps)
    # ax.set_yticks(range(4))
    # ax.set_ylim(-0.2, 3.3)
    max_people = max(TOTAL_M, TOTAL_C)

    ax.set_yticks(range(max_people + 1))
    ax.set_ylim(-0.2, max_people + 0.3)
    ax.grid(alpha=0.25, linestyle="--")
    ax.legend()

    fig.tight_layout()

    fig.savefig(
        OUTPUT / "crossing_sequence.png",
        dpi=200,
        bbox_inches="tight",
        facecolor=PALE,
    )

    plt.close(fig)


# ============================================================
# 8. PERSON DRAWING HELPERS
# ============================================================

def add_person(ax, x, y, color, scale=1.0):
    """Draw a stick figure and return its artists."""
    artists = [
        Circle(
            (x, y + 0.23 * scale),
            0.085 * scale,
            color=color,
            zorder=6,
        ),
        Line2D(
            [x, x],
            [y - 0.02 * scale, y + 0.15 * scale],
            color=color,
            linewidth=2.8 * scale,
            solid_capstyle="round",
            zorder=6,
        ),
        Line2D(
            [x - 0.09 * scale, x + 0.09 * scale],
            [y + 0.10 * scale, y + 0.10 * scale],
            color=color,
            linewidth=2.0 * scale,
            zorder=6,
        ),
        Line2D(
            [x, x - 0.07 * scale],
            [y - 0.02 * scale, y - 0.12 * scale],
            color=color,
            linewidth=2.0 * scale,
            zorder=6,
        ),
        Line2D(
            [x, x + 0.07 * scale],
            [y - 0.02 * scale, y - 0.12 * scale],
            color=color,
            linewidth=2.0 * scale,
            zorder=6,
        ),
    ]

    for artist in artists:
        if isinstance(artist, Circle):
            ax.add_patch(artist)
        else:
            ax.add_line(artist)

    return artists


# ============================================================
# 9. ANIMATED RIVER CROSSING
# ============================================================

def create_animation(path, moves):
    """
    Create a smooth animated river crossing and save a GIF.

    Important fixes:
    - Uses integer frame indices instead of tuple frame objects.
    - Keeps the static scenery and boat artists persistent.
    - Removes only temporary people and labels each frame.
    - Saves explicitly through PillowWriter.
    """

    if len(path) < 2:
        raise ValueError("The solution path must contain a crossing.")

    fig, ax = plt.subplots(figsize=(13, 7), facecolor=PALE)
    ax.set_facecolor(PALE)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")

    # Background scenery: draw once.
    ax.add_patch(Rectangle((0, 0), 12, 7, color=PALE, zorder=0))
    ax.add_patch(Rectangle((0, 0.5), 12, 2.0, color=RIVER, zorder=1))
    ax.add_patch(Rectangle((0, 2.5), 2.7, 4.0, color=BANK, zorder=2))
    ax.add_patch(Rectangle((9.3, 2.5), 2.7, 4.0, color=BANK, zorder=2))

    ax.text(
        1.35, 6.25, "LEFT BANK", ha="center",
        fontsize=13, color=NAVY, fontweight="bold"
    )

    ax.text(
        10.65, 6.25, "RIGHT BANK", ha="center",
        fontsize=13, color=NAVY, fontweight="bold"
    )

    ax.text(
        6, 6.55, "MISSIONARIES & CANNIBALS",
        ha="center", fontsize=17, color=NAVY, fontweight="bold"
    )

    status = ax.text(
        6, 5.85, "", ha="center", fontsize=11, color=NAVY
    )

    move_status = ax.text(
        6, 0.18, "", ha="center", fontsize=11,
        color=NAVY, fontweight="bold",
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor=WHITE,
            edgecolor="#CBD5E1"
        )
    )

    # Boat hull.
    boat_hull = Polygon(
        [[4.4, 1.6], [5.8, 1.6], [5.55, 1.15], [4.65, 1.15]],
        closed=True, color=WOOD, zorder=5
    )
    ax.add_patch(boat_hull)

    # Mast and sail.
    mast = Line2D(
        [5.1, 5.1], [1.6, 2.15],
        color=WOOD, linewidth=3, zorder=5
    )
    ax.add_line(mast)

    sail = Polygon(
        [[5.12, 2.12], [5.12, 1.65], [5.52, 1.7]],
        closed=True, color=WHITE, zorder=5
    )
    ax.add_patch(sail)

    # Passenger circles are reused rather than recreated.
    
    passengers = [
      Circle(
        (4.9 + j * 0.42, 1.78),
        0.075,
        color=BLUE,
        zorder=8
    )
    for j in range(BOAT_CAPACITY)
  ]


    for passenger in passengers:
        ax.add_patch(passenger)

    total_frames = (len(path) - 1) * FRAMES_PER_CROSSING + 1
    dynamic_artists = []

    def update(frame):
        nonlocal dynamic_artists

        # Remove temporary people and labels from the previous frame.
        for artist in dynamic_artists:
            try:
                artist.remove()
            except ValueError:
                pass

        dynamic_artists = []

        # Convert a single integer frame number into a crossing and alpha.
        if frame == total_frames - 1:
            crossing_index = len(path) - 2
            alpha = 1.0
        else:
            crossing_index = frame // FRAMES_PER_CROSSING
            alpha = (
                frame % FRAMES_PER_CROSSING
            ) / FRAMES_PER_CROSSING

        start_state = path[crossing_index]
        end_state = path[crossing_index + 1]

        # People change banks only after the boat arrives.
        displayed_state = end_state if alpha >= 1.0 else start_state

        m_left, c_left, _ = displayed_state
        m_right = TOTAL_M - m_left
        c_right = TOTAL_C - c_left

        def draw_bank(m_count, c_count, center):
            # positions = [
            #     center - 0.55,
            #     center,
            #     center + 0.55,
            # ]
            spacing = min(0.55, 2.0 / max(m_count, c_count, 1))

            positions = [
                center + (j - (max(m_count, c_count, 1) - 1) / 2) * spacing
                for j in range(max(m_count, c_count, 1))
            ]

            for j in range(m_count):
                dynamic_artists.extend(
                    add_person(ax, positions[j], 4.05, BLUE)
                )

            for j in range(c_count):
                dynamic_artists.extend(
                    add_person(ax, positions[j], 2.85, ORANGE)
                )

            dynamic_artists.append(
                ax.text(
                    center, 4.62, f"{m_count} Missionaries",
                    ha="center", color=NAVY, fontsize=10,
                    fontweight="bold"
                )
            )

            dynamic_artists.append(
                ax.text(
                    center, 3.37, f"{c_count} Cannibals",
                    ha="center", color=NAVY, fontsize=10,
                    fontweight="bold"
                )
            )

        draw_bank(m_left, c_left, 1.35)
        draw_bank(m_right, c_right, 10.65)

        # Move the boat between the two river positions.
        boat_from = 3.1 if start_state[2] == 0 else 7.5
        boat_to = 7.5 if start_state[2] == 0 else 3.1

        boat_x = boat_from + (boat_to - boat_from) * alpha
        dx = boat_x - 4.4

        boat_hull.set_xy([
            [4.4 + dx, 1.6],
            [5.8 + dx, 1.6],
            [5.55 + dx, 1.15],
            [4.65 + dx, 1.15],
        ])

        mast.set_data(
            [5.1 + dx, 5.1 + dx],
            [1.6, 2.15]
        )

        sail.set_xy([
            [5.12 + dx, 2.12],
            [5.12 + dx, 1.65],
            [5.52 + dx, 1.7],
        ])

        # Determine passengers from the difference between states.
        bm = abs(start_state[0] - end_state[0])
        bc = abs(start_state[1] - end_state[1])

        passenger_colors = [BLUE] * bm + [ORANGE] * bc

        for j, passenger in enumerate(passengers):
            if alpha < 1.0 and j < len(passenger_colors):
                passenger.set_visible(True)
                passenger.set_color(passenger_colors[j])
                passenger.center = (
                    4.85 + dx + j * 0.42,
                    1.78
                )
            else:
                passenger.set_visible(False)

        crossing_number = min(crossing_index + 1, len(path) - 1)

        status.set_text(
            f"Crossing {crossing_number} / {len(path) - 1}"
            f"   |   {description(displayed_state)}"
        )

        if frame == 0:
            move_status.set_text("Initial configuration")
        elif alpha >= 1.0 and crossing_index == len(moves) - 1:
            move_status.set_text("Goal reached!")
        else:
            move_status.set_text(moves[crossing_index])

        return (
            [boat_hull, mast, sail, status, move_status]
            + passengers
            + dynamic_artists
        )

    # The key fix: a reliable sequence of integer frames.
    anim = FuncAnimation(
        fig,
        update,
        frames=range(total_frames),
        interval=1000 // FPS,
        blit=False,
        repeat=False,
        cache_frame_data=False,
    )

    gif_path = OUTPUT / "river_crossing.gif"

    print(f"\nSaving GIF to: {gif_path.resolve()}")

    try:
        anim.save(
            str(gif_path),
            writer=PillowWriter(fps=FPS),
            dpi=100,
        )
    finally:
        plt.close(fig)

    print("GIF saved successfully.")
    return gif_path


# ============================================================
# 10. SAVE SOLUTION REPORT
# ============================================================

def save_report(path, moves, explored, depth):
    report = OUTPUT / "solution_report.txt"

    with report.open("w", encoding="utf-8") as file:
        file.write("MISSIONARIES AND CANNIBALS - BFS REPORT\n")
        file.write("=" * 65 + "\n")
        file.write(
            "State = (missionaries left, cannibals left, boat L/R)\n"
        )
        file.write(f"Initial state: {label(START)}\n")
        file.write(f"Goal state: {label(GOAL)}\n")
        file.write(f"Minimum crossings: {len(path) - 1}\n\n")

        file.write("SHORTEST PATH\n")
        file.write("-" * 65 + "\n")

        for i, state in enumerate(path):
            file.write(
                f"Step {i}: {label(state)} | {description(state)}\n"
            )

            if i > 0:
                file.write(f"    Move: {moves[i - 1]}\n")

        file.write("\nBFS EXPLORATION ORDER\n")
        file.write("-" * 65 + "\n")

        for i, state in enumerate(explored, start=1):
            file.write(
                f"{i}. {label(state)} | depth={depth[state]} | "
                f"{description(state)}\n"
            )

    return report


# ============================================================
# 11. CONSOLE OUTPUT
# ============================================================

def print_solution(path, moves, explored, depth):
    print("\n" + "=" * 80)
    print("MISSIONARIES AND CANNIBALS - BFS SOLUTION")
    print("=" * 80)

    print(f"Minimum crossings: {len(path) - 1}")
    print(f"States discovered: {len(depth)}")
    print(f"States dequeued: {len(explored)}")

    print("\nSHORTEST PATH")
    print("-" * 80)

    for i, state in enumerate(path):
        print(
            f"Step {i:02}: {label(state):10} | "
            f"{description(state)}"
        )

        if i > 0:
            print(f"      Move: {moves[i - 1]}")

    print("\nBFS EXPLORATION ORDER")
    print("-" * 80)

    for i, state in enumerate(explored, start=1):
        print(
            f"{i:02}. {label(state):10} | "
            f"Depth {depth[state]} | {description(state)}"
        )


# ============================================================
# 12. MAIN PROGRAM
# ============================================================

def main():
    path, moves, explored, parent, discovery, depth = bfs()

    print_solution(path, moves, explored, depth)

    graph = make_graph(discovery)

    print("\nGenerating static visualizations...")

    draw_graph(graph, path, depth)
    draw_tree(parent, path, depth)
    draw_crossing_chart(path)

    report = save_report(path, moves, explored, depth)

    print("\nGenerating animated river crossing...")

    gif_path = create_animation(path, moves)

    print("\nPROJECT OUTPUTS")
    print("-" * 60)

    for output_file in [
        gif_path,
        OUTPUT / "state_space_graph.png",
        OUTPUT / "state_space_tree.png",
        OUTPUT / "crossing_sequence.png",
        report,
    ]:
        print(output_file.resolve())

    print("\nCompleted successfully.")
    print("Open the GIF in a browser to view the animation.")


if __name__ == "__main__":
    main()
