import cv2



def main():

    img = cv2.imread("Google.png")
    
    h, w, c = img.shape 
    colors = set()
    print(img[0][0])
    for i in range(h):
        for j in range(w):
            strcolor = str(img[i][j][0])+","+str(img[i][j][1])+","+str(img[i][j][2])
            if strcolor not in colors:
                print(strcolor)
                colors.add(strcolor)
                
    print(colors)


    # cv2.imshow("win", img)               # display
    # cv2.waitKey(0)                       # wait for key
    # cv2.destroyAllWindows()              # close window

    cv2.imwrite("out.jpg", img)   

     

if __name__ == "__main__":
    main()





