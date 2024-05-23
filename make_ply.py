import numpy as np
import open3d as o3d
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, help='path to npz file')
    parser.add_argument('--format', default='pcd', type=str, help='pcd or mesh')
    parser.add_argument('--alpha', default=0.3, type=float, help='alpha for mesh generation.')
    parser.add_argument('--mat', type=int, help='Material to visualize. 5 for actuator, 3 for sand.')
    parser.add_argument('--frame', default=None, type=int, help='frame to visualize.')
    parser.add_argument('--prefix', default="", type=str, help='prefix for the output file.')
    parser.add_argument('--show', default=False, type=bool, help='show the visualization.')
    parser.add_argument('-o', '--out-dir', type=str, help='Output folder')
    args = parser.parse_args()
    print(args)
    return args

args = parse_args()
data_path = args.data
alpha = args.alpha
output_dir = args.out_dir
prefix = args.prefix

data = np.load(args.data)
pos = data['pos']
mat = data['mat'][0]
if args.mat is not None:
    pos = pos[:,mat==args.mat,:]
if args.frame is not None:
    frames = [args.frame]
else:
    n_frames = pos.shape[0]
    print(f'Use all the frames. Total frames: {n_frames}')
    frames = range(n_frames)
    

for frame in frames:
    # making point cloud
    pcd = o3d.geometry.PointCloud() 
    pcd.points = o3d.utility.Vector3dVector(pos[frame])
    if args.format == 'pcd':
        # save point cloud
        o3d.io.write_point_cloud(f"{output_dir}/{prefix}{frame:04d}.pcd", pcd)
    else:
        # save mesh
        mesh_sand = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
        mesh_sand.compute_vertex_normals()
        o3d.io.write_triangle_mesh(f"{output_dir}/{prefix}{frame:04d}.ply", mesh_sand)

    if args.show:
        if args.format == 'pcd':
            o3d.visualization.draw_geometries([pcd], point_show_normal=False)
        else:
            o3d.visualization.draw_geometries([mesh_sand], mesh_show_back_face=True)


