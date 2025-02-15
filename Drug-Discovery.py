import numpy as np
import plotly.graph_objects as go
import random

# Parameters
RECEPTOR_POSITION = np.array([5, 5, 5])  # Center of the receptor
BINDING_SITE = np.array([5, 6, 5])  # Specific binding pocket on the receptor
LIGAND_START = np.array([0, 0, 0])  # Ligand's starting position
NUM_STEPS = 100  # Total number of Monte Carlo steps
TEMPERATURE = 1.0  # Higher temperature allows more exploration
BINDING_RADIUS = 1.5  # Radius of "binding" pocket

# Monte Carlo Simulation
ligand_positions = [LIGAND_START]  # Track ligand's path
ligand_pos = LIGAND_START.copy()
energies = []  # Store energy at each step

def calculate_energy(ligand_pos, binding_site):
    """Simple energy function: Lower energy when ligand is closer to the binding site."""
    distance = np.linalg.norm(ligand_pos - binding_site)
    return distance  # Lower distance = lower energy

# Perform Monte Carlo simulation
for _ in range(NUM_STEPS):
    # Propose a random move in 3D
    move = np.random.uniform(-1, 1, size=3)
    new_pos = ligand_pos + move

    # Calculate energies
    old_energy = calculate_energy(ligand_pos, BINDING_SITE)
    new_energy = calculate_energy(new_pos, BINDING_SITE)

    # Accept move based on Metropolis criterion
    if new_energy < old_energy or random.random() < np.exp(-(new_energy - old_energy) / TEMPERATURE):
        ligand_pos = new_pos  # Accept move

    ligand_positions.append(ligand_pos)
    energies.append(new_energy)

# Convert ligand positions to a NumPy array for plotting
ligand_positions = np.array(ligand_positions)

# Visualization with Plotly
frames = []
for i in range(len(ligand_positions)):
    # Ligand path up to current frame
    frame = go.Scatter3d(
        x=ligand_positions[:i+1, 0],  # Ligand path up to current frame
        y=ligand_positions[:i+1, 1],
        z=ligand_positions[:i+1, 2],
        mode='lines+markers',
        marker=dict(size=4, color='red'),
        line=dict(color='red', width=2),
        name="Ligand Path"
    )
    # Energy plot up to current frame
    energy_frame = go.Scatter(
        x=list(range(i+1)),
        y=energies[:i+1],
        mode='lines+markers',
        marker=dict(size=6, color='blue'),
        name="Energy"
    )
    frames.append(go.Frame(data=[frame, energy_frame]))

# Create receptor as a large sphere
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = RECEPTOR_POSITION[0] + BINDING_RADIUS * np.cos(u) * np.sin(v)
y = RECEPTOR_POSITION[1] + BINDING_RADIUS * np.sin(u) * np.sin(v)
z = RECEPTOR_POSITION[2] + BINDING_RADIUS * np.cos(v)

# Base figure
fig = go.Figure(
    data=[
        # Receptor sphere
        go.Surface(x=x, y=y, z=z, colorscale='Blues', opacity=0.5, name="Receptor"),
        # Binding pocket marker
        go.Scatter3d(
            x=[BINDING_SITE[0]],
            y=[BINDING_SITE[1]],
            z=[BINDING_SITE[2]],
            mode='markers',
            marker=dict(size=10, color='purple'),
            name="Binding Pocket"
        ),
        # Ligand initial position
        go.Scatter3d(
            x=[ligand_positions[0, 0]],
            y=[ligand_positions[0, 1]],
            z=[ligand_positions[0, 2]],
            mode='markers',
            marker=dict(size=8, color='green'),
            name="Ligand Start"
        ),
        # Initial energy plot
        go.Scatter(
            x=[0],
            y=[energies[0]] if energies else [0],
            mode='markers',
            marker=dict(size=6, color='blue'),
            name="Energy"
        ),
    ],
    layout=go.Layout(
        title="Monte Carlo Ligand-Receptor Docking with Binding Pocket",
        scene=dict(
            xaxis=dict(range=[-5, 10]),
            yaxis=dict(range=[-5, 10]),
            zaxis=dict(range=[-5, 10]),
        ),
        xaxis=dict(title="Step"),
        yaxis=dict(title="Energy"),
        updatemenus=[
            {
                "buttons": [
                    {"args": [None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}],
                     "label": "Play", "method": "animate"},
                    {"args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}],
                     "label": "Pause", "method": "animate"}
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }
        ]
    ),
    frames=frames
)

# Show the animation
fig.show()
