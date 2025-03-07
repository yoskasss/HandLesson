import cv2
from cvzone.HandTrackingModule import HandDetector
import time

class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.detector = HandDetector(detectionCon=0.5, maxHands=2)  # maxHands=2, iki el için
        self.start_time = None
        self.totalFingers = 0
        self.cap = self.video

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, img = self.cap.read()
        if not success:
            return None

        img = cv2.flip(img, 1)  # Görüntüyü yatayda çevir

        # El tespiti yapıyoruz
        hands, img = self.detector.findHands(img)

        if hands:
            self.totalFingers = 0  # Toplam parmak sayısını sıfırla

            for hand in hands:  # Her iki eldeki parmakları kontrol et
                fingers = self.detector.fingersUp(hand)  # Parmakları say
                self.totalFingers += sum(fingers)  # Toplam parmak sayısını artır
                finger = self.totalFingers

           
            if self.start_time is None:
                self.start_time = time.time()

            elapsed_time = time.time() - self.start_time

        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
