# coding = utf-8
import glob
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np


# 计算各级灰度概率密度
def probability(img):
    arr = np.zeros(shape=256)
    # 存储各灰度级的像素个数
    for i in img:
        for j in i:
            arr[j] += 1
    r, c = img.shape
    return arr / (r * c)


def hist(img, prs):
    prs = np.cumsum(prs)
    img_map = np.array(255 * prs + 0.5, dtype=int)
    r, c = img.shape
    for i in range(r):
        for j in range(c):
            img[i, j] = img_map[img[i, j]]
    return img


if __name__ == "__main__":
    paths = os.listdir(r"\imageData")
    path = glob.glob(os.path.join(r"\imageData", paths[3]))
    image = cv2.imread(path[0], 0)
    image_old = np.array(image, copy=True)
    cv2.imwrite(
        "/imageData/01_gray.jpg", image_old,
    )
    pr: np.array = probability(image_old)

    image_new = hist(image_old, pr)
    image_reverse = np.array(image_new, copy=True)
    pr_mean: np.array = probability(image_new)
    cv2.imwrite(
        r"\imageData\01_new.jpg", image_new,
    )

    plt.rcParams["font.sans-serif"] = "SimHei"
    fig = plt.figure(num="灰度值分布直方图")
    fig1 = plt.figure(num="灰度图")
    fig2 = plt.figure(num="灰度反转")
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    ax3 = fig2.add_subplot(1, 1, 1)
    ax4 = fig1.add_subplot(1, 1, 1)
    ax1.bar([i for i in range(256)], pr)
    ax2.bar([i for i in range(256)], pr_mean)
    ax1.set_title("原图像")
    ax2.set_title("均衡化后的图像")
    ax3.imshow(255 - image_reverse, cmap="gray")
    ax3.axis("off")
    ax4.imshow(image_new, cmap="gray")
    ax4.axis("off")
    plt.show()
