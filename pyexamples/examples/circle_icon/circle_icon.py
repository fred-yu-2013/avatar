from PIL import Image, ImageOps

mask = Image.open('mask.png').convert('L')
im = Image.open('image.png')
output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
output.putalpha(mask)
output.save('output.png')