SeisFlows-HPC (WARNING: NOT YET WORKING)
========================================

Extension to the main SeisFlows package

- provides a general framework for multiparameter inversions

- allows nonlinear mappings between "physical parameters" and "inversion parameters"

- allows use of empirical density relations such as Gardner's Law

- provides ready-to-go anisotropic inversion capabilities for SPECFEM2D and SPECFEM3D


Once the main SeisFlows package and its depedenciese are installed, installation of the extension package is very simple:
```
git clone https://github.com/rmodrak/seisflows-multiparameter.git /path/to/seisflows-multiparameter
export PYTHONPATH=$PYTHONPATH:/path/to/seisflows-multiparameter
```
