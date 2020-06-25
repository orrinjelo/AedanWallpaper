from PIL import Image
import numpy as np
import colorsys
import os, sys
import argparse
import matplotlib.pyplot as plt 


rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

def crop(image, box=None):
    if box:
        imageBox = box
    else:
        imageBox = image.getbbox()
    return image.crop(imageBox)

def hue_shift(image, value):
    im = image.convert('RGBA')
    arr = np.array(np.asarray(im).astype(float))
    r,g,b,a = np.rollaxis(arr, axis=-1)
    # print(np.max(r))
    h,s,v = rgb_to_hsv(r, g, b)
    r, g, b = hsv_to_rgb((h + value/360.0) % 1.0, s, v)
    arr = np.dstack((r, g, b, a))

    # print(np.max(r))
    # plt.imshow(arr.astype(int), aspect='auto')
    # plt.show()

    return Image.fromarray(arr.astype('uint8'), 'RGBA')

parser = argparse.ArgumentParser(description='Rainbow an image batch')
parser.add_argument('--filename', dest='filename', type=str)
parser.add_argument('--step',     dest='step',     type=float,  default=5.0)
parser.add_argument('--max_step', dest='max_step', type=float,  default=360.0)
args = parser.parse_args()

color_image = Image.open(args.filename)

basename = os.path.basename(args.filename)
base, ext = os.path.splitext(basename)

if not os.path.exists('anim'):
    os.mkdir('anim')

for n in range(0, int(args.max_step/args.step)):
    dtheta = n*args.step
    print('Writing out', dtheta)
    cropped = crop(color_image, (1620, 780, 2220, 1380))
    new_im = hue_shift(cropped, dtheta)
    new_fn = os.path.join('anim','{0}_{1}{2}'.format(base, n, ext))
    n += 1
    new_im.save(new_fn)