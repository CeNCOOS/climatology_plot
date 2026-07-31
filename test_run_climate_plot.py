import os
import sys
import numpy as np
import pandas as pd
import scipy.io as sio
from climate_anom_plot import climate_anom_plot


pdir='c:/Reiko_code_M1_climate/'
archive_file=os.path.join(pdir,'M1_daily_ctd_temp2026.mat')
# Load archive data
mat_data = sio.loadmat(archive_file)
m1_sdn = mat_data['m1_sdn'].flatten()
m1_jday = mat_data['m1_jday'].flatten()
m1_depth = mat_data['m1_depth'].flatten()
m1_temp = mat_data['m1_temp']
yr_archive = mat_data['yr'].flatten()
#
dates=pd.to_datetime(m1_sdn-719529,unit='D')
df=pd.DataFrame({"Temperature":m1_temp[0,:]},index=dates)
jfile='clim_plot_cfg.json'
#
climate_anom_plot(pdir,df)
