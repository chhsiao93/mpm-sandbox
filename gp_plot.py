import numpy as np
import matplotlib.pyplot as plt
from gp_opt import omega_opt

#X_train = np.array([20., 43., 72.,90., 105.5, 99.5]) # example omega
#y_train = np.array([0.24708621, 0.27738553, 0.37571594, 0.45560429, 0.71624547, 0.59043849]) # example x_pos
X_train = np.load('omegas.npy') # omega
y_train = np.load('x_pos.npy') # x_pos
x_test = np.linspace(0,200, 401).reshape(-1, 1)

def plot_gp(new_omega, mu_s, cov_s, X_train, y_train, x_test):
    # Plot the data, the mean, and 95% confidence interval of the posterior
    plt.figure(figsize=(8, 6))
    plt.scatter(X_train, y_train, c='red', s=50*0.8**(len(X_train)-np.arange(len(X_train))), zorder=10, edgecolors=(0, 0, 0), label='Simulated Results')
    for i, (x, y) in enumerate(zip(X_train, y_train)):
        plt.text(x, y+0.02, f'({x:.1f}, {y:.2f})', ha='right')  # adjust text position as needed
        plt.axvline(x=X_train[i], color='k', linestyle='--', linewidth=0.5**(len(X_train)-i-1))
    plt.plot(x_test, mu_s, 'k', lw=1, zorder=9)
    plt.fill_between(x_test.flatten(), mu_s - 1.96*np.sqrt(np.diag(cov_s)), mu_s + 1.96*np.sqrt(np.diag(cov_s)), alpha=0.2)
    plt.axhline(y=0.6, color='k', linestyle='-') # target

    plt.axvline(x=new_omega, color='k', linestyle='--', linewidth=0.5**(0))
    plt.scatter(new_omega, 0.6, c='blue', s=50, zorder=10, label=f'Opt $\omega$ = {new_omega:.2f}')
    plt.xlim(0,150)
    plt.ylim(0,1)
    plt.xlabel('$\omega_0 (rad/s)$', fontsize=13)
    plt.ylabel('$x_{pos}$', fontsize=13)
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(f'./opt_pic/{len(X_train)}.png') # adjust file name as needed
    #plt.show()

for N in range(6):
    new_omega, mu_s, cov_s = omega_opt(X_train[:N+1], y_train[:N+1], x_test, target=0.6, l=30, sigma_f=0.5)
    plot_gp(new_omega, mu_s, cov_s, X_train[:N+1], y_train[:N+1], x_test)

