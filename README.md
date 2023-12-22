# diffmpm-wheel-optimize
This repo is to simulate wheel(with spikes) rolling on sand material. The simulation is built with taichi MPMsolver from [taichi_elements](https://github.com/taichi-dev/taichi_elements). With differential programming, we want to optimize wheel's configuration.

The project starts with a simple scenario by dropping a wheel with an initial angular velocity.
To run the mpm simulation you can simply run `python run_mpm.py` with an argument `-o "path/to/output/folder"`. It will output `.png` files for each `dt`. 

To make a .gif of these files, you can run `python make_gif.py -i "path/to/png/folder" -o "path/to/output.gif"`. 

Here are some examples of simulation running with two different initial angular velocity. We can observe that the higher inital angular velocity makes the wheel roll further.
### $\omega_0=10 (rad/s)$
![output_w_10](https://github.com/chhsiao93/diffmpm-wheel-optimize/assets/97806906/f5a35594-87c2-4ec1-8ca1-0bcd9412c2e7)
### $\omega_0=80 (rad/s)$
![output_w_80](https://github.com/chhsiao93/diffmpm-wheel-optimize/assets/97806906/66b0d5cb-c786-4804-a639-427bbbf809eb)
