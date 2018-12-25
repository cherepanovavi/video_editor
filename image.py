import cv2


class Image:
    def __init__(self, file_path):
        capture = cv2.VideoCapture(file_path)
        ret, frame = capture.read()
        self.data = frame
