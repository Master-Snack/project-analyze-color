import pandas as pd
import numpy as np
import cv2
import argparse

# phân tích hình ảnh đầu vào
app = argparse.ArgumentParser()
app.add_argument('-i', '--image', required=True, help="Image Path")
b = vars(app.parse_args())
img_path = b['image']

#đọc thông tin hình ảnh
img = cv2.imread(img_path)

#khai báo các biến toàn cục(dùng cho sau này)
clicked = False
r = g = b = xpos = ypos = 0 #các màu sắc tương ứng

#đọc dữ liệu từ file csv và đặt tên cho các data
index = ["color", "color_name", "hex", "R", "G", "B"]
data = pd.read_csv("colors.csv", names=index, header=None)

# tạo hàm để lấy khoảng cách giữa các màu và lấy màu phù hợp nhất
def color(R,G,B):
    minimum = 10000
    for i in range(len(data)):
        d = abs(R- int(data.loc[i,"R"])) + abs(G- int(data.loc[i,"G"]))+ abs(B- int(data.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = data.loc[i,"color_name"]
    return cname

# tạo hàm để lấy tọa độ x, y trong hình ảnh đưa vào sau đó double click
def draw_color(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
    
# làm việc với đối tượng
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_color)

while(1):

    cv2.imshow("image", img)
    if(clicked):
        #đối tượng(hình ảnh, điểm bắt đầu, điểm cuối, màu sắc, độ dày)
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

        #tạo nơi để hiển thị (tên ảnh , kích thuowgns các loại màu sắc)
        text = color(r,g,b) + 'Red='+ str(r) +  ' Green='+ str(g) +  'Blue='+ str(b)

        #setup cho văn bản(bào gồm: hình ảnh, văn bản, bắt đầu, font chữ(0-7), fontScale, màu sắc, độ dày, in đậm)
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        #đối với màu nhạt thì mặc định nó là màu đen
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
        
        clicked = False
    # thoát vòng lặp khi ấn "esc" key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
