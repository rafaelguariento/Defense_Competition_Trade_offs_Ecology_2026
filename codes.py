import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Figures Generation Notebook

    This notebook reproduces the manuscript figures for **Defense–Competition Trade-offs Shape Prey Eco-Evolutionary Dynamics Across Environmental Gradients** (Guariento et al., under review in *Ecology*).
    """)
    return


@app.cell
def _():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from scipy import integrate

    plt.style.use('seaborn-v0_8-ticks')

    PARAMS_TABLE_S1 = {
        'g': 5,
        'f_max_predation': 4,
        'e_N': 0.1,
        'e_P': 0.1,
        'd_N': 0.3,
        'd_P': 0.2,
        'lambda': 1,
        'K': 'variable',
        'alpha': 'variable',
    }

    PARAMS_ISO = {
        'g': 5,
        'f': 4,
        'e_p': 0.1,
        'c': 0.1,
        'd': 0.3,
        'dp': 0.2,
    }

    def color_fader(c1, c2, mix=0.0):
        c1 = np.array(mpl.colors.to_rgb(c1))
        c2 = np.array(mpl.colors.to_rgb(c2))
        return mpl.colors.to_hex((1 - mix) * c1 + mix * c2)

    print('Loaded common imports and parameter dictionaries.')
    return PARAMS_ISO, color_fader, integrate, mpl, np, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Figure 1 - trade-off curves
    """)
    return


@app.cell
def _(np, plt):
    def plot_direct_risk_tradeoff(curves=(1, 2, 0.5), save_path=None):
        if save_path is None:
            import os
            save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'novos_graficos', 'Figure_1.svg')
        base_labels = ['Neutral trade-off', 'Weak trade-off', 'Strong trade-off']
        labels = [f'{lbl} ($\\alpha$={a:g})' for lbl, a in zip(base_labels, curves)]
        colors = ['blue', 'green', 'orange']
        x_points = np.linspace(0, 0.95, 10)

        axis_label_fs = 20
        annotation_fs = 15
        tick_fs = 16
        legend_fs = 16

        fig, ax = plt.subplots(figsize=(8, 8))

        for a, label, color in zip(curves, labels, colors):
            x = np.linspace(0, 0.95, 500)
            y = x ** a
            ax.plot(x, y, label=label, color=color)

        tick_values = np.array([0.00, 0.20, 0.40, 0.60, 0.80, 0.95])
        ax.set_xlim(0, 0.95)
        ax.set_ylim(0, 0.95)
        ax.set_xticks(tick_values)
        ax.set_yticks(tick_values)
        ax.set_xticklabels([f'{v:.2f}' for v in tick_values], fontsize=tick_fs)
        ax.set_yticklabels([f'{v:.2f}' for v in tick_values], fontsize=tick_fs)

        ax.set_xlabel(r'Competitiveness trait value ($x$)', labelpad=16, fontsize=axis_label_fs, loc='center')
        ax.set_ylabel(r'Predation susceptibility ($x^{\alpha}$)', labelpad=16, fontsize=axis_label_fs, loc='center')

        # Place trait-function cues outside axis titles to keep labels clean.
        ax.annotate(
            'Resource consumption rate',
            xy=(0.92, -0.2),
            xytext=(0.18, -0.2),
            xycoords='axes fraction',
            textcoords='axes fraction',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.1),
            ha='center',
            va='center',
            fontsize=annotation_fs,
            annotation_clip=False,
        )
        ax.annotate(
            'Defense',
            xy=(-0.28, 0.13),
            xytext=(-0.28, 0.87),
            xycoords='axes fraction',
            textcoords='axes fraction',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.1),
            ha='center',
            va='center',
            rotation=90,
            fontsize=annotation_fs,
            annotation_clip=False,
        )

        ax.legend(frameon=False, fontsize=legend_fs)
        ax.set_aspect('equal', adjustable='box')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        import os
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight')
        fig.savefig(save_path.replace('.svg', '.png'), dpi=300, bbox_inches='tight')
        plt.close(fig)

    plot_direct_risk_tradeoff()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Figure S2.1
    """)
    return


@app.cell
def _(PARAMS_ISO, np, plt):
    def plot_figureS2_1(alpha=2, save_path=None):
        if save_path is None:
            import os
            save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'novos_graficos', 'Figure_S2_1.svg')
        """Reproduce Figure 1: graphical framework for prey invasion analysis.

        Panel A — Single prey: ZNGI, supply point, and impact vector to equilibrium.
        Panel B — Two prey with trade-off: overlaid ZNGIs, coexistence intersection,
                  impact vectors, and persistence-region annotations.
        Adapted from the ZNGI construction in the alpha = 2 panel.
        """
        g_val = PARAMS_ISO['g']
        f_val = PARAMS_ISO['f']
        e_p = PARAMS_ISO['e_p']
        c_val = PARAMS_ISO['c']
        d_val = PARAMS_ISO['d']
        dp_val = PARAMS_ISO['dp']

        def zngi_curve(R, x):
            return (c_val * g_val * R * x - d_val) / (e_p * f_val * x ** alpha)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6.5))
        R = np.linspace(0.01, 6, 500)
        line_lw = 3.6
        arrow_lw = 3.0
        zone_alpha = 0.24
        axis_label_fs = 20
        tick_fs = 17
        legend_fs = 16
        annotation_fs = 17
        panel_fs = 22

        # ── Panel A: single prey ─────────────────────────────────────
        x0 = 1.0
        P0 = zngi_curve(R, x0)
        pos = P0 >= 0

        ax1.plot(R[pos], P0[pos], color='#1f77b4', lw=line_lw, label='ZNGI$_A$')
        ax1.fill_between(R[pos], 0, P0[pos], color='#1f77b4', alpha=0.12)
        bg_box = dict(facecolor='white', edgecolor='none', alpha=0.7)
        ax1.text(3.5, 2.5, r'$dA/dt > 0$', color='#1f77b4', fontsize=annotation_fs, fontweight='bold', ha='center', bbox=bg_box)
        ax1.text(2.2, 4.2, r'$dA/dt < 0$', color='black', fontsize=annotation_fs, fontweight='bold', ha='center', bbox=bg_box)
        ax1.text(1.5, zngi_curve(1.5, x0), r'$dA/dt = 0$', color='#1f77b4', fontsize=annotation_fs, fontweight='bold', ha='center', rotation=51, bbox=bg_box)

        R_star0 = d_val / (c_val * g_val * x0)

        K_show = 4.0
        ax1.scatter(K_show, 0, c='k', s=170, zorder=6, edgecolor='white', linewidth=0.8, clip_on=False)
        ax1.annotate(
            r'$S=(4,\,0)$', xy=(K_show, 0.1), xytext=(K_show, 1.5),
            fontsize=annotation_fs - 4, ha='center',
            arrowprops=dict(arrowstyle='-', color='gray', lw=0.9, shrinkA=3, shrinkB=3)
        )

        R_eq = 2.5
        P_eq = zngi_curve(R_eq, x0)
        ax1.scatter(R_eq, P_eq, c='red', s=150, zorder=6, edgecolor='white', linewidth=0.8, label=r'$(\hat{R},\,\hat{P})$')

        ax1.annotate(
            '', xy=(R_eq, P_eq), xytext=(K_show, 0),
            arrowprops=dict(
                arrowstyle='-|>', color='#1f77b4', lw=arrow_lw * 0.7,
                mutation_scale=18, shrinkA=0, shrinkB=6
            )
        )

        # ── Additional supply points with impact vectors ─────────────
        # S=(2,0) and S=(3,0) share the same label height; smaller font avoids overlap
        _s_label_y = {2.0: 0.45, 3.0: 0.7}
        for K_extra in [2.0, 3.0]:
            ax1.scatter(K_extra, 0, c='k', s=170, zorder=6, edgecolor='white', linewidth=0.8, clip_on=False)
            ax1.annotate(
                f'$S=({int(K_extra)},\\,0)$',
                xy=(K_extra, 0.1), xytext=(K_extra, _s_label_y[K_extra]),
                fontsize=annotation_fs - 4, ha='center',
                arrowprops=dict(arrowstyle='-', color='gray', lw=0.9, shrinkA=3, shrinkB=3)
            )
            R_eq_extra = K_extra * 0.6
            P_eq_extra = zngi_curve(R_eq_extra, x0)
            ax1.scatter(R_eq_extra, P_eq_extra, c='red', s=100, zorder=6,
                        edgecolor='white', linewidth=0.8)
            ax1.annotate(
                '', xy=(R_eq_extra, P_eq_extra), xytext=(K_extra, 0),
                arrowprops=dict(
                    arrowstyle='-|>', color='#1f77b4', lw=arrow_lw * 0.7,
                    mutation_scale=18, shrinkA=0, shrinkB=6
                )
            )

        ax1.set_xlim(0, 5.5)
        ax1.set_ylim(0, 5.5)
        ax1.set_aspect('equal')
        ax1.set_box_aspect(1)
        ax1.set_xticks(np.arange(0, 6, 1))
        ax1.set_yticks(np.arange(0, 6, 1))
        ax1.set_xlabel('Resource density (cells mL$^{-1}$)', fontsize=axis_label_fs)
        ax1.set_ylabel('Predator density (individuals L$^{-1}$)', fontsize=axis_label_fs)
        ax1.tick_params(labelsize=tick_fs)
        ax1.legend(fontsize=legend_fs, loc='upper left', frameon=False)
        ax1.text(-0.12, 1.05, 'A', transform=ax1.transAxes, fontsize=panel_fs, fontweight='bold')

        # ── Panel B: two prey with trade-off ─────────────────────────
        x_A, x_B = 1.0, 0.5
        cA, cB = '#1f77b4', '#2ca02c'
        cAB = '#2f7f72'

        PA = zngi_curve(R, x_A)
        PB = zngi_curve(R, x_B)
        posA = PA >= 0
        posB = PB >= 0

        r_s = d_val * (-x_A ** alpha + x_B ** alpha) / (
            c_val * g_val * (x_A * x_B ** alpha - x_B * x_A ** alpha)
        )
        p_s = zngi_curve(r_s, x_A)

        mA = (R <= r_s) & posA
        mB = (R >= r_s) & posB
        R_A_seg, P_A_seg = R[mA], PA[mA]
        R_B_seg, P_B_seg = R[mB], PB[mB]

        sl_A = (p_s * (-(e_p * f_val) * x_A ** alpha / dp_val)) / (r_s * (g_val * x_A / r_s))
        sl_B = (p_s * (-(e_p * f_val) * x_B ** alpha / dp_val)) / (r_s * (g_val * x_B / r_s))

        def iv_end(slope, xmax=5.5):
            """Clip impact line to the plot rectangle."""
            R_at_P0 = r_s - p_s / slope
            if R_at_P0 <= xmax:
                return (R_at_P0, 0.0)
            return (xmax, p_s + slope * (xmax - r_s))

        eA = iv_end(sl_A)
        eB = iv_end(sl_B)
        R_star_A = d_val / (c_val * g_val * x_A)

        a_zone = np.column_stack((
            np.concatenate(([R_star_A], R_A_seg, [eA[0]])),
            np.concatenate(([0.0], P_A_seg, [eA[1]]))
        ))
        b_zone = np.column_stack((
            np.concatenate(([r_s], R_B_seg, [eB[0]])),
            np.concatenate(([p_s], P_B_seg, [eB[1]]))
        ))
        # Extend coexistence polygon to touch the x-axis by adding bottom-edge corners
        ab_zone = np.array([(r_s, p_s), eA, (eA[0], 0.0), (eB[0], 0.0), eB])

        ax2.add_patch(plt.Polygon(a_zone, closed=True, fc=cA, alpha=zone_alpha, ec='none', zorder=0))
        ax2.add_patch(plt.Polygon(b_zone, closed=True, fc=cB, alpha=zone_alpha, ec='none', zorder=0))
        ax2.add_patch(
            plt.Polygon(
                ab_zone, closed=True, fc=cAB, alpha=0.42, ec=cAB,
                lw=1.8, hatch='///', zorder=1
            )
        )

        ax2.plot(R_A_seg, P_A_seg, cA, lw=line_lw, label='ZNGI$_A$')
        ax2.plot(R_B_seg, P_B_seg, cB, lw=line_lw, label='ZNGI$_B$')
        ax2.scatter(r_s, p_s, c='red', s=150, zorder=6, edgecolor='white', linewidth=0.8, label=r'$(\hat{R},\,\hat{P})$')
        ax2.text(1.2, zngi_curve(1.2, x_A), r'$dA/dt = 0$', color=cA, fontsize=annotation_fs, fontweight='bold', ha='center', rotation=51, bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
        ax2.text(2.5, zngi_curve(2.5, x_B), r'$dB/dt = 0$', color=cB, fontsize=annotation_fs, fontweight='bold', ha='center', rotation=68, bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

        ax2.text(1.8, 0.3, r'$dA/dt > 0$', color=cA, fontsize=annotation_fs - 2, fontweight='bold', ha='center', bbox=bg_box)
        ax2.text(4.8, 2.5, r'$dB/dt > 0$', color=cB, fontsize=annotation_fs - 2, fontweight='bold', ha='center', bbox=bg_box)
        ax2.text(1.0, 3.2, r'$dA/dt < 0$', color='black', fontsize=annotation_fs - 2, fontweight='bold', ha='center', bbox=bg_box)
        ax2.text(1.0, 2.7, r'$dB/dt < 0$', color='black', fontsize=annotation_fs - 2, fontweight='bold', ha='center', bbox=bg_box)

        ax2.annotate(
            '', xy=(r_s, p_s), xytext=eA,
            arrowprops=dict(
                arrowstyle='-|>', color=cA, lw=arrow_lw*0.7,
                mutation_scale=20, shrinkA=0, shrinkB=6
            )
        )
        ax2.annotate(
            '', xy=(r_s, p_s), xytext=eB,
            arrowprops=dict(
                arrowstyle='-|>', color=cB, lw=arrow_lw*0.7,
                mutation_scale=20, shrinkA=0, shrinkB=6
            )
        )

        label_box = dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.78)
        ax2.text(1.8, 0.7, 'Prey A', fontsize=annotation_fs, color=cA, fontweight='bold', ha='center', bbox=label_box)
        ax2.text(4.25, 4.15, 'Prey B', fontsize=annotation_fs, color=cB, fontweight='bold', ha='center', bbox=label_box)
        ax2.text(
            4.8, 0.15, 'Prey A + B', fontsize=annotation_fs,
            color='black', fontweight='bold', ha='center', bbox=label_box
        )

        ax2.set_xlim(0, 5.5)
        ax2.set_ylim(0, 5.5)
        ax2.set_aspect('equal')
        ax2.set_box_aspect(1)
        ax2.set_xticks(np.arange(0, 6, 1))
        ax2.set_yticks(np.arange(0, 6, 1))
        ax2.set_xlabel('Resource density (cells mL$^{-1}$)', fontsize=axis_label_fs)

        ax2.tick_params(axis='both', labelsize=tick_fs, labelleft=True)
        ax2.legend(fontsize=legend_fs, loc='upper left', frameon=False)
        ax2.text(-0.12, 1.05, 'B', transform=ax2.transAxes, fontsize=panel_fs, fontweight='bold')

        fig.tight_layout()
        import os
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight')
        fig.savefig(save_path.replace('.svg', '.png'), dpi=300, bbox_inches='tight')
        plt.close(fig)

    plot_figureS2_1()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Figure 2
    """)
    return


@app.cell
def _(PARAMS_ISO, np, plt):
    def plot_zngi_by_alpha(a_values=(0.5, 1, 2), zngi_number=2, save_path=None):
        if save_path is None:
            import os
            save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'novos_graficos', 'Figure_2.svg')
        pop_colors = ['#2ca02c', '#1f77b4']
        g, f, e_p, c, d = (
            PARAMS_ISO['g'], PARAMS_ISO['f'], PARAMS_ISO['e_p'], PARAMS_ISO['c'], PARAMS_ISO['d']
        )
        line_lw = 3.0

        R = np.linspace(0.01, 10, 100)
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        for idx, (ax, alpha) in enumerate(zip(axes, a_values)):
            for x in range(1, zngi_number + 1):
                frac = x / zngi_number
                zngi = (c * g * R * frac - d) / (e_p * f * frac ** alpha)
                pop_label = r'ZNGI$_A$' if x == zngi_number else r'ZNGI$_B$'
                ax.plot(R, zngi, color=pop_colors[x - 1], linewidth=line_lw, label=pop_label)

            ax.set_ylim([0, 5])
            ax.set_xlim([0, 5])
            desc = {0.5: 'strong trade-off', 1: 'linear trade-off', 2: 'weak trade-off'}.get(alpha, '')
            ax.set_title(r'$\alpha$ = ' + f'{alpha}' + (f' ({desc})' if desc else ''), fontsize=24)
            ax.set_xlabel('Resource density (cells mL$^{-1}$)', fontsize=22)
            ax.set_ylabel('Predator density (individuals L$^{-1}$)', fontsize=22)
            ax.tick_params(axis='both', which='major', labelsize=19)
            ax.text(-0.14, 1.05, chr(65 + idx), transform=ax.transAxes, fontsize=24, fontweight='bold')

            if idx == 0:
                handles, labels = ax.get_legend_handles_labels()
                order = [labels.index(r'ZNGI$_A$'), labels.index(r'ZNGI$_B$')]
                ax.legend([handles[i] for i in order], [labels[i] for i in order], fontsize=19)

        fig.tight_layout()
        import os
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight')
        fig.savefig(save_path.replace('.svg', '.png'), dpi=300, bbox_inches='tight')
        plt.close(fig)

    plot_zngi_by_alpha()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Figure 3
    """)
    return


@app.cell
def _(PARAMS_ISO, color_fader, np, pd, plt):
    def plot_outermost_zngi_and_impacts(zngi_number=4, alpha=2, save_path=None):
        if save_path is None:
            import os
            save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'novos_graficos', 'Figure_3.svg')
        c1, c2 = '#1f77b4', '#FFBF00'
        g, f, e_p, c, d, dp = (
            PARAMS_ISO['g'], PARAMS_ISO['f'], PARAMS_ISO['e_p'], PARAMS_ISO['c'], PARAMS_ISO['d'], PARAMS_ISO['dp']
        )
        prey_labels = ['Prey D', 'Prey C', 'Prey B', 'Prey A']
        prey_colors = ['#FFBF00', color_fader(c1, c2, 0.33), color_fader(c1, c2, 0.66), '#1f77b4']
        line_lw = 2.6
        impact_lw = 1.2

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # Panel A: all ZNGIs
        R1 = np.linspace(0, 14, 100)
        for x in range(1, zngi_number + 1):
            frac = x / zngi_number
            zngi = (c * g * R1 * frac - d) / ((e_p * f) * (frac ** alpha))
            if x == 1:
                label = f'{prey_labels[x - 1]}\n(more defended), $x$ = {frac:.2f}'
            elif x == zngi_number:
                label = f'{prey_labels[x - 1]}\n(more competitive), $x$ = {frac:.2f}'
            else:
                label = f'{prey_labels[x - 1]}, $x$ = {frac:.2f}'
            ax1.plot(R1, zngi, color=prey_colors[x - 1], linewidth=line_lw, alpha=1, label=label)

        ax1.set_ylim([0, 15])
        ax1.set_xlim([0, 15])
        ax1.set_xlabel('Resource density (cells mL$^{-1}$)', fontsize=22)
        ax1.set_ylabel('Predator density (individuals L$^{-1}$)', fontsize=22)
        ax1.tick_params(axis='both', which='major', labelsize=19)
        ax1.text(0.02, 0.98, 'A', transform=ax1.transAxes, fontsize=24, fontweight='bold',
                 verticalalignment='top', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

        handles, labels = ax1.get_legend_handles_labels()
        legend_order = ['Prey A', 'Prey B', 'Prey C', 'Prey D']
        ordered_handles = []
        ordered_labels = []
        for target in legend_order:
            for handle, label in zip(handles, labels):
                if label.startswith(target):
                    ordered_handles.append(handle)
                    ordered_labels.append(label)
                    break
        legend_style = dict(
            fontsize=15,
            frameon=True,
            facecolor='white',
            edgecolor='none',
            framealpha=0.9,
            borderpad=0.35,
            labelspacing=0.25,
            handlelength=1.2,
            handletextpad=0.45,
        )
        ax1.legend(ordered_handles, ordered_labels, loc='lower right', bbox_to_anchor=(1.02, -0.01), **legend_style)

        # Panel B: outermost ZNGI + intersections + impact vectors
        R2 = np.linspace(0.01, 14, 1000)
        zngis = []
        for x in range(1, zngi_number + 1):
            frac = x / zngi_number
            zngi = (c * g * R2 * frac - d) / ((e_p * f) * (frac ** alpha))
            zngis.append(zngi)

        outermost = np.maximum.reduce(zngis)
        for i, zngi in enumerate(zngis):
            mask = zngi == outermost
            # Extend mask by 1 point on each side so segments overlap at intersections
            idx = np.where(mask)[0]
            if len(idx) > 0:
                lo = max(idx[0] - 1, 0)
                hi = min(idx[-1] + 1, len(mask) - 1)
                mask[lo] = True
                mask[hi] = True
            ax2.plot(R2[mask], zngi[mask], color=color_fader(c1, c2, 1 - i / (zngi_number - 1)), linewidth=line_lw, alpha=1)

        ax2.set_ylim([0, 15])
        ax2.set_xlim([0, 15])
        ax2.set_xlabel('Resource density (cells mL$^{-1}$)', fontsize=22)
        ax2.set_ylabel('Predator density (individuals L$^{-1}$)', fontsize=22)
        ax2.tick_params(axis='both', which='major', labelsize=19)
        ax2.text(0.02, 0.98, 'B', transform=ax2.transAxes, fontsize=24, fontweight='bold',
                 verticalalignment='top', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

        star_values = pd.DataFrame(columns=['index', 'RStar', 'PStar', 'x_value_1', 'x_value_2'])
        index = 0
        for x in range(1, zngi_number + 1):
            x_value_1 = x / zngi_number
            for w in range(x + 1, zngi_number + 1):
                x_value_2 = w / zngi_number
                r_star = d * (-x_value_1 ** alpha + x_value_2 ** alpha) / (
                    c * g * (x_value_1 * x_value_2 ** alpha - x_value_2 * x_value_1 ** alpha)
                )
                p_star = (c * g * r_star * x_value_1 - d) / ((e_p * f) * x_value_1 ** alpha)

                index += 1
                star_values.loc[index] = [index, r_star, p_star, x_value_1, x_value_2]

        outermost_intersections = star_values.loc[
            (star_values['PStar'] >= np.min(outermost)) &
            (star_values['PStar'] <= np.max(outermost))
        ]
        selected_intersections = outermost_intersections.iloc[[0, 3, 5]] if len(outermost_intersections) >= 6 else outermost_intersections

        for _, row in selected_intersections.iterrows():
            ax2.scatter(row['RStar'], row['PStar'], color='red', s=30, zorder=5)

        def _clip_to_axes(x0, y0, x1, y1, xmin=0, xmax=15, ymin=0, ymax=15):
            """Clip the segment (x0,y0)->(x1,y1) to the rectangle, returning the clipped endpoint."""
            dx, dy = x1 - x0, y1 - y0
            t = 1.0
            for edge_val, delta, coord0 in [
                (xmin, dx, x0), (xmax, dx, x0), (ymin, dy, y0), (ymax, dy, y0)
            ]:
                if delta == 0:
                    continue
                t_edge = (edge_val - coord0) / delta
                if t_edge > 0:
                    # Check if we're crossing the boundary from inside to outside
                    if (delta > 0 and edge_val == xmax) or (delta < 0 and edge_val == xmin) or \
                       (delta > 0 and edge_val == ymax) or (delta < 0 and edge_val == ymin):
                        t = min(t, t_edge)
            return x0 + dx * t, y0 + dy * t

        for _, row in selected_intersections.iterrows():
            impact_eq_nx_r_1 = g * row['x_value_1'] / row['RStar']
            impact_eq_nx_p_1 = -(e_p * f) * row['x_value_1'] ** alpha / dp
            impact_eq_nx_r_2 = g * row['x_value_2'] / row['RStar']
            impact_eq_nx_p_2 = -(e_p * f) * row['x_value_2'] ** alpha / dp

            end_r_1 = row['RStar'] * (1 + impact_eq_nx_r_1 * 10)
            end_p_1 = row['PStar'] * (1 + impact_eq_nx_p_1 * 10)
            end_r_2 = row['RStar'] * (1 + impact_eq_nx_r_2 * 10)
            end_p_2 = row['PStar'] * (1 + impact_eq_nx_p_2 * 10)

            # Clip endpoints to the visible axes area so annotate arrows render
            end_r_1, end_p_1 = _clip_to_axes(row['RStar'], row['PStar'], end_r_1, end_p_1)
            end_r_2, end_p_2 = _clip_to_axes(row['RStar'], row['PStar'], end_r_2, end_p_2)

            mix = 1 - (row['index'] / index) if index > 0 else 0.5
            ax2.annotate(
                '', xy=(row['RStar'], row['PStar']), xytext=(end_r_1, end_p_1),
                arrowprops=dict(
                    arrowstyle='-|>', color=color_fader(c1, c2, mix),
                    lw=impact_lw, mutation_scale=18, shrinkA=0, shrinkB=0,
                    alpha=0.6
                )
            )
            ax2.annotate(
                '', xy=(row['RStar'], row['PStar']), xytext=(end_r_2, end_p_2),
                arrowprops=dict(
                    arrowstyle='-|>', color=color_fader(c1, c2, mix),
                    lw=impact_lw, mutation_scale=18, shrinkA=0, shrinkB=0,
                    alpha=0.6
                )
            )

        fig.tight_layout()
        plt.savefig(save_path, format='svg')
        png_path = save_path.replace('.svg', '.png')
        plt.savefig(png_path, format='png', dpi=300)
        plt.show()
        plt.close(fig)

    plot_outermost_zngi_and_impacts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Figure S2.2
    """)
    return


@app.cell
def _(color_fader, integrate, np, pd, plt):
    def model(X, t, alpha, x1, x2, x3, x4, c, g, f, e_p, d, dp, K, r, IZ):
        n1, n2, n3, n4, R, P = X
        n1dot = n1 * (g * c * x1 * R - f * x1 ** alpha * P - d)
        n2dot = n2 * (g * c * x2 * R - f * x2 ** alpha * P - d)
        n3dot = n3 * (g * c * x3 * R - f * x3 ** alpha * P - d)
        n4dot = n4 * (g * c * x4 * R - f * x4 ** alpha * P - d)
        Rdot = r * (K - R) * R - g * R * (x1 * n1 + x2 * n2 + x3 * n3 + x4 * n4)
        Pdot = P * (e_p * f * (x1 ** alpha * n1 + x2 ** alpha * n2 + x3 ** alpha * n3 + x4 ** alpha * n4) - dp)
        return np.array([n1dot, n2dot, n3dot, n4dot, Rdot, Pdot])

    def run_simulation(K, Nt=1000, tmax=1500):
        alpha = 2
        x1, x2, x3, x4 = (1.0, 0.75, 0.5, 0.25)
        c, g, f, e_p = (0.1, 5, 4, 0.1)
        d, dp = (0.3, 0.2)
        r, IZ = (1, 0.0)
        X0 = [1.0, 1.0, 1.0, 1.0, K, 1.0]
        t = np.linspace(0.0, tmax, Nt)
        res = integrate.odeint(model, X0, t, args=(alpha, x1, x2, x3, x4, c, g, f, e_p, d, dp, K, r, IZ))
        return (t, res)

    def plot_timeseries_by_K(K_values=(2.5, 4, 5, 5.5, 7.5, 10, 14), save_path=None):
        if save_path is None:
            import os
            save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'novos_graficos', 'Figure_S2_2.svg')
        c_blue, c_amber = ('#1f77b4', '#FFBF00')
        fig, axes = plt.subplots(2, 4, figsize=(20, 12))
        axes = axes.flatten()
        ax0 = axes[0]
        curve_lw = 2.1
        legend_fs = 20
        title_fs = 23
        axis_label_fs = 23
        tick_fs = 21
        panel_fs = 26
        g_iso, f_iso, e_p_iso, c_iso, d_iso, dp_iso = (5, 4, 0.1, 0.1, 0.3, 0.2)
        zngi_number = 4  # Panel A: Outermost isocline + supply points + intersections + impact vectors
        alpha_iso = 2
        R_iso = np.linspace(0.01, 10, 100)
        zngis = []
        for x in range(1, zngi_number + 1):
            frac = x / zngi_number
            zngi_x = (c_iso * g_iso * R_iso * frac - d_iso) / (e_p_iso * f_iso * frac ** alpha_iso)
            zngis.append(zngi_x)
        outermost_zngi = np.maximum.reduce(zngis)
        ax0.plot(R_iso, outermost_zngi, color='#B2D3C2', linewidth=curve_lw, alpha=1, label='ZNGIs')
        ax0.set_ylim([0, 15])
        ax0.set_xlim([0, 15])
        ax0.set_xlabel('Resource density (cells mL$^{-1}$)', fontsize=axis_label_fs)
        ax0.set_ylabel('Predator density (individuals L$^{-1}$)', fontsize=axis_label_fs)
        ax0.tick_params(axis='both', which='major', labelsize=tick_fs)
        ax0.grid(True, linestyle=':', alpha=0.01)
        for K in K_values:
            ax0.scatter(K, 0, color='black', s=30, zorder=5)
        star_values = []
        index = 0
        for x in range(1, zngi_number + 1):
            x_value_1 = x / zngi_number
            for w in range(x + 1, zngi_number + 1):
                x_value_2 = w / zngi_number
                r_star = d_iso * (-x_value_1 ** alpha_iso + x_value_2 ** alpha_iso) / (c_iso * g_iso * (x_value_1 * x_value_2 ** alpha_iso - x_value_2 * x_value_1 ** alpha_iso))
                p_star = (c_iso * g_iso * r_star * x_value_1 - d_iso) / (e_p_iso * f_iso * x_value_1 ** alpha_iso)
                index = index + 1
                star_values.append((index, r_star, p_star, x_value_1, x_value_2))
        star_df = pd.DataFrame(star_values, columns=['index', 'RStar', 'PStar', 'x_value_1', 'x_value_2'])
        outermost_intersections = star_df[(star_df['PStar'] >= np.min(outermost_zngi)) & (star_df['PStar'] <= np.max(outermost_zngi))]
        selected_intersections = outermost_intersections.iloc[[0, 3, 5]] if len(outermost_intersections) >= 6 else outermost_intersections
        for _, row in selected_intersections.iterrows():
            ax0.scatter(row['RStar'], row['PStar'], color='red', s=50, zorder=5)
        for _, row in selected_intersections.iterrows():
            impact_eq_nx_r_1 = g_iso * row['x_value_1'] / row['RStar']
            impact_eq_nx_p_1 = -(e_p_iso * f_iso) * row['x_value_1'] ** alpha_iso / dp_iso
            impact_eq_nx_r_2 = g_iso * row['x_value_2'] / row['RStar']
            impact_eq_nx_p_2 = -(e_p_iso * f_iso) * row['x_value_2'] ** alpha_iso / dp_iso
            x112 = [row['RStar'], row['RStar'] * (1 + impact_eq_nx_r_1 * 10)]
            y112 = [row['PStar'], row['PStar'] * (1 + impact_eq_nx_p_1 * 10)]
            x212 = [row['RStar'], row['RStar'] * (1 + impact_eq_nx_r_2 * 10)]
            y212 = [row['PStar'], row['PStar'] * (1 + impact_eq_nx_p_2 * 10)]
            mix = row['index'] / index if index > 0 else 0.5
            ax0.plot(x112, y112, color=color_fader(c_blue, c_amber, mix), linewidth=curve_lw, alpha=0.8)
            ax0.plot(x212, y212, color=color_fader(c_blue, c_amber, mix), linewidth=curve_lw, alpha=0.8)
        ax0.get_legend().remove() if ax0.get_legend() else None
        panel_labels = list('ABCDEFGH')
        ax0.text(-0.1, 1.05, panel_labels[0], transform=ax0.transAxes, fontsize=panel_fs, fontweight='bold')
        for i, K in enumerate(K_values):
            ax = axes[i + 1]
            t, res = run_simulation(K)
            n1, n2, n3, n4, _, _ = res.T
            x_fracs = [1.0, 0.75, 0.5, 0.25]
            prey_labels = [
                f'Prey A\n(more competitive), $x$ = {x_fracs[0]:.2f}',
                f'Prey B, $x$ = {x_fracs[1]:.2f}',
                f'Prey C, $x$ = {x_fracs[2]:.2f}',
                f'Prey D\n(more defended), $x$ = {x_fracs[3]:.2f}',
            ]
            prey_colors = [c_blue, color_fader(c_blue, c_amber, 1 / 3), color_fader(c_blue, c_amber, 2 / 3), c_amber]
            for j, data in enumerate([n1, n2, n3, n4]):
                ax.plot(t, data, color=prey_colors[j], linewidth=curve_lw, label=prey_labels[j])
            ax.set_title(f'$S_R$ = {K}', fontsize=title_fs)
            ax.set_xlabel('Time t (days)', fontsize=axis_label_fs)
            ax.set_ylabel('Density (individuals mL$^{-1}$)', fontsize=axis_label_fs)
            ax.tick_params(axis='both', which='major', labelsize=tick_fs)
            if i == 0:
                legend_style = dict(
                    fontsize=int(legend_fs * 0.75),
                    frameon=True,
                    facecolor='white',
                    edgecolor='none',
                    framealpha=0.9,
                    borderpad=0.35,
                    labelspacing=0.25,
                    handlelength=1.2,
                    handletextpad=0.45,
                )
                ax.legend(**legend_style)
            ax.text(-0.1, 1.05, panel_labels[i + 1], transform=ax.transAxes, fontsize=panel_fs, fontweight='bold')
        fig.tight_layout()
        fig.savefig(save_path, format='svg')
        png_path = save_path.replace('.svg', '.png')
        fig.savefig(png_path, format='png', dpi=300)
        plt.show()
        plt.close(fig)
    plot_timeseries_by_K()  # Panels B-H: time series across K
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Figure 4
    """)
    return


@app.cell
def _(np, plt):
    def plot_pip(save_path=None):
        if save_path is None:
            import os
            save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'novos_graficos', 'Figure_4.svg')
        from matplotlib.colors import ListedColormap, BoundaryNorm
        # Constants
        g = 5
        f = 4
        e_p = 0.1
        c = 0.1
        d = 0.3
        R = 2
        P = 0

        def fitness(x, y, alpha):
            return g * c * y * R - e_p * f * y ** alpha * (R * c * g * x - d) / (e_p * f * x ** alpha) - d

        # Define the invasion fitness function
        def invasion_fitness(x, y, alpha):
            return fitness(x, y, alpha) - fitness(x, x, alpha)

        x = np.linspace(0.01, 0.99, 400)
        y = np.linspace(0.01, 0.99, 400)
        X, Y = np.meshgrid(x, y)
        alpha_values = [0.5, 1, 2]

        # Generate the plot data
        plt.rcParams.update({'font.size': 20})
        plt.rcParams['axes.labelsize'] = 18
        plt.rcParams['axes.titlesize'] = 20
        plt.rcParams['xtick.labelsize'] = 18
        plt.rcParams['ytick.labelsize'] = 18

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        for idx, (ax, alpha) in enumerate(zip(axes, alpha_values)):
            Z = invasion_fitness(X, Y, alpha)
            cmap = ListedColormap(['white', 'grey'])
            norm = BoundaryNorm([-1, 0, 1], cmap.N)
            contour_neg = ax.contourf(X, Y, Z, levels=np.linspace(Z.min(), 0, 100), cmap=ListedColormap(['white']))
            contour_pos = ax.contourf(X, Y, Z, levels=np.linspace(0, Z.max(), 100), cmap=ListedColormap(['grey']))

            contour_zero = ax.contour(X, Y, Z, levels=[0], colors='black', linewidths=1)
            ax.contour(X, Y, Z, levels=[0], colors='black', linewidths=0.5, linestyles='-')

            highlight_point = None
            for i in range(1, Z.shape[0] - 1):
                for j in range(1, Z.shape[1] - 1):
                    if Z[i, j] == 0:
                        if Z[i - 1, j] < 0 and Z[i + 1, j] < 0:
                            if Z[i, j - 1] > 0 and Z[i, j + 1] > 0:
                                highlight_point = (x[j], y[i])
                                print(f'Alpha={alpha}: Point at Z=0 with negative invasion fitness above/below and positive invasion fitness left/right found at: x = {x[j]}, y = {y[i]}')
                                break

            if highlight_point:
                ax.plot(highlight_point[0], highlight_point[1], 'ro', markersize=6, label='Highlighted Point')

            ax.set_xlabel('Resident trait', fontsize=18)
            ax.set_ylabel('Mutant trait', fontsize=18)
            desc = {0.5: 'strong trade-off', 1: 'linear trade-off', 2: 'weak trade-off'}.get(alpha, '')
            ax.set_title(r'$\alpha$ = ' + f'{alpha}' + (f' ({desc})' if desc else ''), fontsize=20)
            ax.text(-0.1, 1.05, chr(65 + idx), transform=ax.transAxes, fontsize=18, fontweight='bold', va='bottom', ha='right')

        fig.legend([plt.Rectangle((0, 0), 1, 1, edgecolor='black', facecolor='grey'), plt.Rectangle((0, 0), 1, 1, edgecolor='black', facecolor='white')], ['Positive invasion fitness', 'Negative invasion fitness'], loc='lower center', ncol=2, fontsize=16, frameon=False)
        plt.tight_layout(rect=[0, 0.05, 1, 1])
        plt.savefig(save_path, format='svg')
        png_path = save_path.replace('.svg', '.png')
        plt.savefig(png_path, format='png', dpi=300)
        plt.close(fig)
        return

    fig = plot_pip()
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Supplementary Figure S4
    """)
    return


@app.cell
def _(np, plt):
    from matplotlib.gridspec import GridSpec

    def create_pip_plot(index, a_vals, b_vals):
        x = np.linspace(0, 1, 200)
        y = np.linspace(0, 1, 200)
        X, Y = np.meshgrid(x, y)
        Z = b_vals[index] * (X - Y) * (a_vals[index] * (X - 0.5) - (Y - 0.5))

        ax = plt.gca()
        ax.contour(X, Y, Z, levels=[0], colors='black')
        ax.imshow(Z > 0, extent=[0, 1, 0, 1], origin='lower', cmap='binary', alpha=0.3)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel('Resident trait', fontsize=12)
        ax.set_ylabel('Mutant trait', fontsize=12)

    def plot_pip_panel(save_path=None):
        if save_path is None:
            import os
            save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'novos_graficos', 'Figure_S4.svg')
        a_vals = [2, 1/2, -1/2, -2, 2, 1/2, -1/2, -2]
        b_vals = [1, 1, 1, 1, -1, -1, -1, -1]

        fig = plt.figure(figsize=(10, 10))
        gs = GridSpec(2, 2, figure=fig)

        pip_indices = [7, 5, 1, 3]
        pip_labels = ['CSS', 'Non convergence stable', 'Repeller', 'BP']
        panel_labels = ['A', 'B', 'C', 'D']

        for i, (index, label, panel_label) in enumerate(zip(pip_indices, pip_labels, panel_labels)):
            ax = fig.add_subplot(gs[i // 2, i % 2])
            create_pip_plot(index - 1, a_vals, b_vals)
            ax.set_title(label, fontsize=14)
            ax.text(-0.1, 1.1, panel_label, transform=ax.transAxes, fontsize=16, fontweight='bold')

        fig.tight_layout()
        fig.savefig(save_path, format='svg', bbox_inches='tight')
        png_path = save_path.replace('.svg', '.png')
        fig.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
        plt.show()
        plt.close(fig)

    plot_pip_panel()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Supplementary Figure S5
    """)
    return


@app.cell
def _(mpl, np, plt):
    def colorFader(c1, c2, mix=0):
        c1 = np.array(mpl.colors.to_rgb(c1))
        c2 = np.array(mpl.colors.to_rgb(c2))
        return mpl.colors.to_hex((1 - mix) * c1 + mix * c2)
    c1 = '#1f77b4'
    c2 = '#FFE135'
    g_1 = 5
    f_1 = 4
    e_p_1 = 0.1
    # Parameters
    c_1 = 0.1  # blue
    d_1 = 0.3  # columbia blue
    dp = 0.2
    a = 2
    zngi_number = 10
    plt.style.use('seaborn-v0_8-ticks')
    fig_1, ax_1 = plt.subplots(figsize=(6, 6))
    R_1 = np.linspace(0.01, 5, 100)
    for x_1 in range(1, zngi_number + 1):
        x_value = x_1 / zngi_number

    # Create figure
        def ZNGI_x(R):
            return (c_1 * g_1 * R * x_value - d_1) / (e_p_1 * f_1 * x_value ** a)
        P_values = ZNGI_x(R_1)
    # Generate ZNGI curves
        ax_1.plot(R_1, P_values, color=colorFader(c1, c2, x_value), linewidth=1.5, alpha=1, label=f'$x$ = {x_value}')

    # Plot ZNGIs
    def envelope(R):
        return R ** 2 * c_1 ** 2 * g_1 ** 2 / (4 * d_1 * (e_p_1 * f_1))
    R_envelope = np.linspace(0.01, 5, 100)
    ax_1.plot(R_envelope, envelope(R_envelope), label='envelope', color='red')
    R_impacts = np.linspace(1.5, 4.5, 6)
    for R_value in R_impacts:
        P_start = 0
        P_end = min(envelope(R_value), 5.0)
        ax_1.annotate(
            '', xy=(R_value, P_end), xytext=(R_value, P_start),
            arrowprops=dict(
                arrowstyle='-|>', color='#C0392B', lw=1.6,
                mutation_scale=16, alpha=0.45
            )
        )
    ax_1.set_ylim([0, 5])
    # Define and plot envelope
    ax_1.set_xlim([0, 5])
    ax_1.set_xlabel('Resource density (cells mL$^{-1}$)', fontsize=14)
    ax_1.set_ylabel('Predator density (individuals L$^{-1}$)', fontsize=14)
    ax_1.legend(fontsize=10)
    ax_1.grid(True, linestyle=':', alpha=0.01)
    ax_1.set_aspect('equal')
    # Calculate and plot impact vectors with varying magnitudes
    # We'll space them logarithmically to better show the effect
    plt.tight_layout()
    import os
    save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'novos_graficos', 'Figure_S5.svg')
    plt.savefig(save_path, format='svg', bbox_inches='tight')
    png_path = save_path.replace('.svg', '.png')
    plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
    # Set plot parameters
    plt.show()
    plt.close()
    return


if __name__ == "__main__":
    app.run()
