# Colmap-geological-pipline
This repository provides a script to process a video into a PLY file, generate contour maps and calculate the coastline length and the 
## Installation

To set up the environment, follow these steps:

1. **Clone the repository**:
   ```sh
   git clone https://github.com/Mechanic-rubbish/Colmap-geological-pipline
2. **Create and activate the conda environment**:  
   ```sh
   conda env create -f environment.yml
   conda activate pccontour
3. **Install additional dependencies**:
   If you need to install additional dependencies, ensure they are added to your 'requirements.txt' or 'environment.yml'
4. **Download COLMAP**:
   Download COLMAP from https://github.com/colmap/colmap/releases/tag/3.9.1 (other versions are also supported)

## Script Usage
1. Turn the video into frames using `<get_frame.py>` the frequency of saving the frames can by setting the label of the frames that are been saved in line 33
2. 3D recounstruction using COLMAP
3. Crop point cloud using `<cut_rigion.py>` set the upper and lower bound(x, y, z) in line 38, 39
4. Denoise and obtain the area of each layer using `<extract_pcd_to_contour_map.py>` the command line is used as below
### Arguments Description
- `--ply_file`: (required) Path to the PLY file.
- `--output_dir`: (required) Directory to the output contour map images.
- `--low`: (optional) Low height for area calculation.
- `--high`: (optional) High height for area calculation.
- `--contour_line_number`: (optional, default=20) Number of contour lines to generate.
- `--real_world_height`: (optional, default=15.0) Real world height corresponding to the height range in the data.

### Example Command

To run the script, please refer to the following command example:

> ./extract_pcd_to_contour_map.py --ply_file <path_to_ply_file> --output_dir <path_to_output_images_file> --contour_line_number 20 --real_world_height 30

Replace `<path_to_ply_file>` and `<path_to_output_images_file>` with the appropriate paths.

5. obtain the premeter/ coastline length using `<cacluate_premetre.py>`
