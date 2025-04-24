# カメラで動画を撮る
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.start_and_record_video("test.mp4", duration=10)  # 10秒間録画
