import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import random

# Parameters
CHAIN_LENGTH = 15  # Number of amino acids in the chain
STEPS = 500        # Number of Monte Carlo steps

# Initialize protein chain as a straight line in 3D space
protein_chain = np.array([[i, 0, 0] for i in range(CHAIN_LENGTH)])  # Initial straight line

# Energy function: Penalize overlaps
def calculate_energy(chain):
    unique_positions = len(set(tuple(pos) for pos in chain))
    return CHAIN_LENGTH - unique_positions  # Energy increases with overlaps

# Monte Carlo move in 3D
def monte_carlo_step(chain):
    # Select a random amino acid (not the first or last)
    index = random.randint(1, len(chain) - 2)
    
    # Random move: Change position in a random 3D direction
    move = np.random.choice([-1, 1], size=3)
    new_position = chain[index] + move

    # Create a new chain with the move
    new_chain = chain.copy()
    new_chain[index] = new_position

    # Calculate energy difference
    old_energy = calculate_energy(chain)
    new_energy = calculate_energy(new_chain)

    # Accept move with Metropolis criterion
    if new_energy <= old_energy or random.random() < np.exp(-(new_energy - old_energy)):
        return new_chain  # Accept move
    return chain  # Reject move

# Visualization setup
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(0, CHAIN_LENGTH)
ax.set_ylim(-CHAIN_LENGTH // 2, CHAIN_LENGTH // 2)
ax.set_zlim(-CHAIN_LENGTH // 2, CHAIN_LENGTH // 2)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

protein_plot, = ax.plot([], [], [], "bo-", lw=2)  # Protein chain
energy_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes, fontsize=12, va="top")

# Animation update function
def update(frame):
    global protein_chain
    protein_chain = monte_carlo_step(protein_chain)
    
    # Update protein chain plot
    x_coords, y_coords, z_coords = protein_chain[:, 0], protein_chain[:, 1], protein_chain[:, 2]
    protein_plot.set_data(x_coords, y_coords)
    protein_plot.set_3d_properties(z_coords)
    
    # Update energy text
    energy_text.set_text(f"Energy: {calculate_energy(protein_chain)}")
    return protein_plot, energy_text

# Run animation
ani = FuncAnimation(fig, update, frames=STEPS, blit=True, interval=50, repeat=False)
plt.title("3D Protein Folding Simulation")
plt.show()
