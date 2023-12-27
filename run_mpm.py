import taichi as ti
import numpy as np
import math
from engine.mpm_solver import MPMSolver
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--out-dir', type=str, help='Output folder')
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

ti.init(arch=ti.cuda)  # Try to run on GPU

gui = ti.GUI("Taichi Elements", res=512, background_color=0x112F41)

mpm = MPMSolver(res=(256, 256))
mpm.set_gravity([0, -9.81])

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

for frame in range(500):
    mpm.step(8e-3)
    particles = mpm.particle_info()
    print(mpm.fan_center, mpm.t, mpm.omega)
    gui.circles(particles['position'], radius=1.5, color=particles['color'])
    gui.show(f'{args.out_dir}/{frame:06d}.png' if write_to_disk else None)