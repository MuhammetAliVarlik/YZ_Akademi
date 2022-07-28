from pupil_apriltags import Detector
import cv2

img = cv2.imread("apriltags.png")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
at_detector = Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)
tags = at_detector.detect(img_gray, estimate_tag_pose=False, camera_params=None, tag_size=None)
for apr in tags:
    (A, B, C, D) = apr.corners
    ptA = (int(A[0]), int(A[1]))
    ptB = (int(B[0]), int(B[1]))
    ptC = (int(C[0]), int(C[1]))
    ptD = (int(D[0]), int(D[1]))
    cv2.line(img, ptA, ptB, (0, 255, 0), 2)
    cv2.line(img, ptB, ptC, (0, 255, 0), 2)
    cv2.line(img, ptC, ptD, (0, 255, 0), 2)
    cv2.line(img, ptD, ptA, (0, 255, 0), 2)
    (cntX, cntY) = (int(apr.center[0]), int(apr.center[1]))
    cv2.circle(img, (cntX, cntY), 5, (0, 0, 255), -1)
    tagID = str(apr.tag_id)
    cv2.putText(img, tagID, (ptA[0], ptA[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
