# pip install pupil-apriltags
# pupil-apriltag only works with python 3.6 and 3.7

from pupil_apriltags import Detector
import cv2

# Get the Image
img = cv2.imread("apriltags.png")
# Convert BGR to Gray
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# AprilTag family 'tag36h11'
at_detector = Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)
tags = at_detector.detect(img_gray, estimate_tag_pose=False, camera_params=None, tag_size=None)

# for every tag detection
for apr in tags:
    # calculate corners
    (A, B, C, D) = apr.corners
    ptA = (int(A[0]), int(A[1]))
    ptB = (int(B[0]), int(B[1]))
    ptC = (int(C[0]), int(C[1]))
    ptD = (int(D[0]), int(D[1]))
    # we draw a rectangle around the detected aprilTag
    cv2.line(img, ptA, ptB, (0, 255, 0), 2)
    cv2.line(img, ptB, ptC, (0, 255, 0), 2)
    cv2.line(img, ptC, ptD, (0, 255, 0), 2)
    cv2.line(img, ptD, ptA, (0, 255, 0), 2)
    # center of aprilTag
    (cntX, cntY) = (int(apr.center[0]), int(apr.center[1]))
    cv2.circle(img, (cntX, cntY), 5, (0, 0, 255), -1)
    # we read the aprilTag
    tagID = str(apr.tag_id)
    cv2.putText(img, tagID, (ptA[0], ptA[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
