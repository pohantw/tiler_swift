import numpy as np
import os
from scipy.sparse import random

# Seed for the random number generator
np.random.seed(0)

# Dimensions of the matrices
matrix_sizes = [10, 20, 40, 80, 160]
densities = [0.1, 0.2, 0.4, 0.8, 1.0]

# Generate matrices
for matrix_size in matrix_sizes:
    for density in densities:
        # Assume square matrix for now
        rows = matrix_size
        cols = matrix_size
        # Generate a random sparse 2D matrix
        matrixA = random(rows, cols, density=density, format='csr', random_state=np.random.default_rng())
        matrixB = random(rows, cols, density=density, format='csr', random_state=np.random.default_rng())
        # Convert the sparse matrix to a dense matrix
        dense_matrixA = matrixA.toarray()
        dense_matrixB = matrixB.toarray()
        # create a folder
        folder = f'{matrix_size}x{matrix_size}_density{density}'
        os.makedirs(folder, exist_ok=True)
        # Save the matrix to a .npy file
        np.save(f'{folder}/matrixA.npy', dense_matrixA)
        np.save(f'{folder}/matrixB.npy', dense_matrixB)
