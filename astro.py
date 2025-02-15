import numpy as np
import plotly.graph_objects as go

# Parameters
NUM_PARTICLES = 200  # Number of stars
G = 1  # Gravitational constant (scaled for visualization)
TIME_STEP = 0.01  # Time step for integration
NUM_STEPS = 500  # Number of simulation steps
SOFTENING = 0.1  # To prevent singularities in the gravitational force

# Initialize particle positions, velocities, and masses
np.random.seed(42)  # For reproducibility
positions = np.random.uniform(-5, 5, (NUM_PARTICLES, 3))  # Random 3D positions
velocities = np.random.uniform(-0.5, 0.5, (NUM_PARTICLES, 3))  # Random velocities
masses = np.random.uniform(0.5, 1.5, NUM_PARTICLES)  # Random masses

# Store positions for plotting
positions_over_time = [positions.copy()]

# Function to calculate gravitational forces
def compute_gravitational_force(pos, masses):
    """Compute gravitational forces for all particles."""
    force = np.zeros_like(pos)  # Shape (200, 3) to store forces
    for i in range(len(pos)):
        diff = pos - pos[i]  # Shape (200, 3)
        distance = np.linalg.norm(diff, axis=1) + SOFTENING  # Shape (200,)
        # Compute gravitational force
        force[i] = np.sum(G * masses[i] * masses[:, None] * diff / distance[:, None]**3, axis=0)
    return force

# Simulation loop
for _ in range(NUM_STEPS):
    forces = compute_gravitational_force(positions, masses)
    velocities += forces * TIME_STEP / masses[:, None]  # Update velocities
    positions += velocities * TIME_STEP  # Update positions
    positions_over_time.append(positions.copy())  # Save positions

# Convert to NumPy array for visualization
positions_over_time = np.array(positions_over_time)

# Visualization with Plotly
frames = []
for i in range(len(positions_over_time)):
    frame = go.Scatter3d(
        x=positions_over_time[i, :, 0],
        y=positions_over_time[i, :, 1],
        z=positions_over_time[i, :, 2],
        mode='markers',
        marker=dict(
            size=4,  # Make stars appear glowing
            color=np.linalg.norm(positions_over_time[i], axis=1),  # Brightness by distance
            colorscale='Bluered',  # Glowing stars look
            opacity=0.8  # Semi-transparent stars
        ),
        name="Stars"
    )
    frames.append(go.Frame(data=[frame]))

# Create the base figure
fig = go.Figure(
    data=[
        go.Scatter3d(
            x=positions_over_time[0, :, 0],
            y=positions_over_time[0, :, 1],
            z=positions_over_time[0, :, 2],
            mode='markers',
            marker=dict(
                size=4,
                color=np.linalg.norm(positions_over_time[0], axis=1),
                colorscale='Bluered',
                opacity=0.8,
            ),
        )
    ],
    layout=go.Layout(
        title="Galaxy Formation Simulation",
        scene=dict(
            xaxis=dict(visible=False),  # Hide axes
            yaxis=dict(visible=False),  # Hide axes
            zaxis=dict(visible=False),  # Hide axes
            bgcolor="black"  # Black background for space effect
        ),
        updatemenus=[
            {
                "buttons": [
                    {"args": [None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}],
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
