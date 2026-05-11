import cv2
import numpy as np
import cupy as cp
import time
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

    # bayer = np.array([
    #         [0.125, 0.625],
    #         [0.875, 0.375]
    #     ])  # threshold matrix; you can increase size (4x4, 8x8) if you want
    # for i in range(h):
    #     for j in range(w):
    #         # tile the 2x2 matrix over the whole image
    #         thr = bayer[i % 2, j % 2]
    #         for k in range(c):

    #             if img[i, j, k]/256 >= thr:
    #                 img[i, j, k] = 255.0   # high level
    #             else:
    #                 img[i, j, k] = 0.0   # low level

    return img

def grey_dither_gpu(img_np):
    img = cp.asarray(img_np, dtype=cp.float32) / 255.0
    h, w, _ = img.shape 
    max_light = 220
    min_dark = 20

    # greyscale image
    img = (cp.maximum(img[:, :, 0] * max_light, min_dark)).astype(cp.uint8)

    # noise
    noise = cp.random.uniform(-1, 1, (h, w))
    noise_offset = (20 * noise).astype(cp.int32)
    img = cp.maximum(img.astype(cp.int32) + noise_offset, 0).astype(cp.uint8)

    bayer = np.array([[0.125, 0.625], [0.875, 0.375]])  
    # img = (img > )

    #orderd dithering
    # threshold matrix ~ maybe increase size (4x4, 8x8)
    bayer = np.array([[0.125, 0.625], [0.875, 0.375]])  
    for i in range(h):
        for j in range(w):
            # tile the 2x2 matrix over the whole image
            thr = bayer[i % 2, j % 2]
            for k in range(c):

                if img[i, j, k]/256 >= thr:
                    img[i, j, k] = 255.0   # high level
                else:
                    img[i, j, k] = 0.0   # low level

    return cp.asnumpy(img)


def main():

    img = cv2.imread("Google.png")
    
    start = time.time()
    img = grey_dither_gpu(img)
    # img = grey_dither(img)

    print(f"{time.time() - start:.4f}s")

    cv2.imshow("win", img)               # display
    cv2.waitKey(0)                       # wait for key
    cv2.destroyAllWindows()              # close window
    cv2.imwrite("out.jpg", img)   

    # cap = cv2.VideoCapture(0)
    # grey_flag = False
    # while True:
    #     ret, frame = cap.read()
    #     if not ret:
    #         break
        
    #     if cv2.waitKey(1) & 0xFF == ord('1'):
    #         grey_flag = not grey_flag

    #     if grey_flag:
    #         frame = grey_dither(frame)

    #     cv2.imshow('Webcam', frame)

    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    # cap.release()
    # cv2.destroyAllWindows()
     

if __name__ == "__main__":
    main()





