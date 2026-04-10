import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(2, 3, figsize=(12, 7))
fig.patch.set_facecolor("white")


# Square drawing helper
def draw_square(ax, corners, labels, title="", highlight_color="#4a90d9"):
    """Draw a square with labeled corners.
    corners: dict with keys 'tl','tr','bl','br' mapping to label strings
    labels positions: tl=top-left, tr=top-right, bl=bottom-left, br=bottom-right
    """
    ax.set_xlim(-0.6, 1.6)
    ax.set_ylim(-0.6, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")

    # Draw the square
    sq = patches.FancyBboxPatch(
        (0, 0),
        1,
        1,
        boxstyle="round,pad=0.02",
        linewidth=2,
        edgecolor=highlight_color,
        facecolor=highlight_color + "20",
    )
    ax.add_patch(sq)

    # Corner label positions
    offsets = {
        "tl": (-0.15, 1.15),
        "tr": (1.15, 1.15),
        "bl": (-0.15, -0.15),
        "br": (1.15, -0.15),
    }
    for key, (x, y) in offsets.items():
        ax.text(
            x,
            y,
            corners[key],
            fontsize=16,
            fontweight="bold",
            ha="center",
            va="center",
            color="#333333",
            bbox=dict(
                boxstyle="round,pad=0.15",
                facecolor="white",
                edgecolor="#999999",
                linewidth=0.8,
            ),
        )

    # Corner dots
    dot_pos = {"tl": (0, 1), "tr": (1, 1), "bl": (0, 0), "br": (1, 0)}
    for key, (x, y) in dot_pos.items():
        ax.plot(x, y, "o", color=highlight_color, markersize=6, zorder=5)

    if title:
        ax.set_title(title, fontsize=12, fontweight="bold", pad=10, color="#333333")


# --- Starting square ---
start = {"tl": "A", "tr": "B", "bl": "D", "br": "C"}

# --- Path 1: Rotate 90° CW then reflect across vertical axis ---
# After 90° CW rotation: A→B→C→D maps to D→A→B→C positionally
# tl was A, goes to tr; tr was B, goes to br; br was C, goes to bl; bl was D, goes to tl
rot90 = {"tl": "D", "tr": "A", "bl": "C", "br": "B"}
# After vertical axis reflection (swap left↔right columns):
rot90_then_reflect = {"tl": "A", "tr": "D", "bl": "B", "br": "C"}

# --- Path 2: Reflect across vertical axis then rotate 90° CW ---
# After reflect vertical (swap left↔right):
reflect = {"tl": "B", "tr": "A", "bl": "C", "br": "D"}
# After 90° CW rotation:
reflect_then_rot90 = {"tl": "C", "tr": "B", "bl": "D", "br": "A"}

# Colors for the two paths
color1 = "#2e86de"
color2 = "#e55039"

# --- Row 1: Rotate then Reflect ---
draw_square(axes[0, 0], start, None, "Start", color1)
draw_square(axes[0, 1], rot90, None, "After Rotate 90° CW", color1)
draw_square(axes[0, 2], rot90_then_reflect, None, "Then Reflect Vertical", color1)

# --- Row 2: Reflect then Rotate ---
draw_square(axes[1, 0], start, None, "Start", color2)
draw_square(axes[1, 1], reflect, None, "After Reflect Vertical", color2)
draw_square(axes[1, 2], reflect_then_rot90, None, "Then Rotate 90° CW", color2)

# Add arrows between columns using a hidden axes spanning the full figure
arrow_ax = fig.add_axes([0, 0, 1, 1], facecolor="none")
arrow_ax.set_xlim(0, 1)
arrow_ax.set_ylim(0, 1)
arrow_ax.axis("off")

for row in range(2):
    for col in range(2):
        ax_curr = axes[row, col]
        ax_next = axes[row, col + 1]

        pos_curr = ax_curr.get_position()
        pos_next = ax_next.get_position()

        arrow_y = pos_curr.y0 + pos_curr.height / 2
        arrow_x0 = pos_curr.x1 + 0.008
        arrow_x1 = pos_next.x0 - 0.008

        color = color1 if row == 0 else color2
        arrow_ax.annotate(
            "",
            xy=(arrow_x1, arrow_y),
            xytext=(arrow_x0, arrow_y),
            arrowprops=dict(
                arrowstyle="->,head_width=0.4,head_length=0.3", color=color, lw=2.5
            ),
        )

# Row labels on the left
fig.text(
    0.02,
    0.72,
    "Path 1",
    fontsize=14,
    fontweight="bold",
    color=color1,
    ha="center",
    va="center",
    rotation=90,
)
fig.text(
    0.02,
    0.28,
    "Path 2",
    fontsize=14,
    fontweight="bold",
    color=color2,
    ha="center",
    va="center",
    rotation=90,
)

# Title
fig.suptitle(
    "Non-Commutativity of Square Symmetries",
    fontsize=16,
    fontweight="bold",
    y=0.97,
    color="#222222",
)
fig.text(
    0.5,
    0.92,
    "Rotate then Reflect  ≠  Reflect then Rotate",
    fontsize=12,
    ha="center",
    color="#555555",
    style="italic",
)

plt.tight_layout(rect=[0.04, 0.02, 1.0, 0.90])
plt.savefig("squares.png", dpi=180, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved squares.png")
