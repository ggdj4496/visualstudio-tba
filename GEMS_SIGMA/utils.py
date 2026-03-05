import cv2
def process_sigma(i, o):
    img = cv2.imread(i)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th = cv2.adaptiveThreshold(cv2.medianBlur(gray, 5), 255, 1, 1, 11, 2)
    ct, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    with open(o, 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{img.shape[1]}" height="{img.shape[0]}">')
        [f.write(f'<path d="M ' + ' '.join([f'{p[0][0]},{p[0][1]}' for p in c]) + ' Z" fill="none" stroke="black"/>') for c in ct if cv2.contourArea(c) > 50]
        f.write('</svg>')
