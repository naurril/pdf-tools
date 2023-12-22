from pdf2image import convert_from_path
import os
from PIL import Image
import img2pdf
import numpy as np
import cv2
import argparse

def export_images_from_pdf(pdf, output):

    pages = convert_from_path(pdf, 500)

    for i, page in enumerate(pages):
        page.save('{}/out_{:0>3d}.jpg'.format(output, i), 'JPEG')




# convert jpgs in folder 'jpg' to pdf
def convert_images_to_pdf(folder, out_file):


    files = os.listdir(folder)
    files.sort()
    # create a list of all the image filenames
    image_filenames = [os.path.join(folder, fn) for fn in files if fn.endswith('.jpg')]

    # # open all the images
    # images = [Image.open(fn) for fn in image_filenames]

    # # convert images to bytes
    # image_bytes = [img.tobytes() for img in images]
    # convert the images to pdf
    pdf_bytes = img2pdf.convert(image_filenames)

    # open a file for writing
    file = open(out_file, "wb")

    # write the pdf bytes to the file
    file.write(pdf_bytes)

    # close the file
    file.close()



# remove red part of an image
def remove_color(image, color):

    # convert image to numpy array
    image = np.array(image)

    # set red and green channels to 0

    # if a pixel is red, set the color to white

    # filter red pixels
    i = image
    #red_pixels = (image[:, :, 2] < image[:, :, 0]) & (image[:, :, 1] < image[:, :, 0]) 
    red_pixels = (image[:, :, 0] > 150) #& ( (np.abs(i[:,:,0]-i[:,:,1]) > 100) | (np.abs(i[:,:,0]-i[:,:,2]) > 100))
    if 'b' in color:
         red_pixels = red_pixels | (image[:, :, 2] > 150)
    #convert red pixels to ones
    d = np.zeros_like(red_pixels, np.float32)
    d[red_pixels] = 1.0

    dst = cv2.filter2D(d, cv2.CV_32F, np.ones([4,4]))

    red_inds = (dst > 8 )& red_pixels



    image[red_inds] = [255,255,255]



    # convert numpy array back to image
    image = Image.fromarray(image)

    return image

# open an image, remove red, and save as new image
def remove_color_and_save(image_path, color, new_image_path):
    image = Image.open(image_path)
    image = remove_color(image, color)
    image.save(new_image_path)


def mkdirs_if_not_existed(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
#mkdir('no_red')

parser = argparse.ArgumentParser(description='remove handwritings')        
parser.add_argument('pdf', type=str , help="")
parser.add_argument('--color', default='r', type=str , help="")
args = parser.parse_args()


pdf_file = args.pdf

jpg_folder = pdf_file + "-jpg"
out_jgp_folder = pdf_file + "-jpg-oup"
out_pdf_file = 'out_'+ pdf_file



mkdirs_if_not_existed(jpg_folder)
mkdirs_if_not_existed(out_jgp_folder)

target_color = args.color

export_images_from_pdf(pdf_file, jpg_folder)


# remove red from all images in folder 'jpg' and save in folder 'no_red'
for fn in os.listdir(jpg_folder):
    if fn.endswith('.jpg'):
        remove_color_and_save(os.path.join(jpg_folder, fn), target_color, os.path.join(out_jgp_folder, fn))


convert_images_to_pdf(out_jgp_folder, out_pdf_file)