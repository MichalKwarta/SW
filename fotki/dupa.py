import cv2 

camera = cv2.VideoCapture(2)
_,img = camera.read()

for i in range(10):
    cv2.imwrite(f'{i}doswietloneggora.jpg',img)
