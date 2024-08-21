import string

from sympy.concrete.products import Product
from sympy.concrete.summations import Sum
from sympy.core.function import (diff, expand_func)
from sympy.core import (EulerGamma, TribonacciConstant)
from sympy.core.numbers import (I, Rational, oo, pi)
from sympy.core.singleton import S
from sympy.core.symbol import (Dummy, Symbol, symbols)
from sympy.functions.combinatorial.numbers import carmichael
from sympy.functions.elementary.complexes import (im, re)
from sympy.functions.elementary.integers import floor
from sympy.polys.polytools import cancel
from sympy.series.limits import limit
from sympy.functions import (
    bernoulli, harmonic, bell, fibonacci, tribonacci, lucas, euler, catalan,
    genocchi, partition, motzkin, binomial, gamma, sqrt, cbrt, hyper, log, digamma,
    trigamma, polygamma, factorial, sin, cos, cot, zeta)
from sympy.functions.combinatorial.numbers import _nT

from sympy.core.expr import unchanged
from sympy.core.numbers import GoldenRatio, Integer

from sympy.testing.pytest import XFAIL, raises, nocache_fail
from sympy.abc import x


def test_carmichael():
    assert carmichael.find_carmichael_numbers_in_range(0, 561) == []
    assert carmichael.find_carmichael_numbers_in_range(561, 562) == [561]
    assert carmichael.find_carmichael_numbers_in_range(561, 1105) == carmichael.find_carmichael_numbers_in_range(561,
                                                                                                                 562)
    assert carmichael.find_first_n_carmichaels(5) == [561, 1105, 1729, 2465, 2821]
    assert carmichael.is_prime(2821) == False
    assert carmichael.is_prime(2465) == False
    assert carmichael.is_prime(1729) == False
    assert carmichael.is_prime(1105) == False
    assert carmichael.is_prime(561) == False
    raises(ValueError, lambda: carmichael.is_carmichael(-2))
    raises(ValueError, lambda: carmichael.find_carmichael_numbers_in_range(-2, 2))
    raises(ValueError, lambda: carmichael.find_carmichael_numbers_in_range(22, 2))


def test_bernoulli():
    assert bernoulli(0) == 1
    assert bernoulli(1) == Rational(-1, 2)
    assert bernoulli(2) == Rational(1, 6)
    assert bernoulli(3) == 0
    assert bernoulli(4) == Rational(-1, 30)
    assert bernoulli(5) == 0
    assert bernoulli(6) == Rational(1, 42)
    assert bernoulli(7) == 0
    assert bernoulli(8) == Rational(-1, 30)
    assert bernoulli(10) == Rational(5, 66)
    assert bernoulli(1000001) == 0

    assert bernoulli(0, x) == 1
    assert bernoulli(1, x) == x - S.Half
    assert bernoulli(2, x) == x**2 - x + Rational(1, 6)
    assert bernoulli(3, x) == x**3 - (3*x**2)/2 + x/2

    # Should be fast; computed with mpmath
    b = bernoulli(1000)
    assert b.p % 10**10 == 7950421099
    assert b.q == 342999030

    b = bernoulli(10**6, evaluate=False).evalf()
    assert str(b) == '-2.23799235765713e+4767529'

    # Issue #8527
    l = Symbol('l', integer=True)
    m = Symbol('m', integer=True, nonnegative=True)
    n = Symbol('n', integer=True, positive=True)
    assert isinstance(bernoulli(2 * l + 1), bernoulli)
    assert isinstance(bernoulli(2 * m + 1), bernoulli)
    assert bernoulli(2 * n + 1) == 0
    raises(ValueError, lambda: bernoulli(-2))


def test_fibonacci():
    assert [fibonacci(n) for n in range(-3, 5)] == [2, -1, 1, 0, 1, 1, 2, 3]
    assert fibonacci(100) == 354224848179261915075
    assert [lucas(n) for n in range(-3, 5)] == [-4, 3, -1, 2, 1, 3, 4, 7]
    assert lucas(100) == 792070839848372253127

    assert fibonacci(1, x) == 1
    assert fibonacci(2, x) == x
    assert fibonacci(3, x) == x**2 + 1
    assert fibonacci(4, x) == x**3 + 2*x

    # issue #8800
    n = Dummy('n')
    assert fibonacci(n).limit(n, S.Infinity) is S.Infinity
    assert lucas(n).limit(n, S.Infinity) is S.Infinity

    assert fibonacci(n).rewrite(sqrt) == \
        2**(-n)*sqrt(5)*((1 + sqrt(5))**n - (-sqrt(5) + 1)**n) / 5
    assert fibonacci(n).rewrite(sqrt).subs(n, 10).expand() == fibonacci(10)
    assert fibonacci(n).rewrite(GoldenRatio).subs(n,10).evalf() == \
        fibonacci(10)
    assert lucas(n).rewrite(sqrt) == \
        (fibonacci(n-1).rewrite(sqrt) + fibonacci(n+1).rewrite(sqrt)).simplify()
    assert lucas(n).rewrite(sqrt).subs(n, 10).expand() == lucas(10)
    raises(ValueError, lambda: fibonacci(-3, x))


def test_tribonacci():
    assert [tribonacci(n) for n in range(8)] == [0, 1, 1, 2, 4, 7, 13, 24]
    assert tribonacci(100) == 98079530178586034536500564

    assert tribonacci(0, x) == 0
    assert tribonacci(1, x) == 1
    assert tribonacci(2, x) == x**2
    assert tribonacci(3, x) == x**4 + x
    assert tribonacci(4, x) == x**6 + 2*x**3 + 1
    assert tribonacci(5, x) == x**8 + 3*x**5 + 3*x**2

    n = Dummy('n')
    assert tribonacci(n).limit(n, S.Infinity) is S.Infinity

    w = (-1 + S.ImaginaryUnit * sqrt(3)) / 2
    a = (1 + cbrt(19 + 3*sqrt(33)) + cbrt(19 - 3*sqrt(33))) / 3
    b = (1 + w*cbrt(19 + 3*sqrt(33)) + w**2*cbrt(19 - 3*sqrt(33))) / 3
    c = (1 + w**2*cbrt(19 + 3*sqrt(33)) + w*cbrt(19 - 3*sqrt(33))) / 3
    assert tribonacci(n).rewrite(sqrt) == \
      (a**(n + 1)/((a - b)*(a - c))
      + b**(n + 1)/((b - a)*(b - c))
      + c**(n + 1)/((c - a)*(c - b)))
    assert tribonacci(n).rewrite(sqrt).subs(n, 4).simplify() == tribonacci(4)
    assert tribonacci(n).rewrite(GoldenRatio).subs(n,10).evalf() == \
        tribonacci(10)
    assert tribonacci(n).rewrite(TribonacciConstant) == floor(
            3*TribonacciConstant**n*(102*sqrt(33) + 586)**Rational(1, 3)/
            (-2*(102*sqrt(33) + 586)**Rational(1, 3) + 4 + (102*sqrt(33)
            + 586)**Rational(2, 3)) + S.Half)
    raises(ValueError, lambda: tribonacci(-1, x))


@nocache_fail
def test_bell():
    assert [bell(n) for n in range(8)] == [1, 1, 2, 5, 15, 52, 203, 877]

    assert bell(0, x) == 1
    assert bell(1, x) == x
    assert bell(2, x) == x**2 + x
    assert bell(5, x) == x**5 + 10*x**4 + 25*x**3 + 15*x**2 + x
    assert bell(oo) is S.Infinity
    raises(ValueError, lambda: bell(oo, x))

    raises(ValueError, lambda: bell(-1))
    raises(ValueError, lambda: bell(S.Half))

    X = symbols('x:6')
    # X = (x0, x1, .. x5)
    # at the same time: X[1] = x1, X[2] = x2 for standard readablity.
    # but we must supply zero-based indexed object X[1:] = (x1, .. x5)

    assert bell(6, 2, X[1:]) == 6*X[5]*X[1] + 15*X[4]*X[2] + 10*X[3]**2
    assert bell(
        6, 3, X[1:]) == 15*X[4]*X[1]**2 + 60*X[3]*X[2]*X[1] + 15*X[2]**3

    X = (1, 10, 100, 1000, 10000)
    assert bell(6, 2, X) == (6 + 15 + 10)*10000

    X = (1, 2, 3, 3, 5)
    assert bell(6, 2, X) == 6*5 + 15*3*2 + 10*3**2

    X = (1, 2, 3, 5)
    assert bell(6, 3, X) == 15*5 + 60*3*2 + 15*2**3

    # Dobinski's formula
    n = Symbol('n', integer=True, nonnegative=True)
    # For large numbers, this is too slow
    # For nonintegers, there are significant precision errors
    for i in [0, 2, 3, 7, 13, 42, 55]:
        # Running without the cache this is either very slow or goes into an
        # infinite loop.
        assert bell(i).evalf() == bell(n).rewrite(Sum).evalf(subs={n: i})

    m = Symbol("m")
    assert bell(m).rewrite(Sum) == bell(m)
    assert bell(n, m).rewrite(Sum) == bell(n, m)
    # issue 9184
    n = Dummy('n')
    assert bell(n).limit(n, S.Infinity) is S.Infinity


def test_harmonic():
    n = Symbol("n")
    m = Symbol("m")

    assert harmonic(n, 0) == n
    assert harmonic(n).evalf() == harmonic(n)
    assert harmonic(n, 1) == harmonic(n)
    assert harmonic(1, n).evalf() == harmonic(1, n)

    assert harmonic(0, 1) == 0
    assert harmonic(1, 1) == 1
    assert harmonic(2, 1) == Rational(3, 2)
    assert harmonic(3, 1) == Rational(11, 6)
    assert harmonic(4, 1) == Rational(25, 12)
    assert harmonic(0, 2) == 0
    assert harmonic(1, 2) == 1
    assert harmonic(2, 2) == Rational(5, 4)
    assert harmonic(3, 2) == Rational(49, 36)
    assert harmonic(4, 2) == Rational(205, 144)
    assert harmonic(0, 3) == 0
    assert harmonic(1, 3) == 1
    assert harmonic(2, 3) == Rational(9, 8)
    assert harmonic(3, 3) == Rational(251, 216)
    assert harmonic(4, 3) == Rational(2035, 1728)

    assert harmonic(oo, -1) is S.NaN
    assert harmonic(oo, 0) is oo
    assert harmonic(oo, S.Half) is oo
    assert harmonic(oo, 1) is oo
    assert harmonic(oo, 2) == (pi**2)/6
    assert harmonic(oo, 3) == zeta(3)
    assert harmonic(oo, Dummy(negative=True)) is S.NaN
    ip = Dummy(integer=True, positive=True)
    if (1/ip <= 1) is True:  #---------------------------------+
        assert None, 'delete this if-block and the next line' #|
    ip = Dummy(even=True, positive=True)  #--------------------+
    assert harmonic(oo, 1/ip) is oo
    assert harmonic(oo, 1 + ip) is zeta(1 + ip)

    assert harmonic(0, m) == 0


def test_harmonic_rational():
    ne = S(6)
    no = S(5)
    pe = S(8)
    po = S(9)
    qe = S(10)
    qo = S(13)

    Heee = harmonic(ne + pe/qe)
    Aeee = (-log(10) + 2*(Rational(-1, 4) + sqrt(5)/4)*log(sqrt(-sqrt(5)/8 + Rational(5, 8)))
             + 2*(-sqrt(5)/4 - Rational(1, 4))*log(sqrt(sqrt(5)/8 + Rational(5, 8)))
             + pi*sqrt(2*sqrt(5)/5 + 1)/2 + Rational(13944145, 4720968))

    Heeo = harmonic(ne + pe/qo)
    Aeeo = (-log(26) + 2*log(sin(pi*Rational(3, 13)))*cos(pi*Rational(4, 13)) + 2*log(sin(pi*Rational(2, 13)))*cos(pi*Rational(32, 13))
             + 2*log(sin(pi*Rational(5, 13)))*cos(pi*Rational(80, 13)) - 2*log(sin(pi*Rational(6, 13)))*cos(pi*Rational(5, 13))
             - 2*log(sin(pi*Rational(4, 13)))*cos(pi/13) + pi*cot(pi*Rational(5, 13))/2 - 2*log(sin(pi/13))*cos(pi*Rational(3, 13))
             + Rational(2422020029, 702257080))

    Heoe = harmonic(ne + po/qe)
    Aeoe = (-log(20) + 2*(Rational(1, 4) + sqrt(5)/4)*log(Rational(-1, 4) + sqrt(5)/4)
             + 2*(Rational(-1, 4) + sqrt(5)/4)*log(sqrt(-sqrt(5)/8 + Rational(5, 8)))
             + 2*(-sqrt(5)/4 - Rational(1, 4))*log(sqrt(sqrt(5)/8 + Rational(5, 8)))
             + 2*(-sqrt(5)/4 + Rational(1, 4))*log(Rational(1, 4) + sqrt(5)/4)
             + Rational(11818877030, 4286604231) + pi*sqrt(2*sqrt(5) + 5)/2)

    Heoo = harmonic(ne + po/qo)
    Aeoo = (-log(26) + 2*log(sin(pi*Rational(3, 13)))*cos(pi*Rational(54, 13)) + 2*log(sin(pi*Rational(4, 13)))*cos(pi*Rational(6, 13))
             + 2*log(sin(pi*Rational(6, 13)))*cos(pi*Rational(108, 13)) - 2*log(sin(pi*Rational(5, 13)))*cos(pi/13)
             - 2*log(sin(pi/13))*cos(pi*Rational(5, 13)) + pi*cot(pi*Rational(4, 13))/2
             - 2*log(sin(pi*Rational(2, 13)))*cos(pi*Rational(3, 13)) + Rational(11669332571, 3628714320))

    Hoee = harmonic(no + pe/qe)
    Aoee = (-log(10) + 2*(Rational(-1, 4) + sqrt(5)/4)*log(sqrt(-sqrt(5)/8 + Rational(5, 8)))
             + 2*(-sqrt(5)/4 - Rational(1, 4))*log(sqrt(sqrt(5)/8 + Rational(5, 8)))
             + pi*sqrt(2*sqrt(5)/5 + 1)/2 + Rational(779405, 277704))

    Hoeo = harmonic(no + pe/qo)
    Aoeo = (-log(26) + 2*log(sin(pi*Rational(3, 13)))*cos(pi*Rational(4, 13)) + 2*log(sin(pi*Rational(2, 13)))*cos(pi*Rational(32, 13))
             + 2*log(sin(pi*Rational(5, 13)))*cos(pi*Rational(80, 13)) - 2*log(sin(pi*Rational(6, 13)))*cos(pi*Rational(5, 13))
             - 2*log(sin(pi*Rational(4, 13)))*cos(pi/13) + pi*cot(pi*Rational(5, 13))/2
             - 2*log(sin(pi/13))*cos(pi*Rational(3, 13)) + Rational(53857323, 16331560))

    Hooe = harmonic(no + po/qe)
    Aooe = (-log(20) + 2*(Rational(1, 4) + sqrt(5)/4)*log(Rational(-1, 4) + sqrt(5)/4)
             + 2*(Rational(-1, 4) + sqrt(5)/4)*log(sqrt(-sqrt(5)/8 + Rational(5, 8)))
             + 2*(-sqrt(5)/4 - Rational(1, 4))*log(sqrt(sqrt(5)/8 + Rational(5, 8)))
             + 2*(-sqrt(5)/4 + Rational(1, 4))*log(Rational(1, 4) + sqrt(5)/4)
             + Rational(486853480, 186374097) + pi*sqrt(2*sqrt(5) + 5)/2)

    Hooo = harmonic(no + po/qo)
    Aooo = (-log(26) + 2*log(sin(pi*Rational(3, 13)))*cos(pi*Rational(54, 13)) + 2*log(sin(pi*Rational(4, 13)))*cos(pi*Rational(6, 13))
             + 2*log(sin(pi*Rational(6, 13)))*cos(pi*Rational(108, 13)) - 2*log(sin(pi*Rational(5, 13)))*cos(pi/13)
             - 2*log(sin(pi/13))*cos(pi*Rational(5, 13)) + pi*cot(pi*Rational(4, 13))/2
             - 2*log(sin(pi*Rational(2, 13)))*cos(3*pi/13) + Rational(383693479, 125128080))

    H = [Heee, Heeo, Heoe, Heoo, Hoee, Hoeo, Hooe, Hooo]
    A = [Aeee, Aeeo, Aeoe, Aeoo, Aoee, Aoeo, Aooe, Aooo]
    for h, a in zip(H, A):
        e = expand_func(h).doit()
        assert cancel(e/a) == 1
        assert abs(h.n() - a.n()) < 1e-12


def test_harmonic_evalf():
    assert str(harmonic(1.5).evalf(n=10)) == '1.280372306'
    assert str(harmonic(1.5, 2).evalf(n=10)) == '1.154576311'  # issue 7443


def test_harmonic_rewrite():
    n = Symbol("n")
    m = Symbol("m")

    assert harmonic(n).rewrite(digamma) == polygamma(0, n + 1) + EulerGamma
    assert harmonic(n).rewrite(trigamma) ==  polygamma(0, n + 1) + EulerGamma
    assert harmonic(n).rewrite(polygamma) ==  polygamma(0, n + 1) + EulerGamma

    assert harmonic(n,3).rewrite(polygamma) == polygamma(2, n + 1)/2 - polygamma(2, 1)/2
    assert harmonic(n,m).rewrite(polygamma) == (-1)**m*(polygamma(m - 1, 1) - polygamma(m - 1, n + 1))/factorial(m - 1)

    assert expand_func(harmonic(n+4)) == harmonic(n) + 1/(n + 4) + 1/(n + 3) + 1/(n + 2) + 1/(n + 1)
    assert expand_func(harmonic(n-4)) == harmonic(n) - 1/(n - 1) - 1/(n - 2) - 1/(n - 3) - 1/n

    assert harmonic(n, m).rewrite("tractable") == harmonic(n, m).rewrite(polygamma)

    _k = Dummy("k")
    assert harmonic(n).rewrite(Sum).dummy_eq(Sum(1/_k, (_k, 1, n)))
    assert harmonic(n, m).rewrite(Sum).dummy_eq(Sum(_k**(-m), (_k, 1, n)))


@XFAIL
def test_harmonic_limit_fail():
    n = Symbol("n")
    m = Symbol("m")
    # For m > 1:
    assert limit(harmonic(n, m), n, oo) == zeta(m)


def test_euler():
    assert euler(0) == 1
    assert euler(1) == 0
    assert euler(2) == -1
    assert euler(3) == 0
    assert euler(4) == 5
    assert euler(6) == -61
    assert euler(8) == 1385

    assert euler(20, evaluate=False) != 370371188237525

    n = Symbol('n', integer=True)
    assert euler(n) != -1
    assert euler(n).subs(n, 2) == -1

    raises(ValueError, lambda: euler(-2))
    raises(ValueError, lambda: euler(-3))
    raises(ValueError, lambda: euler(2.3))

    assert euler(20).evalf() == 370371188237525.0
    assert euler(20, evaluate=False).evalf() == 370371188237525.0

    assert euler(n).rewrite(Sum) == euler(n)
    n = Symbol('n', integer=True, nonnegative=True)
    assert euler(2*n + 1).rewrite(Sum) == 0
    _j = Dummy('j')
    _k = Dummy('k')
    assert euler(2*n).rewrite(Sum).dummy_eq(
            I*Sum((-1)**_j*2**(-_k)*I**(-_k)*(-2*_j + _k)**(2*n + 1)*
                  binomial(_k, _j)/_k, (_j, 0, _k), (_k, 1, 2*n + 1)))


def test_euler_odd():
    n = Symbol('n', odd=True, positive=True)
    assert euler(n) == 0
    n = Symbol('n', odd=True)
    assert euler(n) != 0


def test_euler_polynomials():
    assert euler(0, x) == 1
    assert euler(1, x) == x - S.Half
    assert euler(2, x) == x**2 - x
    assert euler(3, x) == x**3 - (3*x**2)/2 + Rational(1, 4)
    m = Symbol('m')
    assert isinstance(euler(m, x), euler)
    from sympy.core.numbers import Float
    A = Float('-0.46237208575048694923364757452876131e8')  # from Maple
    B = euler(19, S.Pi.evalf(32))
    assert abs((A - B)/A) < 1e-31  # expect low relative error
    C = euler(19, S.Pi, evaluate=False).evalf(32)
    assert abs((A - C)/A) < 1e-31


def test_euler_polynomial_rewrite():
    m = Symbol('m')
    A = euler(m, x).rewrite('Sum');
    assert A.subs({m:3, x:5}).doit() == euler(3, 5)


def test_catalan():
    n = Symbol('n', integer=True)
    m = Symbol('m', integer=True, positive=True)
    k = Symbol('k', integer=True, nonnegative=True)
    p = Symbol('p', nonnegative=True)

    catalans = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786]
    for i, c in enumerate(catalans):
        assert catalan(i) == c
        assert catalan(n).rewrite(factorial).subs(n, i) == c
        assert catalan(n).rewrite(Product).subs(n, i).doit() == c

    assert unchanged(catalan, x)
    assert catalan(2*x).rewrite(binomial) == binomial(4*x, 2*x)/(2*x + 1)
    assert catalan(S.Half).rewrite(gamma) == 8/(3*pi)
    assert catalan(S.Half).rewrite(factorial).rewrite(gamma) ==\
        8 / (3 * pi)
    assert catalan(3*x).rewrite(gamma) == 4**(
        3*x)*gamma(3*x + S.Half)/(sqrt(pi)*gamma(3*x + 2))
    assert catalan(x).rewrite(hyper) == hyper((-x + 1, -x), (2,), 1)

    assert catalan(n).rewrite(factorial) == factorial(2*n) / (factorial(n + 1)
                                                              * factorial(n))
    assert isinstance(catalan(n).rewrite(Product), catalan)
    assert isinstance(catalan(m).rewrite(Product), Product)

    assert diff(catalan(x), x) == (polygamma(
        0, x + S.Half) - polygamma(0, x + 2) + log(4))*catalan(x)

    assert catalan(x).evalf() == catalan(x)
    c = catalan(S.Half).evalf()
    assert str(c) == '0.848826363156775'
    c = catalan(I).evalf(3)
    assert str((re(c), im(c))) == '(0.398, -0.0209)'

    # Assumptions
    assert catalan(p).is_positive is True
    assert catalan(k).is_integer is True
    assert catalan(m+3).is_composite is True


def test_genocchi():
    genocchis = [1, -1, 0, 1, 0, -3, 0, 17]
    for n, g in enumerate(genocchis):
        assert genocchi(n + 1) == g

    m = Symbol('m', integer=True)
    n = Symbol('n', integer=True, positive=True)
    assert unchanged(genocchi, m)
    assert genocchi(2*n + 1) == 0
    assert genocchi(n).rewrite(bernoulli) == (1 - 2 ** n) * bernoulli(n) * 2
    assert genocchi(2 * n).is_odd
    assert genocchi(2 * n).is_even is False
    assert genocchi(2 * n + 1).is_even
    assert genocchi(n).is_integer
    assert genocchi(4 * n).is_positive
    # these are the only 2 prime Genocchi numbers
    assert genocchi(6, evaluate=False).is_prime == S(-3).is_prime
    assert genocchi(8, evaluate=False).is_prime
    assert genocchi(4 * n + 2).is_negative
    assert genocchi(4 * n + 1).is_negative is False
    assert genocchi(4 * n - 2).is_negative
    raises(ValueError, lambda: genocchi(Rational(5, 4)))
    raises(ValueError, lambda: genocchi(-2))


@nocache_fail
def test_partition():
    partition_nums = [1, 1, 2, 3, 5, 7, 11, 15, 22]
    for n, p in enumerate(partition_nums):
        assert partition(n) == p

    x = Symbol('x')
    y = Symbol('y', real=True)
    m = Symbol('m', integer=True)
    n = Symbol('n', integer=True, negative=True)
    p = Symbol('p', integer=True, nonnegative=True)
    assert partition(m).is_integer
    assert not partition(m).is_negative
    assert partition(m).is_nonnegative
    assert partition(n).is_zero
    assert partition(p).is_positive
    assert partition(x).subs(x, 7) == 15
    assert partition(y).subs(y, 8) == 22
    raises(ValueError, lambda: partition(Rational(5, 4)))


def test__nT():
       assert [_nT(i, j) for i in range(5) for j in range(i + 2)] == [
    1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 2, 1, 1, 0]
       check = [_nT(10, i) for i in range(11)]
       assert check == [0, 1, 5, 8, 9, 7, 5, 3, 2, 1, 1]
       assert all(type(i) is int for i in check)
       assert _nT(10, 5) == 7
       assert _nT(100, 98) == 2
       assert _nT(100, 100) == 1
       assert _nT(10, 3) == 8


def test_nC_nP_nT():
    from sympy.utilities.iterables import (
        multiset_permutations, multiset_combinations, multiset_partitions,
        partitions, subsets, permutations)
    from sympy.functions.combinatorial.numbers import (
        nP, nC, nT, stirling, _stirling1, _stirling2, _multiset_histogram, _AOP_product)

    from sympy.combinatorics.permutations import Permutation
    from sympy.core.random import choice

    c = string.ascii_lowercase
    for i in range(100):
        s = ''.join(choice(c) for i in range(7))
        u = len(s) == len(set(s))
        try:
            tot = 0
            for i in range(8):
                check = nP(s, i)
                tot += check
                assert len(list(multiset_permutations(s, i))) == check
                if u:
                    assert nP(len(s), i) == check
            assert nP(s) == tot
        except AssertionError:
            print(s, i, 'failed perm test')
            raise ValueError()

    for i in range(100):
        s = ''.join(choice(c) for i in range(7))
        u = len(s) == len(set(s))
        try:
            tot = 0
            for i in range(8):
                check = nC(s, i)
                tot += check
                assert len(list(multiset_combinations(s, i))) == check
                if u:
                    assert nC(len(s), i) == check
            assert nC(s) == tot
            if u:
                assert nC(len(s)) == tot
        except AssertionError:
            print(s, i, 'failed combo test')
            raise ValueError()

    for i in range(1, 10):
        tot = 0
        for j in range(1, i + 2):
            check = nT(i, j)
            assert check.is_Integer
            tot += check
            assert sum(1 for p in partitions(i, j, size=True) if p[0] == j) == check
        assert nT(i) == tot

    for i in range(1, 10):
        tot = 0
        for j in range(1, i + 2):
            check = nT(range(i), j)
            tot += check
            assert len(list(multiset_partitions(list(range(i)), j))) == check
        assert nT(range(i)) == tot

    for i in range(100):
        s = ''.join(choice(c) for i in range(7))
        u = len(s) == len(set(s))
        try:
            tot = 0
            for i in range(1, 8):
                check = nT(s, i)
                tot += check
                assert len(list(multiset_partitions(s, i))) == check
                if u:
                    assert nT(range(len(s)), i) == check
            if u:
                assert nT(range(len(s))) == tot
            assert nT(s) == tot
        except AssertionError:
            print(s, i, 'failed partition test')
            raise ValueError()

    # tests for Stirling numbers of the first kind that are not tested in the
    # above
    assert [stirling(9, i, kind=1) for i in range(11)] == [
        0, 40320, 109584, 118124, 67284, 22449, 4536, 546, 36, 1, 0]
    perms = list(permutations(range(4)))
    assert [sum(1 for p in perms if Permutation(p).cycles == i)
            for i in range(5)] == [0, 6, 11, 6, 1] == [
            stirling(4, i, kind=1) for i in range(5)]
    # http://oeis.org/A008275
    assert [stirling(n, k, signed=1)
        for n in range(10) for k in range(1, n + 1)] == [
            1, -1,
            1, 2, -3,
            1, -6, 11, -6,
            1, 24, -50, 35, -10,
            1, -120, 274, -225, 85, -15,
            1, 720, -1764, 1624, -735, 175, -21,
            1, -5040, 13068, -13132, 6769, -1960, 322, -28,
            1, 40320, -109584, 118124, -67284, 22449, -4536, 546, -36, 1]
    # https://en.wikipedia.org/wiki/Stirling_numbers_of_the_first_kind
    assert  [stirling(n, k, kind=1)
        for n in range(10) for k in range(n+1)] == [
            1,
            0, 1,
            0, 1, 1,
            0, 2, 3, 1,
            0, 6, 11, 6, 1,
            0, 24, 50, 35, 10, 1,
            0, 120, 274, 225, 85, 15, 1,
            0, 720, 1764, 1624, 735, 175, 21, 1,
            0, 5040, 13068, 13132, 6769, 1960, 322, 28, 1,
            0, 40320, 109584, 118124, 67284, 22449, 4536, 546, 36, 1]
    # https://en.wikipedia.org/wiki/Stirling_numbers_of_the_second_kind
    assert [stirling(n, k, kind=2)
        for n in range(10) for k in range(n+1)] == [
            1,
            0, 1,
            0, 1, 1,
            0, 1, 3, 1,
            0, 1, 7, 6, 1,
            0, 1, 15, 25, 10, 1,
            0, 1, 31, 90, 65, 15, 1,
            0, 1, 63, 301, 350, 140, 21, 1,
            0, 1, 127, 966, 1701, 1050, 266, 28, 1,
            0, 1, 255, 3025, 7770, 6951, 2646, 462, 36, 1]
    assert stirling(3, 4, kind=1) == stirling(3, 4, kind=1) == 0
    raises(ValueError, lambda: stirling(-2, 2))

    # Assertion that the return type is SymPy Integer.
    assert isinstance(_stirling1(6, 3), Integer)
    assert isinstance(_stirling2(6, 3), Integer)

    def delta(p):
        if len(p) == 1:
            return oo
        return min(abs(i[0] - i[1]) for i in subsets(p, 2))
    parts = multiset_partitions(range(5), 3)
    d = 2
    assert (sum(1 for p in parts if all(delta(i) >= d for i in p)) ==
            stirling(5, 3, d=d) == 7)

    # other coverage tests
    assert nC('abb', 2) == nC('aab', 2) == 2
    assert nP(3, 3, replacement=True) == nP('aabc', 3, replacement=True) == 27
    assert nP(3, 4) == 0
    assert nP('aabc', 5) == 0
    assert nC(4, 2, replacement=True) == nC('abcdd', 2, replacement=True) == \
        len(list(multiset_combinations('aabbccdd', 2))) == 10
    assert nC('abcdd') == sum(nC('abcdd', i) for i in range(6)) == 24
    assert nC(list('abcdd'), 4) == 4
    assert nT('aaaa') == nT(4) == len(list(partitions(4))) == 5
    assert nT('aaab') == len(list(multiset_partitions('aaab'))) == 7
    assert nC('aabb'*3, 3) == 4  # aaa, bbb, abb, baa
    assert dict(_AOP_product((4,1,1,1))) == {
        0: 1, 1: 4, 2: 7, 3: 8, 4: 8, 5: 7, 6: 4, 7: 1}
    # the following was the first t that showed a problem in a previous form of
    # the function, so it's not as random as it may appear
    t = (3, 9, 4, 6, 6, 5, 5, 2, 10, 4)
    assert sum(_AOP_product(t)[i] for i in range(55)) == 58212000
    raises(ValueError, lambda: _multiset_histogram({1:'a'}))


def test_PR_14617():
    from sympy.functions.combinatorial.numbers import nT
    for n in (0, []):
        for k in (-1, 0, 1):
            if k == 0:
                assert nT(n, k) == 1
            else:
                assert nT(n, k) == 0


def test_issue_8496():
    n = Symbol("n")
    k = Symbol("k")

    raises(TypeError, lambda: catalan(n, k))


def test_issue_8601():
    n = Symbol('n', integer=True, negative=True)

    assert catalan(n - 1) is S.Zero
    assert catalan(Rational(-1, 2)) is S.ComplexInfinity
    assert catalan(-S.One) == Rational(-1, 2)
    c1 = catalan(-5.6).evalf()
    assert str(c1) == '6.93334070531408e-5'
    c2 = catalan(-35.4).evalf()
    assert str(c2) == '-4.14189164517449e-24'


def test_motzkin():
    assert motzkin.is_motzkin(4) == True
    assert motzkin.is_motzkin(9) == True
    assert motzkin.is_motzkin(10) == False
    assert motzkin.find_motzkin_numbers_in_range(10,200) == [21, 51, 127]
    assert motzkin.find_motzkin_numbers_in_range(10,400) == [21, 51, 127, 323]
    assert motzkin.find_motzkin_numbers_in_range(10,1600) == [21, 51, 127, 323, 835]
    assert motzkin.find_first_n_motzkins(5) == [1, 1, 2, 4, 9]
    assert motzkin.find_first_n_motzkins(7) == [1, 1, 2, 4, 9, 21, 51]
    assert motzkin.find_first_n_motzkins(10) == [1, 1, 2, 4, 9, 21, 51, 127, 323, 835]
    raises(ValueError, lambda: motzkin.eval(77.58))
    raises(ValueError, lambda: motzkin.eval(-8))
    raises(ValueError, lambda: motzkin.find_motzkin_numbers_in_range(-2,7))
    raises(ValueError, lambda: motzkin.find_motzkin_numbers_in_range(13,7))
    raises(ValueError, lambda: motzkin.find_first_n_motzkins(112.8))


def test_nD_derangements():
    from sympy.utilities.iterables import (partitions, multiset,
        multiset_derangements, multiset_permutations)
    from sympy.functions.combinatorial.numbers import nD

    got = []
    for i in partitions(8, k=4):
        s = []
        it = 0
        for k, v in i.items():
            for i in range(v):
                s.extend([it]*k)
                it += 1
        ms = multiset(s)
        c1 = sum(1 for i in multiset_permutations(s) if
            all(i != j for i, j in zip(i, s)))
        assert c1 == nD(ms) == nD(ms, 0) == nD(ms, 1)
        v = [tuple(i) for i in multiset_derangements(s)]
        c2 = len(v)
        assert c2 == len(set(v))
        assert c1 == c2
        got.append(c1)
    assert got == [1, 4, 6, 12, 24, 24, 61, 126, 315, 780, 297, 772,
        2033, 5430, 14833]

    assert nD('1112233456', brute=True) == nD('1112233456') == 16356
    assert nD('') == nD([]) == nD({}) == 0
    assert nD({1: 0}) == 0
    raises(ValueError, lambda: nD({1: -1}))
    assert nD('112') == 0
    assert nD(i='112') == 0
    assert [nD(n=i) for i in range(6)] == [0, 0, 1, 2, 9, 44]
    assert nD((i for i in range(4))) == nD('0123') == 9
    assert nD(m=(i for i in range(4))) == 3
    assert nD(m={0: 1, 1: 1, 2: 1, 3: 1}) == 3
    assert nD(m=[0, 1, 2, 3]) == 3
    raises(TypeError, lambda: nD(m=0))
    raises(TypeError, lambda: nD(-1))
    assert nD({-1: 1, -2: 1}) == 1
    assert nD(m={0: 3}) == 0
    raises(ValueError, lambda: nD(i='123', n=3))
    raises(ValueError, lambda: nD(i='123', m=(1,2)))
    raises(ValueError, lambda: nD(n=0, m=(1,2)))
    raises(ValueError, lambda: nD({1: -1}))
    raises(ValueError, lambda: nD(m={-1: 1, 2: 1}))
    raises(ValueError, lambda: nD(m={1: -1, 2: 1}))
    raises(ValueError, lambda: nD(m=[-1, 2]))
    raises(TypeError, lambda: nD({1: x}))
    raises(TypeError, lambda: nD(m={1: x}))
    raises(TypeError, lambda: nD(m={x: 1}))
