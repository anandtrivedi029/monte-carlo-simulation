import numpy as np
import matplotlib.pyplot as plt
import random

# Initial conditions
num_N2 = 50  # Number of N2 molecules
num_H2 = 150  # Number of H2 molecules
num_NH3 = 0   # Initial number of NH3 molecules

reaction_rate = 0.05  # Probability of a successful reaction per step
time_steps = 200      # Total number of simulation steps

# Track molecule counts over time
N2_counts = []
H2_counts = []
NH3_counts = []

# Simulation loop
for t in range(time_steps):
    N2_counts.append(num_N2)
    H2_counts.append(num_H2)
    NH3_counts.append(num_NH3)
    
    # Attempt reactions
    if num_N2 > 0 and num_H2 >= 3:  # Check if enough molecules are available
        if random.random() < reaction_rate:  # Reaction occurs probabilistically
            num_N2 -= 1  # One N2 molecule is consumed
            num_H2 -= 3  # Three H2 molecules are consumed
            num_NH3 += 2  # Two NH3 molecules are produced

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(N2_counts, label="N₂ (Nitrogen)", color="blue")
plt.plot(H2_counts, label="H₂ (Hydrogen)", color="red")
plt.plot(NH3_counts, label="NH₃ (Ammonia)", color="green")
plt.xlabel("Time Steps")
plt.ylabel("Number of Molecules")
plt.title("Haber Process Simulation")
plt.legend()
plt.grid()
plt.show()
