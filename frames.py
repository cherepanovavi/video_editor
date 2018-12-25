import cv2


class Frames:
    def __init__(self, **kwargs):
        if 'file_path' in kwargs.keys():
            capture = cv2.VideoCapture(kwargs['file_path'])
            self.data = []
            self.get_fragments(capture)
            # Find OpenCV version
            (major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')

            if int(major_ver) < 3:
                self.fps = capture.get(cv2.cv.CV_CAP_PROP_FPS)
            else:
                self.fps = capture.get(cv2.CAP_PROP_FPS)
        else:
            self.data = kwargs['data']
            self.fps = kwargs['fps']

    def get_fragments(self, capture):
        ret = True
        while (ret):
            # Capture frame-by-frame
            ret, frame = capture.read()
            self.data.append(frame)


