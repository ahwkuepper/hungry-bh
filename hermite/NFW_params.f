C***********************************************************************
C
C
      FUNCTION r200(timo)
C
C
C***********************************************************************
      INCLUDE 'hermite.h'

      REAL*8 z_loc, g_m
      REAL*8 timo

      z_loc = z_conv(timo)
      g_m = galaxy_mass(timo)
      H = H0*(WV + (1. - WV - WM)*(1. + z_loc)**2 + 
     &    WM*(1. + z_loc)**3)**0.5    !Equation 3 from The Formation of Galactic Disks (Mo, Mao, White)
      r200 = (g_m*G/(100.*H**2.))**(1./3.) !r200 is in parsecs; Equation 2 from The Formation of Galactic Disks (Mo, Mao, White)
      RETURN
      END

C***********************************************************************
C
C
      FUNCTION concentration()
C
C
C***********************************************************************
      INCLUDE 'hermite.h'

      concentration = 10.**(1.025-0.097*LOG(Ms/((10.**12)/little_h)))	!Equation 7 from NFW paper
      RETURN
      END

C***********************************************************************
C
C
      FUNCTION rho_crit(timo)
C
C
C***********************************************************************
      INCLUDE 'hermite.h'

      REAL*8 z_loc, timo

      z_loc = z_conv(timo)
      H = H0*(WV + (1. - WV - WM)*(1. + z_loc)**2 + 
     &    WM*(1. + z_loc)**3)**0.5    !Equation 3 from The Formation of Galactic Disks (Mo, Mao, White)
      rho_crit = 3.*(H**2.)/(8.*PI*G)	!From paragraph above Equation 1 in NFW paper
      RETURN
      END
