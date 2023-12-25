import cv2

class Coordenadas:
    def __init__(self, video_path: str):
        self.cap = cv2.VideoCapture(video_path)

        cv2.namedWindow("Frame")
        cv2.setMouseCallback("Frame", self.printcoordenadas)

        self.video()

    def printcoordenadas(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"[{x}, {y}],")

    def video(self):
        while True:
            estado, frame = self.cap.read()

            if not estado:
                break
            cv2.imshow("Frame", frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    c = Coordenadas(1)
