
def Voight_TTT_2d(dummy, keys, vals):
    input = Struct(zip(keys, vals))
    output = Struct()

    vp = input.vp
    vs = input.vs
    rho = input.rho
    epsilon = input.epsilon
    delta = input.delta
    theta = input.theta

    c11 = rho * vp**2. * (1. + 2.*epsilon)
    c12 = rho * vp**2. * (1. + 2.*epsilon) - 2.*rho * vs**2. * (1. + 2.*epsilon)
    c13 = rho * vp**2. * (1. + 2.*delta) - 2.*rho * vs**2.
    c33 = rho * vp**2.
    c55 = rho * vs**2.

    sint = sin(PI/180. * theta)
    cost = cos(PI/180. * theta)
    sin2t = sin(2.*PI/180. * theta)
    cos2t = cos(2.*PI/180. * theta)

    output.c11 = c11*cost**4 + c33*sint**4 + 2*c13*sint**2*cost**2 + c55*sin2t**2
    output.c12 = 1.e-6
    output.c13 = c13*(cost**4+sint**4) + (c11+c33)*sint**2*cost**2 - c55*sin2t**2
    output.c15 = ((c11-c13)*cost**2 + (c13-c33)*sint**2)*sint*cost - c55*sin2t*cos2t
    output.c23 = 1.e-6
    output.c25 = 0.0
    output.c33 = c11*sint**4 + c33*cost**4 + 2*c13*sint**2*cost**2 + c55*sin2t**2
    output.c35 = ((c11-c13)*sint**2 + (c13-c33)*cost**2)*sint*cost + c55*sin2t*cos2t
    output.c55 = (c11 - 2.*c13+c33)*sint**2*cost**2 + c55*cos2t**2

