cmake_minimum_required(VERSION 3.8)
project(fosa_mini_robot)

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  urdf
  launch
  worlds
  config
  scripts
  DESTINATION share/${PROJECT_NAME}
)

ament_package()