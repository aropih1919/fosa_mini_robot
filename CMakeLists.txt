cmake_minimum_required(VERSION 3.8)
project(parc2026_mini_robot)

find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)

# Installation des dossiers de ressources (URDF, launch, mondes, config)
install(DIRECTORY
  launch
  urdf
  worlds
  config
  DESTINATION share/${PROJECT_NAME}
)

# Installation du script Python en tant qu'exécutable ROS2
install(PROGRAMS
  scripts/obstacle_avoidance.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()