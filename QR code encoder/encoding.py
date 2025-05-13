import qrcode

#encoding qr code
data = "My name is Danish Abbasi"
qr = qrcode.QRCode(version = 1,box_size = 10 , border = 5)
qr.add_data(data)
qr.make(fit=True)
img = qr.make_image(fill_color = 'red',back_color='white')
img.save('E:/GIAIC/Quarter 3/Assignments/Assignment Projects/QR code encoder/myqrcode.png')


