cmake_minimum_required(VERSION 3.8)
project(separable_jaws_description)

find_package(ament_cmake REQUIRED)

install(DIRECTORY config meshes launch urdf
        DESTINATION share/${PROJECT_NAME}
)

ament_package()
