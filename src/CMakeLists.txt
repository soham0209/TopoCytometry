cmake_minimum_required(VERSION 3.5)
project(TopoCytometry)
set(CMAKE_CXX_STANDARD 11)
include_directories("./include")
link_directories(${CMAKE_SOURCE_DIR}/ann_1.1.2/lib/)
set(HEADERS PointSet.h LongVector.h)
add_executable(Gen_vert_weight Gen_vert_weight.cpp PointSet.cpp ${HEADERS})
target_link_libraries(Gen_vert_weight ANN)


