#include </opt/jderobot/include/jderobot/types/image.h>

#include "caminterface.hpp"

namespace camViz {
	CameraClient* getCameraClient(int argc, char** argv, int server, std::string topic,std::string nodeName);

}
