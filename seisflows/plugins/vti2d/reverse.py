


def Thomsen(dummy, keys, vals):
    input = Struct(zip(keys, vals))
    output = Struct()

    vp = input.vp
    vs = input.vs
    rho = input.rho
    epslion = input.epsilon
    delta = input.delta

    output.c11 = rho * vp**2. * (1. + 2.*epsilon)
    output.c12 = rho * vp**2. * (1. + 2.*epsilon) - 2.*rho * vs**2. * (1. + 2.*epsilon)
    output.c13 = rho * vp**2. * (1. + 2.*delta) - 2.*rho * vs**2.
    output.c33 = rho * vp**2.
    output.c55 = rho * vs**2.

    return output



def ChenTromp(dummy, keys, vals):
    raise NotImplementedError
