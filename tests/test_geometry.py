"""Tests for core geometry calculations."""

import math

import pytest

from core.geometry import (
    area_angle,
    area_channel,
    area_chs,
    area_ishape,
    area_plate,
    area_rhs_shs,
    area_rod,
    area_tsection,
    check_angle,
    check_channel,
    check_chs,
    check_ishape,
    check_plate,
    check_rhs_shs,
    check_rod,
    check_tsection,
)


class TestAreaPlate:
    def test_area_plate_basic(self):
        assert area_plate({"Width": 100, "Length": 5, "Thickness": 10}) == 1000

    def test_plate_weight_calculation(self):
        """Test full weight calculation: Width × Thickness × Length × Density"""
        from core.constants import DENSITY_FACTOR

        v = {"Width": 1000, "Length": 2000, "Thickness": 10}
        area = area_plate(v)
        weight = area * v["Length"] * 1000.0 * DENSITY_FACTOR
        expected = 1000 * 10 * 2000 * 1000 * 7.85e-6
        assert math.isclose(weight, expected, rel_tol=1e-9)

    def test_check_plate_valid(self):
        check_plate({"Length": 1000, "Width": 200, "Thickness": 10})

    def test_check_plate_invalid_zero(self):
        with pytest.raises(ValueError):
            check_plate({"Length": 0, "Width": 200, "Thickness": 10})

    def test_check_plate_invalid_negative(self):
        with pytest.raises(ValueError):
            check_plate({"Length": 1000, "Width": -200, "Thickness": 10})


class TestAreaIShape:
    def test_area_ishape_no_corner(self):
        result = area_ishape({"H": 200, "B": 100, "Tw": 6, "Tf": 10, "r1": 0})
        expected = 2 * 100 * 10 + (200 - 2 * 10) * 6
        assert result == expected

    def test_area_ishape_with_corner(self):
        result = area_ishape({"H": 200, "B": 100, "Tw": 6, "Tf": 10, "r1": 5})
        base = 2 * 100 * 10 + (200 - 20) * 6
        expected = base + (4 - math.pi) * 25
        assert math.isclose(result, expected, rel_tol=1e-9)

    def test_check_ishape_valid(self):
        check_ishape({"H": 200, "B": 100, "Tw": 6, "Tf": 10, "r1": 0})

    def test_check_ishape_invalid_dimension(self):
        with pytest.raises(ValueError):
            check_ishape({"H": 0, "B": 100, "Tw": 6, "Tf": 10})

    def test_check_ishape_invalid_relationship(self):
        with pytest.raises(ValueError):
            check_ishape({"H": 100, "B": 50, "Tw": 60, "Tf": 10})

    def test_check_ishape_invalid_radius(self):
        with pytest.raises(ValueError):
            check_ishape({"H": 200, "B": 100, "Tw": 6, "Tf": 10, "r1": -1})


class TestAreaChannel:
    def test_area_channel_no_corner(self):
        result = area_channel({"H": 200, "B": 100, "Tw": 6, "Tf": 10, "r1": 0})
        expected = 2 * 100 * 10 + (200 - 20) * 6
        assert result == expected

    def test_area_channel_with_corner(self):
        result = area_channel({"H": 200, "B": 100, "Tw": 6, "Tf": 10, "r1": 5})
        base = 2 * 100 * 10 + (200 - 20) * 6
        expected = base + (2 - math.pi / 2) * 25
        assert math.isclose(result, expected, rel_tol=1e-9)

    def test_check_channel_valid(self):
        check_channel({"H": 200, "B": 100, "Tw": 6, "Tf": 10, "r1": 0})

    def test_check_channel_invalid_relationship(self):
        with pytest.raises(ValueError):
            check_channel({"H": 100, "B": 50, "Tw": 60, "Tf": 10})


class TestAreaAngle:
    def test_area_angle_no_corner(self):
        result = area_angle({"Leg A": 100, "Leg B": 50, "Thickness": 5, "r1": 0})
        expected = 5 * (100 + 50 - 5)
        assert result == expected

    def test_area_angle_with_corner(self):
        result = area_angle({"Leg A": 100, "Leg B": 50, "Thickness": 5, "r1": 5})
        base = 5 * (100 + 50 - 5)
        expected = base + (1 - math.pi / 4) * 25
        assert math.isclose(result, expected, rel_tol=1e-9)

    def test_check_angle_valid(self):
        check_angle({"Leg A": 100, "Leg B": 50, "Thickness": 5, "r1": 0})

    def test_check_angle_invalid_thickness(self):
        with pytest.raises(ValueError):
            check_angle({"Leg A": 100, "Leg B": 50, "Thickness": 150})


class TestAreaRHS_SHS:
    def test_area_rhs_no_corner(self):
        result = area_rhs_shs({"Width": 100, "Height": 50, "Thickness": 5, "r1": 0})
        expected = 100 * 50 - (100 - 10) * (50 - 10)
        assert result == expected

    def test_area_rhs_with_corner(self):
        result = area_rhs_shs({"Width": 100, "Height": 50, "Thickness": 5, "r1": 5})
        base = 100 * 50 - (100 - 10) * (50 - 10)
        ri = 5
        ro = 10
        expected = base - (4 - math.pi) * (ro**2 - ri**2)
        assert math.isclose(result, expected, rel_tol=1e-9)

    def test_check_rhs_valid(self):
        check_rhs_shs({"Width": 100, "Height": 50, "Thickness": 5, "r1": 0})

    def test_check_rhs_too_thick(self):
        with pytest.raises(ValueError):
            check_rhs_shs({"Width": 100, "Height": 50, "Thickness": 60})


class TestAreaCHS:
    def test_area_chs_basic(self):
        result = area_chs({"OD": 50, "Thickness": 5})
        expected = math.pi / 4.0 * (50**2 - 40**2)
        assert math.isclose(result, expected, rel_tol=1e-9)

    def test_check_chs_valid(self):
        check_chs({"OD": 50, "Thickness": 5})

    def test_check_chs_too_thick(self):
        with pytest.raises(ValueError):
            check_chs({"OD": 50, "Thickness": 30})


class TestAreaRod:
    def test_area_rod_basic(self):
        result = area_rod({"Diameter": 20})
        expected = math.pi * 400 / 4
        assert math.isclose(result, expected, rel_tol=1e-9)

    def test_check_rod_valid(self):
        check_rod({"Diameter": 20})

    def test_check_rod_invalid(self):
        with pytest.raises(ValueError):
            check_rod({"Diameter": 0})


class TestAreaTSection:
    def test_area_tsection_no_corner(self):
        result = area_tsection({"H": 200, "B": 100, "Tw": 6, "Tf": 10, "r1": 0})
        expected = 100 * 10 + (200 - 10) * 6
        assert result == expected

    def test_area_tsection_with_corner(self):
        result = area_tsection({"H": 200, "B": 100, "Tw": 6, "Tf": 10, "r1": 5})
        base = 100 * 10 + (200 - 10) * 6
        expected = base + (2 - math.pi / 2) * 25
        assert math.isclose(result, expected, rel_tol=1e-9)

    def test_check_tsection_valid(self):
        check_tsection({"H": 200, "B": 100, "Tw": 6, "Tf": 10, "r1": 0})

    def test_check_tsection_invalid_relationship(self):
        with pytest.raises(ValueError):
            check_tsection({"H": 100, "B": 50, "Tw": 60, "Tf": 10})
