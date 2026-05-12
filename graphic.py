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

def grey_dither_gpu(img_np, noise_offset):
    img = cp.asarray(img_np, dtype=cp.float32) / 255.0
    h, w, _ = img.shape 
    max_light = 250
    min_dark = 10

    # greyscale image
    img = (cp.maximum(img[:, :, 0] * max_light, min_dark)).astype(cp.uint8)

    # noise
    img = cp.maximum(img.astype(cp.int32) + noise_offset, 0).astype(cp.uint8)

    # bayer dither
    bayer = cp.array([[0.125, 0.625], 
                      [0.875, 0.375]])  
    bayer_tiled = cp.tile(bayer, (h // 2 + 1, w // 2 + 1))[:h, :w]
    img = (img / 256 >= bayer_tiled).astype(cp.uint8) * 255

    return cp.asnumpy(img)


def main():


    # img = cv2.imread("Google.png")
    
    # start = time.time()
    # img = grey_dither_gpu(img)
    # # img = grey_dither(img)

    # print(f"{time.time() - start:.4f}s")

    # cv2.imshow("win", img)               # display
    # cv2.waitKey(0)                       # wait for key
    # cv2.destroyAllWindows()              # close window
    # cv2.imwrite("out.jpg", img)   


    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Webcam', cv2.WINDOW_KEEPRATIO)
    ret, frame = cap.read()
    h, w, _ = frame.shape
    noise = cp.random.uniform(-1, 1, (h, w))
    noise_offset = (30 * noise).astype(cp.int32)

    frame_rate = 1/6 # fps
    while True:
        start = time.time()

        ret, frame = cap.read()
        if not ret:
            break
        
        frame = grey_dither_gpu(frame, noise_offset)
        cv2.imshow('Webcam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.getWindowProperty('Webcam', cv2.WND_PROP_VISIBLE) < 1:
            break

        delta = float(time.time() - start)
        # print(f"{frame_rate - delta} | {frame_rate} - {delta}")
        time.sleep(max(0, frame_rate - delta))

    cap.release()
    cv2.destroyAllWindows()
     

if __name__ == "__main__":
    main()





