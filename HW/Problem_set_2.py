#Problem 1
def evaluate_poly(poly, x):
    """takes in poly as tuple and x as int or float"""
    y = 0
    for i in range(len(poly)):
        y = y + poly[i]*(x**i)
    return y


#Problem 2
def compute_deriv(poly):
    deriv = ()
    for i in range(len(poly)):
        d = (i * poly[i])
        if i > 0:
            deriv = deriv + (d,)
    return deriv


#Problem 3
def compute_root(poly,x,epsilon):
    i = 0;
    while evaluate_poly(poly, x) - 0 > epsilon:
        i += 1
        x = x - (evaluate_poly(poly,x)/ evaluate_poly(compute_deriv(poly),x))

    return (x,i)
