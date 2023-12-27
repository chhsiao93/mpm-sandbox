import taichi as ti
import numpy as np
from engine.mpm_solver import MPMSolver
from gp_opt import omega_opt
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--out-dir', type=str, help='Output folder')
    parser.add_argument('--iter', type=int, default=5, help='Number of iterations')
    parser.add_argument('--guess', type=float, default=20, help='Initial guess')
    parser.add_argument('--target', type=float, default=0.6, help='Target')
    args = parser.parse_args()
    print(args)
    return args

args = parse_args()

write_to_disk = args.out_dir is not None
if write_to_disk:
    try:
        os.mkdir(f'{args.out_dir}')
    except:
        pass
X_train = np.array([args.guess]) # omegas
x_test = np.linspace(0,200, 401)
y_train = np.array([]) # x_pos
# start iteration
for i in range(args.iter):
    ti.init(arch=ti.cuda)  # Try to run on GPU

    gui = ti.GUI("Taichi Elements", res=512, background_color=0x112F41, show_gui=False)

    mpm = MPMSolver(res=(256, 256))
    mpm.set_gravity([0, -9.81])
    mpm.omega[None] = -1 * X_train[-1]
    print(f'iter: {i+1}, omega:{mpm.omega[None]:.2f}, x_pos: {mpm.fan_center.to_numpy()[0]:.2f}')
    mpm.add_spikes(
                sides=8,
                center=[0.2,0.25],
                velocity=[0,0],
                radius=0.1,
                width = 0.02,
                color=0xFFAAAA,
                sample_density=4,
                material=MPMSolver.material_elastic)
    mpm.add_cube(
        lower_corner=[0.,0],
        cube_size=[1,0.1],
        velocity=[0, 0],
        sample_density=2,
        material=mpm.material_sand
    )
    # run simulation for 500 frames
    for frame in range(500):
        mpm.step(8e-3)
    # get x_pos
    y_train = np.append(y_train, mpm.fan_center.to_numpy()[0])
    new_omega, _, _ = omega_opt(X_train, y_train, x_test, target=args.target, l=30, sigma_f=0.5)
    X_train = np.append(X_train, new_omega)

# Save X_train and y_train to .npy files
np.save(f'{args.out_dir}/omegas.npy', X_train)
np.save(f'{args.out_dir}/x_pos.npy', y_train)