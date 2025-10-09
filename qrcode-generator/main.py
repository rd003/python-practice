import qrcode

img = qrcode.make("https://ravindradevrani.com/")
type(img)
img.save("myqr.png")