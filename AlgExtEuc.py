def extended_euclidean_algorithm(a,n):
    s_old, t_old, r_old = 1, 0, a
    s_new, t_new, r_new = 0, 1, n

    while r_new != 0:
        quotient = r_old // r_new
        r_old, r_new = r_new, r_old - quotient * r_new
        s_old, s_new = s_new, s_old - quotient * s_new
        t_old, t_new = t_new, t_old - quotient * t_new

    if r_old == 1:
        return s_old % n
    else:
        raise ValueError("No existe inverso en este modulo")