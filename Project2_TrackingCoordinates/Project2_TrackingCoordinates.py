# pip install youtube-dl==2020.12.2
# pip install pafy
# please install these libraries before using
# we have added the necessary libraries. opencv for image processing. pafy to use video from youtube.
import cv2
import pafy
import sys


class Tracker:
    # Tracker class gets url in initialization. It renders video in this url with opencv
    def __init__(self, url, start_hour, start_minute, start_second):
        # Function to find the frame number in the nth second/minute/hour
        def timeframe(hour=0, minute=0, second=0, framerate=30):
            specific_frame = (hour * 3600 + minute * 60 + second) * framerate
            return int(specific_frame)

        # Clear the contents of the text file the first time the application starts
        with open("frames.txt", "w") as file:
            file.write("")
            file.close()

        # we got the video from the url we gave
        self.video = pafy.new(url)
        self.best = self.video.getbest(preftype="mp4")
        # We included opencv's KCF Tracker method
        self.tracker_KCF = cv2.TrackerKCF_create()
        self.capture = cv2.VideoCapture(self.best.url)
        self.total_frame = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.frame_rate = self.capture.get(cv2.CAP_PROP_FPS)
        self.s_hour, self.s_minute, self.s_second = start_hour, start_minute, start_second
        # Frame number at the time entered
        self.starting_frame_number = timeframe(hour=self.s_hour, minute=self.s_minute, second=self.s_second,
                                               framerate=self.frame_rate)
        # We start the video from the entered time
        self.capture.set(1, self.starting_frame_number)
        # Frame counter
        self.frames = 0
        # Checking for errors in the video
        if not self.capture.isOpened():
            print("Could not open video please try again")
            sys.exit()
        self.ret, self.frame = self.capture.read()
        if not self.ret:
            print('Cannot read video file')
            sys.exit()
        # Marking the object that we will follow at the beginning
        # Select the app to follow with Roi
        self.bbox = cv2.selectROI(self.frame, False)
        cv2.destroyWindow("ROI selector")
        # Initializing the KCF tracker
        self.tracker_KCF.init(self.frame, self.bbox)
        # We called the track function
        self.Track()

    def Track(self):
        while True:
            # we get new image
            self.ret, self.frame = self.capture.read()
            # timer for fps
            timer = cv2.getTickCount()
            success_KCF, bbox_KCF = self.tracker_KCF.update(self.frame)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
            # update bbox if detection happens
            if success_KCF:
                p1 = (int(bbox_KCF[0]), int(bbox_KCF[1]))
                p2 = (int(bbox_KCF[0] + bbox_KCF[2]), int(bbox_KCF[1] + bbox_KCF[3]))
                # mark object with rectangle
                cv2.rectangle(self.frame, p1, p2, (0, 255, 0), 2, 1)
                # print object coordinates w and h values
                cv2.putText(self.frame, "({},{})".format(str(int(bbox_KCF[0])), str(int(bbox_KCF[1]))),
                            (int(bbox_KCF[0]) - 50, int(bbox_KCF[1])),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (255, 0, 0), 1)
                cv2.circle(self.frame, (int(bbox_KCF[0]), int(bbox_KCF[1])), 0, (255, 0, 0), 5)

                cv2.line(self.frame, (int(bbox_KCF[0]), int(bbox_KCF[1] - 5)),
                         (int(bbox_KCF[0] + bbox_KCF[2]), int(bbox_KCF[1] - 5)), (0, 0, 0), 1)
                cv2.line(self.frame, (int(bbox_KCF[0] + bbox_KCF[2] + 5), int(bbox_KCF[1])),
                         (int(bbox_KCF[0] + bbox_KCF[2] + 5), int(bbox_KCF[1] + bbox_KCF[3])), (0, 0, 0), 1)

                cv2.putText(self.frame, "w=" + str(int(bbox_KCF[2])),
                            (int((bbox_KCF[0] + bbox_KCF[0] + bbox_KCF[2]) / 2) - 20, int((bbox_KCF[1] - 10))),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 0, 0), 1)
                cv2.putText(self.frame, "h=" + str(int(bbox_KCF[3])),
                            (int(bbox_KCF[0] + bbox_KCF[2]) + 10, int((bbox_KCF[1] + bbox_KCF[1] + bbox_KCF[3]) / 2)),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 0, 0), 1)
                with open("frames.txt", "a+") as file:
                    file.seek(0)
                    data = file.read()
                    if len(data) > 0:
                        file.write("\n")
                        # add coordinate values to text file
                    file.write(
                        "{}={},{},{},{}".format(self.frames, int(bbox_KCF[0]), int(bbox_KCF[1]), int(bbox_KCF[2]),
                                                int(bbox_KCF[3])))
                    file.close()
            else:
                # If the object is lost, mark again. Close any open windows and activate the roi.
                cv2.destroyAllWindows()
                self.bbox = cv2.selectROI(self.frame, False)
                cv2.destroyWindow("ROI selector")
                # Rebuild the tracker
                self.tracker_KCF = cv2.TrackerKCF_create()
                # Reinitialize the tracker
                self.tracker_KCF.init(self.frame, self.bbox)

            cv2.putText(self.frame, "Frame:" + str(int(self.frames)), (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
            cv2.putText(self.frame, "FPS : " + str(int(fps)), (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
            # Enlarge screen
            scale_percent = 100
            width = int(self.frame.shape[1] * scale_percent / 100)
            height = int(self.frame.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(self.frame, dim, interpolation=cv2.INTER_AREA)
            cv2.imshow('KCF', resized)
            # increase frame number
            self.frames += 1
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                break
        self.capture.release()
        cv2.destroyAllWindows()


# https://www.youtube.com/watch?v=3nbjhpcZ9_g


try:
    print("Algorithm for making a tracking algorithm on any video selected on Youtube.")
    print(
        "Enter the video url in the first input and the time in hours, minutes, seconds to start the tracking "
        "algorithm, leaving a space in the second input.")
    print("\nSample input:\nhttps://www.youtube.com/watch?v=3nbjhpcZ9_g\n0 0 5    ---->0th hour 0th minute 5th second")
    video_url = str(input("Enter the video url:"))

    hms = list(
        map(int, input("Select the time for the tracking algorithm to start:").strip().split(

        )))
    error = 0
    # Check that the entered time values are correct
    if 0 > hms[0] or hms[0] > 24:
        print("The hour value must be between 0 and 24! Please try again.")
        error = 1
    if 0 > hms[1] or hms[1] > 60:
        print("The minute value must be between 0 and 60! Please try again.")
        error = 1
    if 0 > hms[2] or hms[2] > 60:
        print("The second value must be between 0 and 60! Please try again.")
        error = 1
    # if there is no error with time inputs
    if error == 0:
        # define tracking object
        tracking = Tracker(video_url, int(hms[0]), int(hms[1]), int(hms[2]))
        # Call the Track function of the tracking object
        tracking.Track()
except cv2.error:
    print("Exited the video")
else:
    print("Error!!Please try again")
