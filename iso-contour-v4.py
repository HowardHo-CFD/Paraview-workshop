import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, PillowWriter

df = pd.read_csv('v4-dc-50-q-star-1.csv')

x = df['Points_0'].values
y = df['Points_1'].values
z = df['Points_2'].values
omega_z = df['Vorticity_2'].values

# --- USER INPUTS ---
clim_min   = -50
clim_max   =  50
point_size =   3
#cmap       = 'RdBu_r'
cmap = 'coolwarm'

elev_start =  30 #30
azim_start =  180
swing_deg  = 360
n_frames   =  150
fps        =  15

z_min      = None #-0.1   # set to None to disable
z_max      = None #0.1   # set to None to disable

# --- SPANWISE FILTER ---
mask = np.ones(len(z), dtype=bool)
if z_min is not None:
    mask &= (z >= z_min)
if z_max is not None:
    mask &= (z <= z_max)

x       = x[mask]
y       = y[mask]
z       = z[mask]
omega_z = omega_z[mask]

# --- CLIP + NORMALISE ---
omega_clipped = np.clip(omega_z, clim_min, clim_max)

# --- BUILD AZIMUTH SEQUENCE ---
# half = n_frames // 2
# azim_forward = np.linspace(azim_start, azim_start + swing_deg, half)
# azim_back    = np.linspace(azim_start + swing_deg, azim_start, half)
# azim_seq     = np.concatenate([azim_forward, azim_back])

# Enable below and disable 4 lines above to turn into continous spin
azim_seq = np.linspace(azim_start, azim_start + 360, n_frames)

# ============================================================
# FIGURE SETUP
# ============================================================
fig = plt.figure(figsize=(9, 6), facecolor='white')
ax  = fig.add_subplot(111, projection='3d')
ax.set_facecolor('white')

sc = ax.scatter(x, z, y,
                c=omega_clipped,
                cmap=cmap,
                vmin=clim_min, vmax=clim_max,
                s=point_size,
                depthshade=False)

cbar = plt.colorbar(sc, ax=ax, pad=0.1, shrink=0.6)
cbar.set_label(r'$\omega_z$ [1/s]', fontsize=12)

ax.set_zlabel('')
ax.zaxis._axinfo['juggled'] = (2, 2, 2)
ax.set_zticks([])

# --- PANE VISIBILITY ---
ax.zaxis.pane.fill = False
ax.zaxis.pane.set_edgecolor('none')

ax.xaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('none')
ax.yaxis.pane.fill = False
ax.yaxis.pane.set_edgecolor('none')

# --- AXIS LINES ---
ax.xaxis.line.set_color('none')
ax.yaxis.line.set_color('none')
ax.zaxis.line.set_color('none')

# --- TICKS ---
ax.set_xticks([])
ax.set_yticks([])

ax.grid(False)

# ============================================================
# ANIMATION
# ============================================================
def update(frame):
    ax.view_init(elev=elev_start, azim=azim_seq[frame])
    return sc,

anim = FuncAnimation(fig, update, frames=n_frames, interval=1000/fps, blit=False)

print("Saving GIF... this may take a moment")
anim.save('q_criterion_rotation.gif', writer=PillowWriter(fps=fps),
           savefig_kwargs={'facecolor': 'white'})
print("Saved as 'q_criterion_rotation.gif'")

exit()
from matplotlib.animation import FFMpegWriter

writer = FFMpegWriter(fps=fps, bitrate=1800)
anim.save('q_criterion_rotation.mp4', writer=writer,
          savefig_kwargs={'facecolor': 'white'})
print("Saved as 'q_criterion_rotation.mp4'")