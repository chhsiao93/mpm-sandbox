# diffmpm-wheel-optimize
This repo is to simulate wheel(with spikes) rolling on sand material. With differential programming, we want to optimize wheel's configuration.

## Wheel simulation in Taichi MPM
The simulation is built with taichi MPMsolver from [taichi_elements](https://github.com/taichi-dev/taichi_elements).
The project starts with a simple scenario by dropping a wheel with an initial angular velocity $\omega_0$.

To run the mpm simulation you can simply run `python run_mpm.py` with an argument `-o "path/to/output/folder"`. It will output `.png` files for each `dt`. It will run 500 frames for simulation, and store a `.png` file for each frame in output directory. 

To make a .gif of these files, you can run `python make_gif.py -i "path/to/png/folder" -o "path/to/output.gif"`. You can use `--fps` to control the frame rate.

Here are some examples of simulation running with two different initial angular velocity. We can observe that the higher inital angular velocity makes the wheel roll further. One of our tasks is to optimize $\omega_0$, so center of the wheel $x_{pos}$ will stop at target position (currently, we set the target at 0.6)

![output_w_10](https://github.com/chhsiao93/diffmpm-wheel-optimize/assets/97806906/f5a35594-87c2-4ec1-8ca1-0bcd9412c2e7)

Figure 1. $\omega_0=10 (rad/s)$

![output_w_80](https://github.com/chhsiao93/diffmpm-wheel-optimize/assets/97806906/66b0d5cb-c786-4804-a639-427bbbf809eb)

Figure 2. $\omega_0=80 (rad/s)$

## Gaussian Process Optimization
Before using differential programming feature in Taichi, we implement another optimization approach, Gaussian Process (GP), to update $\omega_0$. GP is a probabilistic approach to model unknow function. It is particularly useful in scenarios where evaluating the objective function is time-consuming, expensive, or impractical. (Although it is not our case - one simulation takes about 6 mins with `gpu-a100` node in Lonestar6). The optimization can be summarized by the following steps:
1. Run the first mpm simulation with an initial guess of $\omega_0$ (In this case, $\omega_0$ is 20), and get the final position $x_{pos}$ of the wheel.
2. Use simulated data ($\omega_0$, $x_{pos}$) as test data to update the predicted function in GP.
3. Use predicted function to find the new $\omega_0$ that has highest probability at $x_{pos}=0.6$.
4. Use new $\omega_0$ to run mpm simulation and get results
5. Repeat step 2-4 until $x_{pos}$ close to 0.6

To run GP, simply `python run_mpm_opt -o "path/to/output/folder" --iter num_iter --guess initial_guess --target target_x_pos`

The following figure is an example of Gaussian Process updating omega. The black curve is the predicted function from GP. The blue filled area shows the interval of 95% confidence. The red dots represent the simulation data ($\omega_0$, $x_{pos}$). The blue dot denotes the $\omega_0$ would most likely reach 0.6. For example, we start with $\omega_0=20$. The center of the wheel in the first simulation ends up at 0.25. GP shows that when $\omega_0=0.43$ would have highest probability to have $x_{pos}=0.6$. Therefore, the next simulation uses 43 as $\omega_0$ and it returns 0.28 as x position. The new datapoint is then used to update the predicted function and predict the next $\omega_0$, and so on. After 6 iteraions, the optimized $\omega_0$ is 98.5 and it returns 0.607 as x position. 
![gp_opt](https://github.com/chhsiao93/diffmpm-wheel-optimize/assets/97806906/b7c0f5b6-34e1-4c53-a634-46ad5133282f)

Figure 3. Updating predicted function in Gaussian process
