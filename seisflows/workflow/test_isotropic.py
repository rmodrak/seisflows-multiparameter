
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



class test_isotropic(base):
    """ Postprocessing class
    """

    def check(self):
        """ Checks parameters and paths
        """
        if not hasattr(PAR, 'MATERIALS'):
            raise Exception

        # dummy parameters
        if 'MODEL_INIT' not in PATH:
            setattr(PATH, 'MODEL_INIT', PATH.MODEL_INPUT)

        for key in ['NT','DT','F0']:
            if not hasattr(PAR, 'NT'): PAR[key]=0

        if not hasattr(PAR, 'FORMAT'):
            PAR.FORMAT=None


    def main(self):
        """ 
        """
        try:
            model = solver.load(PATH.MODEL_INPUT)
        except:
            raise Exception("Error reading isotropic model.")

        try:
            solver.save(model, PATH.MODEL_OUTPUT)
        except:
            raise Exception("Error writing isotropic model.")


        # check if input/output models are the same
        #raise NotImplemenetedError



