
import sys

from os.path import join

from seisflows.plugins import io
from seisflows.tools.seismic import ModelDict

from seisflows.tools import unix
from seisflows.tools.tools import exists
from seisflows.config import ParameterError, custom_import

PAR = sys.modules['seisflows_parameters']
PATH = sys.modules['seisflows_paths']


class isotropic(custom_import('solver', 'base')):
    """ Adds isotropic elastic inversion machinery
    """
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

    # variable density
    if PAR.MATERIALS == 'rho_phi_beta':
        parameters = []
        parameters += ['bulk_c']
        parameters += ['bulk_beta']
        parameters += ['rho']

    if PAR.MATERIALS == 'rho_kappa_mu':
        parameters = []
        parameters += ['kappa']
        parameters += ['mu']
        parameters += ['rho']

    if PAR.MATERIALS == 'rho_lambda_mu':
        parameters = []
        parameters += ['lame1']
        parameters += ['lame2']
        parameters += ['rho']

    if PAR.MATERIALS == 'rho_alpha_beta':
        parameters = []
        parameters += ['vp']
        parameters += ['vs']
        parameters += ['rho']

    # constant density
    if PAR.MATERIALS == 'phi_beta':
        parameters = []
        parameters += ['bulk_c']
        parameters += ['bulk_beta']

    if PAR.MATERIALS == 'kappa_mu':
        parameters = []
        parameters += ['kappa']
        parameters += ['mu']

    if PAR.MATERIALS == 'lambda_mu':
        parameters = []
        parameters += ['lame1']
        parameters += ['lame2']

    if PAR.MATERIALS == 'alpha_beta':
        parameters = []
        parameters += ['vp']
        parameters += ['vs']

    # gardner's law density
    if PAR.MATERIALS == 'phi_beta_gardner':
        parameters = []
        parameters += ['bulk_c']
        parameters += ['bulk_beta']

    if PAR.MATERIALS == 'kappa_mu_gardner':
        parameters = []
        parameters += ['kappa']
        parameters += ['mu']

    if PAR.MATERIALS == 'lambda_mu_gardner':
        parameters = []
        parameters += ['lame1']
        parameters += ['lame2']

    if PAR.MATERIALS == 'alpha_beta_gardner':
        parameters = []
        parameters += ['vp']
        parameters += ['vs']


    if PAR.MATERIALS  not in plugins.isotropic.forward:
      raise Exception

    if PAR.MATERIALS  not in plugins.isotropic.reverse:
      raise Exception


    @property
    def forward(key):
       return getattr(plugins.isotropic.forward, PAR.MATERIALS)

    @property
    def inverse(key):
       return getattr(plugins.isotropic.reverse, PAR.MATERIALS)


    def load(self, path, parameters=['vp','vs','rho'],
             prefix='', suffix=''):
        """ Reads isotropic elastic model and optionally converts to a
         different parameter set
        """
        dict = Container()

        # read slices
        nproc = self.mesh_properties.nproc
        for iproc in range(nproc):
            for key in prameters:
                key = prefix+key+suffix
                dict[key] = self.io.read_slice(path, key, iproc)

        if parameters==['vp','vs','rho']:
            dict.map(self.forward, nproc)

        return dict


    def save(self, dict, path, parameters=['vp','vs','rho'],
             prefix='', suffix=''):
        """ Writes isotropic elastic model in vp,vs,rho parameters
        """
        if ['rho'] not in parameters:
            for iproc in range(nproc):
                dict['rho'] = self.io.read_slice(PATH.MODEL_INIT, 'rho', iproc)

        if parameters!=['vp','vs','rho']:
            dict.map(self.inverse, nproc)

        # write slices
        nproc = self.mesh_properties.nproc
        for key, val in dict.items():
            key = prefix+key+suffix
            self.io.write_slice(val, path, key, iproc)


