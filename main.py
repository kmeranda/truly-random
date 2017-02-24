import httplib2 # to issue GET requests
import argparse # to handle flag arguments
from PIL import Image    # to create bitmap
import wave     # to create wav file
import struct   # to create wav file
import random   # test without using quota

def main():
    # parse flags to decide what to do
    parser = argparse.ArgumentParser('Choose what to use the random.org random numbers for.')
    parser.add_argument('-bitmap', help='create 128x128 RGB bitmap.', action='store_true')
    parser.add_argument('-wav', help='create white white_noise.wav file.', action='store_true')
    parser.add_argument('-RSA', help='create RSA key pair.', action='store_true')
    args = parser.parse_args()
    if args.bitmap: # create 128x128 RGB bitmap
        bitmap()
    if args.wav:    # create white white_noise.wav file
        wav()
    if args.RSA:    # create RSA key pair
        RSA()

def bitmap():
    w = 128 # width of image
    h = 128 # height of image
    img = Image.new( 'RGB', (w,h), "black") # create a new black image
    pixels = img.load() # create the pixel map
    vals = []
    total = w*h*3   # number of pixels left
    # issue least number of requests by always requesting the max number of numbers (10000)
    while total > 10000:
        resp, row = httplib2.Http().request("https://www.random.org/integers/?num=" + str(10000) + "&min=1&max=255&col=1&base=10&format=plain&rnd=new")
        row = row.split('\n')
        vals.extend(row)
        total -= 10000
    # get leftover numbers
    resp, row = httplib2.Http().request("https://www.random.org/integers/?num=" + str(total) + "&min=1&max=255&col=1&base=10&format=plain&rnd=new")
    row = row.split('\n')
    vals.extend(row)
    # create bitmap
    for i in range(w):
        for j in range(h):
            pos = 3*(i*h+j)
            pixels[i,j] = (vals[pos], vals[pos+1], vals[pos+2])
    img.save('temp.bmp')    # save generated image as temp.bmp

    # psuedo random testing to keep from going over quota
    #w = 128
    #h = 128
    #img = Image.new( 'RGB', (w,h), "black") # create a new black image
    #pixels = img.load() # create the pixel map

    #for i in range(img.size[0]):    # for every pixel:
    #    for j in range(img.size[1]):
    #        pixels[i,j] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) # set the colour accordingly
    #img.save('temp.bmp')
    #img.show()

def wav():

    samps = 44100   # number of samples per second
    vals = []
    total = 3*samps   # number of samples
    max_freq = 32767
    # issue least number of requests by always requesting the max number of numbers (10000)
    while total > 10000:
        resp, val = httplib2.Http().request("https://www.random.org/integers/?num=" + str(10000) + "&min=" + str(-1*max_freq) + "&max=" + str(max_freq) + "&col=1&base=10&format=plain&rnd=new")
        val = val.split('\n')
        vals.extend(val)
        total -= 10000
    # get leftover numbers
    resp, val = httplib2.Http().request("https://www.random.org/integers/?num=" + str(total) + "&min=" + str(-1*max_freq) + "&max=" + str(max_freq) + "&col=1&base=10&format=plain&rnd=new")
    val = val.split('\n')
    vals.extend(val)
    # create wav file
    outfile = wave.open('white_noise.wav', 'w')
    outfile.setparams((2, 2, samps, 0, 'NONE', 'not compressed'))
    # fill file with random values (white noise)
    for i in range(samps*3):
        packed_value = struct.pack('h', vals[i])
        outfile.writeframes(packed_value)
        outfile.writeframes(packed_value)
    outfile.close()

    # psuedo random testing to keep from going over quota
    #samps = 44100
    #outfile = wave.open('white_noise.wav', 'w')
    #outfile.setparams((2, 2, samps, 0, 'NONE', 'not compressed'))

    #for i in range(samps*3):
    #    value = random.randint(-32767, 32767)
    #    packed_value = struct.pack('h', value)
    #    outfile.writeframes(packed_value)
    #    outfile.writeframes(packed_value)
    #outfile.close()

def RSA():
    pass

if __name__ == '__main__':
    main()
