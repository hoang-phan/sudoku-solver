import cv2
import numpy as np

def preprocess(img):
  imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
  imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)

  return imgThreshold

def stackImages(imgArray, scale):
  rows = len(imgArray)
  cols = len(imgArray[0])

  height = imgArray[0][0].shape[0]
  width = imgArray[0][0].shape[1]

  for x in range(0, rows):
    for y in range(0, cols):
      imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
      if len(imgArray[x][y].shape) == 2:
        imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
  imgBlank = np.zeros((height, width, 3), np.uint8)
  hor = [imgBlank] * rows
  hor_con = [imgBlank] * rows
  for x in range(0, rows):
    hor[x] = np.hstack(imgArray[x])
    hor_con[x] = np.concatenate(imgArray[x])
  ver = np.vstack(hor)
  ver_con = np.concatenate(hor)
  return ver

def biggestContour(contours):
  biggest = np.array([])
  maxArea = 0
  for i in contours:
    area = cv2.contourArea(i)
    if area > 50:
      peri = cv2.arcLength(i, True)
      approx = cv2.approxPolyDP(i, 0.02 * peri, True)
      if area > maxArea and len(approx) == 4:
        biggest = approx
        maxArea = area
  return biggest, maxArea

def reorder(pts):
  pts = pts.reshape((4, 2))
  newPts = np.zeros((4, 1, 2), dtype=np.int32)
  add = pts.sum(1)
  newPts[0] = pts[np.argmin(add)]
  newPts[3] = pts[np.argmax(add)]
  diff = np.diff(pts, axis=1)
  newPts[1] = pts[np.argmin(diff)]
  newPts[2] = pts[np.argmax(diff)]
  return newPts

def splitBoxes(img):
  rows = np.vsplit(img,9)
  boxes=[]
  for r in rows:
    cols= np.hsplit(r,9)
    for box in cols:
      boxes.append(box)
  return boxes

def getBoxes(num, method="left-to-right"):
  flag = 0
  if method == "right-to-left" or method == "bottom-to-top":
    inverted = True
  if method == "top-to-bottom" or method == "bottom-to-top":
    flag = 1
  boxes = [cv2.boundingRect(c) for c in num]
  (num, boxes) = zip(*sorted(zip(num, boxes), key=lambda b:b[1][i]))
  return (num, boxes)