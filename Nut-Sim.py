import numpy as np
import matplotlib.pyplot as plt
import random

# Constants
MEDIUM_SIZE = 10  # Size of the medium (10x10 units)
NUM_NEUTRONS = 1000  # Total number of neutrons
MEAN_FREE_PATH = 1.0  # Average distance between interactions
SCATTER_PROB = 0.6  # Probability of scattering
ABSORPTION_PROB = 0.3  # Probability of absorption
FISSION_PROB = 0.1  # Probability of fission (should sum to 1 with others)

# Initialize neutron positions and tracks
neutron_tracks = []  # Tracks for visualization
absorbed_positions = []  # Positions of absorbed neutrons
fission_positions = []  # Positions of fission events

def random_direction():
    """Generate a random direction in 2D (angle in radians)."""
    angle = random.uniform(0, 2 * np.pi)
    return np.cos(angle), np.sin(angle)

def simulate_neutron():
    """Simulate the path of a single neutron."""
    # Start neutron at random position
    x, y = random.uniform(0, MEDIUM_SIZE), random.uniform(0, MEDIUM_SIZE)
    neutron_path = [(x, y)]  # Store neutron's path

    while 0 <= x <= MEDIUM_SIZE and 0 <= y <= MEDIUM_SIZE:
        # Sample distance to next interaction
        distance = np.random.exponential(MEAN_FREE_PATH)
        dx, dy = random_direction()
        x += dx * distance
        y += dy * distance
        neutron_path.append((x, y))

        # Determine interaction type
        interaction = np.random.choice(
            ["scatter", "absorb", "fission"],
            p=[SCATTER_PROB, ABSORPTION_PROB, FISSION_PROB]
        )

        if interaction == "absorb":
            absorbed_positions.append((x, y))
            break
        elif interaction == "fission":
            fission_positions.append((x, y))
            # Spawn two new neutrons (fission event)
            simulate_neutron()
            simulate_neutron()
            break
        # If scattering, neutron continues with a new random direction

    neutron_tracks.append(neutron_path)

# Simulate all neutrons
for _ in range(NUM_NEUTRONS):
    simulate_neutron()

# Visualization
plt.figure(figsize=(8, 8))
plt.xlim(0, MEDIUM_SIZE)
plt.ylim(0, MEDIUM_SIZE)
plt.title("Neutron Transport Simulation")

# Plot neutron tracks
for path in neutron_tracks:
    x_coords, y_coords = zip(*path)
    plt.plot(x_coords, y_coords, linewidth=0.5, alpha=0.7)

# Plot absorbed and fission events
absorbed_x, absorbed_y = zip(*absorbed_positions) if absorbed_positions else ([], [])
fission_x, fission_y = zip(*fission_positions) if fission_positions else ([], [])
plt.scatter(absorbed_x, absorbed_y, color="red", label="Absorbed", s=10)
plt.scatter(fission_x, fission_y, color="blue", label="Fission", s=10)

plt.legend()
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.grid()
plt.show()
