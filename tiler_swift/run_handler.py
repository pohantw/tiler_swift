import os
import yaml
import numpy
import sparse
import toml

from tiler import Tiler
from util import coo2csf

class RunHandler:


  def __init__( self ):
    pass


  def print_banner( self ):
    print("==============================================================")
    print("*    _______ _ _                  _____         _  __ _      *")
    print("*   |__   __(_) |                / ____|       (_)/ _| |     *")
    print("*      | |   _| | ___ _ __ _____| (_____      ___| |_| |_    *")
    print("*      | |  | | |/ _ \ '__|______\___ \ \ /\ / / |  _| __|   *")
    print("*      | |  | | |  __/ |         ____) \ V  V /| | | | |_    *")
    print("*      |_|  |_|_|\___|_|        |_____/ \_/\_/ |_|_|  \__|   *")
    print("==============================================================")


  def load_config( self, config_path ):
    # check if the config file exists
    if not os.path.exists(config_path):
      print(f"Config file {config_path} does not exist.")
      exit(1)
    # load the config file
    with open(config_path, 'r') as f:
      self._config = yaml.safe_load(f)


  def load_tensors( self, tensor_path ):
    self._tensors = {}
    for name in self._config['input_matrix_names']:
      tensor_file = os.path.join(tensor_path, f"{name}.npy")
      if not os.path.exists(tensor_file):
        print(f"Tensor file {tensor_file} does not exist.")
        exit(1)
      self._tensors[name] = numpy.load(tensor_file)


  def report_config( self ):
    print("")
    print("Configurations:")
    print("--------------------------------------------------------------")
    for key, value in self._config.items():
      print(f"{key:<30}: {value}")
    print("")
    print("Tensors:")
    print("--------------------------------------------------------------")
    for name, tensor in self._tensors.items():
      shape = tensor.shape
      nnz = numpy.count_nonzero(tensor)
      total_elements = tensor.size
      sparsity = 100.0 * ( (total_elements - nnz) / total_elements)
      print(f"{name:<10}: shape: {shape}, nnz: {nnz}, sparsity: {sparsity:.2f}%")
    print("")


  def results_sanity_check( self, results ):
    # The result is a list of tiling pairs:
    # [
    #   {'A': [x, y, w, h], 'B': [x, y, w, h], ...},
    #   {'A': [x, y, w, h], 'B': [x, y, w, h], ...},
    #   ...
    #   {'A': [x, y, w, h], 'B': [x, y, w, h], ...}
    # ]
    # each tiling pair is a dictionary, where the key is the
    # tensor name and the value is the tiling information
    #    x: x-coordinate of the top-left corner
    #    y: y-coordinate of the top-left corner
    #    w: width of the tile
    #    h: height of the tile
    assert isinstance(results, list), "tiling results should be a list"
    for pair in results:
      assert isinstance(pair, dict), "tiling pair should be a dictionary"
      for tensor_name, tensor_tile_info in pair.items():
        assert isinstance(tensor_name, str), "tensor name should be a string"
        assert isinstance(tensor_tile_info, list), "tiling info should be a list"
        assert len(tensor_tile_info) == 4, "tiling info should have 4 elements"
        assert all(isinstance(v, int) for v in tensor_tile_info), "tiling info should be integers"
        assert tensor_name in self._tensors, f"tensor name {tensor_name} not found in the input tensors"
        assert tensor_tile_info[2] >= 0, "width should be positive"
        assert tensor_tile_info[3] >= 0, "height should be positive"
        ulx = tensor_tile_info[0]
        uly = tensor_tile_info[1]
        lrx = tensor_tile_info[0] + tensor_tile_info[2] - 1
        lry = tensor_tile_info[1] + tensor_tile_info[3] - 1
        assert ulx >= 0, "ulx-coordinate should be non-negative"
        assert uly >= 0, "uly-coordinate should be non-negative"
        assert lrx < self._tensors[tensor_name].shape[1], "lrx-coordinate should be within the tensor"
        assert lry < self._tensors[tensor_name].shape[0], "lry-coordinate should be within the tensor"
    print("===Sanity check passed!===")


  def save_results( self, results, output_path ):
    result_file_name = "results.yaml"
    if not os.path.exists(output_path):
      os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, result_file_name), "w") as f:
      yaml.dump(results, f)
    print(f"Results saved to {output_path}/{result_file_name}")


  def gen_tiles ( self, results ):
    self._tile_pairs = []
    for idx, pairs in enumerate(results):
      self._tile_pairs.append({})
      for name, tile_loc_size in pairs.items():
        x = tile_loc_size[0]
        y = tile_loc_size[1]
        w = tile_loc_size[2]
        h = tile_loc_size[3]
        tile = self._tensors[name][x:x+w, y:y+h]
        self._tile_pairs[idx][name] = tile

  def save_tiles( self, output_path, verbose ):
    tile_pair_path_list = {}
    tile_pair_path_list["sam_config"] = {}
    tile_pair_path_list["sam_config"]["sam_path"] = []
    for idx, pairs in enumerate(self._tile_pairs):
      tile_path = os.path.join(output_path, "tile_" + str(idx))
      tile_pair_path_list["sam_config"]["sam_path"].append("tile_" + str(idx))
      if not os.path.exists(tile_path):
        os.makedirs(tile_path, exist_ok=True)
      for name, tile in pairs.items():
        numpy.save(os.path.join(tile_path, name), tile)
        if verbose:
          print(f"Tile {name} in numpy format saved to {tile_path}/{name}.npy")
        tile_coo_sparse = sparse.COO(tile)
        pos_dict, crd_dict, data = coo2csf(tile_coo_sparse)
        for dim, seg_array in pos_dict.items():
          with open(os.path.join(tile_path, "tensor_" + name + "_mode_" + str(dim) + "_seg"), "w") as seg_file:
            for seg in seg_array:
              seg_file.write(str(seg))
              seg_file.write("\n")
            if verbose:
              print(f"Segment data for mode {str(dim)} of tile {name} saved to {seg_file.name}")
        for dim, crd_array in crd_dict.items():
          with open(os.path.join(tile_path, "tensor_" + name + "_mode_" + str(dim) + "_crd"), "w") as crd_file:
            for crd in crd_array:
              crd_file.write(str(crd))
              crd_file.write("\n")
            if verbose:
              print(f"Coordinate data for mode {str(dim)} of tile {name} saved to {seg_file.name}")
        with open(os.path.join(tile_path, "tensor_" + name + "_mode_vals"), "w") as val_file:
          for val in data:
            val_file.write(str(val))
            val_file.write("\n")
          if verbose:
            print(f"Value data of tile {name} saved to {val_file.name}")
      with open(os.path.join(output_path, "tile_pair_paths.toml"), "w") as toml_file:
        toml.dump(tile_pair_path_list, toml_file)
    print(f"Tiles and list of tiles saved to {output_path}")


  def launch( self, config_path, tensor_path, output_path, verbose ):

    # welcome!
    self.print_banner()

    # loading configurations
    self.load_config(config_path)
    
    # loading input tensors
    self.load_tensors(tensor_path)
    
    # report configurations
    self.report_config()

    # Execute the tiler
    tiler = Tiler(config=self._config, tensors=self._tensors)
    results = tiler.tile()

    # sanity check
    self.results_sanity_check(results)

    # generate tiles
    self.gen_tiles(results)

    # save the tiling decision results
    self.save_results(results, output_path)

    # save the generated tiles
    self.save_tiles(output_path, verbose )

    return

