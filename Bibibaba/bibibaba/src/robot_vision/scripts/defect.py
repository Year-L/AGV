import cv2

def generate_video_stream():
    cap = cv2.VideoCapture(0)

    while True:
        res, src = cap.read()
        if not res:
            print("Failed to capture image")
            break

        # Convert image to grayscale
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        # Apply binary thresholding
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        # Morphological opening to remove noise and smooth the image
        se = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3), (-1, -1))
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, se)

        # Extract contours from the binary image
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        height, width = src.shape[:2]
        for c in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[c])
            area = cv2.contourArea(contours[c])
            # Filter out contours that do not meet the requirements
            if h > (height // 2):
                continue
            if area < 150:
                continue
            cv2.rectangle(src, (x, y), (x + w, y + h), (0, 0, 255), 1, 8, 0)
            cv2.drawContours(src, contours, c, (0, 255, 0), 2, 8)

        # Encode frame to JPEG
        ret, buffer = cv2.imencode('.jpg', src)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
