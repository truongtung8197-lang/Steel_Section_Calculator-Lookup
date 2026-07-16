"""Hàm tính diện tích mặt cắt và validation cho từng loại thép."""

import math


def area_plate(v):
    return v["Length"] * v["Width"] * v["Thickness"]


def check_plate(v):
    if v["Length"] <= 0 or v["Width"] <= 0 or v["Thickness"] <= 0:
        raise ValueError()


def area_ishape(v):
    h, b, tw, tf = v["H"], v["B"], v["Tw"], v["Tf"]
    r = v.get("r1", 0)
    base_area = 2 * b * tf + (h - 2 * tf) * tw
    corner_area = (math.pi - 2) * r**2 if r > 0 else 0
    return base_area + corner_area


def check_ishape(v):
    r = v.get("r1", 0)
    if v["Tw"] >= v["B"] or (2 * v["Tf"]) >= v["H"]:
        raise ValueError()
    if r < 0 or r > min(v["Tw"], v["Tf"]) / 2:
        raise ValueError()


def area_channel(v):
    h, b, tw, tf = v["H"], v["B"], v["Tw"], v["Tf"]
    r = v.get("r1", 0)
    base_area = 2 * b * tf + (h - 2 * tf) * tw
    corner_area = 2 * (math.pi - 2) * r**2 if r > 0 else 0
    return base_area + corner_area


def check_channel(v):
    r = v.get("r1", 0)
    if v["Tw"] >= v["B"] or (2 * v["Tf"]) >= v["H"]:
        raise ValueError()
    if r < 0 or r > min(v["Tw"], v["Tf"]) / 2:
        raise ValueError()


def area_tsection(v):
    h, b, tw, tf = v["H"], v["B"], v["Tw"], v["Tf"]
    r = v.get("r1", 0)
    base_area = b * tf + (h - tf) * tw
    corner_area = 2 * (math.pi - 2) * r**2 if r > 0 else 0
    return base_area + corner_area


def check_tsection(v):
    r = v.get("r1", 0)
    if v["Tw"] >= v["B"] or v["Tf"] >= v["H"]:
        raise ValueError()
    if r < 0 or r > min(v["Tw"], v["Tf"]) / 2:
        raise ValueError()


def area_angle(v):
    a, b, t = v["Leg A"], v["Leg B"], v["Thickness"]
    r = v.get("r1", 0)
    base_area = t * (a + b - t)
    corner_area = (math.pi / 4 - 0.5) * r**2 if r > 0 else 0
    return base_area + corner_area


def check_angle(v):
    r = v.get("r1", 0)
    if v["Thickness"] >= v["Leg A"] or v["Thickness"] >= v["Leg B"]:
        raise ValueError()
    if r < 0 or r > v["Thickness"]:
        raise ValueError()


def area_rhs_shs(v):
    w, h, t = v["Width"], v["Height"], v["Thickness"]
    r = v.get("r1", 0)
    base_area = w * h - (w - 2 * t) * (h - 2 * t)
    if r > 0:
        ro = r
        ri = r - t
        corner_area = (4 - math.pi) * (ro**2 - ri**2)
        return base_area - corner_area
    return base_area


def check_rhs_shs(v):
    r = v.get("r1", 0)
    if (2 * v["Thickness"]) >= v["Width"] or (2 * v["Thickness"]) >= v["Height"]:
        raise ValueError()
    if r < 0 or r > v["Thickness"]:
        raise ValueError()


def area_chs(v):
    od, t = v["OD"], v["Thickness"]
    return math.pi / 4.0 * (od**2 - (od - 2 * t) ** 2)


def check_chs(v):
    if (2 * v["Thickness"]) >= v["OD"]:
        raise ValueError()


def area_rod(v):
    return math.pi * v["Diameter"] ** 2 / 4.0


def check_rod(v):
    if v["Diameter"] <= 0:
        raise ValueError()