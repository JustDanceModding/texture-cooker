from PIL import Image
from ..Utils import *

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
