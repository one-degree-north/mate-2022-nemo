import cv2
import numpy as np

def main(source):
    cap = cv2.VideoCapture(source)
    if cap.isOpened() == False: 
        print("Error opening video stream or file")


    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('Frame',frame)
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else: 
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    camera_number = int(input("Camera number: "))
    main(camera_number)
