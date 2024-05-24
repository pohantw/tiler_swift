import numpy

class Tiler_Qtree:

    def __init__( self, config, tensors ):
        self._config = config
        self._tensors = tensors
    

    def _tile_recursive( self, rect ):
        x, y, width, height = rect

        # loop through tensors, count the non-zeros in the tile
        nnz = {}
        for tensor_name, tensor in self._tensors.items():
            tiled_tensor = tensor[y:y+height, x:x+width]
            nnz[tensor_name] = numpy.count_nonzero(tiled_tensor)
        
        # check if the tile fits in the memory tile
        # TODO: also need to check output
        # TODO: now hard-coded to 15, need to change
        tile_fit_ok = True
        for tensor_name, nnz in nnz.items():
            if nnz > 15:
                tile_fit_ok = False

        # if the tile fits, return the tile
        # otherwise, recursively split the tile
        # TODO: there might be overlaps in the tiles, need to fix
        if tile_fit_ok:
            result = {}
            for tensor_name in self._tensors.keys():
                result[tensor_name] = [x, y, width, height]
            return [result]
        else:
            half_width = width // 2
            half_height = height // 2
            q1 = self._tile_recursive( [x, y, half_width, half_height] )
            q2 = self._tile_recursive( [x + half_width, y, half_width, half_height] )
            q3 = self._tile_recursive( [x, y + half_height, half_width, half_height] )
            q4 = self._tile_recursive( [x + half_width, y + half_height, half_width, half_height] )
            return q1 + q2 + q3 + q4


    def tile( self ):
        assert len(self._tensors) == 2, "only support two input tensors"
        tensor_name = list(self._tensors.keys())[0]
        tensor_width = self._tensors[tensor_name].shape[1]
        tensor_height = self._tensors[tensor_name].shape[0]
        return self._tile_recursive([0, 0, tensor_width, tensor_height])
