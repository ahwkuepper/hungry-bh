#! /home/charles/anaconda/bin/python
##! /Users/chaz/anaconda/bin/python

import numpy as np
import matplotlib.pyplot as plt
import collections
import galaxy_mass_coefficients as gmc
import NFW_SO as nfwso
import Constants_NFW
from scipy.optimize import newton as newt
import sigma_equations as se
import sys

''' black hole parameters for Galaxy #1
BH ID		Infall time [Gyr]		Infall mass [Msun]
4		0.891330358			1237391271
6		3.732341011			214762654.2
5		3.739695459			174533439.8
9		7.891740613			1336751979
24		7.990821877			315611465.8
13		8.019273007			147774850.9
18		8.033063371			1375325818
22		8.173075479			134953944.2
38		11.06888207			1031454162
27		11.10294465			2101161483
46		11.24332792			186716693.4
48		11.65254351			1773718716
'''

#Stellar mass coefficients for each galaxy
g1 = np.array([5.55238047e-27, -3.16757613e-22, 7.51108077e-18, -9.59173067e-14, 7.13616762e-10,
                         -3.10946120e-06, 7.48070688e-03, 4.76681897])
g51 = np.array([9.21720403e-28, -5.85756647e-23, 1.59023638e-18, -2.40208805e-14, 2.19815322e-10, -1.23870657e-06,
                4.11467642e-03, 6.60341066])
g65 = np.array([1.40101390e-27, -7.68778493e-23, 1.72469599e-18, -2.05188123e-14, 1.41935495e-10, -6.05073236e-07,
                1.72244648e-03, 9.60556175])

def stellar_mass(t):
    return 10.**(g1[0]*t**7. + g1[1]*t**6. + g1[2]*t**5. + g1[3]*t**4. + g1[4]*t**3. + g1[5]*t**2. + g1[6]*t + g1[7])

def get_eff_rad(t):
    z = nfwso.get_z(t)
    sm = stellar_mass(t)
    return 2500*(sm/1.e11)**0.73*(1.+z)**-0.98

def sigma_eff_rad(t):
    z = nfwso.get_z(t)
    sm = stellar_mass(t)
    return 190.*(sm/1.e11)**0.2*(1.+z)**0.47

def get_rh_from_python_newton(rh0, rc, eff_rad, args):
    if eff_rad >= np.sqrt(rc*rh0):
        func = se.get_sigma_far
        fprime = se.get_dsigfar_drh
    else:
        func = se.get_sigma_near
        fprime = se.get_dsignear_drh
    rh0 = newt(func, rh0, fprime=fprime, args=args)
    return rh0

def get_rh_from_my_own_newton(rh0, eff_rad, rc, G, Mtot, sigma, arktan, lahg, squirt, pie):
    if eff_rad >= np.sqrt(rc*rh0):
        func = se.get_sigma_far
        fprime = se.get_dsigfar_drh
    else:
        func = se.get_sigma_near
        fprime = se.get_dsignear_drh
    tolerance = 0.001
    for i in range(10):
        func_val = func(rh0, eff_rad, rc, G, Mtot, init_guess=sigma, arktan=arktan, lahg=lahg, squirt=squirt,
                         pie=pie)
        fprime_val = fprime(rh0, eff_rad, rc, G, Mtot, init_guess=sigma, arktan=arktan, lahg=lahg,
                                           squirt=squirt, pie=pie)
        rh_next = rh0 -  func_val / fprime_val
        if np.abs(rh_next/rh0-1.) <= tolerance:
            return rh_next, i
        else:
            rh0 = rh_next
            print(func_val, fprime_val, rh_next)
        if i == 9:
            sys.exit('rh couldn\'t converge within 10 iterations!')

def run():
    G = Constants_NFW.G
    t0 = Constants_NFW.t0 #Myr
    mg = gmc.mg
    rc = Constants_NFW.R_C
    arktan = np.arctan
    lahg = np.log
    squirt = np.sqrt
    pie = np.pi
    infall_time = [1000.*it for it in [0.891330358, 3.732341011, 3.739695459, 7.891740613, 7.990821877, 8.019273007,
                                       8.033063371, 8.173075479, 11.06888207, 11.10294465, 11.24332792, 11.65254351]]
    t_s = [t0 + it for it in infall_time]
    for t in t_s:
        Mtot = nfwso.galaxy_mass(mg['1'], t)
        eff_rad = get_eff_rad(t)
        sigma = sigma_eff_rad(t)
        args = (eff_rad, rc, G, Mtot, sigma, arktan, lahg, squirt, pie)

        #Estimate rh from scipy.optimize.newton built-in method
        rh0 = 10000.
        rh = get_rh_from_python_newton(rh0, rc, eff_rad, args)
        print(Mtot, eff_rad, rh, se.get_sigma_far(rh, eff_rad, rc, G, Mtot, init_guess=0., arktan=arktan, lahg=lahg, squirt=squirt,
                                    pie=pie), sigma)

        #Estimate rh from my own newton method, and count how many iterations it takes to converge
        rh0 = 10000.
        rh, i = get_rh_from_my_own_newton(rh0, *args)

        print(Mtot, eff_rad, rh, i, se.get_sigma_far(rh, eff_rad, rc, G, Mtot, init_guess=0., arktan=arktan, lahg=lahg, squirt=squirt,
                                    pie=pie), sigma, '\n')

if __name__ == '__main__':
    run()
