#include <pybind11/pybind11.h>

// Define a Cpp function for python to call
int _ADD(int i, int j) {
    return i + j;
}

// Define a Python module
PYBIND11_MODULE(example, m)       // module name is "example"
{
    m.doc() = "pybind11 example plugin"; // optional module docstring

    // Bind the Cpp function to Python
    m.def("add", &_ADD, "A function which adds two numbers");
    // "add" is the name of the function in Python
    // &_ADD is the Cpp function
    // "A function which adds two numbers" is the docstring
}