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

def f(t):
    if t<0.2:
        return [0,0]
    else:
        return [-1.0, -0.01]

ti.init(arch=ti.cuda, device_memory_GB=4)  # Try to run on GPU

gui = ti.GUI("Taichi Elements", res=512, background_color=0x112F41, show_gui=False)

mpm = MPMSolver(res=(256, 256), act_vel_func=f)
mpm.set_gravity([0, -9.81])

# adding a slope plane
slope_a = 30
slope_l = 0.1
slope_coner = [0.8,0.2]
slope_x = slope_coner[0] + np.linspace(0,slope_l,100)
slope_y = slope_coner[1] + np.linspace(0,slope_l,100)*np.tan(np.radians(slope_a))
slope_pos = np.array([slope_x, slope_y]).T
print(slope_pos.shape)
mpm.add_particles(particles=slope_pos,
                  material=mpm.material_actuator,
                  color=0xFFFF99)
mpm.add_cube(
    lower_corner=[0., 0.],
    cube_size=[1.0,0.3],
    velocity=[0, 0],
    material=mpm.material_sand,
    sample_density=1,
)

positions = []

for frame in range(20):
    mpm.step(8e-3)
    particles = mpm.particle_info()
    print(mpm.t)
    sizes = np.ones(len(particles['color']))*1.0 + (particles['material']==mpm.material_actuator)
    # positions.append(particles['position'])
    gui.circles(particles['position'], radius=sizes, color=particles['color'])
    gui.show(f'{args.out_dir}/{frame:06d}.png' if write_to_disk else None)
# np.save('sandbox_pos.npy', np.array(positions))
np.save('sandbox3d.npz', pos=np.array(positions), mat=np.array(particles['material']))