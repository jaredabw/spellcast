import cv2
import numpy as np
import pytesseract
from scipy import stats
from PIL import ImageGrab

def get_image():
    pil_im = ImageGrab.grabclipboard()
    if pil_im is None:
        return None
    return cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

def parse_game(im):
    ## read image and convert to binary
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

    xywh = [cv2.boundingRect(c) for c in contours]

    for i, _ in enumerate(contours):
        if i in outlier_i:
            continue

        x, y, w, h = xywh[i]
        if np.abs(w - h) > 0.2*w:
            continue

        s = int(0.15*w)
        si = int(0.05*w) + s

        x_nudge = -int(0.1*w)
        y_nudge = -int(0.2*h)

        cropped_img = im_bw[y+s-y_nudge:y+h-s, x+si-x_nudge:x+w-si]

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

def draw_path(im, path, return_im=False, y_offset=0):
    temp_im = im.copy()
    overlay = temp_im.copy()
    scale = (temp_im.shape[0]-y_offset)/5.7

    path = [(int(x*scale), int(y*scale)+y_offset) for y, x in path]

    for i in range(len(path) - 1):
        cv2.line(overlay, path[i], path[i+1], (133, 109, 194), 8)

    cv2.circle(overlay, path[0], 3, (82, 125, 61), 8)
    if path[0] != path[-1]:
        cv2.circle(overlay, path[-1], 3, (122, 73, 48), 8)

    a = 0.9
    image_new = cv2.addWeighted(overlay, a, temp_im, 1-a, 0) 

    if return_im:
        return image_new
    else:
        cv2.imshow("Path", image_new)
        cv2.waitKey(0)

def generate_video(im, possible_words):
    im = cv2.copyMakeBorder(im, 60, 0, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    font = cv2.FONT_HERSHEY_SIMPLEX
    pt = 1.5
    thk = 4
    white = (255, 255, 255)

    video = cv2.VideoWriter('solutions.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 24, (im.shape[1], im.shape[0]), True)

    for word in possible_words:
        temp_im = im.copy()
        width = temp_im.shape[1]

        temp_im = cv2.putText(temp_im, str(word[0].upper()), (int(width//26.1), 45), font, pt, white, thk)
        temp_im = cv2.putText(temp_im, str(word[1]), (int(width//1.2), 45), font, pt, white, thk)

        temp_im = draw_path(temp_im, word[2], return_im=True, y_offset=60)

        video.write(temp_im)

    video.release()

if __name__ == "__main__":
    im = get_image()
    print(parse_game(im))