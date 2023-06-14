import auto_palette

pal = auto_palette.Palette("fff fffee3 ee8")
pal2 = auto_palette.Palette((1, 2, 3), (56, 78, 33), (2, 3, 78, 5))

auto_palette.display_palettes(pal, pal2)
