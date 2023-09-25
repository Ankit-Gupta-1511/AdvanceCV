import cv2
import numpy as np

def calc_sad(left_block, right_block):
    differences = np.abs(left_block - right_block)
    sad = np.sum(differences)
    return sad

# Referred this along with class slides - https://www.cs.cmu.edu/~16385/s17/Slides/13.2_Stereo_Matching.pdf
def block_matching(imgL, imgR):

    # Assuming some parameters
    window_size = 5 # for 5 x 5 window
    max_disparity = 64

    # Since both the images have same dimensions otherwise we would have to first modify them such that both had same dimensions
    height, width = imgL.shape 
    half_window = window_size // 2 # we are using floor division so that we always get integer value and we don't have to worry about type conversions later on

    # setting disparity map buffer
    disparity_map = np.zeros_like(imgL)

    print(imgL.shape)

    # Starting block matching

    # Similarity Algorithm used is SAD - Sum of Absolute Differences
    ## This means we have to minimise the SAD in (window_size x window_size) window 

    # we start the iteration for a block of size (window_size x window_size) i.e (5 x 5), 
    # hence the iteration should start with half window so that top of the window and left of the window align itself with (0,0) 
    # because intiial window will be like (0,0) -> (5,5) and the exit condition will be for window (width - window_size, height - window_size) -> (width, height)
    for y in range(half_window, height - half_window):
        print("Starting with a new row...")
        for x in range(half_window, width - half_window):
            print("Starting matching in the row...")
            disparity = 0

            # Initially defining the optimium SAD cost to infinity and later on we will store the least SAD cost
            optimum_cost = float('inf')

            # image window block centered around (x, y) 
            min_x = x - half_window
            max_x = x + half_window
            min_y = y - half_window
            max_y = y + half_window

            # this will be a 2d array of pixels of size (window_size, window_size) in the left image that will be matched in the right image
            left_img_block = imgL[min_y : max_y + 1, min_x : max_x + 1]

            for d in range(max_disparity):

                # Remove the iterations that will have negative indices
                if (x - half_window) - d < 0:
                    continue

                # this will be a 2d array of pixels of size (window_size, window_size) in the right image
                right_img_block = imgR[min_y:max_y + 1, min_x - d: max_x - d + 1]

                sad_cost = calc_sad(left_img_block, right_img_block)

                if sad_cost < optimum_cost:
                    optimum_cost = sad_cost
                    disparity = d
                    print("Found a better match...")

            disparity_map[y, x] = disparity

    return disparity_map