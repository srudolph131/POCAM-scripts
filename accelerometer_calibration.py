# script to get accelerometer data from calibration runs at TUM used as reference values for special operations
import h5py
import numpy as np
import os

h5path = '' # choose path for POCAM device h5 files from calibration runs at TUM
files = [f for f in os.listdir(h5path) if f.startswith('POCAM_')]
DATASET_NAME = 'polar_master_up' # batch1 devices with varying POCAM position configurations -> choose this one (cable is pointing UP)

print(f"{'device ID':<6} | {'radial distance r [m/s^2]':>16} | {'polar angle [°]':>12} | {'azimuthal angle [°]':>12}")
print("-" * 80)


for file in sorted(files):
    try:
        with h5py.File(os.path.join(h5path, file), 'r') as f:
            if DATASET_NAME in f:
                # get mean value for accelerator data of all ten measurements with 0° angle positioning
                accel_data = f[DATASET_NAME][1, :, :3]
                x, y, z = np.mean(accel_data, axis=0)
                
                # use SPHERICAL coordinates now!
                # calculate radial distance
                r = np.sqrt(x**2 + y**2 + z**2)
                
                # calculate polar angle
                theta = np.degrees(np.arccos(z / r))
                
                # calculate azimuthal angle 
                phi = np.degrees(np.arctan2(y, x))
                
                dev_id = file.split('_')[1]
                print(f"{dev_id:<9} | {r:25.4f} | {theta:15.2f} | {phi:20.2f}")
    except Exception as e:
        continue