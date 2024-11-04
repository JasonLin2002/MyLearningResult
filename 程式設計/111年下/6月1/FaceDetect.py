from face_engine import FaceEngine
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

engine = FaceEngine()
imgFileName = 'C:/Users/jk121/OneDrive - 逢甲大學/文件/Code/learning-result/程式設計/111年下/6月1/Family1.jpg'

#try:
boxes, extra = engine.find_faces(imgFileName)
print(boxes)

img = Image.open(imgFileName)
drawing = ImageDraw.Draw(img)
for i in range(len(boxes)):
    shape = [(boxes[i][0], boxes[i][1]),
                boxes[i][2], boxes[i][3]]
    drawing.rectangle(shape,
                        outline = 'red',
                        width = 2)
    plt.imshow(img)
    plt.show()
#except:
print('No face found!')