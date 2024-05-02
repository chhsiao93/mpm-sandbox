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
    
ti.init(arch=ti.cuda, device_memory_GB=20)  # Try to run on GPU

gui = ti.GUI("Taichi Elements", res=512, background_color=0x112F41, show_gui=False)

mpm = MPMSolver(res=(32, 32, 32), act_vel_func=f)
mpm.set_gravity([0, -9.81, 0])

# adding a slope plane
slope_a = 45
slope_l = 0.1
lower_corner = [0.8,0.29,0.45]
x_ = np.linspace(0.0,slope_l,100)
z_ = np.linspace(0.0,slope_l,100)
x, z = np.meshgrid(x_,z_)
y = x*np.tan(np.radians(slope_a))
slope_pos = np.vstack((x.reshape(-1),y.reshape(-1),z.reshape(-1))).swapaxes(0,1)
slope_pos += lower_corner
print(slope_pos.shape)
mpm.add_particles(particles=slope_pos,
                  material=mpm.material_actuator,
                  color=0xFFFF99)
mpm.add_cube(
    lower_corner=[0., 0., 0.0],
    cube_size=[1.0, 0.3, 1.0],
    velocity=[0, 0, 0],
    material=mpm.material_sand,
)

positions = []
materials = []
for frame in range(200):
    mpm.step(8e-3)
    particles = mpm.particle_info()
    print(mpm.t)
    sizes = np.ones(len(particles['color']))*1.0 + (particles['material']==mpm.material_actuator)
    positions.append(particles['position'])
    materials.append(particles['material'])
    # gui.circles(particles['position'], radius=sizes, color=particles['color'])
    # gui.show(f'{args.out_dir}/{frame:06d}.png' if write_to_disk else None)
positions = np.array(positions)
materials = np.array(materials)
# np.save('sandbox_pos3d.npy', np.array(positions))
np.savez('sandbox3d.npz', positions, materials)