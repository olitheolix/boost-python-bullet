#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_dynamics.test_shapes
"""
from __future__ import unicode_literals, print_function, absolute_import

import unittest

import bullet


class ConvexHullTestCase(unittest.TestCase):
    def setUp(self):
        # Describe a cube
        self.points = (
            bullet.btVector3(-1, -1, -1),
            bullet.btVector3(-1, 1, -1),
            bullet.btVector3(-1, -1, 1),
            bullet.btVector3(-1, 1, 1),
            bullet.btVector3(1, 1, 1),
            bullet.btVector3(1, -1, 1),
            bullet.btVector3(1, -1, -1),
            bullet.btVector3(1, 1, -1)
        )
        self.points_arr = bullet.btVector3Array()
        for p in self.points:
            self.points_arr.append(p)

    def test_empty_ctor(self):
        self.hull = bullet.btConvexHullShape()

    def test_list_ctor(self):
        self.hull = bullet.btConvexHullShape(list(self.points))
        self.assertEquals(self.hull.num_points, len(self.points))

    def test_num_points(self):
        self.test_list_ctor()
        self.assertEquals(self.hull.num_points, self.hull.get_num_points())
        self.assertEquals(self.hull.num_points, len(self.points))

    def test_tuple_ctor(self):
        self.hull = bullet.btConvexHullShape(self.points)
        self.assertEquals(self.hull.num_points, len(self.points))

    def test_array_ctor(self):
        self.hull = bullet.btConvexHullShape(self.points_arr)
        self.assertEquals(self.hull.num_points, len(self.points))

    def test_add_point(self):
        self.test_empty_ctor()
        for p in self.points:
            self.hull.add_point(p)
        self.assertEquals(self.hull.num_points, len(self.points))

    def test_get_unscaled_points(self):
        self.test_list_ctor()
        unscaled_points = self.hull.get_unscaled_points()
        self.assertTrue(isinstance(unscaled_points, bullet.btVector3Array))
        for i in range(len(self.points)):
            self.assertEquals(unscaled_points[i], self.points[i])

    def test_get_scaled_point(self):
        self.test_list_ctor()
        for i in range(len(self.points)):
            point = self.hull.get_scaled_point(i)
            self.assertEquals(self.points[i], point)

    def tearDown(self):
        if hasattr(self, 'hull'):
            del self.hull
        del self.points


class PolyhedralConvexAabbCachingTestCase(unittest.TestCase):
    """
    We use btConvexHullShape to implicitly test abstract base classes
    that it inherits and implements
    """
    def setUp(self):
        # tolerance reflects the internal penetration tolerance
        self.tolerance = bullet.btVector3(0.04, 0.04, 0.04)
        # Describe a cube
        self.points = [
            bullet.btVector3(-1, -1, -1),
            bullet.btVector3(-1, 1, -1),
            bullet.btVector3(-1, -1, 1),
            bullet.btVector3(-1, 1, 1),
            bullet.btVector3(1, 1, 1),
            bullet.btVector3(1, -1, 1),
            bullet.btVector3(1, -1, -1),
            bullet.btVector3(1, 1, -1)
        ]
        self.hull = bullet.btConvexHullShape(self.points)

    def test_ctor(self):
        pass

    def test_get_nonvirtual_aabb(self):
        aabb_min = bullet.btVector3()
        aabb_max = bullet.btVector3()
        trans = bullet.btTransform.identity
        self.hull.recalc_local_aabb()
        self.hull.get_nonvirtual_aabb(trans, aabb_min, aabb_max, 0.00)
        self.assertEquals(aabb_min, self.points[0] - self.tolerance)
        self.assertEquals(aabb_max, self.points[4] + self.tolerance)

    def test_get_aabb(self):
        aabb_min = bullet.btVector3()
        aabb_max = bullet.btVector3()
        trans = bullet.btTransform.identity
        self.hull.recalc_local_aabb()
        self.hull.get_aabb(trans, aabb_min, aabb_max)
        self.assertEquals(aabb_min, self.points[0] - self.tolerance*2)
        self.assertEquals(aabb_max, self.points[4] + self.tolerance*2)

    def tearDown(self):
        del self.hull
        del self.points


class ConvexPolyhedronTestCase(unittest.TestCase):
    """
    Runtime tests for convecpolyhedron, lmited
    as it's a data transfer class
    """
    def setUp(self):
        self.cp = bullet.btConvexPolyhedron()
        # Describe a cube
        self.points = [
            bullet.btVector3(-1, -1, -1),
            bullet.btVector3(-1, 1, -1),
            bullet.btVector3(-1, -1, 1),
            bullet.btVector3(-1, 1, 1),
            bullet.btVector3(1, 1, 1),
            bullet.btVector3(1, -1, 1),
            bullet.btVector3(1, -1, -1),
            bullet.btVector3(1, 1, -1)
        ]
        self.points_arr = bullet.btVector3Array()
        for p in self.points:
            self.points_arr.append(p)

    def test_ctor(self):
        pass

    def test_initialize(self):
        self.cp.vertices = self.points_arr
        self.cp.initialize()
        self.assertTrue(self.cp.test_containment())

    def tearDown(self):
        del self.cp


class PolyhedralConvexTestCase(unittest.TestCase):
    """
    We use btConvexHullShape to implicitly test abstract base classes
    that it inherits and implements
    """
    def setUp(self):
        # Describe a cube
        self.points = [
            bullet.btVector3(-1, -1, -1),
            bullet.btVector3(-1, 1, -1),
            bullet.btVector3(-1, -1, 1),
            bullet.btVector3(-1, 1, 1),
            bullet.btVector3(1, 1, 1),
            bullet.btVector3(1, -1, 1),
            bullet.btVector3(1, -1, -1),
            bullet.btVector3(1, 1, -1)
        ]
        self.hull = bullet.btConvexHullShape(self.points)

    def test_ctor(self):
        pass

    def test_num_vertices(self):
        self.assertEquals(self.hull.num_vertices, 8)

    def test_num_edges(self):
        self.assertEquals(self.hull.num_edges, 8)

    def test_num_planes(self):
        self.assertEquals(self.hull.num_planes, 0)

    def test_is_inside(self):
        """
        is_inside is pure abstract and is never implemented in any class
        so we'll just assert it raises and move on
        """
        def _is_inside_call(vec, margin):
            self.hull.is_inside(vec, margin)
        self.assertRaises(_is_inside_call)

    def test_get_edge(self):
        pa = bullet.btVector3()
        pb = bullet.btVector3()
        self.hull.get_edge(0, pa, pb)
        self.assertEquals(pa, self.points[0])
        self.assertEquals(pb, self.points[1])

    def test_get_vertex(self):
        v = bullet.btVector3()
        for i in range(len(self.points)):
            self.hull.get_vertex(i, v)
            self.assertEquals(v, self.points[i])

    def test_get_plane(self):
        def _get_plane():
            normal = bullet.btVector3()
            support = bullet.btVector3()
            self.hull.get_plane(normal, support, 0)
        self.assertRaises(_get_plane)

    def tearDown(self):
        del self.hull
        del self.points


class ConvexInternalTestCase(unittest.TestCase):
    """
    We use btConvexHullShape to implicitly test abstract base classes
    that it inherits and implements
    """
    def setUp(self):
        # Describe a cube
        self.points = [
            bullet.btVector3(-1, -1, -1),
            bullet.btVector3(-1, 1, -1),
            bullet.btVector3(-1, -1, 1),
            bullet.btVector3(-1, 1, 1),
            bullet.btVector3(1, 1, 1),
            bullet.btVector3(1, -1, 1),
            bullet.btVector3(1, -1, -1),
            bullet.btVector3(1, 1, -1)
        ]
        self.hull = bullet.btConvexHullShape(self.points)
        self.v1 = bullet.btVector3(0, 0, 0)
        self.v2 = bullet.btVector3(0, 0, 0)
        self.v3 = bullet.btVector3(0, 0, 0)
        self.t1 = bullet.btTransform.identity

    def test_implicit_shape_dimensions(self):
        self.hull.implicit_shape_dimensions = bullet.btVector3(2, 2, 2)
        vec = self.hull.implicit_shape_dimensions
        self.assertEquals(vec, bullet.btVector3(2, 2, 2))

    def test_local_scaling(self):
        self.hull.local_scaling = bullet.btVector3(2, 2, 2)
        self.assertEquals(self.hull.local_scaling,
                          bullet.btVector3(2, 2, 2))
        self.hull.get_aabb_non_virtual(self.t1, self.v1, self.v2)
        self.assertNotEquals(self.v1, self.v3)
        self.v3 = bullet.btVector3(2.08, 2.08, 2.08)
        self.assertEquals(self.v1, -self.v3)
        self.assertEquals(self.v2, self.v3)

    def test_margin(self):
        self.hull.margin = 0.07
        self.assertEquals(self.hull.margin, 0.07)
        self.hull.get_aabb_non_virtual(self.t1, self.v1, self.v2)
        self.v3 = bullet.btVector3(1.11, 1.11, 1.11)
        self.assertEquals(self.v1, -self.v3)
        self.assertEquals(self.v2, self.v3)

    def test_aabb_non_virtual(self):
        self.hull.get_aabb_non_virtual(self.t1, self.v1, self.v2)
        self.v3 = bullet.btVector3(1.08, 1.08, 1.08)
        self.assertEquals(self.v1, -self.v3)
        self.assertEquals(self.v2, self.v3)

    def tearDown(self):
        del self.hull
        del self.points
        del self.t1
        del self.v3
        del self.v2
        del self.v1


class ConvexTestCase(unittest.TestCase):
    """
    We use btConvexHullShape to implicitly test abstract base classes
    that it inherits and implements
    """
    def setUp(self):
        # Describe a cube
        self.points = [
            bullet.btVector3(-1, -1, -1),
            bullet.btVector3(-1, 1, -1),
            bullet.btVector3(-1, -1, 1),
            bullet.btVector3(-1, 1, 1),
            bullet.btVector3(1, 1, 1),
            bullet.btVector3(1, -1, 1),
            bullet.btVector3(1, -1, -1),
            bullet.btVector3(1, 1, -1)
        ]
        self.hull = bullet.btConvexHullShape(self.points)
        self.v1 = bullet.btVector3(0, 0, 0)
        self.v2 = bullet.btVector3(0, 0, 0)
        self.v3 = bullet.btVector3(0, 0, 0)
        self.t1 = bullet.btTransform.identity

    def test_get_supporting_vertex(self):
        """Runtime tests only"""
        self.v2 = self.hull.local_get_supporting_vertex_without_margin(self.v1)
        self.assertGreater(self.v1.x, self.v2.x)
        self.assertGreater(self.v1.y, self.v2.y)
        self.assertGreater(self.v1.z, self.v2.z)
        self.v2 = self.hull.local_get_supporting_vertex_without_margin(self.v1)
        self.v3 = self.v2
        self.assertEquals(self.v2, bullet.btVector3(-1, -1, -1))
        self.v2 = \
            self.hull.local_get_supporting_vertex_without_margin_non_virtual(
                self.v1
            )
        self.assertEquals(self.v2, bullet.btVector3(-1, -1, -1))
        self.hull.local_get_support_vertex_non_virtual(self.v1)
        self.assertEquals(self.v2, self.v3)

    def test_margin(self):
        margin = self.hull.get_margin_non_virtual()
        self.assertTrue(isinstance(margin, float))
        m2 = self.hull.get_margin_non_virtual()
        self.assertEquals(m2, margin)

    def test_aabb(self):
        self.hull.get_aabb_non_virtual(self.t1, self.v1, self.v2)
        self.assertNotEquals(self.v1, self.v3)
        self.v3 = bullet.btVector3(1.08, 1.08, 1.08)
        self.assertEquals(self.v1, -self.v3)
        self.assertEquals(self.v2, self.v3)

    def test_project(self):
        _min, _max = 0.0, 0.0
        _min, _max = self.hull.project(self.t1, bullet.btVector3(1, 0, 0))
        self.assertEquals(_min, -1.04)
        self.assertEquals(_max, 1.04)

    def test_get_aabb_slow(self):
        self.hull.get_aabb_slow(self.t1, self.v1, self.v2)
        self.v3 = bullet.btVector3(1.08, 1.08, 1.08)
        self.assertEquals(self.v1, -self.v3)
        self.assertEquals(self.v2, self.v3)

    def tearDown(self):
        del self.hull
        del self.points
        del self.t1
        del self.v3
        del self.v1
        del self.v2


class CollisionShapeTestCase(unittest.TestCase):
    """
    We use different hull types to test functions and properties
    on btCollisionShape as it is abstract
    """
    def setUp(self):
        # Describe a cube
        self.points = [
            bullet.btVector3(-1, -1, -1),
            bullet.btVector3(-1, 1, -1),
            bullet.btVector3(-1, -1, 1),
            bullet.btVector3(-1, 1, 1),
            bullet.btVector3(1, 1, 1),
            bullet.btVector3(1, -1, 1),
            bullet.btVector3(1, -1, -1),
            bullet.btVector3(1, 1, -1)
        ]
        self.hull1 = bullet.btConvexHullShape(self.points)
        self.hull2 = bullet.btBox2dShape(self.points[4])
        self.shape1 = bullet.btCompoundShape()
        self.plane = bullet.btStaticPlaneShape(bullet.btVector3(0, 0, 0),
                                               1.0)
        self.v1 = bullet.btVector3(0, 0, 0)
        self.v2 = bullet.btVector3(0, 0, 0)
        self.v3 = bullet.btVector3(0, 0, 0)
        self.t1 = bullet.btTransform.identity

    def test_abstract(self):
        def _instantiate_abstract():
            bullet.btCollisionShape()
        self.assertRaises(_instantiate_abstract)

    def test_polyhedral(self):
        self.assertTrue(self.hull1.polyhedral)
        self.assertFalse(self.hull2.polyhedral)

    def test_convex2d(self):
        self.assertFalse(self.hull1.convex2d)
        self.assertTrue(self.hull2.convex2d)

    def test_convex(self):
        self.assertTrue(self.hull1.convex)
        self.assertFalse(self.plane.convex)

    def test_concave(self):
        self.assertTrue(self.plane.concave)
        self.assertFalse(self.hull1.concave)

    def test_margin(self):
        self.hull1.margin = 0.01
        self.assertEquals(self.hull1.margin, 0.01)
        self.hull1.get_aabb(self.t1, self.v1, self.v2)
        self.v3 = bullet.btVector3(1.05, 1.05, 1.05)
        self.assertEquals(self.v1, -self.v3)
        self.assertEquals(self.v2, self.v3)

    def test_compound(self):
        self.assertFalse(self.hull1.compound)
        self.assertTrue(self.shape1.compound)

    def test_infinite(self):
        self.assertTrue(self.plane.infinite)
        self.assertFalse(self.hull1.infinite)

    def test_soft_body(self):
        for s in (self.hull1, self.hull2, self.plane, self.shape1):
            print(s)
            self.assertFalse(s.soft_body)

    def test_bounding_sphere(self):
        radius = self.hull1.get_bounding_sphere(self.v1)
        self.assertEquals(self.v1, bullet.btVector3(0, 0, 0))
        self.v3 = bullet.btVector3(1.08, 1.08, 1.08)
        self.assertEquals(radius, self.v3.length)

    def test_local_scaling(self):
        self.v1 = bullet.btVector3(2, 2, 2)
        self.hull1.set_local_scaling(self.v1)
        self.assertEquals(self.hull1.get_local_scaling(),
                          bullet.btVector3(2, 2, 2))
        self.assertEquals(self.hull1.local_scaling,
                          bullet.btVector3(2, 2, 2))
        self.hull1.local_scaling = bullet.btVector3(3, 3, 3)
        self.hull1.recalc_local_aabb()
        self.hull1.get_aabb_slow(self.t1, self.v1, self.v2)
        self.v3 = bullet.btVector3(3.08, 3.08, 3.08)
        self.assertEquals(self.v1, -self.v3)
        self.assertEquals(self.v2, self.v3)

    def tearDown(self):
        del self.hull1
        del self.hull2
        del self.points
        del self.t1
        del self.v3
        del self.v1
        del self.v2
