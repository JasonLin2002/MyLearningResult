from face_engine import FaceEngine
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw      

engine = FaceEngine()
imgList = ['Tom.jpg','Tom1.jpg','Tom2.jpg','Tom3.jpg',
           'Tom4.jpg','Tom5.jpg','Tom6.jpg','Tom7.jpg',
           'Tom8.jpg','Tom9.jpg','pin.jpg']
imgLabel=['']
engine.fit(imgList , imgLabel)

testImage=''
boxes,names = engine.make_prediction(testImage)
print(names,boxes)
drawing = ImageDraw.Draw(img)
for i in range(len(boxes)):
    shape = [(boxes[i][0],boxes[i][1]),
             (boxes[i][2],boxes[i][3])]
    drawing.rectangle(shape,
                      outline='red',
                       width = 2)
plt.imshow(img)
plt.show()