#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/aruco.hpp>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/video.hpp>

using namespace cv;
using namespace std;
int main()
{
	try
	{
		//We created inputImage object from Mat class
		Mat inputImage;

		//We added an image to the inputImage object with the imread function
		inputImage = imread("img/apriltags.png", 1);
		if (inputImage.empty())
			return 0;
		// Integer variable with id's written
		vector<int> markerIds;

		// Array with corner points
		vector<vector<Point2f>> markerCorners, rejectedCandidates;

		// 36h11 class will be detected
		Ptr<aruco::DetectorParameters> parameters = aruco::DetectorParameters::create();
		Ptr<aruco::Dictionary> dictionary = aruco::getPredefinedDictionary(aruco::DICT_APRILTAG_36h11);
		aruco::detectMarkers(inputImage, dictionary, markerCorners, markerIds, parameters, rejectedCandidates);
		Mat outputImage = inputImage.clone();

		// the vertices and perimeters of the detected 36h11s are plotted
		aruco::drawDetectedMarkers(outputImage, markerCorners, markerIds);
		imshow("IMG", outputImage);
		waitKey(0);
	}
	catch (cv::Exception& e)
	{
		cerr << e.msg << endl; // output exception message
	}
	return 0;
}