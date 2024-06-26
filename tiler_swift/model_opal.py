import numpy

class Model_Opal:

    def __init__( self, config, tensors ):
        self._config = config
        self._tensors = tensors
        # why divide by 2.0?
        # because half of the capacity is used for seg
        # unit: number of elements
        self._out_mem_size = config['memory_capacity_mtile'] * 1024 / 2.0 / config['element_size']


    def _estimate_tile_runtime_elemadd( self, rect ):
        x, y, width, height = rect
        # we use the number of output non-zero elements
        # to estimate the runtime, each non-zero output element
        # requires one unit of computation time
        output_nnzs = 0
        for _, tensor in self._tensors.items():
            # for elementwise-add, the worst case is that
            # all input nnzs do not overlap, so we need to
            # add up all input nnzs
            output_nnzs += numpy.count_nonzero( tensor[y:y+height, x:x+width] )
        if output_nnzs > self._out_mem_size:
            # we use negative value to indicate that the tiling is infeasible
            print(f"[Model_Opal] output_nnzs({output_nnzs}) > out_mem_size({self._out_mem_size})")
            return -1
        else:
            print(f"[Model_Opal] output_nnzs({output_nnzs}) fits")
            return self._config['tile_overhead'] + output_nnzs
        
        
    def _estimate_tile_runtime_elemmul( self, rect ):
        x, y, width, height = rect
        # we use the number of output non-zero elements
        # to estimate the runtime, each non-zero output element
        # requires one unit of computation time
        output_nnzs = 0
        for _, tensor in self._tensors.items():
            # for elementwise-mult, the worst case is that
            # all input nnzs overlap, so the output size is
            # the maximum of all input sizes
            output_nnzs = max( output_nnzs,
                               numpy.count_nonzero( tensor[y:y+height, x:x+width] ) )
        if output_nnzs > self._out_mem_size:
            # we use negative value to indicate that the tiling is infeasible
            print(f"[Model_Opal] output_nnzs({output_nnzs}) > out_mem_size({self._out_mem_size})")
            return -1
        else:
            print(f"[Model_Opal] output_nnzs({output_nnzs}) fits")
            return self._config['tile_overhead'] + output_nnzs


    def estimate_tile_runtime( self, rect ):
        if self._config['operation'] == 'elementwise-add':
            return self._estimate_tile_runtime_elemadd( rect )
        elif self._config['operation'] == 'elementwise-mul':
            return self._estimate_tile_runtime_elemmul( rect )
        else:
            raise ValueError( 'Unsupported operation: ' + self._config['operation'] )
        
