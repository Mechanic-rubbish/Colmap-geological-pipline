import open3d as o3d
import numpy as np

def load_point_cloud(file_path):
    pcd = o3d.io.read_point_cloud(file_path)
    return pcd

def crop_point_cloud(pcd, min_bound, max_bound):
    points = np.asarray(pcd.points)
    # 使用条件筛选来保留在边界框内的点
    mask = np.all((points >= min_bound) & (points <= max_bound), axis=1)
    cropped_points = points[mask]
    
    # 创建新的点云对象
    cropped_pcd = o3d.geometry.PointCloud()
    cropped_pcd.points = o3d.utility.Vector3dVector(cropped_points)
    
    return cropped_pcd

def save_point_cloud(pcd, file_path):
    o3d.io.write_point_cloud(file_path, pcd)

def rotate_point_cloud(pcd, rotation_matrix):
    pcd.rotate(rotation_matrix, center=(0, 0, 0))
    return pcd

def reverse_y_values(pcd,y_offset):
    points = np.asarray(pcd.points)
    points[:, 1] = -points[:, 1]
    points[:, 1] += y_offset
    pcd.points = o3d.utility.Vector3dVector(points)
    return pcd

if __name__ == "__main__":
    file_path = "mountain\\sparse\\0\\points3D.ply"
    output_file_path = "mountain\\output cloud\\cropped_point_cloud.ply" 
    y_offset= 1.73
    min_bound = np.array([-3, 0, -4])  
    max_bound = np.array([4, 3, 4]) 
    theta1 = np.radians(-19) 
    rotation_matrix1 = np.array([
        [1, 0, 0],
        [0, np.cos(theta1), -np.sin(theta1)],
        [0, np.sin(theta1), np.cos(theta1)]
    ])
    theta2= np. radians(4)
    rotation_matrix2 = np.array([
    [np.cos(theta2), -np.sin(theta2), 0],
    [np.sin(theta2),  np.cos(theta2), 0],
    [0,              0,             1]
    ])
    pcd = load_point_cloud(file_path)
    cropped_pcd= crop_point_cloud(pcd,min_bound, max_bound)
    rotated_pcd1 = rotate_point_cloud(cropped_pcd, rotation_matrix1) 
    rotated_pcd2 = rotate_point_cloud(rotated_pcd1, rotation_matrix2) 
    reversed_pcd =reverse_y_values(rotated_pcd2,y_offset)
    o3d.visualization.draw_geometries ([reversed_pcd])
    save_point_cloud(reversed_pcd, output_file_path)
    print("saved")
