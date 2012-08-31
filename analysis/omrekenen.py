# Zero point in Amersfoort
L0, B0 = 5.387638889, 52.156160556
X0, Y0 = 155000, 463000

# Coefficients according to Govert Strang van Hees

A01 =  3236.0331637
A20 = -32.5915821
A02 = -0.2472814
A21 = -0.8501341
A03 = -0.0655238
A22 = -0.0171137
A40 =  0.0052771
A23 = -0.0003859
A41 =  0.0003314
A04 =  0.0000371
A42 =  0.0000143
A24 = -0.0000090

B10 = 5261.3028966
B11 = 105.9780241
B12 = 2.4576469
B30 = -0.8192156
B31 = -0.0560092
B13 = 0.0560089
B32 = -0.0025614
B14 = 0.0012770
B50 = 0.0002574
B33 = -0.0000973
B51 = 0.0000293
B15 = 0.0000291

C01 =  190066.98903
C11 = -11830.85831
C21 = -114.19754
C03 = -32.38360
C31 = -2.34078
C13 = -0.60639
C23 =  0.15774
C41 = -0.04158
C05 = -0.00661

D10 =  309020.31810
D02 =  3638.36193
D12 = -157.95222
D20 =  72.97141
D30 =  59.79734
D22 = -6.43481
D04 =  0.09351
D32 = -0.07379
D14 = -0.05419
D40 = -0.03444


def rdgeo(XP, YP):
    """ Convert a RD position to geographic coordinates """

    # Convert units from km to m
    XP = 1000 * XP
    YP = 1000 * YP

    # Berekening kaartcoordinaten
    DX = 0.00001 * (XP - X0)
    DY = 0.00001 * (YP - Y0)

    TermB01 = A01 * DY
    TermB02 = A20 * DX ** 2
    TermB03 = A02 * DY ** 2
    TermB04 = A21 * DX ** 2 * DY
    TermB05 = A03 * DY ** 3
    TermB06 = A22 * DX ** 2 * DY ** 2
    TermB07 = A40 * DX ** 4
    TermB08 = A23 * DX ** 2 * DY ** 3
    TermB09 = A41 * DX ** 4 * DY
    TermB10 = A04 * DY ** 4
    TermB11 = A42 * DX ** 4 * DY ** 2
    TermB12 = A24 * DX ** 2 * DY ** 4

    TermL01 = B10 * DX
    TermL02 = B11 * DX * DY
    TermL03 = B12 * DX * DY ** 2
    TermL04 = B30 * DX ** 3
    TermL05 = B31 * DX ** 3 * DY
    TermL06 = B13 * DX * DY ** 3
    TermL07 = B32 * DX ** 3 * DY ** 2
    TermL08 = B14 * DX * DY ** 4
    TermL09 = B50 * DX ** 5
    TermL10 = B33 * DX ** 3 * DY ** 3
    TermL11 = B51 * DX ** 5 * DY
    TermL12 = B15 * DX * DY ** 5

    db = (TermB01 + TermB02 + TermB03 + TermB04 + TermB05 + TermB06 + TermB07 +
          TermB08 + TermB09 + TermB10 + TermB11 + TermB12)
    dl = (TermL01 + TermL02 + TermL03 + TermL04 + TermL05 + TermL06 + TermL07 +
          TermL08 + TermL09 + TermL10 + TermL11 + TermL12)

    # Geographic coordinates
    BP = B0 + db / 3600
    LP = L0 + dl / 3600

    print LP, BP

def geord(LP, BP):
    """ Convert given long lat coordinates to the corresponding RD position """

    DB = 0.36 * (BP - B0)
    DL = 0.36 * (LP - L0)

    TermX01 = C01 * DL
    TermX02 = C11 * DB * DL
    TermX03 = C21 * DB ** 2 * DL
    TermX04 = C03 * DL ** 3
    TermX05 = C31 * DB ** 3 * DL
    TermX06 = C13 * DB * DL ** 3
    TermX07 = C23 * DB ** 2 * DL ** 3
    TermX08 = C41 * DB ** 4 * DL
    TermX09 = C05 * DL ** 5

    TermY01 = D10 * DB
    TermY02 = D02 * DL ** 2
    TermY03 = D12 * DB * DL ** 2
    TermY04 = D20 * DB ** 2
    TermY05 = D30 * DB ** 3
    TermY06 = D22 * DB ** 2 * DL ** 2
    TermY07 = D04 * DL ** 4
    TermY08 = D32 * DB ** 3*DL ** 2
    TermY09 = D14 * DB * DL ** 4
    TermY10 = D40 * DB ** 4

    dx = (TermX01 + TermX02 + TermX03 + TermX04 + TermX05 + TermX06 + TermX07 +
          TermX08 + TermX09)
    dy = (TermY01 + TermY02 + TermY03 + TermY04 + TermY05 + TermY06 + TermY07 +
          TermY08 + TermY09 + TermY10)

    # RD map coordinates in km
    XP = 0.001 * (X0 + dx)
    YP = 0.001 * (Y0 + dy)

    print XP, YP
