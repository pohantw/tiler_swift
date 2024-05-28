import argparse
import numpy as np
import yaml
from scipy.sparse import csr_matrix
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor

class Visualizer:
    def __init__(self, tensor, tiling, output_img_file):
        self._tensor = tensor
        self._tiling = tiling
        self._output_img_file = output_img_file
        self._border_width = 1
        self._dot_width = 3
    

    def set_border_width(self, border_width):
        self._border_width = border_width
    

    def set_dot_width(self, dot_width):
        self._dot_width = dot_width
    
    
    def visualize(self):
        # Create a sparse matrix for demonstration purposes
        nrows, ncols = self._tensor.shape

        # Create a new image with white background
        img_rows = (nrows * self._dot_width) + ((nrows + 1) * self._border_width)
        img_cols = (ncols * self._dot_width) + ((ncols + 1) * self._border_width)
        img = Image.new('RGB', (img_cols, img_rows), 'white')

        # Create a 3x3 black block
        block_size = self._dot_width
        black_block = Image.new('RGB', (block_size, block_size), 'black')

        # Function to paste a 3x3 block
        def paste_block(y, x):
            im_x = self._border_width + (self._dot_width + self._border_width) * x
            im_y = self._border_width + (self._dot_width + self._border_width) * y
            img.paste(black_block, (im_x, im_y))

        # get the non-zero coordinates using numpy nonzero function in the form of (col, row)
        non_zero_positions = np.transpose(self._tensor.nonzero())

        # Paste the 3x3 blocks for non-zero elements in parallel
        with ThreadPoolExecutor() as executor:
            executor.map(lambda pos: paste_block(*pos), non_zero_positions)
        
        # Draw the borders based on the tiling result
        draw = ImageDraw.Draw(img)
        for tiling in self._tiling:
            x, y, w, h = tiling['A']
            x1 = self._border_width + (self._dot_width + self._border_width) * x - 1
            y1 = self._border_width + (self._dot_width + self._border_width) * y - 1
            x2 = self._border_width + (self._dot_width + self._border_width) * (x + w) - 1
            y2 = self._border_width + (self._dot_width + self._border_width) * (y + h) - 1
            draw.rectangle([x1, y1, x2, y2], outline='red', width=self._border_width)
        
        # Resize the image to 500 pixels wide, maintaining the aspect ratio
        # new_width = 500
        # aspect_ratio = img.height / img.width
        # new_height = int(new_width * aspect_ratio)
        # img_resized = img.resize((new_width, new_height), Image.LANCZOS)

        # Save the resized image
        img.save(self._output_img_file)

if __name__ == "__main__":
  
    # Parse command line
    p = argparse.ArgumentParser()
    p.add_argument( "-r", "--result-path", type=str, default="./output/results.yaml" )
    p.add_argument( "-t", "--tensor-path", type=str, default="./benchmarks/n4c6-b1" )
    p.add_argument( "-n", "--tensor-name", type=str, default="A" )
    p.add_argument( "-o", "--output-path", type=str, default="./output.png" )
    opts = p.parse_args()

    # load the tensor
    tensor_file = f"{opts.tensor_path}/{opts.tensor_name}.npy"
    tensor = np.load(tensor_file)

    # load the tiling result yaml file
    with open(opts.result_path, 'r') as f:
      tiling = yaml.safe_load(f)

    # Create a visualizer
    visualizer = Visualizer(tensor, tiling, opts.output_path)

    # Set the border width and dot width
    visualizer.set_border_width(1)
    visualizer.set_dot_width(3)

    # Visualize the sparse matrix
    visualizer.visualize()
