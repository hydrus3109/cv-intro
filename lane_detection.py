
import cv2
import numpy as np

def detect_lines(img, threshold1=200, threshold2=300, apertureSize=5, minLineLength=600, maxLineGap= 50):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1, threshold2, apertureSize=apertureSize)
    
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, minLineLength, maxLineGap)
    if lines is not None:
        lines = [line[0] for line in lines]  # Extract the actual coordinates of the lines
    else:
        lines = []
    return lines

def draw_lines(img, lines, color=(0, 255, 0)):
    for line in lines:
        x1, y1, x2, y2 = line
        cv2.line(img, (x1, y1), (x2, y2), color, 2)
    return img

def get_slopes_intercepts(lines):
    slopes = []
    intercepts = []
    for line in lines:
        x1, y1, x2, y2 = line
        if x2 - x1 != 0:  # Avoid division by zero
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1
        else:
            slope = None  # Vertical line case
            intercept = None
        slopes.append(slope)
        intercepts.append(intercept)
    return slopes, intercepts

def detect_lanes(lines):
    slopes, intercepts = get_slopes_intercepts(lines)
    lanes = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            if slopes[i] is not None and slopes[j] is not None:
                if abs(slopes[i] - slopes[j]) < 0.1:  # Adjust
                    lanes.append([lines[i], lines[j]])
    return lanes
def draw_lanes(img, lanes):
    colors = [255, 255, 255] 
    for i, lane in enumerate(lanes):
        colors[i%3] - 50
        color = colors
        for line in lane:
            x1, y1, x2, y2 = line
            cv2.line(img, (x1, y1), (x2, y2), color, 2)
    return img
