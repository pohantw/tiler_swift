from model_opal import Model_Opal

from tiler_qtree import Tiler_Qtree
from tiler_btree import Tiler_Btree
from tiler_simple import Tiler_Simple

class Tiler:


    def __init__( self, config, tensors ):
        self._config = config
        self._tensors = tensors

    
    def tile_test( self ):
        results = []
        results.append( {'A':[0,0,10,10], 'B':[0,0,10,10]} )
        return results


    def tile_simple( self ):
        # for now, only support elementwise operations
        assert self._config['operation'] in ['elementwise-add', 'elementwise-mul']
        ts = Tiler_Simple( self._config, self._tensors, max_nnzs=15 )
        return ts.tile()

    
    def tile_qtree( self ):
        # for now, only support elementwise operations
        assert self._config['operation'] in ['elementwise-add', 'elementwise-mul']
        tq = Tiler_Qtree( self._config, self._tensors )
        return tq.tile()


    def tile_btree( self, model ):
        # for now, only support elementwise operations
        assert self._config['operation'] in ['elementwise-add', 'elementwise-mul']
        tb = Tiler_Btree( self._config, self._tensors, model )
        return tb.tile()


    def tile_dynamic_reflexive( self ):
        results = []
        results.append( {'A':[0,0,10,10], 'B':[0,0,10,10]} )
        return results


    def tile( self ):

        if self._config['performance_model'] == "opal":
            model = Model_Opal( self._config, self._tensors )
        else:
            print(f"Unknown performance model: {self._config['performance_model']}")
            exit(1)

        if self._config['tiling_algorithm'] == "test":
            return self.tile_test()
        elif self._config['tiling_algorithm'] == "simple":
            return self.tile_simple()
        elif self._config['tiling_algorithm'] == "qtree":
            return self.tile_qtree()
        elif self._config['tiling_algorithm'] == "btree":
            return self.tile_btree(model)
        elif self._config['tiling_algorithm'] == "dynamic_reflexive":
            return self.tile_dynamic_reflexive()
        else:
            print(f"Unknown tiling algorithm: {self._config['tiling_algorithm']}")
            exit(1)

