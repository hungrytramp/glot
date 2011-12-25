from math import sqrt, radians, sin, cos, tan, atan, atan2

def distance(p1, p2):
    # taken from http://www.movable-type.co.uk/scripts/latlong-vincenty.html and translated into Python

    a = 6378137
    b = 6356752.314245
    f = 1 / 298.257223563

    L = radians(p2['lon'] - p1['lon'])
    U1 = atan((1 - f) * tan(radians(p1['lat'])))
    U2 = atan((1 - f) * tan(radians(p2['lat'])))

    sin_U1 = sin(U1)
    cos_U1 = cos(U1)
    sin_U2 = sin(U2)
    cos_U2 = cos(U2)

    l = L
    prev_l = None
    iter_limit = 100

    while iter_limit > 0 and (prev_l is None or abs(l - prev_l) > 1e-12):
        iter_limit -= 1

        sin_l = sin(l)
        cos_l = cos(l)

        sin_s = sqrt((cos_U2 * sin_l) * (cos_U2 * sin_l) + (cos_U1 * sin_U2 - sin_U1 * cos_U2 * cos_l) * (cos_U1 * sin_U2 - sin_U1 * cos_U2 * cos_l))

        if sin_s == 0:
            return 0

        cos_s = sin_U1 * sin_U2 + cos_U1 * cos_U2 * cos_l

        s = atan2(sin_s, cos_s)

        sin_alpha = cos_U1 * cos_U2 * sin_l / sin_s
        cos_sq_alpha = 1 - sin_alpha * sin_alpha

        try:
            cos2_sm = cos_s - 2 * sin_U1 * sin_U2 / cos_sq_alpha
        except ZeroDivisionError:
            cos2_sm = 0

        C = f / 16 * cos_sq_alpha * (4 + f * (4 - 3 * cos_sq_alpha))
        prev_l = l
        l = L + (1 - C) * f * sin_alpha * (s + C * sin_s * (cos2_sm + C * cos_s * (-1 + 2 * cos2_sm * cos2_sm)))

    if iter_limit == 0:
        raise Exception("Failed to compute distance between %s and %s." % p1, p2)

    u_sq = cos_sq_alpha * (a * a - b * b) / (b * b)
    A = 1 + u_sq / 16384 * (4096 + u_sq * (-768 + u_sq * (320 - 175 * u_sq)))
    B = u_sq / 1024 * (256 + u_sq * (-128 + u_sq * (74 - 47 * u_sq)))
    delta_s = B * sin_s * (cos2_sm + B / 4 * (cos_s * (-1 + 2 * cos2_sm * cos2_sm) - B / 6 * cos2_sm * (-3 + 4 * sin_s * sin_s) * (-3 + 4 * cos2_sm * cos2_sm)))

    return b * A * (s - delta_s)