# pip install pillow

from PIL import Image, ImageDraw

# Define the coordinates for the center white square
dim = (160, 60)

room_size = 20
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
road_beg = [(0, road_top), (road_left, 0), (room_right, road_top), (road_left, room_bottom)]
road_dim = [(road_left, road_size), (road_size, road_top), (road_left, road_size), (road_size, road_top)]
stair_up = [(dim[0] / 2 - 5, road_top + 3), (dim[0] / 2, road_top - 2), (dim[0] / 2 + 5, road_top + 3)]
stair_dn = [(dim[0] / 2 - 5, road_bottom - 3), (dim[0] / 2, road_bottom + 2), (dim[0] / 2 + 5, road_bottom - 3)]


def create_images():
    combos = [
        "0000",
        "1111",
        "1000",
        "0100",
        "0010",
        "0001",
        "1100",
        "1010",
        "1001",
        "0110",
        "0101",
        "0011",
        "1110",
        "1101",
        "1011",
        "0111",
    ]

    for stair in ["", "u", "d", "ud"]:
        for combo in combos:
            # Create a blank image with white background
            img = Image.new("RGB", dim, "black")
            draw = ImageDraw.Draw(img)

            for i in range(len(combo)):
                if combo[i] == "1":
                    color = "#cccccc"
                else:
                    color = "#111111"
                draw.rectangle(
                    [road_beg[i], (road_beg[i][0] + road_dim[i][0], road_beg[i][1] + road_dim[i][1])], fill=color
                )
            # Draw the white square with a black border
            draw.rectangle(square_coords, fill="white", outline="black")

            # Save the image
            if "u" in stair:
                draw.polygon(stair_up, fill="#555555")
            if "d" in stair:
                draw.polygon(stair_dn, fill="#555555")

            img.save(f"{combo}{stair}.png")

    img = Image.new("RGB", dim, "black")
    draw = ImageDraw.Draw(img)
    for i in range(4):
        color = "#111111"
        draw.rectangle([road_beg[i], (road_beg[i][0] + road_dim[i][0], road_beg[i][1] + road_dim[i][1])], fill=color)
    draw.rectangle(square_coords, fill="#111111", outline="black")
    img.save(f"0.png")


create_images()
