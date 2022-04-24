from utils import *
import sys

pathImg = sys.argv[1]

img = cv2.imread(pathImg)
imgThreshold = preprocess(img)

contours, _ = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

biggest, _ = biggestContour(contours)

if biggest.size > 0:
  cx, cy, height, width = cv2.boundingRect(biggest)
  imgWarp = imgThreshold[cy:(cy+width), cx:(cx+height)]
  imgWarp = solidifyGrid(imgWarp, width, height)
  imgWarp = np.invert(imgWarp)

  contours, _ = cv2.findContours(imgWarp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  boxes = contoursToBoxes(contours, width, height)

  print(getSudoku(imgWarp, boxes))
