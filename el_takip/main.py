import math
import sys

import cv2
import mediapipe as mp
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6,
)

# Parmak uç noktaları:
TIP_IDS = [4, 8, 12, 16, 20]


# Parmak sayma

def mesafe(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def parmaklari_say(lm):
    acik = []

    if mesafe(lm[4], lm[17]) > mesafe(lm[3], lm[17]):
        acik.append(1)
    else:
        acik.append(0)

    # Diğer 4 parmak:
    for tip in TIP_IDS[1:]:
        if lm[tip].y < lm[tip - 2].y:
            acik.append(1)
        else:
            acik.append(0)

    return acik


#ses kontrolü

class SesKontrol:

    def __init__(self):
        self.volume = None
        self.son_deger = -1
        try:
            cihaz = AudioUtilities.GetSpeakers()
            if hasattr(cihaz, "EndpointVolume"):
                self.volume = cihaz.EndpointVolume
            else:
                from ctypes import POINTER, cast
                arayuz = cihaz.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                self.volume = cast(arayuz, POINTER(IAudioEndpointVolume))
        except Exception as hata:
            print(f"Ses cihazına erişilemedi ({hata}): sistem sesi değiştirilmeyecek, sadece ekranda gösterilecek.")

    def ayarla(self, yuzde):
        if yuzde == self.son_deger or self.volume is None:
            return
        self.son_deger = yuzde
        try:
            self.volume.SetMasterVolumeLevelScalar(yuzde / 100, None)
        except Exception:
            pass


# Ana program

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Kamera açılamadı!")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

    ses = SesKontrol()
    ses_yuzde = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            print("Görüntü alınamadı.")
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        sonuc = hands.process(rgb)

        parmak_sayisi = 0

        if sonuc.multi_hand_landmarks:
            for el in sonuc.multi_hand_landmarks:

                mp_draw.draw_landmarks(
                    frame,
                    el,
                    mp_hands.HAND_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=4),
                    mp_draw.DrawingSpec(color=(0, 200, 0), thickness=2),
                )

                acik = parmaklari_say(el.landmark)
                parmak_sayisi = sum(acik)

                h, w, _ = frame.shape
                for i, tip in enumerate(TIP_IDS):
                    if acik[i]:
                        cx = int(el.landmark[tip].x * w)
                        cy = int(el.landmark[tip].y * h)
                        cv2.circle(frame, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
            ses_yuzde = parmak_sayisi * 20
            ses.ayarla(ses_yuzde)

        #Ekran bilgileri
        cv2.rectangle(frame, (10, 10), (260, 110), (30, 30, 30), cv2.FILLED)
        cv2.putText(frame, f"Parmak: {parmak_sayisi}", (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 0), 3)
        cv2.putText(frame, f"Ses: %{ses_yuzde}", (20, 98),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # Ses çubuğu
        h, w, _ = frame.shape
        bar_x, bar_ust, bar_alt = w - 60, 100, h - 60
        dolu_y = int(bar_alt - (bar_alt - bar_ust) * ses_yuzde / 100)
        cv2.rectangle(frame, (bar_x, bar_ust), (bar_x + 30, bar_alt), (255, 255, 255), 2)
        cv2.rectangle(frame, (bar_x, dolu_y), (bar_x + 30, bar_alt), (0, 200, 0), cv2.FILLED)

        cv2.imshow("El Takibi", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()

if __name__ == "__main__":
    main()
