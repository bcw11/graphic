import cv2
import numpy as np

def main():

    img = cv2.imread("Google.png")
    
    h, w, c = img.shape 
    print(img[0][0])
    for i in range(h):
        for j in range(w):
            color = max(200*round(int(img[i][j][0])/255), 20)
            img[i][j] = np.array([color, color, color])


    cv2.imshow("win", img)               # display
    cv2.waitKey(0)                       # wait for key
    cv2.destroyAllWindows()              # close window

    cv2.imwrite("out.jpg", img)   

     

if __name__ == "__main__":
    main()





