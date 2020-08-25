def calc_mld(var, dpt, den_lim=0.03, ref_dpt=10):

    """Calculate the mixed layer depth from the density/temperature difference method

    Args:
      var: temperature or density data file
      dpt: depth data

    Return:
        time series of the mixed layer depth

    Dependencies:
        numpy

    """
    import numpy as np

    mld = []
    for i, prof in enumerate(np.arange(len(var))):

        try:
            ref_dpt_ind = np.nanargmin(np.abs(dpt - ref_dpt))
            rho_diff = np.abs(var[prof, ref_dpt_ind:500] - var[prof, ref_dpt_ind])
            x = rho_diff - den_lim
            x = np.squeeze(np.where(x > 0))[0]
            mld_ind = x + ref_dpt_ind
            mld += dpt[mld_ind],

        except:
            mld += np.NaN,
            print('MLD not calculated: profile ' + str(i) + '. Setting to NaN')

    return mld
