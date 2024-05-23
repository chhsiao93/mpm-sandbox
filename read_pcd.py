# import taichi as ti
import numpy as np
import open3d as o3d

pcd = o3d.io.read_point_cloud('cylinder_t0.ply')
print(pcd)
print(np.asarray(pcd.points).max(axis=0))
print(np.asarray(pcd.points).min(axis=0))
pts = np.asarray(pcd.points)
print(pts.shape)

# crop the point cloud
min_bd = np.array([-0.167, -0.167, 0.0])
max_bd = np.array([0.167, 0.167, 0.15])
bbox = o3d.geometry.AxisAlignedBoundingBox(min_bound=min_bd, max_bound=max_bd)
crop_pcd = pcd.crop(bbox, invert=False)
# Define the 8 points of the box
points = [
    [min_bd[0], min_bd[1], min_bd[2]],
    [max_bd[0], min_bd[1], min_bd[2]],
    [min_bd[0], max_bd[1], min_bd[2]],
    [max_bd[0], max_bd[1], min_bd[2]],
    [min_bd[0], min_bd[1], max_bd[2]],
    [max_bd[0], min_bd[1], max_bd[2]],
    [min_bd[0], max_bd[1], max_bd[2]],
    [max_bd[0], max_bd[1], max_bd[2]],
]
# Define the lines for the box
lines = [
    [0, 1],
    [0, 2],
    [1, 3],
    [2, 3],
    [4, 5],
    [4, 6],
    [5, 7],
    [6, 7],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7],
]
colors = [[1, 0, 0] for i in range(len(lines))]
line_set = o3d.geometry.LineSet(
    points=o3d.utility.Vector3dVector(points),
    lines=o3d.utility.Vector2iVector(lines),
)
line_set.colors = o3d.utility.Vector3dVector(colors)
# show pcd and the box
o3d.visualization.draw_geometries([pcd, line_set])
# show cropped pcd and the box
o3d.visualization.draw_geometries([crop_pcd, line_set])