import cv_lib
import numpy as np

from enum import Enum


class LaneDetectionPipelineSteps(Enum):
    All = 0
    ToGrayscale = 1
    GaussianSmoothing = 2
    CannyEdgeDetection = 3
    RoiExtraction = 4
    HoughTransform = 5


def line_extraction_pipeline(img, step=LaneDetectionPipelineSteps.All, smooth_kernel_size=5,
                             canny_low_threshold=50, canny_high_threshold=150,
                             rho=2, theta_deg=1, threshold=15, min_line_len=40, max_line_gap=20):
    # params
    theta = theta_deg * np.pi / 180
    imshape = img.shape
    roi_minx = 0
    roi_miny = 320
    roi_maxx = imshape[1]
    roi_maxy = imshape[0]

    roi_trapezoid_offset = 450
    roi_vertices = np.array(
        [[(roi_minx, roi_maxy), (450, roi_miny), (550, roi_miny),
          (roi_maxx, roi_maxy)]], dtype=np.int32)

    # pipeline
    # Step 1: Conversion to GrayScale
    gray = cv_lib.grayscale(img)
    if step == LaneDetectionPipelineSteps['ToGrayscale'].value:
        return gray

    # Step 2: Gaussian filtering
    smooth = cv_lib.gaussian_blur(gray, smooth_kernel_size)
    if step == LaneDetectionPipelineSteps['GaussianSmoothing'].value:
        return smooth

    # Step 3: Canny edge detector
    edge_det = cv_lib.canny(smooth, low_threshold=canny_low_threshold, high_threshold=canny_high_threshold)
    if step == LaneDetectionPipelineSteps['CannyEdgeDetection'].value:
        return edge_det

    # Step 4 : Region of interest Extraction
    masked_img = cv_lib.region_of_interest(edge_det, vertices=roi_vertices)
    if step == LaneDetectionPipelineSteps['RoiExtraction'].value:
        return masked_img

    # Step 5 : Hough Transform
    lines_det = cv_lib.hough_lines(masked_img, rho, theta, threshold, min_line_len, max_line_gap)
    if step == LaneDetectionPipelineSteps['HoughTransform'].value:
        return lines_det

    final_image = cv_lib.weighted_img(lines_det, img)

    return final_image