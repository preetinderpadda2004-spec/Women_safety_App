# video_record.py
import cv2
import datetime

def record_video():
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    filename = f"alert_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    print(f"🎥 Recording started: {filename}")
    start_time = datetime.datetime.now()

    while (datetime.datetime.now() - start_time).seconds < 10:  # 10 seconds video
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        cv2.imshow('Recording', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"✅ Video saved: {filename}")

if __name__ == "__main__":
    record_video()
