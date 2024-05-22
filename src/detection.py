import hashlib
import cv2
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, frame, confidence_threshold=0.85):
        results = self.model.predict(frame, conf=confidence_threshold, verbose=False)
        return results[0].boxes.data.tolist()

class OrbTracker:
    def __init__(self, tracking_frames=5):
        self.tracking_frames = tracking_frames
        self.prev_keypoints = None
        self.tracking_counter = 0

    def track(self, frame, lava_lamp_box):
        x, y, w, h = map(int, lava_lamp_box)
        lava_lamp_roi = frame[y:y+h, x:x+w]
        lava_lamp_roi = cv2.resize(lava_lamp_roi, (256, 256))
        gray = cv2.cvtColor(lava_lamp_roi, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (11, 11), 0)
        orb = cv2.ORB_create()
        keypoints, descriptors = orb.detectAndCompute(blurred, None)
        self.prev_keypoints = keypoints
        return keypoints

class LavaLampRandomGenerator:
    def __init__(self, video_source=0, model_path="custom_model.pt", tracking_frames=5, confidence_threshold=0.7):
        self.video_source = video_source
        self.model_path = model_path
        self.tracking_frames = tracking_frames
        self.confidence_threshold = confidence_threshold
        self.object_detector = ObjectDetector(model_path)
        self.fast_tracker = OrbTracker(tracking_frames)

    def display_only(self):
        cap = cv2.VideoCapture(self.video_source)
        if not cap.isOpened():
            print("Failed to open the camera.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            detections = self.object_detector.detect(frame, self.confidence_threshold)
            for detection in detections:
                x, y, w, h = map(int, detection[:4])
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Lava Lamp", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            cv2.imshow("Lava Lamp Detection", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('y'):
                cap.release()
                cv2.destroyAllWindows()
                return True
            elif key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return False

    def generate_random_number(self, blob_data, min_value=0, max_value=16000):
        # Ensure blob_data provides sufficient entropy
        blob_string = ''.join(str(x) for x in blob_data)

        # Hash the concatenated string using SHA-256
        hash_value = hashlib.sha256(blob_string.encode()).hexdigest()
        hash_int = int(hash_value, 16)

        # Use rejection sampling to avoid bias
        range_size = max_value - min_value + 1
        while True:
            random_number = hash_int % range_size
            if random_number < range_size:
                break
            hash_value = hashlib.sha256(hash_value.encode()).hexdigest()
            hash_int = int(hash_value, 16)

        return min_value + random_number

    def get_blob_data(self):
        cap = cv2.VideoCapture(self.video_source)
        if not cap.isOpened():
            print("Failed to open the camera.")
            return None

        ret, frame = cap.read()
        if not ret:
            return None

        detections = self.object_detector.detect(frame, confidence_threshold=self.confidence_threshold)
        blob_data = []
        for detection in detections:
            x, y, w, h, conf, class_id = detection
            if int(class_id) == 0:
                keypoints = self.fast_tracker.track(frame, [x, y, w, h])
                if keypoints:
                    for kp in keypoints:
                        blob_data.extend([kp.pt[0], kp.pt[1], kp.size])

        cap.release()
        return blob_data