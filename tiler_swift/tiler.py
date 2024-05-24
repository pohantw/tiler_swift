
from tiler_qtree import Tiler_Qtree

class Tiler:


    def __init__( self, config, tensors ):
        self._config = config
        self._tensors = tensors

    
    def tile_test( self ):
        results = []
        results.append( {'A':[0,0,10,10], 'B':[0,0,10,10]} )
        return results


    def tile_simple( self ):
        results = []
        results.append( {'A':[0,0,10,10], 'B':[0,0,10,10]} )
        return results

    
    def tile_qtree( self ):
        # for now, only support elementwise operations
        assert self._config['operation'] in ['elementwise-add', 'elementwise-mul']
        tq = Tiler_Qtree( self._config, self._tensors )
        return tq.tile()


    def tile_dynamic_reflexive( self ):
        results = []
        results.append( {'A':[0,0,10,10], 'B':[0,0,10,10]} )
        return results


    def tile( self ):

        if self._config['tiling_algorithm'] == "test":
            return self.tile_test()
        elif self._config['tiling_algorithm'] == "simple":
            return self.tile_simple()
        elif self._config['tiling_algorithm'] == "qtree":
            return self.tile_qtree()
        elif self._config['tiling_algorithm'] == "dynamic_reflexive":
            return self.tile_dynamic_reflexive()
        else:
            print(f"Unknown tiling algorithm: {self._config['tiling_algorithm']}")
            exit(1)

