from PIL import Image


def resize_and_crop(img_path, size):
    img = Image.open(img_path)
    img_ratio = img.size[0] / float(img.size[1])
    ratio = size[0] / float(size[1])
    if ratio > img_ratio:
        img = img.resize((size[0], round(size[0] * img.size[1] / img.size[0])),
                         Image.ANTIALIAS)
        box = (0, 0, img.size[0], size[1])
        img = img.crop(box)
    elif ratio < img_ratio:
        img = img.resize((round(size[1] * img.size[0] / img.size[1]), size[1]),
                         Image.ANTIALIAS)
        box = (0, 0, size[0], img.size[1])
        img = img.crop(box)
    else:
        img = img.resize((size[0], size[1]),
                         Image.ANTIALIAS)
    img.save(img_path)
