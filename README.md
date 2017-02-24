Kelsey Meranda

In order to used the python file to generate a bitmap or wav file, you must use flags to indicate which ones you want to use (-bitmap, -wav, -RSA not implemented).
For example, to get the program to only generate a bitmap, you would run it with the following terminal command: "python main.py -bitmap"
If you wanted the program to generate a bitmap and a wav file, youo would run it with the following terminal command: "python main.py -bitmap -wav"
by default, if no flags are used, the program just generates the bitmap

This program uses Python 2.7 and depends on the following libraries: httplib2, argparse (for the flag handling), PIL (Python Image Library), wave, struct, and random (random was only used to test logic without using up my request quota at Random.org, and shouldn't be necessary for the final files submitted)

Note: Unfortunately, I ran out of time and did not have a chance to implement RSA. Using the -RSA flag will result in nothing happening.
