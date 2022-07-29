# pip install pupil-apriltags
# pupil-apriltag only works with python 3.6 and 3.7

from pupil_apriltags import Detector
import cv2
import math

# Get the frames from webcam
vid = cv2.VideoCapture(0)

# tag_size is for calculating distance
tag_size = 15.5
# tag_size=1.9

# experimental value of focal length (in Pixels)
focal_length = 619.35

while True:
    # Capture the video frame by frame
    ret, img = vid.read()
    # Convert BGR to Gray
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # AprilTag family 'tag36h11'
    at_detector = Detector(families='tag36h11',
                           nthreads=1,
                           quad_decimate=2.0,
                           quad_sigma=0.0,
                           refine_edges=1,
                           decode_sharpening=0.05,
                           debug=0)
    if at_detector:
        tags = at_detector.detect(img_gray, estimate_tag_pose=False, camera_params=None, tag_size=None)
        # for every tag detection
        for apr in tags:
            # calculate corners
            (A, B, C, D) = apr.corners
            ptA = (int(A[0]), int(A[1]))
            ptB = (int(B[0]), int(B[1]))
            ptC = (int(C[0]), int(C[1]))
            ptD = (int(D[0]), int(D[1]))

            # with Pythagoras Theorem we calculate the distance between A and B point (in Pixels)
            # we know the real distance so with this we can calculate focal length
            distancePx = int(math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2))

            # we draw a rectangle around the detected aprilTag
            cv2.line(img, ptA, ptB, (255, 0, 0), 2)
            cv2.line(img, ptB, ptC, (255, 0, 0), 2)
            cv2.line(img, ptC, ptD, (0, 255, 0), 2)
            cv2.line(img, ptD, ptA, (0, 255, 0), 2)

            # with geometric similarity
            distance = tag_size * focal_length / distancePx
            distanceCM = str(int(distance)) + "cm"
            # center of aprilTag
            (cntX, cntY) = (int(apr.center[0]), int(apr.center[1]))
            cv2.circle(img, (cntX, cntY), 5, (0, 0, 255), -1)
            # we read the aprilTag
            tagID = str(apr.tag_id)
            cv2.putText(img, tagID, (ptA[0] + 15, ptA[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.putText(img, distanceCM, (ptB[0] + 15, ptB[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
