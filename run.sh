#!/bin/bash

configs=(
    # cgra_elemadd_simple
    # cgra_elemadd_qtree
    # cgra_elemadd_btree
    # cgra_elemmul_simple
    cgra_elemmul_qtree
    cgra_elemmul_btree
)

benchmarks=(
    160x160_density0.1
    # 160x160_density0.2
    # bcsstm26
    # ch7-6-b1
    # mk9-b1
    # n4c6-b1
    # relat5
    # rel5
)

proj_root=$(pwd)
output_root=outputs

# loop through each benchmark
for config in "${configs[@]}"
do
    for benchmark in "${benchmarks[@]}"
    do
        # Setup
        echo "[run.sh] ===== Benchmark: ${benchmark}, config: ${config} ====="
        output_dir=cfg_${config}_bmark_${benchmark}
        output_path=${output_root}/${output_dir}

        # Create output directory
        rm -rf ${output_path}
        mkdir -p ${output_path}

        # Run main tiler tool
        python tiler_swift/main.py \
            -c ./configs/config_${config}.yaml \
            -t ./benchmarks/${benchmark} \
            -o ${output_path} \
            | tee ${output_path}/log_main.log

        # Visualize the results
        python tiler_swift/visualize.py \
            -r ${output_path}/results.yaml \
            -t ./benchmarks/${benchmark} \
            -o ${output_path}/tiling_visualization.png \
            | tee ${output_path}/log_visualize.log
        
        # get the operation type from the config file name
        IFS="_" read -ra split_config <<< "${config}"

        # Run Comal
        cd tests/comal
        cargo run \
            --bin tiler_swift_mat_${split_config[1]} \
            ${proj_root}/${output_path}/tiles/tile_pair_paths.toml \
            | tee ${proj_root}/${output_path}/log_comal.log
        cd ${proj_root}
    done
done
