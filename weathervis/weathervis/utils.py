#Useful function for setup
import platform
import os
from mpl_toolkits.axes_grid1 import make_axes_locatable ##__N
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.colors as mcolors

def domain_input_handler_old(dt, model, domain_name, domain_lonlat, file, point_lonlat=None):

    if domain_name or domain_lonlat:
        if domain_lonlat:
            print(f"\n####### Setting up domain for coordinates: {domain_lonlat} ##########")
            data_domain = domain(dt, model, file=file, lonlat=domain_lonlat)
        else:
            data_domain = domain(dt, model, file=file)

        if domain_name != None and domain_name in dir(data_domain):
            print(f"\n####### Setting up domain: {domain_name} ##########")
            domain_name = domain_name.strip()
            if re.search("\(\)$", domain_name):
                func = f"data_domain.{domain_name}"
            else:
                func = f"data_domain.{domain_name}()"
            eval(func)
    else:
        data_domain = None
    return data_domain
def domain_input_handler(dt, model, domain_name, domain_lonlat, file, point_name, point_lonlat=None):
  #print(point_name)
  #print(domain_name)
  #print(domain_lonlat)
  if domain_name or domain_lonlat:
    if domain_lonlat:
      print(f"\n####### Setting up domain for coordinates: {domain_lonlat} ##########")
      data_domain = domain(dt, model, file=file, lonlat=domain_lonlat)
    else:
      data_domain = domain(dt, model, file=file)

    if domain_name != None and domain_name in dir(data_domain):
      print(f"\n####### Setting up domain: {domain_name} ##########")
      domain_name = domain_name.strip()
      #data_domain = domain(dt, model, file=file, domain_name=domain_name)
      if re.search("\(\)$", domain_name):
        func = f"data_domain.{domain_name}"
      else:
        func = f"data_domain.{domain_name}()"
      print(func)
      print(domain_name)
      eval(func)
    else:
      print(f"No domain found with that name; {domain_name}")
  else:
    data_domain=None
  if (point_name !=None and domain_name == None and domain_lonlat == None):
     print("GGGGGOOOO")
     data_domain = domain(dt, model, file=file, point_name=point_name)
     print("DOM DONE")
  if (point_lonlat != None, point_name == None and domain_name == None and domain_lonlat == None):
  #   print("GGGGGOOOO")
     data_domain = domain(dt, model, file=file, lonlat=point_lonlat)
     print("DOM DONE")

  print(data_domain)
  return data_domain


def setup_directory( path, folder_name):
    projectpath= path+ folder_name
    if not os.path.exists(projectpath):
        os.makedirs(projectpath)
        print("Directory ", projectpath, " Created ")
    else:
        print("Directory ", projectpath, " already exists")
    return projectpath


def adjustable_colorbar_cax(fig1,ax1):#,data, **kwargs):
      #colorbars do not asjust byitself with set_extent when defining a figure size at the start.
      # if u remove figure_size and it adjust, but labels and text will not be consistent.
      # #Some old solutions dont work, this is the best I could find
      divider = make_axes_locatable(ax1) ##__N
      ax_cb = divider.new_horizontal(size="5%", pad=0.1, axes_class=plt.Axes) ##__N
      fig1.add_axes(ax_cb) ##__N
      #cb= fig1.colorbar(data, **kwargs)
      #cb= fig1.colorbar(CF_BLH, fraction=0.046, pad=0.01,aspect=25,cax=ax_cb, label="Boundary layer thickness [m]", extend="both")
      return ax_cb

def nicegrid(ax, xx = np.arange(-20, 80, 20),yy = np.arange(50, 90, 4), color='gray', alpha=0.5, linestyle='--'):
    gl = ax.gridlines(draw_labels=True, linewidth=1, color=color, alpha=alpha, linestyle=linestyle,zorder=10)
    gl.xlabels_top = False
    import matplotlib.ticker as mticker
    gl.xlocator = mticker.FixedLocator(xx)
    gl.ylocator = mticker.FixedLocator(yy)
    gl.xlabel_style = {'color': color}


def remove_pcolormesh_border(xx,yy,data):
    x, y = np.meshgrid(xx,yy)
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
    data = data[ :nx - 1, :ny - 1].copy()
    data[mask] = np.nan
    # ax.pcolormesh(x, y, data[ :, :])#, cmap=plt.cm.Greys_r)
    return x,y,data


def nice_vprof_colorbar(CF, ax, lvl=None, ticks=None, label=None, highlight_val=None, highlight_linestyle="k--",format='%.1f', extend="both",x0=0.75,y0=0.86,width=0.26,height=0.13):
    #x0, y0, width, height = 0.75, 0.86, 0.26, 0.13
    axins = inset_axes(ax, width='80%', height='23%',
                        bbox_to_anchor=(x0, y0, width, height),  # (x0, y0, width, height)
                        bbox_transform=ax.transAxes,
                        loc="upper center")
    cbar = plt.colorbar(CF, extend=extend, cax=axins, orientation="horizontal", ticks=ticks, format=format)
    ax.add_patch(plt.Rectangle((x0, y0), width, height, fc=[1, 1, 1, 0.7],
                                 transform=ax.transAxes, zorder=1000))

    if ticks is not None:
        cbar.ax.xaxis.set_tick_params(pad=-0.5) #all ticks closer attatched to bar

    if highlight_val is not None:
        #only for equally spaced lvls now. Maybe use diff later to correct for irregularies
        #diff = [t[i + 1] - t[i] for i in range(len(t) - 1)] #list of diff between element
        len = lvl[-1] - lvl[0] #17
        us = highlight_val - lvl[0]
        loc_ticks = us/float(len)  #0.5625, 0,975862068965517

        cbar.ax.plot([loc_ticks]*2, [0, 1], highlight_linestyle) #additional contour on plot

    if label is not None:
        cbar.set_label( label, labelpad=-0.5 )
    return cbar

def add_distance_circle():
    print("test")

def add_point_on_map(ax, lonlat = None, point_name=None, labels=None, colors=None):
    #lonlat = [[10,80],[8,60],...[lon,lat]]
    i=0
    colors= mcolors.TABLEAU_COLORS
    iterator = []
    if point_name !=None:
        sites = pd.read_csv("../../data/sites.csv", sep=";", header=0, index_col=0)
        lonlat = [sites.loc[point_name].lon, sites.loc[point_name].lat]
        iterator += lonlat
    if lonlat !=None:
        iterator +=lonlat

    for it in iterator:
        lonlat_p = it
        mainpoint = ax.scatter(it[0], it[1], s=9.0 ** 2, transform=ccrs.PlateCarree(),
                            color=colors[i], zorder=6, linestyle='None', edgecolors="k", linewidths=3)
        i+=1

# for creating nice colormaps from hexcode, see https://towardsdatascience.com/beautiful-custom-colormaps-with-matplotlib-5bab3d1f0e72
def get_continuous_cmap(hex_list, float_list=None):
    ''' creates and returns a color map that can be used in heat map figures.
        If float_list is not provided, colour map graduates linearly between each color in hex_list.
        If float_list is provided, each color in hex_list is mapped to the respective location in float_list. 
        
        Parameters
        ----------
        hex_list: list of hex code strings
        float_list: list of floats between 0 and 1, same length as hex_list. Must start with 0 and end with 1.
        
        Returns
        ----------
        colour map'''
    rgb_list = [rgb_to_dec(hex_to_rgb(i)) for i in hex_list]
    if float_list:
        pass
    else:
        float_list = list(np.linspace(0,1,len(rgb_list)))
        
    cdict = dict()
    for num, col in enumerate(['red', 'green', 'blue']):
        col_list = [[float_list[i], rgb_list[i][num], rgb_list[i][num]] for i in range(len(float_list))]
        cdict[col] = col_list
    cmp = mcolors.LinearSegmentedColormap('my_cmp', segmentdata=cdict, N=256)
    return cmp
def hex_to_rgb(value):
    '''
    Converts hex to rgb colours
    value: string of 6 characters representing a hex colour.
    Returns: list length 3 of RGB values'''
    value = value.strip("#") # removes hash symbol if present
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_dec(value):
    '''
    Converts rgb to decimal colours (i.e. divides each value by 256)
    value: list (length 3) of RGB values
    Returns: list (length 3) of decimal values'''
    return [v/256 for v in value]
