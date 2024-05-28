import numpy

class Tiler_Simple:

    def __init__( self, config, tensors, max_nnzs ):
        self._config = config
        self._tensors = tensors
        self._max_nnzs = max_nnzs
    
    def _create_tile_pairs( self, tile_width, tile_height ):
        results = []
        for x in range(0, self._tensors['A'].shape[1], tile_width):
            for y in range(0, self._tensors['A'].shape[0], tile_height):
                if tile_width + x > self._tensors['A'].shape[1]:
                    tw = self._tensors['A'].shape[1] - x
                else:
                    tw = tile_width
                if tile_height + y > self._tensors['A'].shape[0]:
                    th = self._tensors['A'].shape[0] - y
                else:
                    th = tile_height
                result = {}
                result['A'] = [x, y, tw, th]
                result['B'] = [x, y, tw, th]
                results.append(result)
        return results
    
    def _check_if_all_tiles_fit( self, results, max_nnzs ):
        for result in results:
            nnzs = {}
            for tensor_name, tensor in self._tensors.items():
                x_start = result[tensor_name][0]
                y_start = result[tensor_name][1]
                x_end = result[tensor_name][0] + result[tensor_name][2]
                y_end = result[tensor_name][1] + result[tensor_name][3]
                tiled_tensor = tensor[y_start:y_end, x_start:x_end]
                nnzs[tensor_name] = numpy.count_nonzero(tiled_tensor)
            for tensor_name, nnz in nnzs.items():
                if nnz > max_nnzs:
                    return False
        return True

    def tile( self ):
        assert len(self._tensors) == 2, "only support two input tensors"
        tensor_name = list(self._tensors.keys())[0]
        tensor_width = self._tensors[tensor_name].shape[1]
        tensor_height = self._tensors[tensor_name].shape[0]

        all_tiles_fit = False
        tw = tensor_width
        th = tensor_height
        while not all_tiles_fit:
            results = self._create_tile_pairs(tw, th)
            all_tiles_fit = self._check_if_all_tiles_fit(results, self._max_nnzs)
            if not all_tiles_fit:
                tw = tw // 2
                th = th // 2

        return results
