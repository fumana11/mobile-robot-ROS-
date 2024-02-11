#!/usr/bin/env python
import cv2
import numpy as np

# Fungsi yang akan dipanggil ketika nilai trackbar berubah
def on_trackbar_change(x):
    pass

# Fungsi untuk mendeteksi dua warna yang berbeda dan menghitung pusat massa
def detect_colors(image, lower_color1, upper_color1, lower_color2, upper_color2):
    # Konversi gambar ke format HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Membuat mask untuk warna pertama
    mask1 = cv2.inRange(hsv, lower_color1, upper_color1)

    hasil1 = cv2.bitwise_and(image,image, mask = mask1)

    # Membuat mask untuk warna kedua
    mask2 = cv2.inRange(hsv, lower_color2, upper_color2)
    hasil2 = cv2.bitwise_and(image,image, mask = mask2)

    # Menghitung momen untuk mask1
    moments1 = cv2.moments(mask1)
    if moments1["m00"] != 0:
        cX1 = int(moments1["m10"] / moments1["m00"])
        cY1 = int(moments1["m01"] / moments1["m00"])
        cv2.circle(image, (cX1, cY1), 5, (0, 0, 255), -1)
    else:
        cX1, cY1 = None, None

    # Menghitung momen untuk mask2
    moments2 = cv2.moments(mask2)
    if moments2["m00"] != 0:
        cX2 = int(moments2["m10"] / moments2["m00"])
        cY2 = int(moments2["m01"] / moments2["m00"])
        cv2.circle(image, (cX2, cY2), 5, (0, 255, 0), -1)
    else:
        cX2, cY2 = None, None

    return image, (cX1, cY1), (cX2, cY2),hasil1, hasil2

# Inisialisasi VideoCapture untuk feed kamera (0 adalah kamera default)
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

# Tentukan nilai awal untuk batas warna pertama dan kedua dalam format HSV
hue_min1, saturation_min1, value_min1 = 0, 50, 50
hue_max1, saturation_max1, value_max1 = 30, 255, 255

hue_min2, saturation_min2, value_min2 = 150, 50, 50
hue_max2, saturation_max2, value_max2 = 179, 255, 255

# Buat jendela OpenCV
cv2.namedWindow('Deteksi Warna')

# Buat trackbar untuk nilai HSV warna pertama
cv2.createTrackbar('Hue Min 1', 'Deteksi Warna', hue_min1, 179, on_trackbar_change)
cv2.createTrackbar('Hue Max 1', 'Deteksi Warna', hue_max1, 179, on_trackbar_change)
cv2.createTrackbar('Saturation Min 1', 'Deteksi Warna', saturation_min1, 255, on_trackbar_change)
cv2.createTrackbar('Saturation Max 1', 'Deteksi Warna', saturation_max1, 255, on_trackbar_change)
cv2.createTrackbar('Value Min 1', 'Deteksi Warna', value_min1, 255, on_trackbar_change)
cv2.createTrackbar('Value Max 1', 'Deteksi Warna', value_max1, 255, on_trackbar_change)

# Buat trackbar untuk nilai HSV warna kedua
cv2.createTrackbar('Hue Min 2', 'Deteksi Warna', hue_min2, 179, on_trackbar_change)
cv2.createTrackbar('Hue Max 2', 'Deteksi Warna', hue_max2, 179, on_trackbar_change)
cv2.createTrackbar('Saturation Min 2', 'Deteksi Warna', saturation_min2, 255, on_trackbar_change)
cv2.createTrackbar('Saturation Max 2', 'Deteksi Warna', saturation_max2, 255, on_trackbar_change)
cv2.createTrackbar('Value Min 2', 'Deteksi Warna', value_min2, 255, on_trackbar_change)
cv2.createTrackbar('Value Max 2', 'Deteksi Warna', value_max2, 255, on_trackbar_change)

while True:
    # Baca frame dari feed kamera
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.resize(frame,(360,310))
    cv2.imshow('Frame Asli', frame)
    # Dapatkan nilai trackbar saat ini
    hue_min1 = cv2.getTrackbarPos('Hue Min 1', 'Deteksi Warna')
    hue_max1 = cv2.getTrackbarPos('Hue Max 1', 'Deteksi Warna')
    saturation_min1 = cv2.getTrackbarPos('Saturation Min 1', 'Deteksi Warna')
    saturation_max1 = cv2.getTrackbarPos('Saturation Max 1', 'Deteksi Warna')
    value_min1 = cv2.getTrackbarPos('Value Min 1', 'Deteksi Warna')
    value_max1 = cv2.getTrackbarPos('Value Max 1', 'Deteksi Warna')

    hue_min2 = cv2.getTrackbarPos('Hue Min 2', 'Deteksi Warna')
    hue_max2 = cv2.getTrackbarPos('Hue Max 2', 'Deteksi Warna')
    saturation_min2 = cv2.getTrackbarPos('Saturation Min 2', 'Deteksi Warna')
    saturation_max2 = cv2.getTrackbarPos('Saturation Max 2', 'Deteksi Warna')
    value_min2 = cv2.getTrackbarPos('Value Min 2', 'Deteksi Warna')
    value_max2 = cv2.getTrackbarPos('Value Max 2', 'Deteksi Warna')

    # Tentukan batas warna dalam format HSV
    lower_color1 = np.array([hue_min1, saturation_min1, value_min1])
    upper_color1 = np.array([hue_max1, saturation_max1, value_max1])

    lower_color2 = np.array([hue_min2, saturation_min2, value_min2])
    upper_color2 = np.array([hue_max2, saturation_max2, value_max2])

    # Deteksi warna dan hitung pusat massa
    result, (cX1, cY1), (cX2, cY2),hasil1,hasil2 = detect_colors(frame, lower_color1, upper_color1, lower_color2, upper_color2)

    # Tampilkan gambar hasil
    #cv2.imshow('Deteksi Warna', result)
    cv2.imshow('belakang', hasil1)
    cv2.imshow('depan', hasil2)

    # Tampilkan pusat massa
    if cX1 is not None and cY1 is not None:
        cv2.circle(frame, (cX1, cY1), 5, (0, 0, 255), -1)
    if cX2 is not None and cY2 is not None:
        cv2.circle(frame, (cX2, cY2), 5, (0, 255, 0), -1)

    # Tampilkan frame asli dengan pusat massa
    cv2.imshow('Frame koordinat', frame)

    # Tombol 'q' untuk keluar dari loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tutup kamera dan jendela OpenCV
cap.release()
cv2.destroyAllWindows()
