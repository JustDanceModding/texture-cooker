from CookerFunctions import *
from os import makedirs, listdir

makedirs("toCook", exist_ok=True)

PLATFORM = "NX"
IMAGETODDS = True

makedirs(f"cooked\\{PLATFORM.lower()}", exist_ok=True)

print("UbiArt Multi-Platform Texture Handler by Sen\n\nThis tool was last modified on:\n17 October 2023 - 18:24\n")

for texture in listdir("toCook"):
    print(f"Current Texture: {texture}")
    Cook(texture_input=f"toCook\\{texture}", output_path=f"cooked\\{PLATFORM.lower()}", platform=PLATFORM, todds=IMAGETODDS)