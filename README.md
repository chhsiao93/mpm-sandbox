# MPM-Sandbox
This project uses [Taichi-MPM](https://github.com/taichi-dev/taichi_elements) engine simulating an inclined plane (actuator) pushing sand in one direction. This MPM result is our real-world observation. We want to use the observation (video) to inverse the material property. To do that, the MPM results are later imported to Blender to generate a video to train a NeRF model, which reconstructs the 3D point cloud and meshes. We will later use the point cloud and meshes as the material points for MPM, meaning we convert the real-world observation to simulation. With differentiability of Taichi-MPM, we will be able to inverse the material properties of the original MPM simulation (real-world observation).

## MPM
In the `engine/mpm_solver.py`, we create a new material type `actuator`, which will be forced to move horizontally at a constant velocity.

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

## Import data to Blender
Before we import the MPM result in Blender, we need to convert the material points to an accetable format. Since we are going to render texture on meshes, we can use `make_ply` to generate `.ply` files by running 

`python make_ply.py --data /path/to/.npz --format mesh -o /output/folder`

By default, it will convert all the frame of data into .ply file. We can specify which frame to convert by using `--frame which_frame`. In addition, we can specify which material to convert by indicate `--mat materail_number`.
## Generate video in Blender
After we import `.ply` file in the Blender, we can render the texture of sand and the actuactor. We will use [BlenderNeRF](https://github.com/maximeraafat/BlenderNeRF) addon to generate the snapshots for training NeRF. It will be stored as a `.zip` file. 

<img width="45%" alt="image" src="https://github.com/chhsiao93/mpm-sandbox/assets/97806906/0d28bb0e-ae0b-49a2-a628-117a2cfdddef">
<img width="45%" alt="image" src="https://github.com/chhsiao93/mpm-sandbox/assets/97806906/eb6c77ed-a7dc-48c7-8c77-4f2336bf1134">

## NeRF - 3D Reconstruction
We use `nerf-sandbox.ipynb` to train a NeRF model. This code is modified from [nerfstudio](https://docs.nerf.studio/). It works fine in the colab environment (GPU A-100). On the colab, you will need to upload the zip file generated from Blender. We recommand upload the zip file to your own drive and mount the drive on the colab. This way is much faster than uploading files directly on colab. Follow the steps in the .ipynb, it will copy and unzip the zip file to colab working space `/content/`. After unzipping the file, change the name of `transform_train.json` to `transform.json`. If everything works fine, you should about to see a terminal inside the colab output. Copy and paste one of command lines above (I would recommand use instant-ngp. It provides much better results). 

<img width="600" alt="image" src="https://github.com/chhsiao93/mpm-sandbox/assets/97806906/a2181e21-a32a-44fb-be84-c3cee87daf8f">

When the training starts, you will see a link that you can connect to nerfstudio UI. In the UI, you can monitor the output while NeRF is still training. By default, it will train the model for 30,000 steps (20~30 mins on A100). When the training finished, use the tool in nerfstudio UI to draw a camera path. I recommand save the camera path to your drive, so you can reuse it in the future. With camera path, you will be able to generate the video like this.



https://github.com/chhsiao93/mpm-sandbox/assets/97806906/8588f6db-ae9c-4b20-b508-b596c2db459c


https://github.com/chhsiao93/mpm-sandbox/assets/97806906/9eba5c4f-4549-49fc-acf9-e61916383192

Additionally, the NeRF model can generate the point cloud and the meshes as `.ply` file (However, the mesh results are weird). You can download and visualize the point cloud by running the code `read_pcd.py`. The code is not modulized yet, you might need to modify the code accordingly.

<img width="45%" alt="image" src="https://github.com/chhsiao93/mpm-sandbox/assets/97806906/180c021e-9e09-48e8-98b0-4a2059c76e98">
<img width="45%" alt="image" src="https://github.com/chhsiao93/mpm-sandbox/assets/97806906/c8bc0623-6bec-4d9d-ba71-0d50c6c40682">

# TODO
## Convert Point Cloud to Material Point for Taichi
## Inverse Material Property from diff-taichi
