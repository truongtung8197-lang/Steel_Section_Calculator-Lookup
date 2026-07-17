"""Định nghĩa các loại thép và danh sách STEEL_TYPES."""

from dataclasses import dataclass
from typing import Callable, List, Tuple

from core.constants import DENSITY_FACTOR
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


@dataclass(frozen=True)
class SteelType:
    key: str
    name: str
    fields: List[Tuple[str, str]]
    calc: Callable[[dict], float]
    validator: Callable[[dict], None]
    image_file: str
    tooltip: str = ""


# Danh sách 8 loại thép
STEEL_TYPES: List[SteelType] = [
    SteelType(
        "plate",
        "Plate",
        [("Length", "mm"), ("Width", "mm"), ("Thickness", "mm")],
        lambda v: area_plate(v) * v["Length"] * 1000.0 * DENSITY_FACTOR,
        check_plate,
        "PL.PNG",
        tooltip="Tấm thép phẳng. Tính khối lượng = Dài × Rộng × Dày × Mật độ thép",
    ),
    SteelType(
        "ih",
        "I Beam / H Beam",
        [("H", "mm"), ("B", "mm"), ("Tw", "mm"), ("Tf", "mm"), ("Length", "m")],
        lambda v: area_ishape(v) * v["Length"] * 1000.0 * DENSITY_FACTOR,
        check_ishape,
        "I.PNG",
        tooltip="Dầm I/H: H=chiều cao, B=chiều rộng cánh, Tw=dày nhịp, Tf=dày cánh",
    ),
    SteelType(
        "channel",
        "PFC / U Channel",
        [("H", "mm"), ("B", "mm"), ("Tw", "mm"), ("Tf", "mm"), ("Length", "m")],
        lambda v: area_channel(v) * v["Length"] * 1000.0 * DENSITY_FACTOR,
        check_channel,
        "U.PNG",
        tooltip="Thép hình U: H=chiều cao, B=chiều rộng đáy, Tw=dày nhịp, Tf=dày đáy",
    ),
    SteelType(
        "angle",
        "Angle / L Section",
        [("Leg A", "mm"), ("Leg B", "mm"), ("Thickness", "mm"), ("Length", "m")],
        lambda v: area_angle(v) * v["Length"] * 1000.0 * DENSITY_FACTOR,
        check_angle,
        "L.PNG",
        tooltip="Thép góc: Leg A/B=chiều dài 2 cạnh, Thickness=dày",
    ),
    SteelType(
        "rhs_shs",
        "RHS / SHS",
        [("Width", "mm"), ("Height", "mm"), ("Thickness", "mm"), ("Length", "m")],
        lambda v: area_rhs_shs(v) * v["Length"] * 1000.0 * DENSITY_FACTOR,
        check_rhs_shs,
        "RHS.PNG",
        tooltip="Thép hộp: Width=chiều rộng, Height=chiều cao, Thickness=dày thành",
    ),
    SteelType(
        "chs",
        "CHS / Pipe",
        [("OD", "mm"), ("Thickness", "mm"), ("Length", "m")],
        lambda v: area_chs(v) * v["Length"] * 1000.0 * DENSITY_FACTOR,
        check_chs,
        "CHS.PNG",
        tooltip="Thép ống: OD=đường kính ngoài, Thickness=dày thành",
    ),
    SteelType(
        "rod",
        "Rod / Round Bar",
        [("Diameter", "mm"), ("Length", "m")],
        lambda v: area_rod(v) * v["Length"] * 1000.0 * DENSITY_FACTOR,
        check_rod,
        "ROD.PNG",
        tooltip="Thép tròn: Diameter=đường kính",
    ),
    SteelType(
        "tsection",
        "T Section",
        [("H", "mm"), ("B", "mm"), ("Tw", "mm"), ("Tf", "mm"), ("Length", "m")],
        lambda v: area_tsection(v) * v["Length"] * 1000.0 * DENSITY_FACTOR,
        check_tsection,
        "T.PNG",
        tooltip="Thép chữ T: H=chiều cao, B=chiều rộng đỉnh, Tw=dày nhịp, Tf=dày đỉnh",
    ),
]