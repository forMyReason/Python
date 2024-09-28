cmake_minimum_required(VERSION 3.4)
project(pybind11_example)

set(PYTHON_EXECUTABLE "C:/Users/79160/AppData/Local/Programs/Python/Python312/python.exe")
set(PYTHON_INCLUDE_DIR "C:/Users/79160/AppData/Local/Programs/Python/Python312/include")

add_subdirectory(extern/pybind11)
pybind11_add_module(example source.cpp)
# 编译成一个库叫pybind11_example，源文件是source.cpp

# Copy the pyd file to the current directory
add_custom_command(
        TARGET ${PROJECT_NAME}  POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_BINARY_DIR}/$<CONFIGURATION> ${CMAKE_CURRENT_LIST_DIR}
        )