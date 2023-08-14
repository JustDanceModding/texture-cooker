from PIL import Image
import subprocess

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

class RDF:
    def make(image, imageOnRDF, rdfOut):
        imageStream = Image.open(image)
        width, height = imageStream.size

        alpha = has_transparency(image)

        if alpha:
            format = "D3DFMT_DXT5"
        else:
            format = "D3DFMT_DXT1"

        rdf = f'''<RDF Version="XPR2"><Texture Name = "StrName" Source = "{imageOnRDF}" Format = "{format}" Width = "{width}" Height = "{height}" Levels = "1" /></RDF>'''

        open(rdfOut, "w").write(rdf)

        imageStream.close()
