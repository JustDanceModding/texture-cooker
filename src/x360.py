import subprocess
from os import listdir, makedirs, SEEK_SET
from shutil import rmtree
from CookerFunctions.UbiHeader import UbiartHeader
from CookerFunctions.ConvertPlatform import ConvertTexture
from CookerFunctions.RDF import RDF

def convert_to_png_MAGICK(image_path, output_png, binary_path="bin"):
    subprocess.run(
        f'''{binary_path}\\magick.exe convert "{image_path}" "{output_png}"''',
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )

def has_transparency(image_path, binary_path="bin"):
    completed_process = subprocess.Popen(
        f'''{binary_path}\\magick.exe identify -format '%[channels]' "{image_path}"''',
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        shell=True,
        text=True
    )

    stdout_output, stderr_output = completed_process.communicate()

    if completed_process.returncode == 0:
        output = stdout_output
    else:
        output = stderr_output

    if "srgba" in output:
        return True
    elif "srgb" in output and "srgba" not in output:
        return False
    elif "rgba" in output:
        return True
    elif "rgb" in output and "rgba" not in output:
        return False
    elif "p" in output:
        return True
    
def main():
    print("Texture Cooker for X360")
    makedirs("toCook", exist_ok=True)
    makedirs("cooked\\x360", exist_ok=True)

    for image in listdir("toCook"):
        print("Current Texture:", image)
        makedirs("temp", exist_ok=True)
        png = image.split(".") [0] + '.png'
        rdf = image.split(".") [0] + '.rdf'
        xpr = image.split(".") [0] + '.xpr'

        transparency = has_transparency(f"toCook/{image}")

        ckd = image.split(".")[0] + '.png.ckd' if transparency else image.split(".")[0] + '.tga.ckd'

        convert_to_png_MAGICK(f"toCook/{image}", f"temp/{png}")

        MakeRDF = RDF.make(f"temp\\{png}", png, f"temp\\{rdf}")
        MakeXPR = ConvertTexture.convert(f"temp\\{rdf}", platform="x360")

        MakeHeader = UbiartHeader.create_header

        header = MakeHeader(f"temp/{png}", imageEncoded=f"temp\\{xpr}")

        with open(f"cooked/x360/{ckd}", "wb") as final:
            final.write(header)
            with open(f"temp/{xpr}", "rb") as temp:
                temp.read(0x2D)
                final.write(temp.read(0x33))
                temp.seek(2060, SEEK_SET)
                final.write(temp.read())

    rmtree("temp")

if __name__ == "__main__":
    main()