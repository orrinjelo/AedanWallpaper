from PIL import Image
import os, sys
import argparse

def crop(image, box=None):
	if box:
		imageBox = box
	else:
		imageBox = image.getbbox()
	return image.crop(imageBox)


parser = argparse.ArgumentParser(description='Rotate an image batch')
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
	new_im = color_image.rotate(dtheta)
	new_fn = os.path.join('anim','{0}_{1}{2}'.format(base, n, ext))
	n += 1
	cropped = crop(new_im, (1620, 780, 2220, 1380))
	cropped.save(new_fn)