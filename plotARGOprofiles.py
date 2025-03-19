import os
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime

# === Set folder and time range ===
folder_path = "C:/Users/rugbug/Documents/OCNGresearch/argo_nc_files"

# Set desired time filter
start_date = datetime(2019, 10, 1)
end_date   = datetime(2019, 10, 31)

# Storage for filtered data
all_lats = []
all_lons = []
all_temps = []
all_dates = []

# === Loop through files ===
for filename in os.listdir(folder_path):
    if filename.endswith('.nc'):
        file_path = os.path.join(folder_path, filename)
        try:
            ds = netCDF4.Dataset(file_path)

            lat = ds.variables['LATITUDE'][:]
            lon = ds.variables['LONGITUDE'][:]
            temp = ds.variables['TEMP'][:]  # use TEMP_ADJUSTED if you prefer
            juld = ds.variables['JULD'][:]
            time_units = ds.variables['JULD'].units
            time_calendar = ds.variables['JULD'].calendar if 'calendar' in ds.variables['JULD'].ncattrs() else 'standard'

            # Convert JULD to datetime
            times = netCDF4.num2date(juld, units=time_units, calendar=time_calendar)

            # If multidimensional TEMP (profile x depth), take surface
            if temp.ndim > 1:
                temp = temp[:, 0]

            # Filter by time range
            for i in range(len(times)):
                if start_date <= times[i] <= end_date and np.isfinite(temp[i]):
                    all_lats.append(lat[i])
                    all_lons.append(lon[i])
                    all_temps.append(temp[i])
                    all_dates.append(times[i])

        except Exception as e:
            print(f"Error reading {filename}: {e}")

# === Plotting ===
fig = plt.figure(figsize=(12, 7))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-70, -40, -50, -30])  # Adjust extent as needed

# Add map features
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.gridlines(draw_labels=True)

# Plot filtered profiles by temperature
sc = ax.scatter(all_lons, all_lats, c=all_temps, cmap='viridis', s=30, edgecolor='k', alpha=0.8)

# Colorbar
cbar = plt.colorbar(sc, ax=ax, orientation='vertical', pad=0.02)
cbar.set_label("Temperature (°C)")

plt.title(f"ARGO Profile Locations in {start_date.month}/{start_date.year} (Color-coded by Temperature)")
plt.show()
