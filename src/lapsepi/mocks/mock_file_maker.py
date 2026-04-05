from PIL import Image, ImageDraw

def create_mock_jpg(path):
    # create blank image
    img = Image.new("RGB", (640, 480), color="black")


    # draw blue square bottom-left
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 480-5, 5, 480], fill="blue")

    img.save(path)

    return path


# note on positioning
# if image size (640, 480), then:
# top-left = (0, 0)
# bottom-right = (640, 480)
#
# rectangle coords:
# [x_start, y_start, x_end, y_end]
#
# x increases → right
# y increases → down