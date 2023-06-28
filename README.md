## Requirements
WARNING: nvcompress is required for every platform.
- Bundler.exe from the Xbox 360 SDK for Xbox 360
- [Wiimms Image Tool](https://szs.wiimm.de/wimgt/) for Wii
- [XTX-Extractor](https://github.com/aboood40091/XTX-Extractor) for NX
- TexConv2 for WiiU
- dds2gtf for PS3
- nvcompress for PC/PS4/Xbox One

## How to use
In the "toCook" folder you need to put your textures (dosen't matter which format)
Run the cooker of the platform you're going to cook for, ex. cook-ps3.py
And then on the folder "cookedTex" you'll get the cooked textures in  base of your platform. ex. "cookedTex/ps3/texture.tga.ckd"

Create a "bin" folder and inside you put the programs required for the cooking. ex. "bin\dds2gtf.exe"

## TODO
- Refactor the header classes as our implementation is not so right.
- PS4 Cooking
- Xbox 360 Encoding
- Wii Encoding
- Wii U Encoding
- PS3 Encoding
- NX Encoding

If you found this useful, leave a star! :D
