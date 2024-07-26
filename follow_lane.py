import cv2 
import numpy as np
def get_slopes_intercepts(lines):
    slopes = []
    intercepts = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x2 - x1 != 0:  # Avoid division by zero
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1
        else:
            slope = None  # Vertical line case
            intercept = None
        slopes.append(slope)
        intercepts.append(intercept)
    return slopes, intercepts

def get_lane_center(lanes, img_width):
    if not lanes:
        return None, None
    
    # Initialize the closest lane variables
    closest_distance = float('inf')
    closest_intercept = None
    closest_slope = None

    # Image center
    img_center_x = img_width // 2

    # Compute center of each lane and find the closest
    for lane in lanes:
        for line in lane:
            x1, y1, x2, y2 = line
            # Calculate the average x position of the line
            line_center_x = (x1 + x2) // 2
            # Calculate the distance from the image center
            distance = abs(img_center_x - line_center_x)
            
            if distance < closest_distance:
                closest_distance = distance
                slopes, intercepts = get_slopes_intercepts([line])
                closest_slope = slopes[0]
                closest_intercept = intercepts[0]

    return closest_intercept, closest_slope

def recommend_direction(center_intercept, slope, img_width):
    if center_intercept is None or slope is None:
        return "unknown"
    
    # Image center
    img_center_x = img_width // 2

    # Determine the position of the lane center
    if center_intercept is not None:
        if center_intercept < img_center_x - 50:  # Adjust threshold as needed
            return "left"
        elif center_intercept > img_center_x + 50:  # Adjust threshold as needed
            return "right"
        else:
            return "forward"
    else:
        return "unknown"
