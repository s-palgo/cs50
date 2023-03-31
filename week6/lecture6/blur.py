from PIL import Image, ImageFilter

before = Image.open("stadium.bmp")
after = before.filter(ImageFilter.BoxBlur(10))
after.save("stadium_blurred.bmp")