# AIL7140: Advanced Computer Vision
## Programming Assignment 1

### Problem statement
Consider two stereo images I1 (“bikeL.png”) and I2 (“bikeR.png”) of a static scene captured from a
stereo camera with the given intrinsic matrices of both the cameras in the file (“bike.txt”). Implement
the stereo 3D reconstruction algorithm to find the disparity map, depth map (depth map at each pixels),
and 3D point cloud representation of the underlying scene.

### How to run Programme?


Requirements - **Python 3.10.x**
*Python 3.11.x may not work due to open3d dependencies which are used to render the point cloud.*

1. Create a virtual env (optional)

```
python -m venv ./venv
```

2. Activate virtual env

Linux/MacOS (tested on any terminal) - 
```
source ./venv/bin/activate
```

Windows (tested on powershell) - 

```
./venv/Scripts/activate
```

Refer to - https://docs.python.org/3/library/venv.html for more details

3. Install Dependencies

```
pip install -r ./requirements.txt
```

The dependencies are listed in requirements.txt

If this does not work for any reason try using

```
pip install numpy opency-python open3d
```

4. Run the program

```
python ./stereo_3d_reconstruction.py
```

Before running the programme you can modify the downscale factor (`downscale_factor` line - 42) to trade off accuracy for computation speed.

The program should start running and it should show the iteration number that is running. 
In the end the point cloud visualization window will open in open3d

### Project structure

├── Data
│   ├── bike.txt
│   ├── bikeL.png
│   ├── bikeR.png
├── Results
│   ├── actual_dim - contains results of the actual dimension results
│   ├── Dim_747_502 - contains results of downscaled images - downscaled by a factor of 4
├── utils
│   ├── disparity_block_maching.py
│   ├── disparity_column_maching.py (not working properly and not being used in programme. This was to try out another approach.)
│   └── point_cloud.py
├── requirements.txt
├── README.md
├── stereo_3d_reconstruction.py


### Approach

1. All the disparity computation logic is present in `disparity_block_matching.py`. We take the following parameters - 
    - `window_size` = template window size default 5 x 5

2. We try to move the window across the horizontal line on the right image corresponding to the left image(`Epipolar lines`). The given images doesn't need to be rectified we can simply use them as it is.

3. We use `SAD - Sum of Absolute differences` for similarity criterion.

4. Using this disparity map and camera intrinsic matrices and baseline we compute the depth map. (`stereo_3d_reconstruction.py`)

5. Then we project the points to 3d using the depth map info. (`point_cloud.py`)

All the above mentioned files contain relevant comments for step by step process