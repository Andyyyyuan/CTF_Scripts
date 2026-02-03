from PIL import Image

def arnold(infile: str, outfile: str = None, a: int = 1, b: int = 1, shuffle_times: int = 1, reverse: bool = False) -> None:
    """
    Arnold猫脸变换函数

    Parameters:
        infile - 输入图像路径
        outfile - 输出图像路径
        a - Anrold 变换参数
        b - Anrold 变换参数
        shuffle_times - 置乱次数
        reverse - 逆变换
    """
    inimg = Image.open(infile)
    width, height = inimg.size
    indata = inimg.load()
    outimg = Image.new(inimg.mode, inimg.size)
    outdata = outimg.load()

    for _ in range(shuffle_times):
        for x in range(width):
            for y in range(height):
                if reverse:
                    nx = ((a * b + 1) * x - a * y) % width
                    ny = (y - b * x) % height
                else:
                    nx = (x + a * y) % width
                    ny = (b * x + (a * b + 1) * y) % height
                outdata[ny, nx] = indata[y, x]
    
    outimg.save(outfile if outfile else "arnold_"+infile, inimg.format)

arnold("before.png", "encode.png", 9, 39, 1)
arnold("encode.png", "decode.png", 9, 39, 1, True)
