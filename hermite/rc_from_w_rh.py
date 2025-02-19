#!/home/charles/anaconda/bin/python

import matplotlib.pyplot as plt
import sys
import sympy
import numpy as np
sys.path.append('/home/charles/Dropbox/Columbia/Ostriker/Cannibalism_code/mergertree/scripts')
import calculate_r200

#W, rh, rc, G, Mtot = sympy.symbols('W rh rc G Mtot')
#expr = W - (-G*Mtot**2./(np.pi*(rh - rc)**2.)*(rc*sympy.ln(4.) + rh*sympy.ln(4.) - 2*rc*sympy.ln(1.+rh/rc) - 2*rh*sympy.ln(1.+rc/rh)))
#solution = sympy.solve(expr, rc)
#print solution

little_h = 0.7
G=0.0043009211
t=1.5653765e+03
z = 7.20196192*(t/1000)**(-0.59331986) - 1.52145449

def get_Mtot(t):
    mg1 = 6.35274705e-06
    mg2 = -3.59251989e-04
    mg3 = 8.42526718e-03
    mg4 = -1.06114735e-01
    mg5 = 7.76146840e-01
    mg6 = -3.31471302
    mg7 = 7.80416677
    mg8 = 5.36229410
    Mtot = 10.**(mg1*(t/1000)**7. + mg2*(t/1000)**6. + mg3*(t/1000)**5. + mg4*(t/1000)**4. + mg5*(t/1000)**3. + \
                mg6*(t/1000)**2. + mg7*(t/1000) + mg8)
    return Mtot

def get_rh(Mtot):
    H = calculate_r200.get_H(z)
    rs = calculate_r200.get_r200(Mtot, H)
    concentration = 10.**(1.025-0.097*np.log(Mtot/((10.**12)/little_h)))
    rh = rs*(0.6082 - 0.1843*np.log(concentration) - 0.1011*(np.log(concentration)**2.) + \
             0.03918*(np.log(concentration)**3.))
    return rh

def get_W(Mtot, rh, rc):
    return -G*Mtot**2./(np.pi*(rh-rc)**2.)*(rc*np.log(4) + rh*np.log(4) - 2*rc*np.log(1.+rh/rc) -\
                 2*rh*np.log(1.+rc/rh))

def get_dW_drc(Mtot, rh, rc):
    return -G*Mtot**2./(np.pi*(rh-rc)**2.)*(np.log(4.) - 2*np.log(1.+rh/rc) + \
                                            2*rh/(rc+rh) - 2/(1.+rc/rh)) - \
            2*G*Mtot**2./(np.pi*(rh-rc)**3.)*(rc*np.log(4.) + rh*np.log(4.) - \
                                              2*rc*np.log(1.+rh/rc) - 2*rh*np.log(1.+rc/rh))

def get_dW_drh(Mtot, rh, rc):
    return -G*Mtot**2./(np.pi*(rh-rc)**2.)*(np.log(4.) - 2*np.log(1.+rc/rh) + \
                                            2*rc/(rc+rh) - 2/(1.+rh/rc)) + \
            2*G*Mtot**2./(np.pi*(rh-rc)**3.)*(rc*np.log(4.) + rh*np.log(4.) - \
                                              2*rc*np.log(1.+rh/rc) - 2*rh*np.log(1.+rc/rh))

def run():
    Mtot = get_Mtot(t)
    rh_base = get_rh(Mtot)
    rc_s = np.arange(1., 1000.)
    W = []
    dW_drc = []
    plt.figure()
    for rc in rc_s:
        W.append(get_W(Mtot, rh_base, rc))
        dW_drc.append(get_dW_drc(Mtot, rh_base, rc))
    plt.subplot(211)
    plt.plot(rc_s, W)
    plt.xlabel('rc (pc)')
    plt.ylabel('W (Msun*(km/s)^2)')
    plt.title('W as function of rc')

    plt.subplot(212)
    plt.semilogy(rc_s, dW_drc)
    plt.xlabel('rc (pc)')
    plt.ylabel('dW/drc (Msun*(km/s)^2/pc)')
    plt.title('dW/drc')

    plt.show()
####################################################
    rc_base = 100.
    rh_s = np.arange(7000., 70000.)
    W = []
    dW_drh = []
    plt.figure()
    for rh in rh_s:
        W.append(get_W(Mtot, rh, rc_base))
        dW_drh.append(get_dW_drh(Mtot, rh, rc_base))
    plt.subplot(211)
    plt.plot(rh_s, W)
    plt.xlabel('rh (pc)')
    plt.ylabel('W (Msun*(km/s)^2)')
    plt.title('W as function of rh')

    plt.subplot(212)
    plt.semilogy(rh_s, dW_drh)
    plt.xlabel('rh (pc)')
    plt.ylabel('dW/drh (Msun*(km/s)^2/pc)')
    plt.title('dW/drh')

    plt.show()


if __name__ == '__main__':
    run()
