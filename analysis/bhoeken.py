#snijpunt op basis van hoeken
from math import pi, tan

# Coordinaten Amsterdam, Eindhoven en Groningen
XA, YA, GA = 125.2667666, 485.3137747, -0.35
XE, YE, GE = 161.9724388, 384.3876739, 0.08
XG, YG, GG = 231.0298275, 585.3039689, 0.91

def hoekbep(RA, RE, RG):

    RArad = (RA + GA) * pi / 180
    RErad = (RE + GE) * pi / 180
    RGrad = (RG + GG) * pi / 180

    YB1 = (XG - XA + YA * tan(RArad) - YG * tan(RGrad)) / (tan(RArad) - tan(RGrad))
    XB1 = XA + (YB1 - YA) * tan(RArad)

    YB2 = (XA - XE + YE * tan(RErad) - YA * tan(RArad)) / (tan(RErad) - tan(RArad))
    XB2 = XE + (YB2 - YE) * tan(RErad)

    YB3 = (XE - XG + YG * tan(RGrad) - YE * tan(RErad)) / (tan(RGrad) - tan(RErad))
    XB3 = XG + (YB3 - YG) * tan(RGrad)

    print XB1, YB1, XB2, YB2, XB3, YB3
