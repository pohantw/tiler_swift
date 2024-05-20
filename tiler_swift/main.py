#=========================================================================
# tiler_swift
#=========================================================================

import argparse
import os
import sys
import yaml

#-------------------------------------------------------------------------
# Command line processing
#-------------------------------------------------------------------------

def parse_cmdline():
  p = argparse.ArgumentParser()
  p.add_argument( "-c", "--config-path", type=str )
  p.add_argument( "-t", "--tensor-path", type=str )
  p.add_argument( "-o", "--output-path", type=str )

  opts = p.parse_args()
  #if opts.help and not opts.args: p.error() # print help only if not stash
  return opts

#-------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------
class RunHandler:

  def __init__( s ):
    pass

  #-----------------------------------------------------------------------
  # helpers
  #-----------------------------------------------------------------------



  #-----------------------------------------------------------------------
  # launch
  #-----------------------------------------------------------------------
  # Dispatch function for commands
  #

  def launch( s, config_path, tensor_path, output_path ):

    print("config_path: ", config_path)
    print("tensor_path: ", tensor_path)
    print("output_path: ", output_path)

    with open(config_path, 'r') as f:
      config = yaml.safe_load(f)
    
    print(config)

    return


#-------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------

def main():

  opts = parse_cmdline()

  # # Version

  # if opts.version:
  #   print( __version__ )
  #   return

  # Dispatch

  rhandler = RunHandler()

  rhandler.launch(
    config_path = opts.config_path,
    tensor_path = opts.tensor_path,
    output_path = opts.output_path
  )

  return

if __name__ == "__main__":
  main()

  