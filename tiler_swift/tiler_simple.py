import numpy

class Tiler_Simple:

    def __init__( self, config, tensors, model ):
        self._config = config
        self._tensors = tensors
        self._model = model
    
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
    
    def _check_if_all_tiles_fit( self, results ):
        fit_ok = True
        for result in results:
            for tensor_name, tensor in self._tensors.items():
                x, y, w, h = result[tensor_name]
                tile_runtime = self._model._estimate_tile_runtime_elemadd([x, y, w, h])
                if tile_runtime == -1:
                    fit_ok = False
        return fit_ok

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
            all_tiles_fit = self._check_if_all_tiles_fit(results)
            if not all_tiles_fit:
                if tw != 1:
                    tw = tw // 2
                if th != 1:
                    th = th // 2

        return results
