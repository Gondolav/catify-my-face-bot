import cv2

# Load the cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Load the cat image
cat_img = cv2.imread('cat.jpeg')


def replace_faces(filename):
    '''
    Replaces the faces in the image specified by the given filename with a cat face.
    
    Returns true if at least one face was detected and replaced, false otherwise
    '''

    # Read the image
    img = cv2.imread(filename)

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray)

    if len(faces) == 0:
        return False

    # Replace faces with the cat face
    for (x, y, w, h) in faces:
        cat_img_resized = cv2.resize(
            cat_img, (w, h), interpolation=cv2.INTER_AREA)
        img[y:y+h, x:x+w, :] = cat_img_resized

    # Save the output
    cv2.imwrite(f'{filename.split(".")[0]}_with_cat.png', img)

    return True
