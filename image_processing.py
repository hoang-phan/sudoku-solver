from utils import *
import sys
import pytesseract

pathImg = sys.argv[1]
width = 450
height = 450

img = cv2.imread(pathImg)
img = cv2.resize(img, (width, height))
imgBlank = np.zeros((height, width, 3), np.uint8)
imgThreshold = preprocess(img)

imgContours = img.copy()
imgBigContour = img.copy()
contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)

biggest, maxArea = biggestContour(contours)

if biggest.size > 0:
  biggest = reorder(biggest)
  # cv2.drawContours(imgBigContour, biggest, -1, (255, 0, 0), 25)
  pts1 = np.float32(biggest)
  pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
  matrix = cv2.getPerspectiveTransform(pts1, pts2)
  imgWarpColored = cv2.warpPerspective(img, matrix, (width, height))
  imgWarp = cv2.warpPerspective(cv2.cvtColor(imgThreshold, cv2.COLOR_GRAY2BGR), matrix, (width, height))
  imgWarp = cv2.cvtColor(imgWarp, cv2.COLOR_BGR2GRAY)

  boxes = splitBoxes(imgWarp)

  for x in range(width):
    whitePixelCount = 0

    for y in range(height):
      if imgWarp[x][y] > 50:
        whitePixelCount += 1

    if whitePixelCount > 400:
      for y in range(height):
        imgWarp[x][y] = 255

  for y in range(height):
    whitePixelCount = 0

    for x in range(width):
      if imgWarp[x][y] > 50:
        whitePixelCount += 1

    if whitePixelCount > 400:
      for x in range(width):
        imgWarp[x][y] = 255

  boxes = 81 * [0]

  imgWarp = np.invert(imgWarp)
  contours, hierarchy = cv2.findContours(imgWarp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  for contour in contours:
    area = cv2.contourArea(contour)
    if area > 1000:
      cx, cy, w, h = cv2.boundingRect(contour)
      midX = cx + w // 2
      midY = cy + h // 2
      x = midX // (width // 9)
      y = midY // (height // 9)
      boxes[x * 9 + y] = [cx, cy, cx + w, cy + h]

  custom_config = r'--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'
  result = []

  for box in boxes:
    boxImage = imgWarp[(box[0] + 2):(box[2] - 2), (box[1] + 2):(box[3] - 2)]
    result.append(pytesseract.image_to_string(boxImage, config=custom_config).strip())

  print(",".join(result))