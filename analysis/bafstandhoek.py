#snijpunt op basis van afstand en richting per station
from math import pi, cos, sin

# Coordinaten Amsterdam, Eindhoven en Groningen
XA, YA, GA = 125, 485, -0.35
XE, YE, GE = 162, 384, 0.08
XG, YG, GG = 231, 585, 0.91

def hoekafstand(RA, RE, RG, LA, LE, LG):

    RArad = (RA + GA) * pi / 180
    RErad = (RE + GE) * pi / 180
    RGrad = (RG + GG) * pi / 180

    XB1 = XA + LA * sin(RArad)
    YB1 = YA + LA * cos(RArad)

    XB2 = XE + LE * sin(RErad)
    YB2 = YE + LE * cos(RErad)

    XB3 = XG + LG * sin(RGrad)
    YB3 = YG + LG * cos(RGrad)

    print 'meting t.o.v. Amsterdam'
    print XB1, YB1
    print 'meting t.o.v. Eindhoven'
    print XB2, YB2
    print 'meting t.o.v. Groningen'
    print XB3, YB3

if __name__ == '__main__':
    print 'Vrijthof (176, 318)'
    hoekafstand(163.03, 167.79, 191.55479, 175, 68, 273)
    print ''
    print 'Thialf (192, 550)'
    hoekafstand(45.85, 10.35, 227.97, 93, 169, 52)
    print ''
    print 'Evoluon (159, 384)'
    hoekafstand(161.58, 257.27, 199.64, 107, 3, 214)
    print ''
    print 'Vliegv. Enschede (258, 477)'
    hoekafstand(93.45, 45.79, 166.21, 132, 133, 111)
    print ''
    print 'Pier Scheveningen (79, 459)'
    hoekafstand(240.52, 312.08, 230.31, 53, 112, 197)
    print ''
    print 'Neeltje Jans (38, 406)'
    hoekafstand(227.59, 279.80, 227.05, 118, 126, 263)
    print ''
    print 'Dam (121, 487)'
    hoekafstand(295.96, 338.41, 228.23, 4, 111, 147)
