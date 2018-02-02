

from seisflows.config import custom_import

class isotropic2d(custom_import('solver', 'isotropic'), custom_import('solver', 'specfem2d')):
    """ Adds isotropic inversion machinery to SPECFEM2D
    """
    pass

