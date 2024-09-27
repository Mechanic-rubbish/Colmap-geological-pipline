import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import cv2
import os
import argparse



def read_and_denoise_ply(ply_file="mountain\output cloud\points3D.ply", nb_neighbors=20, std_ratio=2.0):
    """
    Reads a PLY file and applies statistical outlier removal to denoise the point cloud.

    Parameters:
    -----------
    ply_file : str
        Path to the PLY file.
    nb_neighbors : int, optional
        Number of neighbors to consider for the statistical analysis (default is 20).
    std_ratio : float, optional
        Standard deviation ratio for the statistical outlier removal (default is 2.0).

    Returns:
    --------
    numpy.ndarray
        Numpy array of denoised point cloud coordinates.
    """
    pcd = o3d.io.read_point_cloud(ply_file)
    print("Ply file read")
    pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)
    print(f"Noise canceled with nb_neighbors = {nb_neighbors}, std_ratio = {std_ratio}")
    return np.asarray(pcd.points)

def calculate_contour_areas(Y, Y_levels, grid_cell_area, output_dir):
    """
    Calculates the area of each contour level in the provided height map and saves mask images.

    Parameters:
    -----------
    Y : numpy.ndarray
        2D array of heights interpolated over the grid.
    Y_levels : numpy.ndarray
        Contour levels used for area calculation.
    grid_cell_area : float
        Area of a single grid cell in real-world units.
    output_dir : str
        Directory to save the mask images.

    Returns:
    --------
    list
        List of areas for each contour level.
    """
    areas = []

    for idx, level in enumerate(Y_levels):
        mask = (Y >= level).astype(np.uint8)
        area = np.sum(mask) * grid_cell_area
        areas.append(area)

        mask_img_path = os.path.join(output_dir, f"mask_level_{idx}_with_area_{area}.png")
        cv2.imwrite(mask_img_path, mask * 255)
        print(f"Saved mask image for level {level} at {mask_img_path}")

    return areas



def process_point_cloud(points, low=None, high=None, real_world_height=15.0,contour_line_number=10, output_dir='./output_contour'):
    """
    Processes a point cloud to generate a contour map and optionally calculates contour areas.

    Parameters:
    -----------
    points : numpy.ndarray
        Array of point cloud coordinates.
    low : float, optional
        Lower height limit for area calculation (default is None).
    high : float, optional
        Upper height limit for area calculation (default is None).
    real_world_height : float, optional
        Real-world height corresponding to the height range in the data (default is 15.0).
    contour_line_number : int, optional
        Number of contour lines (default is 10).
    output_dir : str, optional
        Directory to save output files (default is './output_contour').

    Returns:
    --------
    list or int
        List of calculated areas for the specified height range or 0 if no areas are calculated.
    """
    y_min, y_max = np.min(points[:, 1]), np.max(points[:, 1])
    
    
    scaling_factor = real_world_height / (y_max - y_min)
    print(scaling_factor)
    
    y_scaled = points[:, 1] * scaling_factor
    print(y_scaled)
    
    points[:, 1] = y_scaled
    if low is not None and high is not None:
        height_range = (low, high)
    elif low is not None:
        if low <= y_min * scaling_factor:
            exit(1)
        # height_range = (np.min(y_scaled), low)
        height_range = (low, np.max(y_scaled))
    elif high is not None:
        if high >= y_max * scaling_factor:
            exit(1)
        # height_range = (high, np.max(y_scaled))
        height_range = (np.min(y_scaled), high)
    else:
        height_range = (np.min(y_scaled), np.max(y_scaled))
    
    y_min, y_max = height_range
    points = points[(points[:, 1] >= y_min) & (points[:, 1] <= y_max)]
    
    if points.shape[0] < 100:
        return "Not enough to process."
    
    # y_scaled = points[:, 1]
    # x_scaled = points[:, 0] * scaling_factor
    # z_scaled = points[:, 2] * scaling_factor
    
    points[:, 0] = points[:, 0] * scaling_factor
    # points[:, 1] = y_scaled
    points[:, 2] = points[:, 2] * scaling_factor
    
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    
    x_min, x_max = np.min(x), np.max(x)
    z_min, z_max = np.min(z), np.max(z)
    
    x_range = x_max - x_min
    z_range = z_max - z_min

    x_grid_cell_size = x_range / 100
    z_grid_cell_size = z_range / 100

    # Area of one grid cell in real-world units
    grid_cell_area = x_grid_cell_size * z_grid_cell_size
    
    xi = np.linspace(x_min, x_max, 100)
    zi = np.linspace(z_min, z_max, 100)
    X, Z = np.meshgrid(xi, zi)
    
    Y = griddata((points[:, 0], points[:, 2]), points[:, 1], (X, Z), method='linear')
    
    Y_min, Y_max = np.nanmin(Y), np.nanmax(Y)
    Y_levels = np.linspace(Y_min, Y_max, contour_line_number)
    Y = np.clip(Y, Y_min, Y_max)
    
    
    
    _, ax = plt.subplots()
    CS = ax.contour(X, Z, Y, levels=Y_levels, linewidths=0.5, colors='k')
    CSF = ax.contourf(X, Z, Y, levels=Y_levels, cmap='viridis')
    
    ax.clabel(CS, inline=True, fontsize=10)
    
    ax.set_title("Contour plot from point cloud data")
    ax.set_xlabel('X')
    ax.set_ylabel('Z')
    
    y_ticks = np.linspace(Y_min, Y_max, len(ax.get_yticks()))
    ax.yaxis.set_ticks(y_ticks)
    ax.set_yticklabels([f'{ytick:.2f}' for ytick in y_ticks])
    
    plt.colorbar(CSF)
    
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(f'{output_dir}/contour_map_lines_{contour_line_number}.png')
    plt.close()
    print("plt close, image saved")
    
    if low is not None or high is not None:
        areas = calculate_contour_areas(Y, Y_levels, grid_cell_area, output_dir)
        print(f"Calculated areas: {areas}")
        return areas
    else:
        print("No areas calculated")
        return 0

def main():
    parser = argparse.ArgumentParser(description="Process point cloud to calculate contour areas.")
    parser.add_argument('--ply_file', type=str, help="Path to the PLY file")
    parser.add_argument('--output_dir', type=str, help="Directory to save output files.")
    parser.add_argument('--low', type=float, help="Low height for area calculation.")
    parser.add_argument('--high', type=float, help="High heigh for area calculation.")
    parser.add_argument('--contour_line_number', type=int, default=20, help="Number of contour lines.")
    parser.add_argument('--real_world_height', type=float, default=15.0, help="Real world height corresponding to the height range in the data")
    args = parser.parse_args()
    
    points = read_and_denoise_ply(args.ply_file)
    
    print(args)
    
    areas = process_point_cloud(points, low=args.low, high=args.high, contour_line_number=args.contour_line_number, real_world_height=args.real_world_height, output_dir=args.output_dir)
    print(f"Calculated areas for the specified height range: {areas}")
    
if __name__  == "__main__":
    main()