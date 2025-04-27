import cv2
from collections import Counter
from module import findnameoflandmark, findpostion, pause, speak, rockstar, wave, tailWag, dab
import serial
import time
import serial.tools.list_ports

arduino = None

# ======================
# SERIAL FUNCTIONS
# ======================
def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description or 'usbmodem' in port.device:
            return port.device
    return None

def setup_serial():
    global arduino
    # ls /dev/tty.* 
    port = find_arduino_port()
    if port:
        try:
            arduino = serial.Serial(port, 9600, timeout=1)
            arduino.setDTR(False)
            time.sleep(1)
            arduino.flushInput()
            arduino.setDTR(True)
            time.sleep(4)
            print(f"✅ Connected to Arduino on {port}")
        except Exception as e:
            print(f"❌ Error connecting to Arduino: {e}")
    else:
        print("❌ No Arduino port found.")

def reconnect_serial():
    global arduino
    try:
        if arduino and arduino.is_open:
            arduino.close()
    except:
        pass
    print("🔁 Attempting to reconnect...")
    setup_serial()

def wait_for_done():
    global arduino
    if arduino is None or not arduino.is_open:
        return
    start_time = time.time()
    while True:
        if arduino.in_waiting:
            line = arduino.readline().decode('utf-8').strip()
            print(f"Arduino says: {line}")
            if "Done" in line:
                break
        if time.time() - start_time > 10:
            print("⚠️ Timed out waiting for Arduino response.")
            break

def set_servo(emote):
    global arduino
    cmd = f"{emote}\n"
    try:
        if arduino is not None and arduino.is_open:
            arduino.write(cmd.encode())
            print(f"Sent to Arduino: {cmd.strip()}")
        else:
            print("⚠️ Arduino is not connected.")
            reconnect_serial()
    except Exception as e:
        print(f"❌ Error sending to Arduino: {e}")
        reconnect_serial()

# ======================
# 📷 CAMERA SETUP
# ======================
cap = cv2.VideoCapture(0)
tip = [8, 12, 16, 20]   # Index, Middle, Ring, Pinkie
processing = False

setup_serial()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame")
        continue

    frame1 = cv2.resize(frame, (640, 480))

    if not processing:
        a = findpostion(frame1)
        b = findnameoflandmark(frame1)

        if len(a) != 0 and len(b) != 0:
            finger = []
            if a[0][1:] < a[4][1:]: 
                finger.append(1)
            else:
                finger.append(0)

            fingers = []
            for id in range(4):  # Index to Pinkie
                tip_id = tip[id]
                if a[tip_id][2:] < a[tip_id - 2][2:]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            x = fingers + finger
            print(x)
            c = Counter(x)
            up = c[1]
            down = c[0]
            print(f"👆 Fingers up: {up}, 👇 Fingers down: {down}")

            # RockStar----------------------
            rock = rockstar(x)
            if rock:
                print("RoCKSTAR")
                processing = True
                set_servo("rockstar")
                processing = False
            

            # Pause----------------------
            stop = pause(x)
            if stop:
                print("PAUSE")
                processing = True
                set_servo("pause")
                processing = False

            # Wave----------------------
            waving = wave(x)
            if waving:
                print("WAVE")
                processing = True
                set_servo("wave")
                processing = False

            # tailWag----------------------
            wag = tailWag(x)
            if wag:
                print("WAGGING")
                processing = True
                set_servo("tailWag")
                processing = False

            # dab----------------------
            dab = dab(x)
            if dab:
                print("DABBING")
                processing = True
                set_servo("dab")
                processing = False
            


    cv2.imshow("Frame", frame1)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
