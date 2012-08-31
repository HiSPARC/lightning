from math import radians, degrees, tan, atan

def gamma(Ldet, Bdet):
    """ Calculate gamma

    This is needed to compensate for the curvature of the Earth
    """
    L0 = 5.3876389
    B0 = 52.15616

    term1 = tan(radians(0.5 * (Ldet - L0)))
    term2 = tan(radians(0.5 * (Bdet + B0)))
    term3 = tan(radians(0.5 * (Bdet - B0)))

    Gdet = degrees(2 * atan(term1 * term2 / term3))

    return Gdet
