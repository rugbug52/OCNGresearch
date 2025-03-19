import os
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

folder_path = "C:/Users/rugbug/Documents/OCNGresearch/argo_nc_files"

fig = plt.figure(figsize=(12, 7))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.COASTLINE)
ax.set_extent([-80, 20, -60, 60])  # Atlantic region

for filename in os.listdir(folder_path):
    if filename.endswith('.nc'):
        path = os.path.join(folder_path, filename)
        try:
            ds = netCDF4.Dataset(path)
            lat = ds.variables['LATITUDE'][:]
            lon = ds.variables['LONGITUDE'][:]
            ax.plot(lon, lat, linestyle='-', marker='.', label=filename.split('.')[0])
        except Exception as e:
            print(f"Error reading {filename}: {e}")

plt.title("ARGO Float Tracks (Atlantic Ocean)")
plt.show()
