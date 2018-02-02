
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


raise NotImplementedError
TTI3D = []


class anisotropic2d(custom_import('solver', 'specfem2d')):
    """ Adds 3D TTI machinery
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
        if PAR.MATERIALS == 'ChenTromp_3d_tti':
            self.parameters = []
            self.parameters = []
            self.parameters += ['A']
            self.parameters += ['C']
            self.parameters += ['L']
            self.parameters += ['N']
            self.parameters += ['F']
            self.parameters += ['Jc']
            self.parameters += ['Js']
            self.parameters += ['Kc']
            self.parameters += ['Ks']
            self.parameters += ['Mc']
            self.parameters += ['Ms']
            self.parameters += ['Gc']
            self.parameters += ['Gs']
            self.parameters += ['Bc']
            self.parameters += ['Bs']
            self.parameters += ['Hc']
            self.parameters += ['Hs']
            self.parameters += ['Dc']
            self.parameters += ['Ds']
            self.parameters += ['Ec']
            self.parameters += ['Es']


        if PAR.MATERIALS == 'Thomsen_3d_tti':
            self.parameters = []
            self.parameters += ['vp']
            self.parameters += ['vs']
            self.parameters += ['epsilon']
            self.parameters += ['delta']
            self.parameters += ['gamma']
            self.parameters += ['theta']
            self.parameters += ['azimuth']




    def load(self, path, parameters=VOIGT2D,
             prefix='', suffix=''):
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


