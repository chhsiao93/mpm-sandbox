# MPM-Sandbox
This project uses [Taichi-MPM](https://github.com/taichi-dev/taichi_elements) engine simulating an inclined plane (actuator) pushing sand in one direction. In the `engine/mpm_solver.py`, we create a new material type `actuator`, which will be forced to move horizontally at a constant velocity.

By running `python sandbox3d.py`, it will generate a npz file `sandbox.npz` which stores trajectories of material points and the material information. The npz file is a dictionary structure. 
- 'pos': material point trajectories `[n_frame, n_pts, xyz]`
- 'mat': material number of each material points `[n_frame, n_pts]`

The corresponding material of material number is listed here or can be found in `engine/mpm_solver.py`
- material_water = 0
- material_elastic = 1
- material_snow = 2
- material_sand = 3
- material_stationary = 4
- material_actuator = 5

## Generate video in Blender
Before we import the MPM result in Blender, we need to convert the material points to an accetable format. Since we are going to render texture on meshes, we can use `make_ply` to generate `.ply` files by running 

`python make_ply.py --data /path/to/.npz --format mesh -o /output/folder`

By default, it will convert all the frame of data into .ply file. We can specify which frame to convert by using `--frame which_frame`. In addition, we can specify which material to convert by indicate `--mat materail_number`.

