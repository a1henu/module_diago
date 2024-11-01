from module_diago import hsolver
import numpy as np
import scipy

import time

def load_mat(mat_file):
    h_mat = scipy.io.mmread(mat_file)
    nbasis = h_mat.shape[0]
    nband = 8
    
    return h_mat, nbasis, nband

def calc_eig_pyabacus(mat_file, method):
    algo = {
        'dav_subspace': hsolver.dav_subspace,
        'davidson': hsolver.davidson
    }
    
    h_mat, nbasis, nband = load_mat(mat_file)
    
    print('============')
    print(f"nbasis: {nbasis}, nband: {nband}")
    
    v0 = np.random.rand(nbasis, nband)
    diag_elem = h_mat.diagonal()
    diag_elem = np.where(np.abs(diag_elem) < 1e-8, 1e-8, diag_elem)
    precond = 1.0 / np.abs(diag_elem)

    def mm_op(x):
        return h_mat.dot(x)
    
    start_time = time.time()
    e, _ = algo[method](
        mm_op,
        v0,
        nbasis,
        nband,
        precond,
        dav_ndim=8,
        tol=1e-8,
        max_iter=1000
    )
    end_time = time.time()

    # print(f'eigenvalues calculated by pyabacus-{method} is: \n', e)
    print(f'time: {end_time - start_time} s')
    print('============')
    
    return e

def calc_eig_scipy(mat_file):
    h_mat, _, nband = load_mat(mat_file)
    e, _ = scipy.sparse.linalg.eigsh(h_mat, k=nband, which='SA', maxiter=1000)
    e = np.sort(e)
    print('eigenvalues calculated by scipy is: \n', e)
    
    return e

if __name__ == '__main__':
    mat_files = ['./Si2.mtx', './SiH4.mtx', './Si10H16.mtx', './SiO.mtx', './H2O.mtx', './Ga10As10H30.mtx']
    methods = ['dav_subspace']
    
    for m in mat_files:
        print(f'\n====== Calculating eigenvalues... ======')
        print(f'file: {m}')
        e_pyabacus = calc_eig_pyabacus(m, 'dav_subspace')
        e_scipy = calc_eig_scipy(m)
        print('pyabacus - scipy: \n', np.average(e_pyabacus - e_scipy))
        
    
    