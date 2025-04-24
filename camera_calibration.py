import cv2
import numpy as np
from picamera2 import Picamera2

square_size = 10.15      # 正方形の1辺のサイズ[cm]
pattern_size = (7, 7)  # 交差ポイントの数

reference_img = 200 # 参照画像の枚数

pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
pattern_points *= square_size
objpoints = []
imgpoints = []

# Picamera2でカメラ初期化
picam2 = Picamera2()
picam2.start()

while len(objpoints) < reference_img:
    # 画像の取得
    img = picam2.capture_array()
    height, width = img.shape[:2]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # チェスボードのコーナーを検出
    ret, corner = cv2.findChessboardCorners(gray, pattern_size)
    if ret:
        print("detected corner!")
        print(str(len(objpoints)+1) + "/" + str(reference_img))
        term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
        cv2.cornerSubPix(gray, corner, (5,5), (-1,-1), term)
        imgpoints.append(corner.reshape(-1, 2))
        objpoints.append(pattern_points)

    # 画像表示（GUI環境が必要。Liteの場合はコメントアウト）
    cv2.imshow('image', img)
    if cv2.waitKey(200) & 0xFF == ord('q'):
        break

print("calculating camera parameter...")
# 内部パラメータを計算
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# 計算結果を保存
np.save("mtx", mtx)
np.save("dist", dist.ravel())
# 計算結果を表示
print("RMS = ", ret)
print("mtx = \n", mtx)
print("dist = ", dist.ravel())

cv2.destroyAllWindows()
