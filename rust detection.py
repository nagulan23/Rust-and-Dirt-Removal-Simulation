import cv2
import numpy as np
from tkinter import *
from tkinter.ttk import *
import os


tk = Tk()
animationNo = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]

def replace(img,mask):
    new_img=img.copy()
    for i in range(len(img)):
        #progress['value'] = i
        #tk.update_idletasks()
        sys.stdout.write("\r" + animation[(i*10)//len(img)]+" "+animationNo[(i*10)//len(img)])
        sys.stdout.flush()
        for j in range(len(img[0])):
            if(mask[i][j]==255):
                x=i-10 if(i-10>=0) else 0
                y=j-10 if(j-10>=0) else 0
                n=i+10 if(i+10<len(img)) else 0
                m=j+10 if(j+10<len(img[0])) else 0
                avg=[0,0,0]
                c=0
                while(x<n):
                    y1=y
                    while(y1<m):
                        if(mask[x,y1]==0 and (img[x,y1,0]!=255 and img[x,y1,1]!=255 and img[x,y1,2]!=255)):#and img[x][y1].all()!=255
                            c+=1
                            avg[0]=avg[0]+img[x,y1,0]
                            avg[1]=avg[1]+img[x,y1,1]
                            avg[2]=avg[2]+img[x,y1,2]
                        y1+=1
                    x+=1
                if(c!=0):
                    avg=[x//c for x in avg]
                    new_img[i][j]=avg
    return new_img

def remove_background(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    original = img.copy()
    mask = np.zeros(img.shape, dtype=np.uint8)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_TRIANGLE+cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:
        cv2.drawContours(mask, [c], -1, (255, 255, 255), -1)
        break

    close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=4)
    close = cv2.cvtColor(close, cv2.COLOR_BGR2GRAY)
    result = cv2.bitwise_and(original, original, mask=close)
    result[close == 0] = (255, 255, 255)
    return(result)

def resize_image(img):
    h, w = img.shape[0:2]
    print("Image original size is ",h,"x",w)
    print("Image resized size is ",h//2,"x",w//2)
    print()
    return(cv2.resize(img,(w//2,h//2)))

def rust_detect(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([30, 200, 150])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 200, 150])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    # add both masks
    mask = mask0+mask1
    print("Number of pixels depicting rust \n >> %d" % (np.sum(mask) / 255))
    print("\nProcessing image...")
    return mask




# Progress bar widget

original_img = cv2.imread("rust_old_image.png")
resized_img=resize_image(original_img)
#progress = Progressbar(tk, orient=HORIZONTAL,length=len(resized_img), mode='determinate')
#progress.pack(pady=10)
#Button(tk,text='start',command=bar).pack(pady=10)
#mainloop()
img=remove_background(resized_img)
mask=rust_detect(img)
rust_img = cv2.bitwise_and(img, img, mask=mask)
new_img=replace(img,mask)
cv2.imwrite('Original image.png', original_img)
cv2.imwrite('resized image with background.png', resized_img)
cv2.imwrite('resized image without background.png', img)
cv2.imwrite('rust area.png', mask)
cv2.imwrite('rust.png', rust_img)
cv2.imwrite('Rust removed image.png', new_img)

#cv2.imshow('Original image', original_img)
cv2.imshow('resized image with background', resized_img)
#cv2.imshow('resized image without background', img)
cv2.imshow('rust area', mask)
cv2.imshow('rust', rust_img)
cv2.imshow('Rust removed image', new_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
os.system("cls")