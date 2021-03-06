#include "CollisionDispatcher.hpp"

#include <boost/python.hpp>
#include <boost/shared_ptr.hpp>

using namespace boost::python;

btCollisionDispatcher*
make_CollisionDispatcher(btCollisionConfiguration& config)
{
    return new btCollisionDispatcher(&config);
}

void defineCollisionDispatcher()
{
    enum_<btCollisionDispatcher::DispatcherFlags>("DispatcherFlags")
        .value("CD_STATIC_STATIC_REPORTED",
            btCollisionDispatcher::CD_STATIC_STATIC_REPORTED)
        .value("CD_USE_RELATIVE_CONTACT_BREAKING_THRESHOLD",
            btCollisionDispatcher::CD_USE_RELATIVE_CONTACT_BREAKING_THRESHOLD)
        .value("CD_DISABLE_CONTACTPOOL_DYNAMIC_ALLOCATION",
            btCollisionDispatcher::CD_DISABLE_CONTACTPOOL_DYNAMIC_ALLOCATION)
        .export_values()
    ;

    class_<btDispatcher, boost::noncopyable>("btDispatcher", no_init);

    class_<btCollisionDispatcher, bases<btDispatcher>, boost::noncopyable>
        ("btCollisionDispatcher", no_init)
        .def("__init__", make_constructor(&make_CollisionDispatcher))
        .add_property("flags",
            &btCollisionDispatcher::getDispatcherFlags,
            &btCollisionDispatcher::setDispatcherFlags)
    ;
}
