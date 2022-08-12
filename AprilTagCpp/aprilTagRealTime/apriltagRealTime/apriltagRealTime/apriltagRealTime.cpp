#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/aruco.hpp>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/video.hpp>
#include <cmath>
#include <cstdlib>

using namespace cv;
using namespace std;

int main()
{
	try
	{
		// Get the frames from webcam
		VideoCapture cap(0);

		// tag_size is for calculating distance
		float tag_size = 15.5;
		//float tag_size=1.9;

		// Check if camera opened successfully
		float focal_length = 619.35;

		if (!cap.isOpened()) {
			cout << "Error opening video stream or file" << endl;
			return -1;
		}

		while (1)
		{
			Mat frame;
			// Capture the video frame by frame
			cap >> frame;

			// If the frame is empty, break immediately
			if (frame.empty())
				break;

			// vector holding int markerIds
			vector<int> markerIds;

			// vector holding 2D float corner values
			vector<vector<Point2f>> markerCorners, rejectedCandidates;

			// get the parameters
			Ptr<aruco::DetectorParameters> parameters = aruco::DetectorParameters::create();

			// AprilTag family 'tag36h11'
			Ptr<aruco::Dictionary> dictionary = aruco::getPredefinedDictionary(aruco::DICT_APRILTAG_36h11);
			aruco::detectMarkers(frame, dictionary, markerCorners, markerIds, parameters, rejectedCandidates);

			// copy frame to manipulate it
			Mat outputImage = frame.clone();

			for (int i = 0; i < markerCorners.size(); i++)
			{

				// get corner information for distance calculation
				Point ptA(int(markerCorners[i][0].x), int(markerCorners[i][0].y));
				Point ptB(int(markerCorners[i][1].x), int(markerCorners[i][1].y));
				Point ptC(int(markerCorners[i][2].x), int(markerCorners[i][2].y));
				Point ptD(int(markerCorners[i][3].x), int(markerCorners[i][3].y));

				// with Pythagoras Theorem we calculate the distance between A and B point (in Pixels)
				// we know the real distance so with this we can calculate focal length
				float A = (float)pow(abs(ptA.x - ptB.x), 2);
				float B = (float)pow(abs(ptA.y - ptB.y), 2);
				float distancePx = (float)sqrt(A + B);
				// with geometric similarity we can calculate distance
				float distance = (float)(tag_size * focal_length / distancePx);
				string disttxt = to_string((int)distance) + " cm";

				// we read the aprilTag
				string id = "id= " + to_string(markerIds[0]);

				//put text to the image
				putText(outputImage, disttxt, cv::Point(ptA.x + 15, ptA.y - 15), cv::FONT_HERSHEY_DUPLEX, 0.5, cv::Scalar(0, 0, 255), 0.5, false);
				putText(outputImage, id, Point(ptB.x + 15, ptB.y - 15), cv::FONT_HERSHEY_DUPLEX, 0.5, cv::Scalar(0, 0, 255), 0.5, false);
				int thickness = 2;

				// we draw a rectangle around the detected aprilTag
				line(outputImage, ptA, ptB, Scalar(255, 0, 0), thickness, LINE_8);
				line(outputImage, ptB, ptC, Scalar(255, 0, 0), thickness, LINE_8);
				line(outputImage, ptC, ptD, Scalar(0, 255, 0), thickness, LINE_8);
				line(outputImage, ptD, ptA, Scalar(0, 255, 0), thickness, LINE_8);

				cout << disttxt << endl;
			}

			// draw markers
			imshow("IMG", outputImage);

			char c = (char)waitKey(25);
			if (c == 27)
				break;
		}
		cap.release();

		// closes all the frames
		destroyAllWindows();
	}
	catch (cv::Exception& e)
	{
		cerr << e.msg << endl; // output exception message
	}
	return 0;
}