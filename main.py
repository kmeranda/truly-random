import httplib2 # to issue GET requests
import argparse # to handle flag arguments
from PIL import Image    # to create bitmap
import wave     # to create wav file
import struct   # to create wav file
#import random   # test without using quota

def main():
    # parse flags to decide what to do
    parser = argparse.ArgumentParser('Choose what to use the random.org random numbers for.')
    parser.add_argument('-bitmap', help='create 128x128 RGB bitmap. (default if nothing selected)', action='store_true')
    parser.add_argument('-wav', help='create white white_noise.wav file.', action='store_true')
    parser.add_argument('-RSA', help='create RSA key pair.', action='store_true')
    args = parser.parse_args()
    if args.bitmap: # create 128x128 RGB bitmap
        bitmap(128, 128, 'temp.bmp')
    if args.wav:    # create white white_noise.wav file
        wav(3, 'white_noise.wav')
    if args.RSA:    # create RSA key pair
        RSA()
    if not(args.bitmap or args.wav or args.RSA):
        print 'No option selected, defaulted to bitmap generation'
        bitmap()

# get random numbers from Random.org HTTP API
def get_nums(total, min_val, max_val, base):
    vals = []
    # issue least number of requests by always requesting the max number of numbers (10000)
    while total > 10000:
        resp, val = httplib2.Http().request("https://www.random.org/integers/?num=" + str(10000) + "&min=" + str(min_val) + "&max=" + str(max_val) + "&col=1&base=" + str(base) + "&format=plain&rnd=new")
        val = val.split('\n')
        vals.extend(val)
        total -= 10000
    # get leftover numbers
    resp, val = httplib2.Http().request("https://www.random.org/integers/?num=" + str(total) + "&min=" + str(min_val) + "&max=" + str(max_val) + "&col=1&base=" + str(base) + "&format=plain&rnd=new")
    val = val.split('\n')
    vals.extend(val)
    return vals

def bitmap(w, h, filename):
    img = Image.new( 'RGB', (w,h), "black") # create a new black image
    pixels = img.load() # create the pixel map
    total = w*h*3   # number of pixels
    vals = get_nums(total, 0, 255, 10)  # get random numbers from Random.org
    # create bitmap
    for i in range(w):
        for j in range(h):
            pos = 3*(i*h+j)
            pixels[i,j] = (int(vals[pos]), int(vals[pos+1]), int(vals[pos+2]))
    img.save(filename)    # save generated image as rand.bmp
    print w, ' by ', h,' sized RGB bitmap file created and stored in file ', filename

    # psuedo random testing to keep from going over quota
    #w = 128
    #h = 128
    #img = Image.new( 'RGB', (w,h), "black") # create a new black image
    #pixels = img.load() # create the pixel map

    #for i in range(img.size[0]):    # for every pixel:
    #    for j in range(img.size[1]):
    #        pixels[i,j] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) # set the colour accordingly
    #img.save(filename)
    #img.show()

def wav(sec, filename):
    samps = 44100   # number of samples per second
    vals = []
    total = sec*samps   # total number of samples needed for file
    max_freq = 32767
    vals = get_nums(total, -1*max_freq, max_freq, 10)   # get random numbers from Random.org
    # create wav file
    outfile = wave.open(filename, 'w')
    outfile.setparams((2, 2, samps, 0, 'NONE', 'not compressed'))
    # fill file with random values (white noise)
    for i in range(total):
        packed_value = struct.pack('h', int(vals[i]))
        outfile.writeframes(packed_value)
        outfile.writeframes(packed_value)
    outfile.close()
    print sec, ' second long wav file created and stored in file ', filename

    # psuedo random testing to keep from going over quota
    #samps = 44100
    #outfile = wave.open(filename, 'w')
    #outfile.setparams((2, 2, samps, 0, 'NONE', 'not compressed'))

    #for i in range(samps*3):
    #    value = random.randint(-32767, 32767)
    #    packed_value = struct.pack('h', value)
    #    outfile.writeframes(packed_value)
    #    outfile.writeframes(packed_value)
    #outfile.close()

def RSA():
    print 'RSA functionality not yet implemented'

if __name__ == '__main__':
    main()
