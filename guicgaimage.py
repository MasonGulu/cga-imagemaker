# This will take in an image (uncompressed JPG probably)
# And convert it to a binary file for loading into CGA RAM
# In the respective graphic mode
# Copyright (C) 2021 Mason Gulu
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# If you have any questions or comments you may contact me at mason.gulu@gmail.com


from PIL import Image
import sys 
import math
import shutil
import PySimpleGUI as sg
resizeEnable = True # When enabled this script will attempt to resize images to fit the selected mode, after cropping to the correct aspect ratio
splitFile = False # When enabled seperate even/odd files will be written
comMode = True # Make main file into an executable comfile instead of a binary file
openImage = False # Open image after script is done
savePostImage = True # Save image after filtering

# Palettes
p4c0  = [0x000000, 0x5c9c0c, 0x993100, 0x9e5a02]
p4c1  = [0x000000, 0x55a6ab, 0x954eab, 0xababab]
p4cm  = [0x000000, 0x858585, 0xacacac, 0xffffff] # This is close to the monochrome video mode of my composite CGA card
p256co0 = [0x000000,0x460153,0x271d00,0x000000,0xa92748,0x720757,0x532700,0xa6302f,0x3a1f00,0x812442,0x634200,0x391f00,0xe54b37,0xad2a46,0x8e4b00,0xe2541d,0x093198,0x5937ff,0x2d536c,0x03308b,0xa15bb8,0x8339ff,0x605d73,0xb65edf,0x455587,0x945ced,0x68765b,0x3e547a,0xdd7ea6,0xbe5df3,0x9a8062,0xf382d0,0x006103,0x355666,0x1d8e00,0x005015,0x938444,0x625b6c,0x468200,0x988645,0x2e8400,0x717857,0x59b200,0x2b7404,0xcfa731,0x9d7e5b,0x81a600,0xd3a833,0x007968,0x4385b9,0x24ae32,0x00875a,0x96a195,0x6d7eca,0x4fa146,0xb6a5d4,0x359c59,0x7fa8aa,0x60d221,0x36aa49,0xd2c684,0xa8a2b8,0x8ac533,0xf1cac2,0x000000,0x430149,0x272300,0x000000,0xb02558,0x7c056b,0x522100,0xa4292d,0x392000,0x634800,0x381e00,0xec4946,0xb6295a,0xb6295a,0x8d4400,0xe04d1d,0x0c135a,0x541aad,0x363b33,0x091354,0xad3b93,0x8e1ed5,0x5b3a29,0xc03cb5,0x48364a,0x8e3d9c,0x726022,0x453643,0xe96081,0xca42c4,0x965f18,0xfb61a4,0x003f00,0x413341,0x286d00,0x002c00,0xa47a0b,0x6c3845,0x557500,0xa3661c,0x396300,0x7b582f,0x649100,0x365100,0xdf9d00,0xa75c35,0x909900,0xdf890c,0x007777,0x4684bd,0x28ab3c,0x00825b,0x96a192,0x6e89ba,0x56b33b,0xb6bab5,0x3a9a66,0x80a8ac,0x64d02b,0x35a549,0xd2c582,0xa9aca8,0x91d72a,0xf3dfa5,0x0d215a,0x5427ad,0x354437,0x0c2159,0xb74da2,0x802db1,0x614d2f,0xb45688,0x474347,0x8c4899,0x6e6423,0x454245,0xf06e8e,0xb84e9d,0x996e1c,0xed7776,0x1757f1,0x665dff,0x3b78c7,0x1156e5,0xaf81ff,0x9160ff,0x6d83cd,0xc684ff,0x5078df,0x9f7eff,0x7499b2,0x4a77d2,0xe8a1ff,0xca80ff,0xa6a3b9,0xfda4ff,0x00875f,0x447bc2,0x2bb433,0x007670,0xa1aa9d,0x7181c7,0x53a83f,0xa6ab9f,0x39a74c,0x7c9cac,0x65d521,0x36965c,0xdacb8a,0xa8a1b2,0x8cca2c,0xdfcd8b,0x089fc5,0x51abff,0x31d58c,0x09adb4,0xa4c8f1,0x7ba5ff,0x5dc8a1,0xc5ccff,0x3fc0af,0x89ccff,0x6bf57a,0x42cea1,0xdde9dd,0xb3c6ff,0x95e98d,0xfcedff,0x0c2252,0x5126a2,0x354a2a,0x0c1f54,0xc04bb2,0x892bc5,0x604731,0xb25088,0x45433e,0x89488f,0x6e6a17,0x44413f,0xf76c9e,0xc34cb1,0x98681e,0xeb7074,0x1a38b4,0x613fff,0x44628d,0x1738ad,0xbb62ed,0x9c45ff,0x696182,0xce62ff,0x535aa0,0x9a61f4,0x7d827a,0x505a9a,0xf582da,0xd565ff,0xa18170,0xff83fc,0x0c663a,0x4f5a9c,0x36940d,0x09534d,0xb19f65,0x7a5ea0,0x639b09,0xb18c78,0x468727,0x877a87,0x6fb300,0x427338,0xebc152,0xb27f8b,0x9bbb00,0xeaac63,0x0e9cd2,0x54aaff,0x35d196,0x07a8b3,0xa3c8ec,0x7cafff,0x64da96,0xc5e1ff,0x47bdbd,0x8ccbff,0x6ff283,0x41c9a1,0xdde8d9,0xb4d0ff,0x9cfa82,0xfdfffc]
p256co1 = [0x000000,0x642aec,0x000914,0x012166,0x5d027c,0x741dd7,0x000003,0x6a28ef,0x430a4e,0xa637ff,0x3a1764,0x442eb2,0xa010cb,0xb52aff,0x3f0850,0xad36ff,0x000000,0x5937ff,0x000000,0x002a72,0x5c027a,0x671bd7,0x000001,0x5834ff,0x3f0a4e,0x9b45ff,0x3b084e,0x3d37be,0x9e0fc8,0xaa28ff,0x3b084f,0x9b42ff,0x267800,0x8ca6a4,0x1d8e00,0x25aa30,0x88833a,0x9b9e97,0x247700,0x8bb1ba,0x698607,0xcfb4f2,0x609b27,0x68b77d,0xcc9187,0xdface4,0x678509,0xcfc0ff,0x005700,0x6183cf,0x005800,0x00875a,0x5c6268,0x6979c1,0x005600,0x558ce5,0x3e6432,0xa391ff,0x396638,0x3e95a7,0x9e70b4,0xac86ff,0x3b6436,0x9799ff,0x461c00,0x9344c6,0x321800,0x2e393e,0xb12558,0xaa3bb6,0x361800,0x9144cd,0x882a2a,0xd751ff,0x77252b,0x70478c,0xf433a5,0xec49ff,0x78252c,0xd451ff,0x000002,0x8c2ce6,0x000000,0x001a61,0x63027d,0x8e1ed5,0x000004,0x572bfb,0x3e0850,0xcf39ff,0x3b054f,0x4228ad,0xa60fca,0xd12cff,0x3b0652,0x9a38ff,0x4c7600,0x9d9d9a,0x497300,0x369312,0xbb7d28,0x9f8f88,0x557500,0xa49d9e,0x8f8400,0xe0aae7,0x8d8000,0x7aa060,0xfe8b76,0xe29cd5,0x978300,0xe8abed,0x3b8000,0xc1ad9a,0x387a00,0x4b9f12,0x9c802c,0xc89c83,0x467e00,0xb6bab5,0x7f8d05,0xffbbe8,0x7b8802,0x8dac60,0xe08d79,0xffaad1,0x888b03,0xf9c9ff,0x073800,0x6a66e8,0x004611,0x085e62,0x643e79,0x7a59d4,0x023600,0x7165ec,0x474347,0xaa71ff,0x3d505d,0x4968ac,0xa349c3,0xba64ff,0x43424a,0xb06fff,0x033900,0x5f74fc,0x003700,0x01676e,0x623d77,0x6d57d3,0x003500,0x5f71ff,0x434447,0x9f7eff,0x3f4248,0x4171b8,0xa249c1,0xad62ff,0x414148,0x9f7bff,0x2cb400,0x93e3a0,0x23cb00,0x2be72c,0x8fbe35,0xa1db94,0x2bb300,0x92eeb7,0x6dc000,0xd3edec,0x64d520,0x6cf177,0xcfca81,0xe2e5de,0x6cbe02,0xd3f9ff,0x029200,0x67c0cc,0x009400,0x03c456,0x629d63,0x70b4bc,0x009100,0x5bc8e1,0x439d2b,0xa7caff,0x3e9e30,0x42cfa1,0xa2a8ae,0xafc0ff,0x3e9c2e,0x9bd3ff,0x4c5900,0x9a7fc3,0x3a5500,0x34763b,0xb76154,0xb078b2,0x3c5500,0x977fc9,0x8c6323,0xda8aff,0x7a5f24,0x758085,0xf86c9e,0xf182fd,0x7d5f26,0xd88aff,0x033600,0x9269e3,0x003300,0x06575d,0x6a3d79,0x945bd2,0x003400,0x5d67f8,0x424149,0xd373ff,0x3f3e48,0x4661a7,0xa949c4,0xd565ff,0x3f3e4b,0x9d72ff,0x52b100,0xa4da96,0x50af00,0x3dcf0e,0xc2b825,0xa6cb84,0x5cb100,0xabda9b,0x92bc00,0xe4e4e1,0x90b900,0x7dda59,0xffc46f,0xe6d6cf,0x9bbb00,0xece4e5,0x43bb00,0xc7e996,0x3eb600,0x52db0e,0xa2bb28,0xced980,0x4cb900,0xbcf7b2,0x83c700,0xfff4e1,0x7fc200,0x91e659,0xe3c773,0xffe3cb,0x8cc500,0xfdfffc]
p256cn0 = [0x000000,0x0f0017,0x341000,0x260000,0x5b0000,0x45000a,0x6a2300,0x9e2200,0x3d0f00,0x6b0d00,0x904100,0x822f00,0xb72c00,0xa01c00,0xc65300,0xfa5300,0x000039,0x100078,0x2f3000,0x201f17,0x4e1c34,0x460b6b,0x684200,0x9f3d33,0x392e0b,0x6c2c4b,0x8b6000,0x7c4f00,0xaa4d07,0xa03a3f,0xc37300,0xfb6e05,0x003a40,0x042f80,0x297000,0x1a4f2f,0x4d544e,0x3b3f73,0x5e7600,0x937335,0x336a13,0x606052,0x84a000,0x757f03,0xa98422,0x956f47,0xb9a600,0xeea308,0x004a7a,0x054dac,0x278530,0x197153,0x49697c,0x3b56a8,0x5d8b2e,0x9d8785,0x327b4c,0x617d80,0x82b503,0x75a027,0xa59850,0x96867c,0xb9ba02,0xf9b759,0x000008,0x10003c,0x372500,0x290f00,0x610a2a,0x4d0041,0x6c2e00,0xa02e00,0x3f1f00,0x6c1d10,0x925400,0x853f00,0xbd3a00,0xa72a15,0xc75e00,0xfc5e00,0x000043,0x140077,0x3a3507,0x2a2027,0x5b1b4c,0x510b7f,0x6b4000,0xaa3b47,0x422f17,0x702e4a,0x966500,0x865100,0xb64b20,0xac3c52,0xc77100,0xff6b1b,0x003958,0x112e98,0x356f16,0x264d49,0x5b5e5a,0x463c8b,0x6a7f03,0x9e714c,0x40692b,0x6d5e6c,0x919f00,0x837d1f,0xb68e2d,0xa16c5f,0xc6ae00,0xfaa21e,0x005aaf,0x095ddd,0x2c9464,0x1b7f82,0x4a78a8,0x3c6cc9,0x62a453,0x9ea29e,0x388a83,0x658eaf,0x87c438,0x77b054,0xa6a87c,0x969c9d,0xbdd526,0xf9d272,0x001373,0x1811a8,0x3d453a,0x303458,0x643186,0x4f229b,0x735825,0xa8575f,0x413f41,0x703d78,0x95710a,0x876027,0xbc5d56,0xa44e69,0xca8400,0xff842d,0x0032ca,0x1a31ff,0x38658c,0x2a54a8,0x5752c4,0x5040fe,0x727781,0xaa72c6,0x3f5f9a,0x725ed9,0x90915d,0x82807a,0xaf7d96,0xa66bce,0xc9a34e,0xff9f94,0x006fd1,0x0e64ff,0x32a58f,0x2384c1,0x5689df,0x4474ff,0x67ab88,0x9ca8c6,0x389ba0,0x6690e1,0x8ad15f,0x7bb091,0xaeb5af,0x9ba0d4,0xbfd858,0xf3d494,0x007fff,0x1082ff,0x30bac1,0x22a6e4,0x529eff,0x458bff,0x67c0bf,0xa6bcff,0x38acdb,0x67aeff,0x88e592,0x7ad2b4,0xaac9df,0x9bb8ff,0xbfec90,0xfee7e8,0x002499,0x1a22d0,0x405a5e,0x324483,0x6a3fbb,0x5630d2,0x756353,0xa9638b,0x44516a,0x714e9e,0x98862f,0x897051,0xc26a8d,0xac5ca1,0xcc9021,0xff8f59,0x0034d4,0x1e33ff,0x436a98,0x3455b8,0x6450de,0x5b40ff,0x757583,0xb370d9,0x4760a4,0x7560d8,0x9b9668,0x8b8186,0xbc7cae,0xb16ce1,0xcda253,0xff9caa,0x006eeb,0x1b63ff,0x3fa4a7,0x3182dc,0x6493eb,0x5071ff,0x74b494,0xa8a6dd,0x459aba,0x728ff9,0x97d077,0x88aeaa,0xbbbfb9,0xa59dea,0xcce064,0xffd2ab,0x008fff,0x1491ff,0x36c8f6,0x25b3ff,0x54acff,0x47a0ff,0x6bd8e3,0xa8d7ff,0x3ebaff,0x6bbeff,0x8df5c4,0x7ddfe2,0xacd9ff,0x9cccff,0xc3ffb3,0xffffff]
p256cn1 = [0x000000,0x140072,0x210043,0x24007b,0x350051,0x3f008f,0x46005e,0x7f00f1,0x48005c,0x7b00ee,0x8900be,0x8d02f7,0x9d00cd,0xa700ff,0xad00da,0xe802ff,0x000000,0x100078,0x280031,0x24017b,0x39004a,0x3c008a,0x490057,0x7704f7,0x4b0056,0x7805f3,0x9000ad,0x8c0bf7,0xa000c5,0xa400ff,0xb100d3,0xe00dff,0x006100,0x21742b,0x297000,0x2a7f39,0x43620a,0x4c724b,0x516613,0x8480b1,0x536a14,0x887da6,0x90797a,0x9288b5,0xab6c86,0xb37bc7,0xb86f8e,0xed89ff,0x005200,0x0e6545,0x1c5609,0x197153,0x2f5527,0x356265,0x3d582e,0x6b70cb,0x425b2e,0x756ec1,0x836086,0x817acf,0x975ea2,0x9d6be0,0xa561aa,0xd379ff,0x060a00,0x2d1b50,0x431015,0x3c2358,0x610a2a,0x5a176d,0x63113b,0x9322cf,0x6d1439,0x9424cc,0xab1991,0xa42cd4,0xca13a6,0xc221e9,0xcb1ab7,0xfb2bff,0x000000,0x2e1162,0x27022b,0x28156c,0x3b0044,0x510b7f,0x470452,0x761aec,0x490651,0x961add,0x900ba7,0x8f1ee8,0xa205bf,0xb914fb,0xae0dce,0xde23ff,0x027a00,0x2a8a1d,0x457c00,0x368f23,0x607800,0x4d843b,0x6a7f03,0x938f98,0x698407,0x939399,0xae8559,0x9e989e,0xc88272,0xb48db7,0xd2887f,0xfa99ff,0x008300,0x429515,0x3f8500,0x46991b,0x527f00,0x678e2f,0x658801,0x9ea29e,0x648d05,0xab9e90,0xa68e57,0xaea296,0xba896f,0xcf97ab,0xcd917c,0xffacff,0x003900,0x114d5c,0x1f472c,0x215564,0x333a3a,0x3c4878,0x434248,0x7c55da,0x413f41,0x7552d4,0x834da4,0x855bdd,0x963fb1,0xa04ef1,0xa847bf,0xe05aff,0x003e00,0x0e5861,0x25441b,0x215e66,0x363e33,0x394c74,0x474640,0x7560e0,0x44433b,0x725ed9,0x8a4992,0x8663dd,0x9a43ab,0x9e51eb,0xab4bb9,0xd965ff,0x00bc00,0x1ecf14,0x26cc00,0x27dc23,0x40bf00,0x49cd34,0x4dc300,0x80dc9b,0x4dc200,0x81d58c,0x8ad15f,0x8ce09a,0xa4c46b,0xacd3ac,0xb2c774,0xe5e1ff,0x00ae00,0x0bc12e,0x18b300,0x16cc3c,0x2cb110,0x32be4e,0x3bb417,0x68ccb5,0x3ab314,0x6ec6a6,0x7db86a,0x7ad2b4,0x91b687,0x95c3c6,0x9fba8f,0xcbd1ff,0x036500,0x2a763a,0x406a00,0x397d42,0x5e6515,0x587258,0x616c25,0x907eba,0x676b20,0x8f7bb1,0xa56f77,0x9e82b9,0xc26a8d,0xbc77cf,0xc5719c,0xf482ff,0x005900,0x2c6c4b,0x245e16,0x247256,0x38582d,0x4f6768,0x44603b,0x7376d6,0x435e37,0x9072c3,0x89638d,0x8976cd,0x9c5ea5,0xb16ce1,0xa865b3,0xd87bff,0x00d600,0x27e607,0x42d800,0x34eb0c,0x5dd400,0x4ae024,0x68da00,0x90ec83,0x62db00,0x8bec7f,0xa6dd3f,0x98f083,0xc0da58,0xaee69c,0xcce064,0xf4f0fa,0x00de00,0x3ef100,0x3ce000,0x44f305,0x4fda00,0x64e91b,0x63e200,0x9bfd89,0x5ce400,0xa3f677,0xa0e53e,0xa6f97e,0xb2e057,0xc9ee92,0xc7e863,0xffffff]

# Mode categories
m2bpp = ["4cm", "4c0", "4c1"] # 2 bit per pixel
m1bpp = ["2c"] # 1 bit per pixel
m2Bpp = ["256co0", "256co1", "256cn0", "256cn1"] # 2 byte per pixel
m512 = ["512co", "512cn"]

# Com Template filenames
cFolder = "com-templates/"
c4c0 = "com4c0.bin"
c4c1 = "com4c1.bin"
c2c = "com2c.bin"
c512c = "com512c.bin"




# Functions
def RGBDifference(value, compare):
    return abs(value[0] - (compare>>16)) + abs(value[1] - ((compare>>8)&0xff)) + abs(value[2] - (compare&0xff))

def cropImage(im, size):
    height = round(size[0]*0.625/2)
    top = round(size[1]/2 - height)
    bottom = round(size[1]/2 + height)
    im = im.crop(box=(0, top, size[0], bottom)) # left, up, right, down
    return im

def getPixel(im,x,y,palette):
    pixel = im.getpixel((x,y))
    closestIndex = 0
    closestValue = 256*256*256
    for i in range(0, len(palette)):
        if RGBDifference(pixel, palette[i]) < closestValue:
            closestValue = RGBDifference(pixel, palette[i])
            closestIndex = i
                
    im.putpixel((x,y), (palette[closestIndex] >> 16, (palette[closestIndex] >> 8)&0xff, palette[closestIndex]&0xff))
    return closestIndex

def executeScript(operation, m, input, output):
    sys.argv = [operation, m, input, output]
    
    if len(sys.argv) < 1:
        print("This program is licensed under GPLv2 and comes with ABSOLUTELY NO WARRANTY.")
        print("Usage: cgaimage.py [help, create, pattern]")
        return True

    if sys.argv[0].lower() == "help":
        if len(sys.argv) > 1:
            # This is a specific help command
            if sys.argv[1].lower() == "4cm":
                print("4 color greyscale")
                print("320x200 COMP")
                print("Palette: gimp-palettes/p4cm.gpl")
            elif sys.argv[1].lower() == "4c0":
                print("4 color palette 0")
                print("320x200 CGA")
                print("Palette: gimp-palettes/p4c0.gpl")
            elif sys.argv[1].lower() == "4c1":
                print("4 color palette 1")
                print("320x200 CGA")
                print("Palette: gimp-palettes/p4c1.gpl")
            elif sys.argv[1].lower() == "2c":
                print("2 color monochrome")
                print("640x200 CGA")
                print("Palette: N/A")
            elif sys.argv[1].lower() == "256co0":
                print("256 color")
                print("80 x100 COMP")
                print("Palette: gimp-palettes/p256co0.gpl")
            elif sys.argv[1].lower() == "256co1":
                print("256 color")
                print("80 x100 COMP")
                print("Palette: gimp-palettes/p256co1.gpl")
            elif sys.argv[1].lower() == "512co":
                print("512 color")
                print("80 x100 COMP")
                print("Palette: gimp-palettes/p512o.gpl")
            elif sys.argv[1].lower() == "256cn0":
                print("256 color")
                print("80 x100 COMP")
                print("Palette: gimp-palettes/p256cn0.gpl")
            elif sys.argv[1].lower() == "256cn2":
                print("256 color")
                print("80 x100 COMP")
                print("Palette: gimp-palettes/p256cn1.gpl")
            elif sys.argv[1].lower() == "512cn":
                print("512 color")
                print("80 x100 COMP")
                print("Palette: gimp-palettes/p512n.gpl")
            else:
                print("Invalid palette.")
        else:
            # This is a generic help command
            print("To get information on a specific mode, use |cgaimage.py help [mode]|")
            print("All modes supported are as follows")
            print("4cm   : 4 color monochrome 320x200 COMP")
            print("4c0   : 4 color palette 0  320x200 CGA")
            print("4c1   : 4 color palette 1  320x200 CGA")
            print("2c    : 2 color            640x200 CGA")
            print("256co0: 256 color palette0 80 x100 COMP")
            print("256co1: 256 color palette1 80 x100 COMP")
            print("512co : 512 color          80 x100 COMP")
            print("256cn0: 256 color palette0 80 x100 COMP")
            print("256cn1: 256 color palette1 80 x100 COMP")
            print("512cn : 512 color          80 x100 COMP")
        return True
    elif sys.argv[0].lower() == "create":
        if len(sys.argv) < 4:
            print("Usage:")
            print("cgaimage.py create [mode] [input file] [output file]")
            return True
        mode = sys.argv[1].lower()
        im = Image.open(sys.argv[2])
        size = im.size
        if (not comMode):
            outputfile = open(sys.argv[3], "wb")
        else:
            # Copy appropriate com file, then open ab
            if mode in ["4c0", "4cm"]:
                shutil.copy(cFolder+c4c0, sys.argv[3])
            elif mode == "4c1":
                shutil.copy(cFolder+c4c1, sys.argv[3])
            elif (mode in m2Bpp) or (mode in m512):
                shutil.copy(cFolder+c512c, sys.argv[3])
            elif mode in m1bpp:
                shutil.copy(cFolder+c2c, sys.argv[3])
            else:
                print("Unsupported mode!")
                return True
            outputfile = open(sys.argv[3], "ab")
        if mode in m2bpp:
            if (size != (320, 200) and resizeEnable):
                print("Image size is not correct. Attempting resize.")
                im = cropImage(im, size)
                im = im.resize((320, 200))
                size = (320,200)
            # 2 bit per pixel mode
            even = []
            odd = []
            if mode == "4cm":
                palette = p4cm 
            elif mode == "4c0":
                palette = p4c0 
            elif mode == "4c1":
                palette = p4c1
            if im.mode != "RGB":
                print("Image is in an unsupported mode!")
                return True
            tmpint = 0
            tmppos = 8
            for y in range(0, size[1]):
                for x in range(0, size[0]):
                    tmppos = tmppos - 2
                    tmpint = tmpint + (getPixel(im,x,y,palette) << tmppos)
                    if (tmppos == 0):
                        # This is the end of the byte.
                        tmppos = 8
                        if (y % 2 == 0):
                            even.append(tmpint.to_bytes(1,"little")) # Note, this is called even because I'm starting at 0
                        else:
                            odd.append(tmpint.to_bytes(1,"little"))
                            # I hate emulating bitwise stuff, and then converting my emulated bitwise stuff into actual byte objects resulting in the question of am I accidentally reversing what I already did? or is this the correct orientation, and then when you look at it later you are incredibly confused on if I intended on reversing the order of the bits, or if it just miraculously lined up. yes this line is long.
                        tmpint = 0 
            # File saving
            count = 0 # Amount of bytes written
            if (splitFile):
                evenfile = open(sys.argv[3]+"even", "wb") # Mixing up the filenames was wrong. CGA starts at 0.
            for byte in even:
                count = count + 1
                outputfile.write(byte)
                if (splitFile):
                    evenfile.write(byte)
            if (splitFile):
                evenfile.close()
            for byte in range(count, 8192):
                outputfile.write(int.to_bytes(0,1,"little"))
            if (splitFile):
                oddfile = open(sys.argv[3]+"odd", "wb")
            for byte in odd:
                outputfile.write(byte)
                if (splitFile):
                    oddfile.write(byte)
            if (splitFile):
                oddfile.close()

            outputfile.close()
        elif mode in m1bpp:
            if (size != (640, 200) and resizeEnable):
                print("Image size is not correct. Attempting resize.")
                im = cropImage(im, size)
                im = im.resize((640, 200))
                size = (640,200)
            even = []
            odd = []
            # Two bit per pixel monochrome
            tmpint = 0
            tmppos = 8
            for y in range(0, size[1]):
                for x in range(0, size[0]):
                    tmppos = tmppos - 1
                    color = im.getpixel((x,y))
                    color = (color[0] << 16) + (color[1] << 8) + color[2]
                    if color > 0x777777:
                        color = 1
                    else:
                        color = 0
                    im.putpixel((x,y), (255*color, 255*color, 255*color))
                    tmpint = tmpint + (color << tmppos)
                    if (tmppos == 0):
                        # This is the end of the byte.
                        tmppos = 8
                        if (y % 2 == 0):
                            even.append(tmpint.to_bytes(1,"little")) # Note, this is called even because I'm starting at 0
                        else:
                            odd.append(tmpint.to_bytes(1,"little"))
                            # I hate emulating bitwise stuff, and then converting my emulated bitwise stuff into actual byte objects resulting in the question of am I accidentally reversing what I already did? or is this the correct orientation, and then when you look at it later you are incredibly confused on if I intended on reversing the order of the bits, or if it just miraculously lined up. yes this line is long.
                        tmpint = 0
            count = 0 # Amount of bytes written
            if (splitFile):
                evenfile = open(sys.argv[3]+"even", "wb") # Mixing up the filenames was wrong. CGA starts at 0.
            for byte in even:
                count = count + 1
                outputfile.write(byte)
                if (splitFile):
                    evenfile.write(byte)
            if (splitFile):
                evenfile.close()
            for byte in range(count, 8192):
                outputfile.write(int.to_bytes(0,1,"little"))
            if (splitFile):
                oddfile = open(sys.argv[3]+"odd", "wb")
            for byte in odd:
                outputfile.write(byte)
                if (splitFile):
                    oddfile.write(byte)
            if (splitFile):
                oddfile.close()

            outputfile.close()
        elif mode in m2Bpp:
            if (size != (80, 100) and resizeEnable):
                print("Image size is not correct. Attempting resize.")
                im = cropImage(im, size)
                im = im.resize((80, 100))
                size = (80,100)
            # Two byte per pixel High Color Text mode
            if mode == "256co0":
                # Palette 0
                char = 0x55
                palette = p256co0
            elif mode == "256cn0":
                char = 0x55
                palette = p256cn0 
            elif mode == "256co1":
                char = 0x13
                palette = p256co1
            elif mode == "256cn1":
                char = 0x13
                palette = p256cn1
            image = []
            for y in range(0, size[1]):
                for x in range(0, size[0]):
                    image.append(int.to_bytes(char, 1, "little"))
                    col = getPixel(im, x, y, palette) # So turns out I had mixed up the nibbles..
                    col = ((col<<4)&0xf0) + (col>>4)# Nibble correction
                    image.append(int.to_bytes(col, 1, "little"))
            for byte in image:
                outputfile.write(byte)
            outputfile.close()
        elif mode in m512:
            # Two byte per pixel High Color Text mode, 512 color
            if (size != (80, 100) and resizeEnable):
                print("Image size is not correct. Attempting resize.")
                im = im.resize((80, 100))
                size = (80,100)
            if mode == "512co":
                palette = p256co0 + p256co1
            elif mode == "512cn":
                palette = p256cn0 + p256cn1
            image = []
            for y in range(0, size[1]):
                for x in range(0, size[0]):
                    col = getPixel(im, x, y, palette) # So turns out I had mixed up the nibbles..
                    if col > 255:
                        # Part of second palette
                        char = 0x13 
                        col = col - 256
                    else:
                        char = 0x55
                    image.append(int.to_bytes(char, 1, "little"))
                    col = ((col<<4)&0xf0) + (col>>4)# Nibble correction
                    image.append(int.to_bytes(col, 1, "little"))
            for byte in image:
                outputfile.write(byte)
            outputfile.close()
        else:
            print("Invalid mode.")
            return True
        # Image resizing to correct aspect ratio
        if resizeEnable:
            # Don't bother if resizing isn't enabled
            if mode in m1bpp:
                # Double height
                im2 = Image.new("RGB", (640,400))
                for x in range(0, 640):
                    for y in range(0, 200):
                        im2.putpixel((x,y*2), im.getpixel((x,y)))
                        im2.putpixel((x,(y*2)+1), im.getpixel((x,y)))
                im = im2
            elif mode in m2Bpp or mode in m512:
                # Double width
                im2 = Image.new("RGB", (160,100))
                for x in range(0, 80):
                    for y in range(0, 100):
                        im2.putpixel((x*2,y), im.getpixel((x,y)))
                        im2.putpixel(((x*2)+1,y), im.getpixel((x,y)))
                im = im2
        if savePostImage:
            while '/' in sys.argv[2]:
                # The file contains a directory
                index = sys.argv[2].index('/')
                sys.argv[2] = sys.argv[2][index+1:]
            im.save(sys.argv[2][:-4]+'_post.jpg', quality=95, subsampling=0)
        if openImage: 
            im.show()
    elif sys.argv[0].lower() == "pattern":
        # Generate a test pattern
        if len(sys.argv) < 3:
            print("Usage:")
            print("cgaimage.py pattern [mode] [output file]")
            return True
        mode = sys.argv[1].lower()
        if mode in m2bpp:
            # 2 bit per pixel, 320x200
            if mode == "4c0":
                palette = p4c0
            elif mode == "4c1":
                palette = p4c1 
            elif mode == "4cm":
                palette = p4cm
            im = Image.new("RGB", (320,200))
            colorsPerRow = 2
            colorsPerColumn = 2
            colorCellWidth = math.floor(320 / colorsPerRow)
            colorCellHeight = math.floor(200 / colorsPerColumn)
            for y in range(0, 200):
                for x in range(0, 320):
                    colorIndex = math.floor(x / colorCellWidth) + (math.floor(y / colorCellHeight) * colorsPerRow)
                    color = palette[colorIndex]
                    colorT = (color >> 16, (color >> 8)&0xff, color & 0xff)
                    im.putpixel((x,y), colorT)
            if openImage:
                im.show()
        elif mode in m1bpp:
            # 1 bit per pixel, 640x200
            if mode == "2c":
                palette = [0x000000, 0xffffff]
            im = Image.new("RGB", (640,200))
            colorsPerRow = 2
            colorsPerColumn = 1
            colorCellWidth = math.floor(640 / colorsPerRow)
            colorCellHeight = math.floor(200 / colorsPerColumn)
            for y in range(0, 200):
                for x in range(0, 640):
                    colorIndex = math.floor(x / colorCellWidth) + (math.floor(y / colorCellHeight) * colorsPerRow)
                    color = palette[colorIndex]
                    colorT = (color >> 16, (color >> 8)&0xff, color & 0xff)
                    im.putpixel((x,y), colorT)
            if openImage:
                im.show()
        elif mode in m2Bpp:
            # 2 bytes per pixel, 80x100
            if mode == "256co0":
                palette = p256co0
            elif mode == "256cn0":
                palette = p256cn0
            elif mode == "256co1":
                palette = p256co1
            elif mode == "256cn1":
                palette = p256cn1
            else:
                print("Palette not found")
                return True
            im = Image.new("RGB", (80,100))
            colorsPerRow = 16
            colorsPerColumn = 16
            colorCellWidth = math.floor(80 / colorsPerRow)
            colorCellHeight = math.floor(100 / colorsPerColumn)
            for y in range(0, 100):
                for x in range(0, 80):
                    colorIndex = math.floor(x / colorCellWidth) + (math.floor(y / colorCellHeight) * colorsPerRow)
                    if (colorIndex > 255):
                        colorIndex = 0
                    color = palette[colorIndex]
                    colorT = (color >> 16, (color >> 8)&0xff, color & 0xff)
                    im.putpixel((x,y), colorT)
            if openImage:
                im.show()
        elif mode in m512:
            # 2 bytes per pixel, 80x100
            if mode == "512co":
                palette = p256co0 + p256co1 
            elif mode == "512cn":
                palette = p256cn0 + p256cn1
            im = Image.new("RGB", (80,100))
            colorsPerRow = 16
            colorsPerColumn = 32
            colorCellWidth = math.floor(80 / colorsPerRow)
            colorCellHeight = math.floor(100 / colorsPerColumn)
            for y in range(0, 100):
                for x in range(0, 80):
                    colorIndex = math.floor(x / colorCellWidth) + (math.floor(y / colorCellHeight) * colorsPerRow)
                    if (colorIndex > 511):
                        colorIndex = 0
                    color = palette[colorIndex]
                    colorT = (color >> 16, (color >> 8)&0xff, color & 0xff)
                    im.putpixel((x,y), colorT)
            if openImage:
                im.show()
        else:
            print("Mode not supported.", mode)
        im.save(sys.argv[2], "JPEG", quality=95, subsampling=0)
    else:
        print("Usage:")
        print("cgaimage.py [help, create, pattern]")
        return True

sg.theme('DarkBlack')

layout = [[sg.Text('Input File:', size=(20,1)), sg.Input(key='if', size=(40,1)), sg.FileBrowse()],
    [sg.Text('Mode:', size=(20,1)), sg.Combo(m1bpp+m2bpp+m2Bpp+m512, expand_x=True, key='mode')],
    [sg.HorizontalSeparator()],
    [sg.Text('Settings:', size=(23,1)), sg.Checkbox('Resize', default=resizeEnable, size=(20,1), key='resizeEnable')],
    [sg.Checkbox('Split', default=splitFile, size=(20,1), key='splitFile'), sg.Checkbox('COM Mode', default=comMode, size=(20,1), key='comMode')],
    [sg.Checkbox('Open Afterwards', default=openImage, size=(20,1), key='openImage'), sg.Checkbox('Save post JPG', default=savePostImage, size=(20,1), key='savePostImage')],
    [sg.HorizontalSeparator()],
    [sg.Input(key='create', visible=False, enable_events=True), sg.FileSaveAs(button_text='create'),sg.Input(key='pattern', visible=False, enable_events=True), sg.FileSaveAs(button_text='pattern')]]

win = sg.Window('cgaimagegui', layout=layout)
while True:
    event, values = win.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    # Update variables
    resizeEnable = values['resizeEnable']
    splitFile = values['splitFile']
    comMode = values['comMode']
    openImage = values['openImage']
    savePostImage = values['savePostImage']

    if event == 'create' and len(values['create']) > 3:
        try:
            err = executeScript('create', values['mode'], values['if'], values['create'])
        except Exception as e:
            print(e) 
            err = True
        if err:
            sg.popup('An error occured.')
    elif event == 'pattern' and len(values['pattern']) > 3:
        try:
            err = executeScript('pattern', values['mode'], values['pattern'], '')
        except Exception as e:
            print(e) 
            err = True
        if err:
            sg.popup('An error occured.')