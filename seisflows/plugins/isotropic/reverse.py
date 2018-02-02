
# please do not remove this module  -- it may be used in a future version of
# seisflows

# also, please leave dummy arguments in place for the time being


from seisflows.tools.tools import Struct



def phi_beta(dummy, keys, vals):
    input = Struct(zip(keys, vals))
    output = Struct()

    phi = input.bulk_c
    vs = input.bulk_beta
    rho = input.rho

    kappa = rho*phi**2.
    mu = rho*vs**2.

    output.vp = ((kappa+(4./3.)*mu)/rho)**0.5
    output.vs = vs
    output.rho = rho

    return output


def kappa_mu(dummy, keys, vals):
    input = Struct(zip(keys, vals))
    output = Struct()

    kappa = input.kappa
    mu = input.mu
    rho = input.rho

    output.vp = ((kappa+(4./3.)*mu)/rho)**0.5
    output.vs = (mu/rho)**0.5
    output.rho = rho

    return output


def lambda_mu(dummy, keys, vals):
    input = Struct(zip(keys, vals))
    output = Struct()

    lame1 = input.lame1
    lame2 = input.lame2
    rho = input.rho

    output.vp = ((lame1 + 2.*lame2)/rho)**0.5
    output.vs = (lame2/rho)**0.5
    output.rho = rho

    return output


