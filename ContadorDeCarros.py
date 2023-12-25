import cv2
import torch
import numpy as np
import matplotlib.path as plt

coordenadas = np.array([
    [17, 17],
    [626, 17],
    [626, 459],
    [15, 456]
])

def obtenerCentro(bbox):
    centro = ((bbox[0]+bbox[2])//2,(bbox[1]+bbox[3]//2))
    return centro

def cargarModelo():
    modelo = torch.hub.load("ultralytics/yolov5", model="yolov5x", pretrained=True)
    return modelo

def Obtenerbboxes(preds: object):

    df = preds.pandas().xyxy[0]
    df = df[df["confidence"] >= 0.5]
    df = df[df["name"] == "car"]
    return df[["xmin","ymin","xmax","ymax"]].values.astype(int)

def DeteccionValida(xc, yc):
    return plt.Path(coordenadas).contains_point((xc, yc))

def Detector(cap: object):
    modelo = cargarModelo()

    while cap.isOpened():
        estado, frame = cap.read()
        if not estado:
            break
        preds = modelo(frame)
        bboxes = Obtenerbboxes(preds)

        deteccion = 0
        for box in bboxes:
            xc, yc = obtenerCentro(box)

            if DeteccionValida(xc, yc):
                deteccion += 1

            cv2.circle(img=frame, center=(xc, yc), radius=5, color=(0,255,0), thickness=-1)
            cv2.rectangle(img=frame, pt1=(box[0], box[1]), pt2=(box[2], box[3]), color=(255, 0, 0), thickness=1)

        cv2.putText(img=frame, text=f"Carros Detectados: {deteccion}", org=(100,100), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(243,239,238), thickness=3)
        cv2.polylines(img=frame, pts=[coordenadas], isClosed=True, color=(0,0,255), thickness=4)

        cv2.imshow("frame", frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()

if __name__ == '__main__':
    cap = cv2.VideoCapture(1)
    Detector(cap)
