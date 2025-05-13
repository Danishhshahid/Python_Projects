from pyzbar.pyzbar import decode
from PIL import Image
img = Image.open('E:/GIAIC/Quarter 3/Assignments/Assignment Projects/QR code encoder/myqrcode.png')
result = decode(img)
print(result)