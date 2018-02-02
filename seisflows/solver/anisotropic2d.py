
import sys

from os.path import join

import seisflows.plugins.isotropic.forward as forward
import seisflows.plugins.isotropic.reverse as reverse

from seisflows.tools.seismic import Container

from seisflows.tools import unix
from seisflows.tools.tools import exists, Struct
from seisflows.config import ParameterError, custom_import

PAR = sys.modules['seisflows_parameters']
PATH = sys.modules['seisflows_paths']


VOIGT2D = ['c11','c13','c15','c33','c35','c55']


class anisotropic2d(custom_import('solver', 'specfem2d')):
    """ Adds 2D full anisotropy machinery

       Must supply a model in c11,c13,c15,c33,c35,c55
    """

    def check(self):
        super(isotropic, self).check()

        if not hasattr(forward, PAR.MATERIALS):
          raise Exception

        if not hasattr(reverse, PAR.MATERIALS):
          raise Exception

        assert PAR.MATERIALS in [
            'ChenTromp2d',
            'Thomsen2d',
            'Voigt2d'
            ]


    def __init__(self):
        # constant density
        if PAR.MATERIALS == 'ChenTromp2d':
            self.parameters = []
            self.parameters += ['A']
            self.parameters += ['C']
            self.parameters += ['N']
            self.parameters += ['L']
            self.parameters += ['F']

        if PAR.MATERIALS == 'Thomsen2d':
            self.parameters = []
            self.parameters += ['vp']
            self.parameters += ['vs']
            self.parameters += ['epsilon']
            self.parameters += ['delta']
            self.parameters += ['gamma']
            self.parameters += ['theta']

        if PAR.MATERIALS == 'Voigt2d':
            self.parameters = []
            self.parameters += ['c11']
            self.parameters += ['c13']
            self.parameters += ['c15']
            self.parameters += ['c33']
            self.parameters += ['c35']
            self.parameters += ['c55']


    def load(self, path, parameters=VOIGT2D,
             prefix='', suffix=''):
        """ Reads fully anisotropic 2D model
        """
        dict = Container()

        nproc = self.mesh_properties.nproc
        for iproc in range(nproc):
            for key in parameters:
                key = prefix+key+suffix
                dict[key] = self.io.read_slice(path, key, iproc)

        if parameters==VOIGT2D:
            dict.map(self.forward, nproc)

        return dict


    def save(self, dict, path, parameters=VOIGT2D,
             prefix='', suffix=''):
        """ Writes fully anisotropic 2D model
        """
        nproc = self.mesh_properties.nproc
        if ['rho'] not in parameters:
            for iproc in range(nproc):
                dict['rho'] = self.io.read_slice(PATH.MODEL_INIT, 'rho', iproc)

        if parameters!=VOIGT2D:
            dict.map(self.reverse, nproc)

        nproc = self.mesh_properties.nproc
        for key, val in dict.items():
            key = prefix+key+suffix
            self.io.write_slice(val, path, key, iproc)


    @staticmethod
    def forward(*args):
       return getattr(forward, PAR.MATERIALS)(*args)

    @staticmethod
    def reverse(*args):
       return getattr(reverse, PAR.MATERIALS)(*args)

    def check_mesh_properties(
            self, path=None, parameters=VOIGT2D):
        super(isotropic, self).check_mesh_properties(
            path, parameters)


