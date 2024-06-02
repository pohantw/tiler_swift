import numpy

class Tiler_Btree:

    def __init__( self, config, tensors, model ):
        self._config = config
        self._tensors = tensors
        self._model = model
    

    def _tile_recursive( self, rect ):
        x, y, width, height = rect

        # assumption: if the tile can have positive runtime estimate,
        # then its runtime must be better than its splits
        tile_runtime = self._model.estimate_tile_runtime( rect )
        if tile_runtime < 0:
            # the tile is infeasible, so we need to split it
            if width > height:
                hw = width // 2
                r1, t1 = self._tile_recursive( [x, y, hw, height] )
                r2, t2 = self._tile_recursive( [x + hw, y, width-hw, height] )
                return r1 + r2, t1 + t2
            else:
                hh = height // 2
                r1, t1 = self._tile_recursive( [x, y, width, hh] )
                r2, t2 = self._tile_recursive( [x, y + hh, width, height-hh] )
                return r1 + r2, t1 + t2
        else:
            result = {}
            for tensor_name in self._tensors.keys():
                result[tensor_name] = [x, y, width, height]
            return tile_runtime, [result]


    def tile( self ):
        assert len(self._tensors) == 2, "only support two input tensors"
        tensor_name = list(self._tensors.keys())[0]
        tensor_width = self._tensors[tensor_name].shape[1]
        tensor_height = self._tensors[tensor_name].shape[0]
        run_time_estimate, result = self._tile_recursive([0, 0, tensor_width, tensor_height])
        return result
