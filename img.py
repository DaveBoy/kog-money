import os

from PIL import Image
from PIL import ImageFile


# 压缩图片文件
def compress_image(infile, outfile, mb=2048, quality=3, k=0.5):
    """不改变图片尺寸压缩到指定大小
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """

    o_size = os.path.getsize(infile) // 1024
    print(o_size, mb)
    if o_size <= mb:
        return outfile

    ImageFile.LOAD_TRUNCATED_IMAGES = True
    while o_size > mb:
        im = Image.open(infile)
        x, y = im.size
        out = im.resize((int(x * k), int(y * k)), Image.ANTIALIAS)
        try:
            out.save(outfile, quality=quality)
        except Exception as e:
            print(e)
            break
        o_size = os.path.getsize(outfile) // 1024
    return outfile


if __name__ == '__main__':
    pwd = os.getcwd()
    w_path = os.path.join(pwd, "pic")

    target = os.path.join(pwd, "chr")

    for i in os.listdir(w_path):
        if (not i.startswith(".")):
            f = os.path.join(w_path, i)
            tf = os.path.join(target, i)
            compress_image(f, tf)
