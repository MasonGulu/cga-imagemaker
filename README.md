# This has been superceded by a (Java port)[https://github.com/MasonGulu/CGA-Image-Maker]

# cga-imagemaker
Create COM files from JPG images

To use this program you will need Python 3 installed. You will also need https://pillow.readthedocs.io/en/stable/ pillow.

After installing Python 3 and pillow simply download the zip file from this repository, and extract it to a directory of your choice. For this script to function properly you *MUST* leave the com-templates folder in the same directory as the script *AND* you must only call the script from within the folder it's contained in. 

# Usage
The script has 2 main modes of operation, along with a help option.
* create - This takes an image mode, input JPG, and output COM. This will resize the image, convert it to a COM file, and also output a post processed image which will represent how it will appear on a compatible CGA computer/card.
* pattern - This takes an image mode and an output JPG. This creates a new image which will have every color of the palette on it, in an appropriate size to be turned into a COM file.

## com-templates folder
The com-templates folder has several partial com files in it, which handle setting the video mode and moving the image into CGA ram. The appropriate file is then copied and the image data is appended to the end of it.

## gimp-palettes folder
Inside the gimp-palettes folder are several palettes for gimp, which you may use to properly adapt the image to fit the palette. Without doing this the image may have large spots of color and will be very rough, as the script simply picks the closest color from the palette for each pixel. The 512 color images do not need this step (Not that you can do it regardless, gimp only allows images to be limited to 256 color palettes).

### Using gimp to limit image palettes
First import the desired palette into gimp, then open the desired image and resize it. Then press Image > Mode > Indexed and select the palette you desire from the menu, enable dithering (optional), and press apply. Make sure to export the image as a JPG (The script does not support some of the more advanced color modes found in Indexed PNGs).

### Tips for good looking images
* For 640x200 modes, I suggest resizing/cropping your image down to 640x400 and then *scaling* your image down to 640x200. The pixel ratio will be adjusted to that of your original image when it's displayed. I also suggest using gimp to limit the image to 2 colors, and enabling dithering.
* For 80x100 modes, I suggest resizing/cropping your image down to 160x100 and then *scaling* your image down to 80x100
