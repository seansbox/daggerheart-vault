# python3 -m pip install pillow

from PIL import Image, ImageDraw


class COLORS:
    BACK = "#3b4252"
    NONE = "#434c5e"
    HIDE = "#bf616a"
    PATH = "#a3be8c"
    ROOM = "#eceff4"
    DOWN = "#2e3440"


# Define the coordinates for the center white square
dim = (160, 60)

room_size = 26
room_left = dim[0] / 2 - room_size / 2
room_top = dim[1] / 2 - room_size / 2
room_right = dim[0] / 2 + room_size / 2
room_bottom = dim[1] / 2 + room_size / 2

road_size = 10
road_left = dim[0] / 2 - road_size / 2
road_top = dim[1] / 2 - road_size / 2
road_right = dim[0] / 2 + road_size / 2
road_bottom = dim[1] / 2 + road_size / 2

square_coords = [(room_left, room_top), (room_right, room_bottom)]
road_beg = [
    (0, road_top),
    (road_left, 0),
    (room_right, road_top),
    (road_left, room_bottom),
]
road_dim = [
    (road_left, road_size),
    (road_size, road_top),
    (road_left, road_size),
    (road_size, road_top),
]
stair_up = [
    (dim[0] / 2 - 5, road_top + 3),
    (dim[0] / 2, road_top - 2),
    (dim[0] / 2 + 5, road_top + 3),
]
stair_dn = [
    (dim[0] / 2 - 5, road_bottom - 3),
    (dim[0] / 2, road_bottom + 2),
    (dim[0] / 2 + 5, road_bottom - 3),
]


def create_images():
    combos = []
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    combos.append(f"{a}{b}{c}{d}")

    for stair in ["", "u", "d", "ud"]:
        for combo in combos:
            # Create a blank image with white background
            img = Image.new("RGB", dim, COLORS.BACK)
            draw = ImageDraw.Draw(img)

            for i in range(len(combo)):
                if combo[i] == "1":
                    color = COLORS.PATH
                elif combo[i] == "2":
                    color = COLORS.HIDE
                else:
                    color = COLORS.NONE
                draw.rectangle(
                    [
                        road_beg[i],
                        (
                            road_beg[i][0] + road_dim[i][0],
                            road_beg[i][1] + road_dim[i][1],
                        ),
                    ],
                    fill=color,
                )
            # Draw the white square with a black border
            draw.rectangle(square_coords, fill=COLORS.ROOM, outline=COLORS.BACK)

            # Save the image
            if "u" in stair:
                draw.polygon(stair_up, fill=COLORS.DOWN)
            if "d" in stair:
                draw.polygon(stair_dn, fill=COLORS.DOWN)

            img.save(f"{combo}{stair}.png")

    img = Image.new("RGB", dim, COLORS.BACK)
    draw = ImageDraw.Draw(img)
    for i in range(4):
        color = COLORS.NONE
        draw.rectangle(
            [
                road_beg[i],
                (road_beg[i][0] + road_dim[i][0], road_beg[i][1] + road_dim[i][1]),
            ],
            fill=color,
        )
    draw.rectangle(square_coords, fill=COLORS.NONE, outline=COLORS.BACK)
    img.save(f"0.png")


create_images()
