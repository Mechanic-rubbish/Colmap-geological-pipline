import open3d as o3d

# Read the PLY file
ply_file = "./point_clouds/cropped_point_cloud.ply"
pcd = o3d.io.read_point_cloud(ply_file)
print("Ply file read")

# Visualize the point cloud
o3d.visualization.draw_geometries([pcd], window_name="Point Cloud Visualization", width=800, height=600)
