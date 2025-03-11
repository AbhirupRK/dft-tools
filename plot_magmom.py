#%%
import numpy as np
from matplotlib import pyplot as plt
from modules.plotting import DrawArrow
from modules.dft import ReadVaspOutput

##########################################################################
##### Inputs for the plot #####

directory = "./"
output_data = ReadVaspOutput(directory)

# Atoms
atom_size = 50
atom_colors = ['red', 'green', 'blue']
exclude_atoms = range(1,28)     # List: starts from 1

# Magnetic moments range
min_magmom, max_magmom = 0.01, 1

# Arrows
arrow_scale = 20
arrow_color = 'red'
head_size=0.5; head_thickness=0.4; shaft_thickness=0.1

# Initial view angles (in degree)
elevation=0; azimuth=-100; roll_z=0

##########################################################################
##### The Main Script #####

#%% ##### Reading output data
nions = output_data.data["nions"]
natoms = sum(nions)
lattice = output_data.data["lattice"]
pos_cart = output_data.data["pos_cart"]
magmom = output_data.data["magmom"]
sel_atoms = [i for i in range(natoms) if i+1 not in exclude_atoms]

##### Ingredients for plotting
# Define the 3 lattice vectors
origin = np.array([0, 0, 0])
v1, v2, v3 = lattice
atoms = pos_cart

# Generate the 8 vertices of the parallelepiped
vertices = np.array([
    origin,
    origin + v1,
    origin + v2,
    origin + v3,
    origin + v1 + v2,
    origin + v1 + v3,
    origin + v2 + v3,
    origin + v1 + v2 + v3
])

# Edges of the cube
edges = [
    (0, 1), (0, 2), (0, 3),  # Edges from origin
    (1, 4), (1, 5),          # Edges from v1
    (2, 4), (2, 6),          # Edges from v2
    (3, 5), (3, 6),          # Edges from v3
    (4, 7), (5, 7), (6, 7)   # Top edges
]

#%% ##### Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot lattice vectors
ax.quiver(*origin, *v1, color='r', arrow_length_ratio=0, lw=2)
ax.quiver(*origin, *v2, color='g', arrow_length_ratio=0, lw=2)
ax.quiver(*origin, *v3, color='b', arrow_length_ratio=0, lw=2)

# Plot edges of the unit cell
for edge in edges:
    ax.plot(*zip(vertices[edge[0]], vertices[edge[1]]), color='k')

# Plot the atoms
for i in sel_atoms:
    for j in range(len(nions)):
        if i < nions[j]:
            try:
                ax.scatter(atoms[i, 0], atoms[i, 1], atoms[i, 2], color=atom_colors[j], s=atom_size)
            except:
                ax.scatter(atoms[i, 0], atoms[i, 1], atoms[i, 2], color=atom_colors[0], s=atom_size)
                print("ERROR: Not enough atom colors")


# Plot magmom arrows
for i in sel_atoms:
    if min_magmom <= np.linalg.norm(magmom[i]) <= max_magmom:
        DrawArrow(ax, pos_cart[i], magmom[i]*arrow_scale, head_size=head_size, shaft_thickness=shaft_thickness, head_thickness=head_thickness, color=arrow_color)

# Remove the background stuffs
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
# removes grid lines
ax.grid(False) 
# Remove background panes
ax.xaxis.pane.set_visible(False)
ax.yaxis.pane.set_visible(False)
ax.zaxis.pane.set_visible(False)

# Optionally remove axis lines and ticks
ax.xaxis.line.set_visible(False)
ax.yaxis.line.set_visible(False)
ax.zaxis.line.set_visible(False)

ax.set_aspect('equal')
ax.view_init(elev=elevation, azim=azimuth, roll=roll_z)
plt.show()

#%% 
