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

    
    def tile_greedy( self ):
        results = []
        results.append( {'A':[0,0,10,10], 'B':[0,0,10,10]} )
        return results


    def tile_dynamic_reflexive( self ):
        results = []
        results.append( {'A':[0,0,10,10], 'B':[0,0,10,10]} )
        return results


    def tile( self ):

        # FIXME: testing
        self._config['tiling_algorithm'] = "test"

        if self._config['tiling_algorithm'] == "test":
            return self.tile_test()
        elif self._config['tiling_algorithm'] == "simple":
            return self.tile_simple()
        elif self._config['tiling_algorithm'] == "greedy":
            return self.tile_greedy()
        elif self._config['tiling_algorithm'] == "dynamic_reflexive":
            return self.tile_dynamic_reflexive()
        else:
            print(f"Unknown tiling algorithm: {self._config['tiling_algorithm']}")
            exit(1)

