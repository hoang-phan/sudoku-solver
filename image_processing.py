from utils import *
import sys
import pytesseract

LINE_DETECTION_DENSITY = 0.85
WHITE_PIXEL_THRESHOLD = 50

pathImg = sys.argv[1]

img = cv2.imread(pathImg)
height = img.shape[0]
width = img.shape[1]
imgBlank = np.zeros((height, width, 3), np.uint8)
imgThreshold = preprocess(img)

contours, _ = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

biggest, _ = biggestContour(contours)

if biggest.size > 0:
  cx, cy, height, width = cv2.boundingRect(biggest)
  imgWarp = imgThreshold[cy:(cy+width), cx:(cx+height)]

  for x in range(width):
    whitePixelCount = 0

    for y in range(height):
      if imgWarp[x][y] > WHITE_PIXEL_THRESHOLD:
        whitePixelCount += 1

    if whitePixelCount > LINE_DETECTION_DENSITY * height:
      for y in range(height):
        imgWarp[x][y] = 255

  for y in range(height):
    whitePixelCount = 0

    for x in range(width):
      if imgWarp[x][y] > WHITE_PIXEL_THRESHOLD:
        whitePixelCount += 1

    if whitePixelCount > LINE_DETECTION_DENSITY * width:
      for x in range(width):
        imgWarp[x][y] = 255

  boxes = 81 * [0]

  imgWarp = np.invert(imgWarp)
  contours, _ = cv2.findContours(imgWarp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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

  custom_config = r'--psm 10 --oem 3 -c tessedit_char_whitelist=123456789'
  result = []

  for i in range(81):
    box = boxes[i]
    boxImage = imgWarp[(box[0] + 2):(box[2] - 2), (box[1] + 2):(box[3] - 2)]
    result.append(pytesseract.image_to_string(boxImage, config=custom_config).strip())

  print(",".join(result))