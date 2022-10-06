#include "stream.hpp"

vector<string> capture_source = {
    "/home/dellpb/Pictures/3dp/data/video/1.mp4",
    "/home/dellpb/Pictures/3dp/data/video/2.mp4",
    "/home/dellpb/Pictures/3dp/data/video/3.mp4",
    "/home/dellpb/Pictures/3dp/data/video/4.mp4",
    "/home/dellpb/Pictures/3dp/data/video/5.mp4"
};


std::vector<cv::Mat> _vecMat;
VideoStreamer cam_streamer(capture_source);

int main()
{

    auto CAMERAS = [](VideoStreamer &cam_streamer , vector<string> capture_source){

        while (true){
 
        }
    };

    auto AIMODEL = [](VideoStreamer &cam_streamer , vector<string> capture_source){

        while(true){

        }
        
    };

    auto SCREENS = [](VideoStreamer &cam_streamer , vector<string> capture_source){
        while(true){
 
        }
    };

  //threads
  thread t1(std::thread(CAMERAS, std::ref(cam_streamer),  std::ref(capture_source) ));
  thread t2(std::thread(AIMODEL, std::ref(cam_streamer),  std::ref(capture_source) ));
  thread t3(std::thread(SCREENS, std::ref(cam_streamer),  std::ref(capture_source) ));
  t1.join();
  t2.join();
  t3.join();

  //std::this_thread::sleep_for(std::chrono::milliseconds(1000));
  return 0;

}
