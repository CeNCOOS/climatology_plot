import os
import sys
from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd
import scipy.io as sio
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.collections import PolyCollection
import json
import pdb
#
# Create climatology style plot
#
def climate_anom_plot(path,data):
    """ path is path to the configuration file
        data is a time-series of the data in a pandas dataframe
        have a json file for configuration?
    """
    #
    jfile='clim_plot_cfg.json'
    # open the json file
    fid=open(path+jfile,'r')
    # get the configuration information
    cfg_info=json.load(fid)
    # get years to compute climate for
    c_years=cfg_info[0]['climate_years']
    ylims=cfg_info[0]['yaxis_limits']
    ylabel=cfg_info[0]['var_name']
    filepath=cfg_info[0]['data_path']
    #
    #pdb.set_trace()
    data=data.sort_index()
    data.index=data.index.round("1s")
    data=data[~data.index.duplicated(keep='first')]
    #dup_ind=np.where(data.index.duplicated())[0].tolist()
    #pdb.set_trace()
    #data=data.drop(data.index[dup_ind],inplace=True)
    
    #
    # assume data is a pandas data frame with index of datetimes
    #
    df_limited=data[(data.index.year >= c_years[0])&(data.index.year <= c_years[1])]
    #
    # compute seasonal statistics
    #
    climatology=df_limited.groupby(df_limited.index.dayofyear)[ylabel].agg(["mean","min","max"])
    # get current time for current year
    current_date=date.today()
    currentdata=data[data.index.year==current_date.year]
    # or
    # currentdata=data.loc[current_date.year]
    # get day of year for plotting against
    days=currentdata.index.dayofyear
    # compute anomaly of the data
    anoms=[]
    for i in range(len(days)-1):
        aval=currentdata[ylabel].iloc[i]-climatology["mean"].iloc[i]
        anoms.append(aval)
    # convert list to an array for use in next step
    anomaly=np.array(anoms)
    verts=[]
    # create the shape of the vertical bars for the plot
    # 
    #
    for i in range(len(days)-1):
        x_quad=[days[i],days[i],days[i+1],days[i+1]]
        y_quad=[climatology["mean"].iloc[i],currentdata[ylabel].iloc[i],currentdata[ylabel].iloc[i+1],climatology["mean"].iloc[i+1]]
        verts.append(list(zip(x_quad,y_quad)))
    # get the colormap we want
    cmap=matplotlib.colormaps.get_cmap('coolwarm')
    min_val=min(-1.0,anomaly.min())
    max_val=max(1.0,anomaly.max())
    # set up so middle is always zero
    norm=TwoSlopeNorm(vmin=min_val,vcenter=0.0,vmax=max_val)
    #pdb.set_trace()
    coll=PolyCollection(
        verts,
        array=anomaly,
        cmap=cmap,
        norm=norm,
        edgecolors='none'
        )
    #
    # Define day of year values
    #
    # Jan=0 or 15 for center
    # Feb=32 or 45
    # Mar=60 or 74
    # Apr=91 or 105
    # May=121 or 135
    # Jun=152 or 166
    # Jul=182 or 196
    # Aug=213 or 227
    # Sep=244 or 258
    # Oct=274 or 288
    # Nov=305 or 319
    # Dec=335 or 349
    #
    xtick_locs=[1,32,60,91,121,152,182,213,244,274,305,335]
    xtick_labs=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    #
    # Now to see if the magic can happen
    #
    fig,ax=plt.subplots(figsize=(12,6), facecolor='#FAF5EF')
    ax.set_facecolor('#FAF5EF')
    # add filled segments
    ax.add_collection(coll)
    # plot bounding values
    #ax.plot(climatology["mean"],color='#333333', linestyle='--',linewidth=1.2,label='Mean')
    # Francisco's suggestion to solid black
    ax.plot(climatology["mean"],color='k', linestyle='-',linewidth=1.2,label='Mean')
    ax.plot(days,currentdata[ylabel],color='#222222', linewidth=1.2, label='Actual Temp')
    ax.plot(climatology["min"],color='lightgrey')
    ax.plot(climatology["max"],color='lightgrey')
    # Francisco's suggestion
    # I tried this and I'm not a fan (FLB)
    #ax.plot(climatology["min"],color='b')
    #ax.plot(climatology["max"],color='r')
    # styling?
    ax.set_xlim(1, 366)
    plt.xticks(ticks=xtick_locs,labels=xtick_labs)
    ax.text(
        0.5, -0.15, str(current_date.year),
        transform=ax.transAxes,
        ha='center',va='top',
        fontsize=12, fontweight='bold'
        )
    #ax.set_xlim(day.min(),day.max())
    ax.set_ylim(ylims[0],ylims[1])
    #ax.set_ylim(6,18)
    # We will need more labelling parameters
    ax.set_ylabel('Daily '+ylabel)
    #ax.set_ylabel('Daily Temperature (C)')
    ax.grid(True,axis='y', color='#E0D8D0',linestyle='-',linewidth=0.8)
    #for spine in ['top','right','left','bottom']:
    for spine in ['top','right']:
        ax.spines[spine].set_visible(False)
    # Colorbar
    cbar=fig.colorbar(
        plt.cm.ScalarMappable(norm=norm, cmap=cmap),
        ax=ax,
        orientation='horizontal',
        pad=0.15,
        shrink=0.4
        )
    #
    # Now to print out the plot
    #
    #plt.show()
    plot_name='Climatology_anomaly_for_'+str(current_date.year)+'.png'
    plt.savefig(plot_name,dpi=300,bbox_inches='tight')
    return
    
    
    
    
    
    
    
    
    
    
