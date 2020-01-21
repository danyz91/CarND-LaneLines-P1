import cv2
import numpy as np
import os
import cv_lane_detector
import argparse


def nothing(x):
    pass

parser = argparse.ArgumentParser(description='Lane Detection Parameters Tuning GUI')
parser.add_argument('-d', '--images_dir', help='test images directory', type=str, required=True)
parser.add_argument('-s', '--step', help='pipeline steps to plot. 0 for final output', 
    type=int, choices=(0,1,2,3,4,5), default=0)


def main():
    args = parser.parse_args()
    pipeline_step = args.step
    # Create main window
    cv2.namedWindow('lane_detect_window')
    
    # Create trackbars for parameter tuning
    cv2.createTrackbar('smooth_kernel_size', 'lane_detect_window', 7, 20, nothing)
    cv2.createTrackbar('canny_low_threshold', 'lane_detect_window', 80, 255, nothing)
    cv2.createTrackbar('canny_high_threshold', 'lane_detect_window', 160, 255, nothing)
    cv2.createTrackbar('rho', 'lane_detect_window',  2,  255,  nothing)
    cv2.createTrackbar('theta_deg', 'lane_detect_window', 1, 360, nothing)
    cv2.createTrackbar('threshold', 'lane_detect_window', 15, 50, nothing)
    cv2.createTrackbar('min_line_len', 'lane_detect_window', 10, 255, nothing)
    cv2.createTrackbar('max_line_gap', 'lane_detect_window', 10, 255, nothing)

    # Load images from test folder
    test_images_dir = args.images_dir
    test_images_names = os.listdir(test_images_dir)

    test_images = list()
    for filename in test_images_names:
        test_images.append(cv2.imread(os.path.join(test_images_dir, filename)))

    frame_result_list = list()

    # Enter main loop
    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

        # get current positions of trackbars
        smooth_kernel_size = cv2.getTrackbarPos('smooth_kernel_size', 'lane_detect_window')
        canny_low_threshold = cv2.getTrackbarPos('canny_low_threshold', 'lane_detect_window')
        canny_high_threshold = cv2.getTrackbarPos('canny_high_threshold', 'lane_detect_window')
        rho = cv2.getTrackbarPos('rho', 'lane_detect_window')
        theta_deg = cv2.getTrackbarPos('theta_deg', 'lane_detect_window')
        threshold = cv2.getTrackbarPos('threshold', 'lane_detect_window')
        min_line_len = cv2.getTrackbarPos('min_line_len', 'lane_detect_window')
        max_line_gap = cv2.getTrackbarPos('max_line_gap', 'lane_detect_window')

        # Assert smooth_kernel size is even
        if smooth_kernel_size % 2 == 0:
            smooth_kernel_size += 1

        # Running lane detector on all images
        frame_result_list.clear()
        for image in test_images:
            curr_result = cv_lane_detector.line_extraction_pipeline(image.copy(), pipeline_step,
                                                                    smooth_kernel_size,
                                                                    canny_low_threshold, canny_high_threshold,
                                                                    rho, theta_deg, threshold,
                                                                    min_line_len, max_line_gap)

            curr_result_resize = cv2.resize(curr_result, (int(image.shape[1]/2.0), int(image.shape[0]/2.0)))  # Resize image

            frame_result_list.append(curr_result_resize)

        # Concatenate result on two rows for visualization
        final_frame1 = cv2.hconcat( (frame_result_list[0], frame_result_list[1], frame_result_list[2]) )
        final_frame2 = cv2.hconcat( (frame_result_list[3], frame_result_list[4], frame_result_list[5]) )

        final_frame = cv2.vconcat((final_frame1, final_frame2))

        cv2.imshow('lane_detect_window', final_frame)

    cv2.destroyAllWindows()

    print("Thanks for using Lane detection tuning app")
    print("Your final parameters are :")

    print("smooth_kernel_size : ", smooth_kernel_size)
    print("canny_low_threshold : ", canny_low_threshold)
    print("canny_high_threshold : ", canny_high_threshold)
    print("rho : ", rho)
    print("theta_deg : ", theta_deg)
    print("threshold : ", threshold)
    print("min_line_len : ", min_line_len)
    print("max_line_gap : ", max_line_gap)

    print("Press any button to exit...")
    input()


if __name__=='__main__':
    main()