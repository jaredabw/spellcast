import cv2
import numpy as np
import pytesseract
from scipy import stats

def parse_game(file_path):
    ## read image and convert to binary
    im = cv2.imread(file_path)
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
    _, im_bw = cv2.threshold(im_gray, 250, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    ##

    ## find contours
    contours, _ = cv2.findContours(im_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = list(contours)
    contours.reverse()
    ##

    ## for use in loop
    dilate_kernel = np.ones((3, 3), np.uint8)
    letters = []
    ##

    ## filter out outliers
    areas = [cv2.contourArea(c) for c in contours]
    
    threshold = 2
    z = np.abs(stats.zscore(areas))
    
    outlier_i = np.where(z > threshold)[0]
    ##

    mean = np.mean(areas)

    xywh = [cv2.boundingRect(c) for c in contours]

    for i, _ in enumerate(contours):
        if i in outlier_i:
            continue

        x, y, w, h = xywh[i]
        if np.abs(w - h) > 0.2*w:
            continue

        s = int(0.22*w)
        si = int(0.08*w) + s

        x_nudge = int(0.05*w)
        if np.abs(areas[i] - mean) > 0.1*mean:
            x_nudge = -int(0.1*w)

        cropped_img = im_bw[y+s:y+h-s, x+si-x_nudge:x+w-si]

        dilated = cv2.dilate(cropped_img, dilate_kernel)

        # cv2.imwrite(f"img/{i}.png", dilated)

        config = "-psm 10"
        text: str = pytesseract.image_to_string(dilated, config=config).rstrip()
        
        # common mistakes
        if text == "/": text = "B"
        if text == "0": text = "O"

        centerx = x + w//2
        centery = y + h//2
        letters.append((text, (centerx, centery)))

    letters = sorted(letters, key=lambda x: (x[1][1], x[1][0]))
    letters = [l for l in letters if l[0] != ""]
    plain_letters = "".join([l[0] for l in letters])
    
    width_mode = stats.mode([w for _, _, w, _ in xywh]).mode

    bonuses = {}
    bonuses["x2"] = None
    bonuses["dl"] = None
    bonuses["tl"] = None

    for bonus in ("x2", "dl", "tl"):
        bonus_img = cv2.imread(f"img/{bonus}.png")

        result = cv2.matchTemplate(im, bonus_img, cv2.TM_SQDIFF_NORMED)
        diff, _, location, _ = cv2.minMaxLoc(result)

        if diff < 0.4:
            bx, by = bonus_img.shape[:2]

            lx = location[0] + bx//2
            ly = location[1] + by//2

            if bonus == "x2":
                lx -= int(0.8*width_mode)

            location = (lx, ly)
            for j, l in enumerate(letters):
                if np.abs(l[1][0] - lx) < 0.5*width_mode and np.abs(l[1][1] - ly) < 0.5*width_mode:
                    r = j//5 + 1
                    c = j - r*5 + 6
                    coords = (r, c)
                    bonuses[bonus] = coords

    return plain_letters, bonuses

if __name__ == "__main__":
    print(parse_game("img/image.png"))