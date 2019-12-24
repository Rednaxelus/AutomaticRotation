import glob
import pathlib
import numpy as np
import imutils
import cv2
import re
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Alex\AppData\Local\Tesseract-OCR\tesseract'

imageFileEnding = "jpg"
dirnameIn = 'INPUT'
dirnameOut = 'OUTPUT'

pathlib.Path(dirnameOut).mkdir(parents=True, exist_ok=True)

filePaths = "*." + imageFileEnding

if dirnameIn:
    filePaths = dirnameIn + "/" + filePaths

fileNames = []

print(filePaths)

images = []

for file in glob.glob(filePaths):
    images.append(cv2.imread(file, cv2.IMREAD_COLOR))
    fileNames.append(file[len(dirnameIn)+1:])

print("how many images: " + str(len(images)))
print("All the images: " + str(fileNames))


def unsharp_mask(image2, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    """Return a sharpened version of the image, using an unsharp mask."""
    blurred = cv2.GaussianBlur(image2, kernel_size, sigma)
    sharpened = float(amount + 1) * image2 - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image2 - blurred) < threshold
        np.copyto(sharpened, image2, where=low_contrast_mask)
    return sharpened


for image in images:
    image = unsharp_mask(image)

    newdata = pytesseract.image_to_osd(image, lang="equ+eng+deu")
    print(newdata)
    info = int(re.search('(?<=Orientation in degrees: )\d+', newdata).group(0))
    print("----------------------", info)

   # cv2.imshow("before", image)
    #cv2.waitKey(0)

    image = imutils.rotate_bound(image, info)

    imageName = "RESULT_" + fileNames.pop(0)
    cv2.imwrite(os.path.join(dirnameOut, imageName), image)

   # cv2.imshow("Rotated (Correct)", image)
    #cv2.waitKey(0)
