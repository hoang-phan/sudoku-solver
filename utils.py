import cv2
import numpy as np
import pytesseract

LINE_DETECTION_DENSITY = 0.85
WHITE_PIXEL_THRESHOLD = 50
TESSERACT_CONFIG = r'--psm 10 --oem 3 -c tessedit_char_whitelist=123456789'

def preprocess(img):
  imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
  imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)

  return imgThreshold

def biggestContour(contours):
  biggest = np.array([])
  max_area = 0
  for i in contours:
    area = cv2.contourArea(i)
    if area > 50:
      peri = cv2.arcLength(i, True)
      approx = cv2.approxPolyDP(i, 0.02 * peri, True)
      if area > max_area and len(approx) == 4:
        biggest = approx
        max_area = area
  return biggest,max_area

def solidifyGrid(img, width, height):
  for x in range(width):
    whitePixelCount = 0

    for y in range(height):
      if img[x][y] > WHITE_PIXEL_THRESHOLD:
        whitePixelCount += 1

    if whitePixelCount > LINE_DETECTION_DENSITY * height:
      for y in range(height):
        img[x][y] = 255

  for y in range(height):
    whitePixelCount = 0

    for x in range(width):
      if img[x][y] > WHITE_PIXEL_THRESHOLD:
        whitePixelCount += 1

    if whitePixelCount > LINE_DETECTION_DENSITY * width:
      for x in range(width):
        img[x][y] = 255

  return img

def contoursToBoxes(contours, width, height):
  boxes = 81 * [0]
  areaThresold = (width * height) / 81 / 2

  for contour in contours:
    area = cv2.contourArea(contour)
    if area > areaThresold:
      cx, cy, w, h = cv2.boundingRect(contour)
      midX = cx + w // 2
      midY = cy + h // 2
      x = midX // (width // 9)
      y = midY // (height // 9)
      boxes[x * 9 + y] = [cx, cy, cx + w, cy + h]

  return boxes

def getSudoku(img, boxes):
  result = []

  for i in range(81):
    box = boxes[i]
    boxImage = img[(box[0] + 2):(box[2] - 2), (box[1] + 2):(box[3] - 2)]
    result.append(pytesseract.image_to_string(boxImage, config=TESSERACT_CONFIG).strip())

  return ",".join(result)
