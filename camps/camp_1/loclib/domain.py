
import numpy as np
from netCDF4 import Dataset

#Preset domain.
if __name__ == "__main__":
    print("Run by itself")

def lonlat2idx(lonlat, url):
    #Todo: add like, when u have a domain outside region of data then return idx= Only the full data.
    dataset = Dataset(url)
    lon = dataset.variables["longitude"][:]
    lat = dataset.variables["latitude"][:]
    # DOMAIN FOR SHOWING GRIDPOINT:: MANUALLY ADJUSTED
    idx = np.where((lat > lonlat[2]) & (lat < lonlat[3]) & \
                   (lon >= lonlat[0]) & (lon <= lonlat[1]))
    dataset.close()
    return idx

def idx2lonlat(idx, url):
    #todo: Remember if u do this once, you can just copy paste into function and u will only need this when new domain.
    # Todo: add like, when u have a domain outside region of data then return idx= Only the full data.
    dataset = Dataset(url)
    lon = dataset.variables["longitude"][:]
    lat = dataset.variables["latitude"][:]
    # DOMAIN FOR SHOWING GRIDPOINT:: MANUALLY ADJUSTED
    lon = lon[idx[0].min():idx[0].max(),idx[1].min(): idx[1].max()]
    lat = lat[idx[0].min():idx[0].max(),idx[1].min(): idx[1].max()]
    dataset.close()
    latlon = [lon.min(), lon.max(),lat.min(), lat.max(), ]

    return latlon


class DOMAIN():
    def __init__(self, lonlat=None, idx=None):
        self.lonlat = lonlat
        self.idx = idx

    def MEPS(self):
        self.lonlat = [ -1, 60., 49., 72]
        url = "https://thredds.met.no/thredds/dodsC/meps25epsarchive/2020/03/06/meps_det_2_5km_20200306T21Z.nc?latitude,longitude"
        self.idx = lonlat2idx(self.lonlat, url)

    def Finse(self):
        self.lonlat = [ 7.524026, 8.524026, 60, 61.5]
        url = "https://thredds.met.no/thredds/dodsC/meps25epsarchive/2020/03/06/meps_det_2_5km_20200306T21Z.nc?latitude,longitude"
        self.idx = lonlat2idx(self.lonlat, url)

    def South_Norway(self):
        self.lonlat = [4., 9.18, 58.01, 62.2]  # lonmin,lonmax,latmin,latmax,
        url = "https://thredds.met.no/thredds/dodsC/meps25epsarchive/2020/03/06/meps_det_2_5km_20200306T21Z.nc?latitude,longitude"
        self.idx = lonlat2idx(self.lonlat, url)

    def Arome_arctic(self):
        self.lonlat = [1,30,70,88] #lonmin,lonmax,latmin,latmax,
        url = "https://thredds.met.no/thredds/dodsC/aromearcticlatest/arome_arctic_sfx_2_5km_latest.nc?latitude,longitude"
        self.idx = lonlat2idx(self.lonlat,url) # RIUGHNone#[0, -1, 0, -1]  # Index; y_min,y_max,x_min,x_max such that lat[y_min] = latmin

    def Svalbard_z1(self): #map
        url = "https://thredds.met.no/thredds/dodsC/aromearcticlatest/arome_arctic_sfx_2_5km_latest.nc?latitude,longitude"

        self.lonlat = [4,23, 76.3, 82]  #
        self.idx = lonlat2idx(self.lonlat,url)# RIUGHNone#[0, -1, 0, -1]  # Index; y_min,y_max,x_min,x_max such that lat[y_min] = latmin
    def Svalbard(self): #data
        url = "https://thredds.met.no/thredds/dodsC/aromearcticlatest/arome_arctic_sfx_2_5km_latest.nc?latitude,longitude"

        self.lonlat = [15,25, 75, 83]  #
        self.idx = lonlat2idx(self.lonlat,url)# RIUGHNone#[0, -1, 0, -1]  # Index; y_min,y_max,x_min,x_max such that lat[y_min] = latmin

    def KingsBay(self): #bigger data
        url = "https://thredds.met.no/thredds/dodsC/aromearcticlatest/arome_arctic_sfx_2_5km_latest.nc?latitude,longitude"

        self.lonlat = [10, 13.3, 78.6, 79.3]
        self.idx = lonlat2idx(self.lonlat,url) #Rough

    def KingsBay_Z0(self): #map
        url = "https://thredds.met.no/thredds/dodsC/aromearcticlatest/arome_arctic_sfx_2_5km_latest.nc?latitude,longitude"

        self.lonlat = [11, 13., 78.73, 79.16]
        self.idx = lonlat2idx(self.lonlat, url) #Rough

    def KingsBay_Z1(self): #smaller data
        url = "https://thredds.met.no/thredds/dodsC/aromearcticlatest/arome_arctic_sfx_2_5km_latest.nc?latitude,longitude"

        self.idx = np.array([[517, 517, 518, 518, 518, 518, 518, 519, 519, 519, 519, 519, 519, 520, 520, 520, 520, 520,
                     520, 520,520, 520, 521, 521, 521, 521, 521, 521, 521, 521, 521, 522, 522, 522, 522, 522,
                     522, 522, 522, 522,523, 523, 523, 523, 523, 523, 524, 524, 524, 524, 524, 525, 525, 525],
                    [183, 184, 182, 183, 184, 185, 186, 182, 183, 184, 185, 186, 187, 181, 182, 183, 184, 185,
                     186, 187,188, 189, 182, 183, 184, 185, 186, 187, 188, 189, 190, 183, 184, 185, 186, 187,
                     188, 189, 190, 191,185, 186, 187, 188, 189, 190, 186, 187, 188, 189, 190, 187, 188, 189]]) #y,x
        self.lonlat = idx2lonlat(self.idx, url)  # rough


