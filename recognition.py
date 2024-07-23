import cv2
import supervision as sv
from ultralytics import YOLOv10
import cv2
import paramiko
import serial

hostname, port = 'ev3dev.local', 22
username, password = 'robot', 'maker'


def recognize_harvest():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Не удалось захватить кадр")
            break

        results = model(frame, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(results)
        if 'pomidor' in detections.data['class_name']:
            return 'move forward'
        elif detections.data['class_name'].size != 0:
            return 'kick off'


def send_message(message):
    ser.write(message.encode('utf-8'))


def get_message():
    return ser.readline().decode('utf-8').rstrip()

print('Started!')
model = YOLOv10('best.pt')
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
print('Camera is opened')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, port, username, password)
print('Connected to ev3 - now there is silence')
client.exec_command('python3 detection.py', timeout=0)
client.close()

ser = serial.Serial('/dev/ttyS0', 9600)

try:
    while True:
        message = get_message()
        if message == 'detected':
            result = recognize_harvest()
            send_message(result)
except KeyboardInterrupt: 
    cap.release()
    print('Finished!')
except SystemExit:
    cap.release()
    print('Finished!')