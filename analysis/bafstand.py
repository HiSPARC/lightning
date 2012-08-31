#snijpunt op basis van afstanden
from math import sqrt, sin, cos, atan

# Coordinaten Amsterdam, Eindhoven en Groningen
XA, YA, GA = 125.2667666, 485.3137747, -0.35
XE, YE, GE = 161.9724388, 384.3876739, 0.08
XG, YG, GG = 231.0298275, 585.3039689, 0.91

#Berekening afstanden tussen stations.
LAE = sqrt((XA - XE) ** 2 + (YA - YE) ** 2)
LAG = sqrt((XA - XG) ** 2 + (YA - YG) ** 2)
LEG = sqrt((XE - XG) ** 2 + (YE - YG) ** 2)

#Hoeken tussen de stations.
RAE = atan((YE - YA) / (XE - XA))
RAG = atan((YG - YA) / (XG - XA))
REG = atan((YG - YE) / (XG - XE))


print RAE, RAG, REG

def afstandbep(LA, LE, LG):

    #Meting Amsterdam-Eindhoven
    XT = 0.5 * (LAE ** 2 + LA ** 2 - LE ** 2) / LAE
    YT = sqrt(abs(LA ** 2 - XT ** 2))

    XB11 = XA + XT * cos(RAE) - YT * sin(RAE)
    YB11 = YA + XT * sin(RAE) + YT * cos(RAE)
    XB12 = XA + XT * cos(RAE) + YT * sin(RAE)
    YB12 = YA + XT * sin(RAE) - YT * cos(RAE)

    #Meting Amsterdam-Groningen
    XT = 0.5 * (LAG ** 2 + LA ** 2 - LG ** 2) / LAG
    YT = sqrt(abs(LA ** 2 - XT ** 2))

    XB21 = XA + XT * cos(RAG) - YT * sin(RAG)
    YB21 = YA + XT * sin(RAG) + YT * cos(RAG)
    XB22 = XA + XT * cos(RAG) + YT * sin(RAG)
    YB22 = YA + XT * sin(RAG) - YT * cos(RAG)

    #Metingen Eindhoven-Groningen
    XT = 0.5 * (LEG ** 2 + LE ** 2 - LG ** 2) / LEG
    YT = sqrt(abs(LE ** 2 - XT ** 2))

    XB31 = XE + XT * cos(REG) - YT * sin(REG)
    YB31 = YE + XT * sin(REG) + YT * cos(REG)
    XB32 = XE + XT * cos(REG) + YT * sin(REG)
    YB32 = YE + XT * sin(REG) - YT * cos(REG)

    print XB11, YB11
    print XB12, YB12
    print XB21, YB21
    print XB22, YB22
    print XB31, YB31
    print XB32, YB32

if __name__ == '__main__':
    print 'Vrijthof (176, 318)'
    afstandbep(175, 68, 273)
    print 'Thialf (192, 550)'
    afstandbep(93, 169, 52)
    print 'Evoluon (159, 384)'
    afstandbep(107, 3, 214)
    print 'Vliegv.Enschede (258, 477)'
    afstandbep(132, 133, 111)
    print 'Pier Scheveningen (79, 459)'
    afstandbep(53, 112, 197)
    print 'Neeltje Jans (38, 406)'
    afstandbep(117.9405, 125.6137, 263.4777)
    print 'Dam (121, 487)'
    afstandbep(4, 111, 147)
