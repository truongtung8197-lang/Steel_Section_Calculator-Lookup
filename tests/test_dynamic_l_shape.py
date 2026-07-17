"""Tests for DynamicLShape and DynamicIShape geometry (pure logic, no QWidget)."""

import math

import pytest

from gui.widgets.dynamic_shapes.i_shape import _i_shape_points
from gui.widgets.dynamic_shapes.l_shape import _l_shape_points


class TestLShapePointsNoCorner:
    def test_basic(self):
        pts = _l_shape_points(100, 50, 5, 0)
        assert len(pts) == 6
        assert pts[0].x() == 0 and pts[0].y() == 0
        assert pts[1].x() == 100 and pts[1].y() == 0
        assert pts[2].x() == 100 and pts[2].y() == 5
        assert pts[3].x() == 5 and pts[3].y() == 5
        assert pts[4].x() == 5 and pts[4].y() == 50
        assert pts[5].x() == 0 and pts[5].y() == 50

    def test_square(self):
        pts = _l_shape_points(60, 60, 10, 0)
        assert len(pts) == 6
        assert pts[3].x() == 10 and pts[3].y() == 10

    def test_invalid_dimension(self):
        with pytest.raises(ValueError):
            _l_shape_points(0, 50, 5, 0)

    def test_too_thick(self):
        with pytest.raises(ValueError):
            _l_shape_points(50, 50, 30, 0)


class TestLShapePointsWithCorner:
    def test_with_corner(self):
        pts = _l_shape_points(100, 50, 5, 3)
        assert len(pts) > 6
        assert pts[0].x() == 0 and pts[0].y() == 0
        assert pts[1].x() == 100 and pts[1].y() == 0
        assert pts[2].x() == 100 and pts[2].y() == 5
        assert abs(pts[3].x() - (5 + 3)) < 1e-6
        assert abs(pts[3].y() - 5) < 1e-6
        last = pts[-1]
        assert abs(last.x() - 0) < 1e-6
        assert abs(last.y() - 50) < 1e-6

    def test_zero_corner(self):
        pts0 = _l_shape_points(100, 50, 5, 0)
        pts1 = _l_shape_points(100, 50, 5, 1e-12)
        assert len(pts1) == 6

    def test_corner_too_large(self):
        with pytest.raises(ValueError):
            _l_shape_points(100, 50, 5, 100)

    def test_negative_corner(self):
        with pytest.raises(ValueError):
            _l_shape_points(100, 50, 5, -1)


class TestIShapePointsNoCorner:
    def test_basic(self):
        pts = _i_shape_points(200, 100, 6, 10, 0)
        assert len(pts) == 12
        assert pts[0].x() == 0 and pts[0].y() == 0
        assert pts[1].x() == 100 and pts[1].y() == 0
        assert pts[2].x() == 100 and pts[2].y() == 10
        assert pts[3].x() == 94 and pts[3].y() == 10
        assert pts[4].x() == 94 and pts[4].y() == 190
        assert pts[5].x() == 100 and pts[5].y() == 190
        assert pts[6].x() == 100 and pts[6].y() == 200
        assert pts[7].x() == 0 and pts[7].y() == 200
        assert pts[8].x() == 0 and pts[8].y() == 190
        assert pts[9].x() == 6 and pts[9].y() == 190
        assert pts[10].x() == 6 and pts[10].y() == 10
        assert pts[11].x() == 0 and pts[11].y() == 10

    def test_invalid_dimension(self):
        with pytest.raises(ValueError):
            _i_shape_points(0, 100, 6, 10, 0)

    def test_invalid_web_geometry(self):
        with pytest.raises(ValueError):
            _i_shape_points(200, 100, 120, 10, 0)


class TestIShapePointsWithCorner:
    def test_with_corner(self):
        pts = _i_shape_points(200, 100, 6, 10, 5)
        assert len(pts) > 12
        assert pts[0].x() == 0 and pts[0].y() == 0

    def test_zero_corner(self):
        pts0 = _i_shape_points(200, 100, 6, 10, 0)
        pts1 = _i_shape_points(200, 100, 6, 10, 1e-12)
        assert len(pts1) == len(pts0)

    def test_corner_clamped(self):
        pts = _i_shape_points(200, 100, 6, 10, 999)
        assert len(pts) > 12
