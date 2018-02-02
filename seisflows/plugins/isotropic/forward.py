
# please do not remove this module  -- it may be used in a future version of
# seisflows

# also, please leave dummy arguments in place for the time being


from seisflows.tools.tools import Struct



def phi_beta(dummy, keys, vals):
    input = Struct(zip(keys, vals))
    output = Struct()

    vp = input.vp
    vs = input.vs
    rho = input.rho

    kappa = rho*(vp**2.-(4./3.)*vs**2.)

    output.bulk_c = (kappa/rho)**0.5
    output.bulk_beta = vs
    output.rho = rho

    return output


def kappa_mu(dummy, keys, vals):
    input = Struct(zip(keys, vals))
    output = Struct()

    vp = input.vp
    vs = input.vs
    rho = input.rho

    output.kappa = rho*(vp**2.-(4./3.)*vs**2.)
    output.mu = rho*vs**2.
    output.rho = rho

    return output


def lambda_mu(dummy, keys, vals):
    input = Struct(zip(keys, vals))
    output = Struct()

    vp = input.vp
    vs = input.vs
    rho = input.rho

    output.lame1 = rho*(vp**2. - 2.*vs**2.)
    output.lame2 = rho*vs**2.
    output.rho = rho    

    return output


