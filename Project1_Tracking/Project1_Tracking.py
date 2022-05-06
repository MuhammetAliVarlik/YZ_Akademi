# pip install youtube-dl==2020.12.2
import cv2
import pafy
import sys


class Tracker:
    def __init__(self, url):
        def timeframe(hour=0, minute=0, second=0, framerate=30):
            self.hour = hour
            specific_frame = (self.hour * 3600 + minute * 60 + second) * framerate
            return int(specific_frame)

        self.video = pafy.new(url)
        self.best = self.video.getbest(preftype="mp4")
        self.tracker_MIL = cv2.TrackerMIL_create()
        self.tracker_KCF = cv2.TrackerKCF_create()
        self.tracker_CSRT = cv2.TrackerCSRT_create()
        self.tracker_Median = cv2.legacy.TrackerMedianFlow_create()
        self.tracker_Boosting = cv2.legacy.TrackerBoosting_create()
        self.tracker_GOTURN = cv2.legacy.TrackerMOSSE_create()
        self.capture = cv2.VideoCapture(self.best.url)
        self.total_frame = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.frame_rate = self.capture.get(cv2.CAP_PROP_FPS)
        self.s_hour, self.s_minute, self.s_second = 0, 0, 2
        self.e_hour, self.e_minute, self.e_second = 0, 0, 18
        self.starting_frame_number = timeframe(hour=self.s_hour, minute=self.s_minute, second=self.s_second,
                                               framerate=self.frame_rate)
        self.ending_frame_number = timeframe(hour=self.e_hour, minute=self.e_minute, second=self.e_second,
                                             framerate=self.frame_rate)
        self.capture.set(1, self.starting_frame_number)
        self.frames = 0
        if not self.capture.isOpened():
            print("Could not open video")
            sys.exit()
        self.ret, self.frame = self.capture.read()
        if not self.ret:
            print('Cannot read video file')
            sys.exit()
        self.bbox = (335, 159, 28, 73)
        self.tracker_MIL.init(self.frame, self.bbox)
        self.tracker_KCF.init(self.frame, self.bbox)
        self.tracker_CSRT.init(self.frame, self.bbox)
        self.tracker_Boosting.init(self.frame, self.bbox)
        self.tracker_GOTURN.init(self.frame, self.bbox)
        self.Track()

    def Track(self):
        while True:
            self.ret, self.frame = self.capture.read()
            timer = cv2.getTickCount()
            self.success_MIL, self.bbox_MIL = self.tracker_MIL.update(self.frame)
            self.success_KCF, self.bbox_KCF = self.tracker_KCF.update(self.frame)
            self.success_CSRT, self.bbox_CSRT = self.tracker_CSRT.update(self.frame)
            self.success_Median, self.bbox_Median = self.tracker_Median.update(self.frame)
            self.success_Boosting, self.bbox_Boosting = self.tracker_Boosting.update(self.frame)
            self.success_GOTURN, self.bbox_GOTURN = self.tracker_GOTURN.update(self.frame)
            self.fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

            if self.success_MIL:
                p1 = (int(self.bbox_MIL[0]), int(self.bbox_MIL[1]))
                p2 = (int(self.bbox_MIL[0] + self.bbox_MIL[2]), int(self.bbox_MIL[1] + self.bbox_MIL[3]))
                cv2.rectangle(self.frame, p1, p2, (0, 0, 255), 2, 1)
                cv2.putText(self.frame, "MIL is red one", (10, 320),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            else:
                cv2.putText(self.frame, "MIL could not follow", (10, 320),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

            if self.success_CSRT:
                p1 = (int(self.bbox_CSRT[0]), int(self.bbox_CSRT[1]))
                p2 = (int(self.bbox_CSRT[0] + self.bbox_CSRT[2]), int(self.bbox_CSRT[1] + self.bbox_CSRT[3]))
                cv2.rectangle(self.frame, p1, p2, (255, 0, 0), 2, 1)
                cv2.putText(self.frame, "CSRT is blue one", (10, 290),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
            else:
                cv2.putText(self.frame, "CSRT could not follow", (10, 290),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)

            if self.success_KCF:
                p1 = (int(self.bbox_KCF[0]), int(self.bbox_KCF[1]))
                p2 = (int(self.bbox_KCF[0] + self.bbox_KCF[2]), int(self.bbox_KCF[1] + self.bbox_KCF[3]))
                cv2.rectangle(self.frame, p1, p2, (0, 255, 0), 2, 1)
                cv2.putText(self.frame, "KCF is green one", (10, 350),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            else:
                cv2.putText(self.frame, "KCF could not follow", (10, 350),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            if self.success_Median:
                p1 = (int(self.bbox_Median[0]), int(self.bbox_Median[1]))
                p2 = (int(self.bbox_Median[0] + self.bbox_Median[2]), int(self.bbox_Median[1] + self.bbox_Median[3]))
                cv2.rectangle(self.frame, p1, p2, (0, 0, 0), 2, 1)
                cv2.putText(self.frame, "MedianFlow is black one", (10, 260),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
            else:
                cv2.putText(self.frame, "MedianFlow could not follow", (10, 260),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)

            if self.success_Boosting:
                p1 = (int(self.bbox_Boosting[0]), int(self.bbox_Boosting[1]))
                p2 = (
                int(self.bbox_Boosting[0] + self.bbox_Boosting[2]), int(self.bbox_Boosting[1] + self.bbox_Boosting[3]))
                cv2.rectangle(self.frame, p1, p2, (0, 245, 233), 2, 1)
                cv2.putText(self.frame, "Boosting is yellow one", (10, 230),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 245, 233), 2)
            else:
                cv2.putText(self.frame, "Boosting could not follow", (10, 230),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 245, 233), 2)

            if self.success_GOTURN:
                p1 = (int(self.bbox_GOTURN[0]), int(self.bbox_GOTURN[1]))
                p2 = (int(self.bbox_GOTURN[0] + self.bbox_GOTURN[2]), int(self.bbox_GOTURN[1] + self.bbox_GOTURN[3]))
                cv2.rectangle(self.frame, p1, p2, (196, 0, 245), 2, 1)
                cv2.putText(self.frame, "MOSSE is pink one", (10, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (196, 0, 245), 2)
            else:
                cv2.putText(self.frame, "MOSSE could not follow", (10, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (196, 0, 245), 2)

            cv2.putText(self.frame, "Frame:" + str(int(self.frames)), (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
            cv2.putText(self.frame, "FPS : " + str(int(self.fps)), (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
            scale_percent = 200  # percent of original size
            self.width = int(self.frame.shape[1] * scale_percent / 100)
            self.height = int(self.frame.shape[0] * scale_percent / 100)
            dim = (self.width, self.height)

            cv2.imshow('KCF', self.frame)

            self.frames += 1
            if self.frames == self.ending_frame_number: break
            k = cv2.waitKey(1) & 0xff
            if k == 27: break

        self.video.release()
        cv2.destroyAllWindows()


url_Bolt = "https://www.youtube.com/watch?v=3nbjhpcZ9_g"
tracking = Tracker(url_Bolt)
tracking.Track()
