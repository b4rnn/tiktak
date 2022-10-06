#include "gala.hpp"

vector<string> capture_source = {
    "/home/dellpb/Pictures/3dp/data/video/1.mp4",
    "/home/dellpb/Pictures/3dp/data/video/2.mp4",
    "/home/dellpb/Pictures/3dp/data/video/3.mp4",
    "/home/dellpb/Pictures/3dp/data/video/4.mp4",
    "/home/dellpb/Pictures/3dp/data/video/5.mp4"
};

class XDELETE
{
  public :
    Redis *_redis = new Redis("tcp://127.0.0.1:6379?keep_alive=true&socket_timeout=100ms&connect_timeout=100ms");
    void operator()(string &msg) const
    { 
        /*
        int pos = msg.find(":");
        std::string key = msg.substr(0 , pos);
        std::string id = msg.substr(pos + 1);
        std::cout << "Key " << key <<" "<<"Id " << id << "\n";
        _redis->xdel(key, id);
        */
    }
};

std::vector<cv::Mat> _vecMat;
VideoStreamer cam_streamer(capture_source);

int main()
{   
    
    boost::signals2::signal<void(string &msg)> sig;
    sig.connect(XDELETE());

    auto PUB_GSM = [](VideoStreamer &cam_streamer , vector<string> capture_source){

        while (true){
 
        }
    };

    auto SUB_GSM = [](VideoStreamer &cam_streamer , vector<string> capture_source){

        while (true){
 
        }
    };

    auto PUB_PERSON = [](VideoStreamer &cam_streamer , vector<string> capture_source){

        while(true){

        }
        
    };

    auto SUB_PERSON = [](VideoStreamer &cam_streamer , vector<string> capture_source){

        while(true){

        }
        
    };

    auto PUB_PARKING = [](VideoStreamer &cam_streamer , vector<string> capture_source){

        while(true){

        }
        
    };

    auto SUB_PARKING = [](VideoStreamer &cam_streamer , vector<string> capture_source){

        while(true){

        }
        
    };

    auto PUB_WEATHER = [](VideoStreamer &cam_streamer , vector<string> capture_source){
        while(true){
 
        }
    };

    auto SUB_WEATHER = [](VideoStreamer &cam_streamer , vector<string> capture_source){
        while(true){
 
        }
    };

    auto PUB_TRAFFIC = [](VideoStreamer &cam_streamer , vector<string> capture_source){
        while(true){
 
        }
    };

    auto SUB_TRAFFIC = [](VideoStreamer &cam_streamer , vector<string> capture_source){
        while(true){
 
        }
    };

  //threads
  /*
  thread t1(std::thread(PUB_GSM, std::ref(cam_streamer),  std::ref(capture_source) ));
  thread t2(std::thread(SUB_GSM, std::ref(cam_streamer),  std::ref(capture_source) ));
  thread t3(std::thread(PUB_PERSON,std::ref(cam_streamer),std::ref(capture_source) ));
  thread t4(std::thread(SUB_PERSON,std::ref(cam_streamer),std::ref(capture_source) ));
  thread t5(std::thread(PUB_PARKING,std::ref(cam_streamer),std::ref(capture_source) ));
  thread t6(std::thread(SUB_PARKING,std::ref(cam_streamer),std::ref(capture_source) ));
  thread t7(std::thread(PUB_WEATHER,std::ref(cam_streamer),std::ref(capture_source) ));
  thread t8(std::thread(SUB_WEATHER,std::ref(cam_streamer),std::ref(capture_source) ));
  thread t9(std::thread(PUB_TRAFFIC,std::ref(cam_streamer),std::ref(capture_source) ));
  thread t10(std::thread(SUB_TRAFFIC,std::ref(cam_streamer),std::ref(capture_source)));
  t1.join();
  t2.join();
  t3.join();
  t4.join();
  t5.join();
  t6.join();
  t7.join();
  t8.join();
  t9.join();
  t10.join();
  */
  XDELETE xdelete;
  string s="DELETE USED TRAFIC FILES";
  boost::thread t3((XDELETE()),boost::move(s));
  thread t1(std::thread(PUB_TRAFFIC,std::ref(cam_streamer),std::ref(capture_source) ));
  thread t2(std::thread(SUB_TRAFFIC,std::ref(cam_streamer),std::ref(capture_source) ));
  t1.join();
  t2.join();
  t3.join();
   
        
  //std::this_thread::sleep_for(std::chrono::milliseconds(1000));
  return 0;

}
