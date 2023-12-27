import numpy as np
from scipy.stats import norm

# Define the Radial Basis Function kernel
def rbf_kernel(x1, x2, l=1.0, sigma_f=1.0):
    sqdist = np.sum(x1**2, 1).reshape(-1, 1) + np.sum(x2**2, 1) - 2 * np.dot(x1, x2.T)
    return sigma_f**2 * np.exp(-0.5 / l**2 * sqdist)

def omega_opt(X_train, y_train, x_test, target, l=30, sigma_f=0.5):
    # Generating the x and y data arrays with floats
    X_train = X_train.reshape(-1, 1)
    x_test = x_test.reshape(-1, 1)

    # Compute the posterior mean and covariance
    K = rbf_kernel(X_train, X_train, l=l, sigma_f=sigma_f)
    K_s = rbf_kernel(X_train, x_test, l=l, sigma_f=sigma_f)
    K_ss = rbf_kernel(x_test, x_test, l=l, sigma_f=sigma_f) + np.identity(x_test.shape[0]) * 1e-5 # adding uncertainty to covariance matrix of testing data
    K_inv = np.linalg.inv(K)

    # Computation for mu_s and cov_s:
    mu_s = K_s.T.dot(K_inv).dot(y_train)
    cov_s = K_ss - K_s.T.dot(K_inv).dot(K_s)

    ## Find the omega value that maximizes the probability of x_pos = target
    # Compute the standard deviation
    std_dev = np.sqrt(np.diag(cov_s))
    # Create a normal distribution
    normal_dist = norm(loc=mu_s, scale=std_dev)
    # Compute the probability density function at 0.6
    pdf_at_target = normal_dist.pdf(target)
    # Find the index of the maximum value
    index = np.argmax(pdf_at_target) 
    new_omega = x_test[index][0]
    
    return new_omega, mu_s, cov_s

