# -*- coding: utf-8 -*-
# comparison_with_certified_value.py

import numpy as np
import pandas as pd

def f_comparison_with_certified_value(c_m=3., u_m=0.1, c_CRM=3.1, u_CRM=0.05):
    """Comparison of measurement result with the certified value 
    see: *Thomas Linsinger*, Application Note 1, IRMM __2010__
    c_m:   mean measured value
    c_CRM: certified value
    u_m:   uncertainty of the measurement result
    u_CRM: uncertainty of the certified value
    En: normalized error (also called En-number, see eq. B.5 in EN ISO/IEC 17043:2010)
    returns a pandas dataframe
    """

    Delta_m     = np.abs(c_m-c_CRM)
    Delta_m_rel = Delta_m/c_CRM*100
    u_Delta = np.sqrt(u_m**2 + u_CRM**2)
    U_Delta = 2*u_Delta

    # Normalized error (or En number, see eq. B.5 in EN ISO/IEC 17043:2010 )
    U_m = 2*u_m; U_CRM = 2*u_CRM
    E_n = (c_m-c_CRM)/np.sqrt(U_m**2 + U_CRM**2)

    df = pd.DataFrame({
        'c_m':  [c_m],
        'u_m':  [u_m],
        'c_CRM':[c_CRM],
        'u_CRM':[u_CRM],
        'Delta': [Delta_m],
        'Delta %':[Delta_m_rel],
        'En': [E_n]
    })

    print("Measured value  = {:.2e} ± {:.2e}".format(c_m, u_m))
    print("Certified value = {:.2e} ± {:.2e}".format(c_CRM, u_CRM))
    print("The absolute difference between the mean measured "
          "and the certified value is D = {:.2e} ({:.2f}%).".format(Delta_m,Delta_m_rel))
    print("The expanded uncertainty of difference between result "
          "and certified value is U = {:.2e}.".format(U_Delta))

    from IPython.display import display, HTML
    if Delta_m < U_Delta:
        print("The difference of values is < expanded uncertainty.")
        print("There is no significant difference between measured result and certified value.")
        print()
        display(HTML("The value is <strong style=\"color: green\">OK</strong>!"))
        print()
    if Delta_m > U_Delta:
        print("The difference of values is > expanded uncertainty.")
        print("There is a significant difference between measured result and certified value!")
        print()
        display(HTML("The value is <strong style=\"color: red\">NOT</strong> ok!"))
        print()

    #display(df)
    return df

# vim: set ts=4 sts=4 sw=4 tw=0: