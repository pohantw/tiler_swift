#=========================================================================
# tiler_swift
#=========================================================================

import argparse
import os
import sys

from run_handler import RunHandler

#-------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------

def main():

  # default inputs
  default_config_path = "./configs/config_cgra.yaml"
  default_tensor_path = "./benchmarks/80x80_density0.1"
  default_output_path = "./output"

  # Parse command line
  p = argparse.ArgumentParser()
  p.add_argument( "-c", "--config-path", type=str, default=default_config_path )
  p.add_argument( "-t", "--tensor-path", type=str, default=default_tensor_path )
  p.add_argument( "-o", "--output-path", type=str, default=default_output_path )
  p.add_argument( "-v", "--verbose", action='store_true' )

  opts = p.parse_args()

  # Dispatch
  rhandler = RunHandler()
  rhandler.launch(
    config_path = opts.config_path,
    tensor_path = opts.tensor_path,
    output_path = opts.output_path,
    verbose     = opts.verbose
  )

  return

if __name__ == "__main__":
  main()

  