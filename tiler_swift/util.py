import scipy.sparse as sparse
import numpy as np

def coo2csf(coo_matrix):
  # The number of values in the tensor
  num_values = len(coo_matrix.data)
  n_dim = len(coo_matrix.shape)

  crd_dict = {} 
  pos_dict = {}
  if coo_matrix.nnz == 0:
    # this is a completely empty matrix
    for dim in range(0, n_dim):
      crd_dict[dim] = [0]
      pos_dict[dim] = [0, 1]
    data_array = [0]
    return pos_dict, crd_dict, data_array
  else: 
    cur_fiber_length = [num_values]
    next_level_fiber_length = [1]
    for dim in range(0, n_dim):
      idx = 0
      for fiber_length in cur_fiber_length:
        pos_count = 1
        for i in range(0, fiber_length):
          # The very first element in the crd/seg output
          if (idx == 0):
            crd_dict[dim] = [coo_matrix.coords[dim][idx]]
            pos_dict[dim] = [0]
          else:
            # Beginning of a fiber
            if (i == 0):
              crd_dict[dim].append(coo_matrix.coords[dim][idx])
            else:
              if (crd_dict[dim][-1] != coo_matrix.coords[dim][idx]):
                crd_dict[dim].append(coo_matrix.coords[dim][idx])
                next_level_fiber_length.append(1)
                pos_count += 1
              else:
                next_level_fiber_length[-1] += 1
          idx += 1
        pos_dict[dim].append(pos_count + pos_dict[dim][-1])
        pos_count = 1
      cur_fiber_length = next_level_fiber_length
      next_level_fiber_length = [1]
  return pos_dict, crd_dict, coo_matrix.data



