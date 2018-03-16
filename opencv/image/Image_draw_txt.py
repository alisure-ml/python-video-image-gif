from PIL import Image, ImageDraw, ImageFont


def draw_one_data(image_file, txt):
    im = Image.open(image_file).convert("RGB")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("simhei.ttf", 15, encoding="utf-8")

    point = [(100, 100), (200, 100), (200, 200), (100, 200)]

    draw.line((point[0], point[1]), fill=(255, 0, 0), width=2)
    draw.line((point[1], point[2]), fill=(255, 0, 0), width=2)
    draw.line((point[2], point[3]), fill=(255, 0, 0), width=2)
    draw.line((point[3], point[0]), fill=(255, 0, 0), width=2)
    draw.text((point[0][0], point[0][1] - 20), txt, (255, 0, 0), font=font)

    im.show(im)
    pass

if __name__ == '__main__':
    draw_one_data("demo.png", "你好abc123!@#")
