import cv2
import numpy as np
import random


def grey_dither(img):
    h, w, c = img.shape 
    max_light = 220
    min_dark = 20

    # greyscale image
    for i in range(h):
        for j in range(w):
            color = max(max_light*round(int(img[i][j][0])/255), min_dark)
            img[i][j] = np.array([color]*3)


    # adding noise
    for i in range(h):
        for j in range(w):
            noise_offset = max(int(img[i][j][0]) + int(20 * random.uniform(-1, 1)), 0)
            img[i][j] += noise_offset

    bayer = np.array([
            [0.125, 0.625],
            [0.875, 0.375]
        ])  # threshold matrix; you can increase size (4x4, 8x8) if you want
    for i in range(h):
        for j in range(w):
            # tile the 2x2 matrix over the whole image
            thr = bayer[i % 2, j % 2]
            for k in range(c):

                if img[i, j, k]/256 >= thr:
                    img[i, j, k] = 255.0   # high level
                else:
                    img[i, j, k] = 0.0   # low level

    return img


def main():

    img = cv2.imread("Google.png")
    
    img = grey_dither(img)
    # bayer_8bit = np.array([[16, 96], [224, 144]])
    # ordered dithering 
    # for i in range(h):
    #     for j in range(w):
    #         r = i % 2
    #         c = j % 2
    #         threshold = bayer_8bit[r][c]
    #         if int(img[i][j][0]) >= threshold:
    #             img[i][j] = 1
    #         else:
    #             img[i][j] = 0

    
    cv2.imshow("win", img)               # display
    cv2.waitKey(0)                       # wait for key
    cv2.destroyAllWindows()              # close window

    cv2.imwrite("out.jpg", img)   

     

if __name__ == "__main__":
    main()





