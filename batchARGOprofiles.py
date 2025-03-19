import arcpy
import os

# ------------------- CONFIG -------------------
# Folder containing your NetCDF files
input_folder = "C:/Users/rugbug/Documents/OCNGresearch/argo_nc_files"

# Output file geodatabase (create if needed)
output_gdb = "C:/Users/rugbug/Documents/ArcGIS/Projects/Whales/ARGOtest1.gdb"

# Set ArcPy environment
arcpy.env.workspace = input_folder
arcpy.env.overwriteOutput = True

# # Create output GDB if it doesn't exist
# if not arcpy.Exists(output_gdb):
#     arcpy.management.CreateFileGDB(os.path.dirname(output_gdb), os.path.basename(output_gdb))
#     print(f"Created GDB: {output_gdb}")

# ------------------- BATCH PROCESSING -------------------
for file in os.listdir(input_folder):
    if file.endswith(".nc"):
        nc_path = os.path.join(input_folder, file)
        layer_name = os.path.splitext(file)[0] + "_point"

        print(f"➡️ Processing: {file}")

        try:
            # ArcGIS NetCDF to Feature Layer tool
            arcpy.md.MakeNetCDFFeatureLayer_md(
                in_netCDF_file=nc_path,
                out_feature_layer=layer_name,
                x_variable="longitude",
                y_variable="latitude",
                variables="temp_adjusted;psal_adjusted;pres_adjusted",  # Add more if needed
                z_variable="",        # Skip for now, unless you want to use depth as z
                time_variable="time"  # Time attribute to enable time slider later
            )

            # Export the layer to the geodatabase
            out_fc = os.path.join(output_gdb, layer_name)
            arcpy.management.CopyFeatures(layer_name, out_fc)
            print(f"✅ Saved: {out_fc}")

        except Exception as e:
            print(f"❌ Error with {file}: {e}")

print("🎉 All NetCDF profiles processed successfully.")
