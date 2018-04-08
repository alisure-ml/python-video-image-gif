import imagehash
from PIL import Image


def image_hash(image_file="../gif/test/img/0.png", hash_size=8):
    im = Image.open(image_file)
    a_hash_value = imagehash.average_hash(im, hash_size)
    d_hash_value = imagehash.dhash(im, hash_size)
    d_hash_value_h = imagehash.dhash_vertical(im, hash_size)
    p_hash_value = imagehash.phash(im, hash_size)
    p_hash_value_s = imagehash.phash_simple(im, hash_size)
    w_hash_value = imagehash.whash(im, hash_size)
    return [a_hash_value, d_hash_value, d_hash_value_h, p_hash_value, p_hash_value_s, w_hash_value]


if __name__ == '__main__':
    image_1 = image_hash(image_file="../gif/test/img/11000.png", hash_size=8)
    image_2 = image_hash(image_file="../gif/test/img/19000.png", hash_size=8)
    result = [image_1[i] - image_2[i] for i in range(len(image_1))]
    print(result)
