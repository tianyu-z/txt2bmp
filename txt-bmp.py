# reference: https://www.bilibili.com/video/BV1Ai4y1V7rg
from PIL import Image
import math


def txt2bmp(text, width=None, height=None):
    """
    convert text to bmp
    principle: 3 characters -> 2 pixels
    ord function of python: return the unicode of the character
    ranging from [0, 65535] inclusively, which is equal to 16 bits
    pixel value: (red, green, blue)
    ranging from [0, 255] inclusively, which is equal to 8 bits
    one pixel can store 24 bits of information
    so we can store 3 characters (16 x 3 = 48 bits) in 2 pixels (12 x 2 = 48 bits)
    """
    str_len = len(text)
    # padding, make the length of text a multiple of 3
    if str_len % 3 == 1:
        text += "  "
    elif str_len % 3 == 2:
        text += " "
    str_len = len(text)
    # number of pixels, width of the image is the square root of the number of pixels
    nb_pix = (str_len // 3) * 2
    if width is not None and height is not None:
        assert width % 2 == 0, "width must be even"
        nb_pix = width * height
        assert nb_pix >= (str_len // 3) * 2, "width and height are too small"
    elif width is not None and height is None:
        height = math.ceil(nb_pix / width)
    elif width is None and height is not None:
        raise ValueError("width must be specified if height is specified")
    else:
        width = math.ceil(nb_pix**0.5)
        height = math.ceil(nb_pix / width)
        # make the width of the image even
        if width % 2 == 1:
            width += 1
    im = Image.new("RGB", (width, height), 0x0)
    x, y = 0, 0
    for i in range(0, len(text), 3):
        # get the unicode of the character, 3 characters in a row
        index_1 = ord(text[i])
        index_2 = ord(text[i + 1])
        index_3 = ord(text[i + 2])
        # store the unicodes in the pixel value, 2 pixels in a row
        # the first pixel red value is the first character's high 8 bits
        # the first pixel green value is the first character's low 8 bits
        # the first pixel blue value is the second character's high 8 bits
        # the second pixel red value is the second character's low 8 bits
        # the second pixel green value is the third character's high 8 bits
        # the second pixel blue value is the third character's low 8 bits
        rgb_1 = ((index_1 & 0xFF00) >> 8, index_1 & 0xFF, (index_2 & 0xFF00) >> 8)
        rgb_2 = (index_2 & 0xFF, (index_3 & 0xFF00) >> 8, index_3 & 0xFF)
        # put the pixel value into the image
        im.putpixel((x, y), rgb_1)
        # move to the next pixel
        if x == width - 1:
            x = 0
            y += 1
        else:
            x += 1
        # put the pixel value into the image
        im.putpixel((x, y), rgb_2)
        # move to the next pixel
        if x == width - 1:
            x = 0
            y += 1
        else:
            x += 1
    return im


def pad_width_1(im):
    """
    pad the width of the image to be even
    """
    right = 1
    left = 0
    top = 0
    bottom = 0
    width, height = im.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(im.mode, (new_width, new_height), (0, 0, 0))
    result.paste(im, (left, top))
    return result


def bmp2txt(im):
    """
    convert bmp to text
    """
    # padding, make the width of the image even
    width, height = im.size
    if width * height % 2 == 1:
        im = pad_width_1(im)
        width, height = im.size
    lst = []
    # get the pixel value, 2 pixels in a row
    for y in range(height):
        for x in range(0, width, 2):
            red_1, green_1, blue_1 = im.getpixel((x, y))
            red_2, green_2, blue_2 = im.getpixel((x + 1, y))
            # if the pixel value is (0, 0, 0), then the text is over
            if (red_1 | green_1 | blue_1) == 0 and (red_2 | green_2 | blue_2) == 0:
                break
            # get the unicode of the character, 3 characters in a row

            index_1 = (red_1 << 8) + green_1
            index_2 = (blue_1 << 8) + red_2
            index_3 = (green_2 << 8) + blue_2
            lst.append(chr(index_1))
            lst.append(chr(index_2))
            lst.append(chr(index_3))
    return "".join(lst)


if __name__ == "__main__":
    # txt to bmp
    with open("input.txt", encoding="utf-8") as f:
        all_text = f.read()

        im = txt2bmp(all_text)
        im.save("out.bmp")
    # bmp to txt
    all_text = bmp2txt(Image.open("out.bmp", "r"))
    with open("decode.txt", "w", encoding="utf-8") as f:
        f.write(all_text)
