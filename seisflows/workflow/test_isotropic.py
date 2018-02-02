
import sys
import numpy as np

from copy import deepcopy
from seisflows.tools import unix
from seisflows.tools.tools import exists
from seisflows.config import custom_import, ParameterError
from seisflows.workflow.base import base

PAR = sys.modules['seisflows_parameters']
PATH = sys.modules['seisflows_paths']

solver = sys.modules['seisflows_solver']



class test_postprocess(base):
    """ Postprocessing class
    """

    def check(self):
        """ Checks parameters and paths
        """
        if 'MODEL' not in PATH:
            setattr(PATH, 'MODEL', None)


    def main(self):
        """ 
        """
        forward = getattr(forward, materials)
        reverse = getattr(reverse, materials)
        model1 = solver.load(PATH.MODEL)
        model2 = deepcopy(model1)
        model2 = model.apply(forward).apply(reverse)

