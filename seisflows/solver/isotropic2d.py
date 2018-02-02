
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


class isotropic2d(custom_import('solver', 'specfem2d')):
    """ Adds isotropic elastic inversion machinery

       Must supply a model in vp,vs,rho
    """

    def check(self):
        super(isotropic2d, self).check()

        if not hasattr(forward, PAR.MATERIALS):
          raise Exception

        if not hasattr(reverse, PAR.MATERIALS):
          raise Exception

        assert PAR.MATERIALS in [
            'rho_phi_beta',
            'rho_kappa_mu'
            'rho_lambda_mu',
            'rho_alpha_beta'
            'phi_beta_gardner',
            'kappa_mu_gardner'
            'lambda_mu_gardner',
            'alpha_beta_gardner',
            'phi_beta',
            'kappa_mu'
            'lambda_mu',
            'alpha_beta']


    def __init__(self):
        # variable density
        if PAR.MATERIALS == 'rho_phi_beta':
            self.parameters = []
            self.parameters += ['bulk_c']
            self.parameters += ['bulk_beta']
            self.parameters += ['rho']

        if PAR.MATERIALS == 'rho_kappa_mu':
            self.parameters = []
            self.parameters += ['kappa']
            self.parameters += ['mu']
            self.parameters += ['rho']

        if PAR.MATERIALS == 'rho_lambda_mu':
            self.parameters = []
            self.parameters += ['lame1']
            self.parameters += ['lame2']
            self.parameters += ['rho']

        if PAR.MATERIALS == 'rho_alpha_beta':
            self.parameters = []
            self.parameters += ['vp']
            self.parameters += ['vs']
            self.parameters += ['rho']

        # constant density
        if PAR.MATERIALS == 'phi_beta':
            self.parameters = []
            self.parameters += ['bulk_c']
            self.parameters += ['bulk_beta']

        if PAR.MATERIALS == 'kappa_mu':
            self.parameters = []
            self.parameters += ['kappa']
            self.parameters += ['mu']

        if PAR.MATERIALS == 'lambda_mu':
            self.parameters = []
            self.parameters += ['lame1']
            self.parameters += ['lame2']

        if PAR.MATERIALS == 'alpha_beta':
            self.parameters = []
            self.parameters += ['vp']
            self.parameters += ['vs']

        # gardner's law density
        if PAR.MATERIALS == 'phi_beta_gardner':
            self.parameters = []
            self.parameters += ['bulk_c']
            self.parameters += ['bulk_beta']

        if PAR.MATERIALS == 'kappa_mu_gardner':
            self.parameters = []
            self.parameters += ['kappa']
            self.parameters += ['mu']

        if PAR.MATERIALS == 'lambda_mu_gardner':
            self.parameters = []
            self.parameters += ['lame1']
            self.parameters += ['lame2']

        if PAR.MATERIALS == 'alpha_beta_gardner':
            self.parameters = []
            self.parameters += ['vp']
            self.parameters += ['vs']


    def load(self, path, parameters=['vp','vs','rho'],
             prefix='', suffix=''):
        """ Reads isotropic elastic model
        """
        dict = Container()

        nproc = self.mesh_properties.nproc
        for iproc in range(nproc):
            for key in parameters:
                key = prefix+key+suffix
                dict[key] = self.io.read_slice(path, key, iproc)

        if parameters==['vp','vs','rho']:
            dict.map(self.forward, nproc)

        return dict


    def save(self, dict, path, parameters=['vp','vs','rho'],
             prefix='', suffix=''):
        """ Writes isotropic elastic
        """
        nproc = self.mesh_properties.nproc
        if ['rho'] not in parameters:
            for iproc in range(nproc):
                dict['rho'] = self.io.read_slice(PATH.MODEL_INIT, 'rho', iproc)

        if parameters!=['vp','vs','rho']:
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
            self, path=None, parameters=['vp','vs','rho']):
        super(isotropic2d, self).check_mesh_properties(
            path, parameters)


