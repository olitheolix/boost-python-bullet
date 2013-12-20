#ifndef BT_BOOST_WRAPPER_HW
#define BT_BOOST_WRAPPER_HW

#pragma GCC diagnostic ignored "-Wunused-variable"
#pragma GCC diagnostic ignored "-Wreorder"

#include <boost/python.hpp>
#include "btBoostLinearMath.hpp"


const char* hello_world()
{
    return "Hello world";
}


BOOST_PYTHON_MODULE(bullet)
{
    using namespace boost::python;

    def("hello_world", &hello_world);

    defineLinearMath();
}

#endif // BT_BOOST_WRAPPER_HW