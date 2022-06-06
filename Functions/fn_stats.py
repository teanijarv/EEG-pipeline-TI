# ========== Packages ==========
import numpy as np
from scipy import stats
import pandas as pd

# ========== Functions ==========
def apply_stat_test(df_psd,conditions,stat_test):
    """
    Perform a paired t-test on dataframe with two conditions.

    Parameters
    ----------
    df_psd: A Pandas dataframe of the power spectra values (for all the channels or regions)
    condition_comp_list: A list of two strings for experiment conditions codes to compare (e.g. ['EC_00','EC_06'])
    
    Returns
    -------
    df_pvals: A Pandas dataframe of p-values from the performed test
    significant_locs: An array of locations (regions/channels) where p <= 0.05
    """
    bands = df_psd['Frequency band'].unique()
    regions = df_psd.drop(columns=['Subject','Frequency band','Condition']).columns.to_numpy()
    df_pvals = pd.DataFrame(index=regions, columns=bands)
    significant_locs = []

    for band in bands:
        df_psd_band = df_psd[df_psd['Frequency band'] == band]
        df_psd_band_cond1 = df_psd_band[df_psd_band['Condition'] == conditions[0]]\
                                .drop(columns=['Subject','Frequency band','Condition'])
        df_psd_band_cond2 = df_psd_band[df_psd_band['Condition'] == conditions[1]]\
                                .drop(columns=['Subject','Frequency band','Condition'])
        for region in df_psd_band_cond1.columns:
            if stat_test=='t-test_paired':
                _,df_pvals[band][region] = stats.ttest_rel(df_psd_band_cond1[region], df_psd_band_cond2[region])
            elif stat_test=='Wilcoxon':
                _,df_pvals[band][region] = stats.wilcoxon(df_psd_band_cond1[region], df_psd_band_cond2[region])
            else:
                print('No valid statistical test chosen')
        sign_idx = df_pvals.index[df_pvals[band]<=0.05].to_numpy()
        sign_pvals = df_pvals[df_pvals[band]<=0.05][band].to_numpy()
        if len(sign_idx) != 0:
            print(conditions,'Significant changes of',band,'are at',sign_idx)
        for i in range(len(sign_idx)):
            significant_locs = np.append(significant_locs,{band: sign_idx[i]})

    return [df_pvals,significant_locs]