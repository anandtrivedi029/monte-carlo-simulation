import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# Parameters
CHAIN_LENGTH = 20  # Number of amino acids
GRID_SIZE = 20     # Size of the grid
STEPS = 1000       # Total Monte Carlo steps

# Initialize protein chain as a line in the grid
protein_chain = [(i, GRID_SIZE // 2) for i in range(CHAIN_LENGTH)]

# Energy function: Penalize overlaps (simplified)
def calculate_energy(chain):
    unique_positions = len(set(chain))
    return CHAIN_LENGTH - unique_positions  # Energy increases with overlaps

# Monte Carlo step
def monte_carlo_step(chain):
    # Select a random amino acid (not the first or last)
    index = random.randint(1, len(chain) - 2)
    
    # Random move: Up, down, left, right
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    dx, dy = random.choice(moves)
    new_position = (chain[index][0] + dx, chain[index][1] + dy)
    
    # Create a new chain with the move
    new_chain = chain[:]
    new_chain[index] = new_position
    
    # Apply periodic boundary conditions
    new_chain[index] = (new_chain[index][0] % GRID_SIZE, new_chain[index][1] % GRID_SIZE)
    
    # Calculate energy difference
    old_energy = calculate_energy(chain)
    new_energy = calculate_energy(new_chain)
    
    # Accept move with Metropolis criterion
    if new_energy <= old_energy or random.random() < np.exp(-(new_energy - old_energy)):
        return new_chain  # Accept move
    return chain  # Reject move

# Visualization
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, GRID_SIZE)
ax.set_ylim(0, GRID_SIZE)
ax.set_xticks([])
ax.set_yticks([])

protein_plot, = ax.plot([], [], "bo-", lw=2)  # Protein chain
energy_text = ax.text(0.05, 0.95, "", transform=ax.transAxes, fontsize=12, va="top")

# Animation update function
def update(frame):
    global protein_chain
    protein_chain = monte_carlo_step(protein_chain)
    
    # Update protein chain plot
    x_coords, y_coords = zip(*protein_chain)
    protein_plot.set_data(x_coords, y_coords)
    
    # Update energy text
    energy_text.set_text(f"Energy: {calculate_energy(protein_chain)}")
    return protein_plot, energy_text

# Run animation
ani = FuncAnimation(fig, update, frames=STEPS, blit=True, interval=50, repeat=False)
plt.title("Protein Folding Simulation")
plt.show()
