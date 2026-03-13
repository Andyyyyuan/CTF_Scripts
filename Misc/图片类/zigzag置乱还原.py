from PIL import Image
import numpy as np


def zigzag_indices(h, w):
    """
    生成标准 ZigZag 扫描顺序：
    按副对角线遍历，方向交替
    """
    order = []
    for s in range(h + w - 1):
        diag = []
        r_start = max(0, s - w + 1)
        r_end = min(h - 1, s)
        for r in range(r_start, r_end + 1):
            c = s - r
            diag.append((r, c))

        # 标准 ZigZag：偶数对角线反转
        if s % 2 == 0:
            diag.reverse()

        order.extend(diag)
    return order


def inverse_zigzag(img_array):
    """
    把“按 ZigZag 顺序展开后再按行填充”的图像还原回原图
    """
    h, w = img_array.shape
    flat = img_array.reshape(-1)
    order = zigzag_indices(h, w)

    restored = np.zeros_like(img_array)
    for k, (r, c) in enumerate(order):
        restored[r, c] = flat[k]

    return restored


def main():
    input_path = "1.png"          # 加密图
    output_path = "restored_qr.png"  # 还原图

    # 读取灰度图
    img = Image.open(input_path).convert("L")
    arr = np.array(img)

    # 二值化，避免灰度抗锯齿影响
    binary = np.where(arr > 128, 255, 0).astype(np.uint8)

    # ZigZag 逆还原
    restored = inverse_zigzag(binary)

    # 保存结果
    Image.fromarray(restored).save(output_path)
    print(f"还原完成，已保存到: {output_path}")


if __name__ == "__main__":
    main()
