"""
Application to classify shapes
"""
import cv2

# import the image
img = cv2.imread("YZ.PNG")
# turn bgr image to gray
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# threshold for getting better results
ret, thresh = cv2.threshold(img_gray, 170, 255, cv2.THRESH_BINARY)
# findContours finds the shell of shapes and classifies them hierarchically
cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# for each shape in cnts array
for cnt in cnts:
    # use approxPolyDb to simplify polylines (RDP based)
    approx = cv2.approxPolyDP(cnt, 0.031 * cv2.arcLength(cnt, True), True)
    x = approx.ravel()[0]
    y = approx.ravel()[1]
    # classify and paint
    if len(approx) == 3:
        color = (0, 255, 255)
        image = cv2.fillPoly(img, [approx], color)
        cv2.putText(img, "Triangle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    elif len(approx) == 4:
        color = (200, 0, 1)
        image = cv2.fillPoly(img, [approx], color)
        cv2.putText(img, "Rectangle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    elif len(approx) == 5:
        color = (178, 104, 254)
        image = cv2.fillPoly(img, [approx], color)
        cv2.putText(img, "Pentagon", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    elif len(approx) == 6:
        color = (0, 69, 255)
        image = cv2.fillPoly(img, [approx], color)
        cv2.putText(img, "Hexagon", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    if 6 < len(approx):
        color = (1, 255, 0)
        ((x1, y1), radius) = cv2.minEnclosingCircle(cnt)
        M = cv2.moments(cnt)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 5:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(img, (int(x1), int(y1)), int(radius), color, -1)
        cv2.putText(img, "Circle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
hierarchy = hierarchy[0]  # get the actual inner list of hierarchy descriptions

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
