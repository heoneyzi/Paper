"""Shared chart style for the portfolio figures (light + dark variants).

Palette: validated categorical slots 1-3 (blue, orange, aqua) and neutral inks,
checked with a CVD/contrast validator for both surfaces. Every figure is rendered
twice so a README can serve the dark file through <picture> on dark themes.
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

THEMES = {
    "light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
                  grid="#e1e0d9", axis="#c3c2b7", wash="#e9e8e2", deemph="#c3c2b7",
                  s1="#2a78d6", s2="#eb6834", s3="#1baf7a"),
    "dark": dict(surface="#1a1a19", ink="#ffffff", ink2="#c3c2b7", muted="#898781",
                 grid="#2c2c2a", axis="#383835", wash="#2f2f2c", deemph="#5b5a55",
                 s1="#3987e5", s2="#d95926", s3="#199e70"),
}


def style_axes(ax, t, grid_axis="y"):
    """Recessive chrome: hairline solid grid, no top/right spines, muted ticks."""
    ax.set_facecolor(t["surface"])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(t["axis"])
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(colors=t["muted"], labelcolor=t["ink2"], labelsize=9, length=3, width=0.8)
    if grid_axis:
        ax.grid(axis=grid_axis, color=t["grid"], linewidth=0.8, linestyle="-")
        ax.set_axisbelow(True)
    ax.title.set_color(t["ink"])
    ax.xaxis.label.set_color(t["ink2"])
    ax.yaxis.label.set_color(t["ink2"])


def render_both(draw, out_stem, dpi=130):
    """Call draw(theme_dict) -> Figure for each theme; save <stem>.png and <stem>_dark.png."""
    paths = []
    for mode, suffix in (("light", ""), ("dark", "_dark")):
        t = THEMES[mode]
        fig = draw(t)
        fig.patch.set_facecolor(t["surface"])
        path = f"{out_stem}{suffix}.png"
        fig.savefig(path, dpi=dpi, facecolor=t["surface"])
        plt.close(fig)
        paths.append(path)
    return paths
