from weathervis.config import *
from weathervis.utils import *
from weathervis.domain import *
from weathervis.get_data import *
from weathervis.check_data import *

from weathervis.calculation import *
import os
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
import matplotlib.cm as cm
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.lines import Line2D
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sys
import matplotlib.patheffects as pe
from cartopy.io import shapereader  # For reading shapefiles containg high-resolution coastline.
from copy import deepcopy
import numpy as np
import matplotlib.colors as colors
import matplotlib as mpl
from weathervis.checkget_data_handler import *


def Wind_on_levels(datetime, steps, model,p_level, domain_name = None, domain_lonlat = None, legend=False, info = False,grid=True):
    for dt in datetime:
        date = dt[0:-2]
        hour = int(dt[-2:])
        all_param = ['x_wind_pl','y_wind_pl','air_pressure_at_sea_level','surface_geopotential']
        dmet,data_domain,bad_param = checkget_data_handler(all_param=all_param, date=dt, model=model,
                                                       step=steps,p_level=p_level)
        
        dmet.air_pressure_at_sea_level /= 100
        # print(dmet.pressure) 
        # prepare plot
        x,y = np.meshgrid(dmet.x, dmet.y)

        nx, ny = x.shape
        mask = (
          (x[:-1, :-1] > 1e20) |
          (x[1:, :-1] > 1e20) |
          (x[:-1, 1:] > 1e20) |
          (x[1:, 1:] > 1e20) |
          (x[:-1, :-1] > 1e20) |
          (x[1:, :-1] > 1e20) |
          (x[:-1, 1:] > 1e20) |
          (x[1:, 1:] > 1e20)
        )

        # plot map
        lon0 = dmet.longitude_of_central_meridian_projection_lambert
        lat0 = dmet.latitude_of_projection_origin_projection_lambert
        parallels = dmet.standard_parallel_projection_lambert

        globe = ccrs.Globe(ellipse='sphere', semimajor_axis=6371000., semiminor_axis=6371000.)
        crs = ccrs.LambertConformal(central_longitude=lon0, central_latitude=lat0,
                                    standard_parallels=parallels,globe=globe)
        make_modelrun_folder = setup_directory(OUTPUTPATH, "{0}".format(dt))
        # for the generation of the colormap, list of hexcodes
        C = ['#093b85','#1068e9','#f9db65','#f45510','#c22ecb','#531357']

        # loop over pressure levels, do not forget the indent the whole routine
        for ip,p in enumerate(dmet.pressure):
           
            for tim in np.arange(np.min(steps), np.max(steps)+1, 1):
    
                #ax1 = plt.subplot(projection=crs)
    
                # determine if image should be created for this time step
                stepok=False
                if tim<25:
                    stepok=True
                elif (tim<=36) and ((tim % 3) == 0):
                    stepok=True
                elif (tim<=66) and ((tim % 6) == 0):
                    stepok=True
                if stepok==True:
    
                    fig1, ax1 = plt.subplots(1, 1, figsize=(7, 9),subplot_kw={'projection': crs})
                    ttt = tim #+ np.min(steps)
                    tidx = tim - np.min(steps)
    
                    ZS = dmet.surface_geopotential[tidx, 0, :, :]
                    MSLP = np.where(ZS < 3000, dmet.air_pressure_at_sea_level[tidx, 0, :, :],
                                    np.NaN).squeeze()
                    # calculate windspeed
                    WS = np.sqrt(dmet.x_wind_pl[tidx,ip,:,:]**2 + dmet.y_wind_pl[tidx,ip,:,:]**2)
                    uxx = dmet.x_wind_pl[tidx, ip,:, :].squeeze()
                    vxx = dmet.y_wind_pl[tidx, ip,:, :].squeeze()
 
                    #pcolor as pcolormesh and  this projection is not happy together. If u want faster, try imshow
                    #data =  WS[:nx - 1, :ny - 1].copy()
                    #data[mask] = np.nan
                    #CC=ax1.pcolormesh(x, y,  data[:, :], cmap=plt.cm.get_cmap('Accent', 6), vmin=0, vmax=30,zorder=2)
                    #######################
                    # THIS MAKES THE COLORMAP, FOR AINA TO NOTICE ME
                    cm = get_continuous_cmap(C) # <-- HERE, HERE,HERE 
                    #########################
                    CC=ax1.contourf(x,y,WS,levels=np.linspace(0.0, 30, 7),cmap=cm,zorder=2)
                    # add the wind barbs or quivers
                    skip = (slice(40, -40, 50), slice(40, -40, 50)) #70
                    CVV = ax1.barbs( x[skip], y[skip], uxx[skip]*1.94384, vxx[skip]*1.94384, zorder=3)
    
                    # MSLP
                    # MSLP with contour labels every 10 hPa
                    C_P = ax1.contour(dmet.x, dmet.y, MSLP, zorder=4, alpha=1.0,
                                      levels=np.arange(960, 1050, 1),
                                      colors='grey', linewidths=0.5)
                    C_P = ax1.contour(dmet.x, dmet.y, MSLP, zorder=5, alpha=1.0,
                                      levels=np.arange(960, 1050, 10),
                                      colors='grey', linewidths=1.0, label="MSLP [hPa]")
                    ax1.clabel(C_P, C_P.levels, inline=True, fmt="%3.0f", fontsize=10)
                    ax1.add_feature(cfeature.GSHHSFeature(scale='intermediate'),zorder=6,facecolor="none",edgecolor="gray") 
                    # ‘auto’, ‘coarse’, ‘low’, ‘intermediate’, ‘high, or ‘full’ (default is ‘auto’).
                    if domain_name != model and data_domain !=None: #weird bug.. cuts off when sees no data value
                         ax1.set_extent(data_domain.lonlat)
                    ax1.text(0, 1, "{0}_WS_{1}_{2}+{3:02d}".format(model,int(p), dt, ttt), ha='left', va='bottom', \
                                           transform=ax1.transAxes, color='black')
                    print("filename: "+make_modelrun_folder +"/{0}_{1}_{2}_{3}_{4}+{5:02d}.png".format(model, domain_name, "WS",int(p), dt, ttt))
                    grid = True
                    if grid:
                         nicegrid(ax=ax1)
    
                    legend = True
                    if legend:
                        
                        ax_cb = adjustable_colorbar_cax(fig1, ax1)

                        plt.colorbar(CC,cax = ax_cb, fraction=0.046, pad=0.01, aspect=25,
                                     label=r"wind speed [m/s]",extend='max')

                        proxy = [plt.axhline(y=0, xmin=0, xmax=0, color="gray",zorder=7)]
                        # proxy.extend(proxy1)
                        # legend's location fixed, otherwise it takes very long to find optimal spot
                        lg = ax1.legend(proxy, ["MSLP [hPa]"],loc='upper left')
                        frame = lg.get_frame()
                        frame.set_facecolor('white')
                        frame.set_alpha(0.8)
                        proxy = [plt.axhline(y=0, xmin=0, xmax=0, color="gray",zorder=7)]
    
                    fig1.savefig(make_modelrun_folder +"/{0}_{1}_{2}_{3}_{4}+{5:02d}.png".format(model, domain_name, "WS",int(p), dt, ttt), bbox_inches="tight", dpi=200)
                    ax1.cla()
                    plt.clf()
                    plt.close(fig1)
        plt.close("all")

if __name__ == "__main__":
  import argparse
  def none_or_str(value):
    if value == 'None':
      return None
    return value
  parser = argparse.ArgumentParser()
  parser.add_argument("--datetime", help="YYYYMMDDHH for modelrun", required=True, nargs="+")
  parser.add_argument("--steps", default=0, nargs="+", type=int,help="forecast times example --steps 0 3 gives time 0 to 3")
  parser.add_argument("--p_level", default=1000, nargs="+", type=int,help="p_level example --p_level 1000 925")
  parser.add_argument("--model",default="MEPS", help="MEPS or AromeArctic")
  parser.add_argument("--domain_name", default=None, help="see domain.py", type = none_or_str)
  parser.add_argument("--domain_lonlat", default=None, help="[ lonmin, lonmax, latmin, latmax]")
  parser.add_argument("--legend", default=False, help="Display legend")
  parser.add_argument("--grid", default=True, help="Display legend")
  parser.add_argument("--info", default=False, help="Display info")
  args = parser.parse_args()

  # chunck it into 24-h steps, first find out how many chunks we need, s = steps
  s  = np.arange(np.min(args.steps),np.max(args.steps))
  cn = np.int(len(s)/24)
  if cn == 0:  # length of 24 not exceeded
      Wind_on_levels(datetime=args.datetime, steps = [np.min(args.steps), np.max(args.steps)], model = args.model,
                     p_level=args.p_level,domain_name = args.domain_name, domain_lonlat=args.domain_lonlat,
                     legend = args.legend,info = args.info,grid=args.grid)
  else: # lenght of 24 is exceeded, split in chunks, set by cn+1
      print(f"\n####### request exceeds 24 timesteps, will be chunked to smaller bits due to request limit ##########")
      chunks = np.array_split(s,cn+1)
      for c in chunks:
          Wind_on_level(datetime=args.datetime, steps = [np.min(c), np.max(c)], model = args.model,p_level=args.p_level,
                  domain_name = args.domain_name,domain_lonlat=args.domain_lonlat, legend = args.legend,
                  info = args.info,grid=args.grid)

