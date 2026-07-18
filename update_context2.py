with open('docs/context.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Update directory structure
old_struct = """|-- gui/                       # UI components
|   |-- styles.py              # Stylesheet (light mode)
|   |-- dialogs.py             # show_about, show_help
|   |-- widgets/
|   |   |-- image_box.py       # ImageBox widget (QLabel + QPixmap)
|   |-- tabs/
|   |   |-- calc_tab.py        # CalculatorTab (315 dong)
|   |   |-- lookup_tab.py      # LookupTab (162 dong)"""

new_struct = """|-- gui/                       # UI components
|   |-- styles.py              # Stylesheet (light mode)
|   |-- dialogs.py             # show_about, show_help
|   |-- widgets/
|   |   |-- image_box.py       # ImageBox widget (QLabel + QPixmap)
|   |   |-- dynamic_shapes/    # Dynamic shape widgets (QPainter)
|   |       |-- base_shape.py      # Base class DynamicShapeWidget
|   |       |-- plate_shape.py     # DynamicPlateShape
|   |       |-- i_shape.py         # DynamicIShape
|   |       |-- chs_shape.py       # DynamicCHSShape
|   |       |-- rhs_shape.py       # DynamicRHSShape
|   |       |-- u_shape.py         # DynamicUShape
|   |       |-- l_shape.py         # DynamicLShape
|   |       |-- t_shape.py         # DynamicTShape
|   |       |-- rod_shape.py       # DynamicRodShape
|   |-- tabs/
|   |   |-- calc_tab.py        # CalculatorTab (315 dong)
|   |   |-- lookup_tab.py      # LookupTab (162 dong)"""

content = content.replace(old_struct, new_struct)

with open('docs/context.md', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated directory structure successfully')