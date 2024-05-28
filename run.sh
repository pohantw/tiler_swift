#!/bin/bash

# benchmark=80x80_density0.1
# benchmark=160x160_density0.1
# benchmark=bcsstm26
# benchmark=ch7-6-b1
# benchmark=mk9-b1
# benchmark=n4c6-b1
# benchmark=rel5
benchmark=relat5

# Run main tiler tool
python tiler_swift/main.py \
    -c ./configs/config_cgra.yaml \
    -t ./benchmarks/${benchmark} \
    -o ./output

# Visualize the results
python tiler_swift/visualize.py \
    -r ./output/results.yaml \
    -t ./benchmarks/${benchmark} \
    -o ./output_${benchmark}.png
