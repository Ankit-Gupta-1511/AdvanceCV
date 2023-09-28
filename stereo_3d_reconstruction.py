import cv2
import numpy as np

from utils.disparity_block_maching import block_matching
from utils.disparity_column_maching import column_matching
from utils.point_cloud import get_point_Cloud, visualize_point_cloud

def read_calibration_data(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Extract matrices and baseline based on the provided format
    cam0_data = content.split("cam0=")[1].split("]")[0].strip()[1:].split(";")
    K1 = np.array([list(map(float, row.split())) for row in cam0_data])

    cam1_data = content.split("cam1=")[1].split("]")[0].strip()[1:].split(";")
    K2 = np.array([list(map(float, row.split())) for row in cam1_data])

    baseline = float(content.split("baseline=")[1].strip())

    return K1, K2, baseline

def compute_disparity(imgL, imgR, type="block"):

    disparity = None
    if type == "block":
        # block matching takes hours
        disparity = block_matching(imgL, imgR)
    else:
        # Column matching
        disparity = column_matching(imgL, imgR)
    
    return disparity

def disparity_to_depth(disparity, baseline, focal_length):
    # Avoid division by zero when disparity = 0
    depth = focal_length * baseline / (disparity + 0.00001)
    return depth

def main():

    downscale_factor = 4
    # Load the images
    imgL = cv2.imread("Data/bikeL.png", cv2.IMREAD_GRAYSCALE)
    imgR = cv2.imread("Data/bikeR.png", cv2.IMREAD_GRAYSCALE)

    # downscaling image for faster processing
    downscale_shape = (int(imgL.shape[1] / downscale_factor), int(imgL.shape[0] / downscale_factor))
    imgL = cv2.resize(imgL, downscale_shape, interpolation=cv2.INTER_AREA)
    imgR = cv2.resize(imgR, downscale_shape, interpolation=cv2.INTER_AREA)

    # Read intrinsic matrices 
    K1, K2, baseline = read_calibration_data("Data/bike.txt")

    # Since bikeL.png and bikeR.png are in a format such that epipolar lines will be horizontal, 
    # the intrinsic matrices are enough to rectify the images (no distortion, etc.)
    # Otherwise, we would need the extrinsic matrices, distortion coefficients, etc.


    # Step 1
    # Compute the disparity map
    # Defining if we want to use block matching or column matching 
    algo_type = "block"
    disparity_map = compute_disparity(imgL, imgR, algo_type)
    cv2.imwrite((algo_type + "_Disparity.png"), disparity_map )  # Normalize for visualization

    # Step 2
    # Convert disparity to depth
    focal_length = K1[0, 0]  # Since fx = fy = 5299.313 in the given data, hence using fx as focal length
    depth_map = disparity_to_depth(disparity_map, baseline, focal_length)
    depth_map_normalized = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    cv2.imwrite((algo_type + "_Depth.png"), depth_map_normalized)  # Normalize for visualization

    # Step 3
    # 3d point cloud representation
    point_cloud = get_point_Cloud(depth_map=depth_map, img=imgL, K=K1)
    visualize_point_cloud(points=point_cloud)

if __name__ == "__main__":
    main()
