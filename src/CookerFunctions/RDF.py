from PIL import Image

class RDF:
    def make(im, imageForRDF, rdfOut):
        imageStream = Image.open(im)
        width, height = imageStream.size

        if imageStream.mode == "RGBA" or (imageStream.mode == "P" and "transparency" in imageStream.info):
            format = "D3DFMT_DXT5"
        else:
            format = "D3DFMT_DXT1"

        rdf = f'''
        <RDF Version="XPR2">
        <Texture 
        Name = "StrName"
        Source = "{imageForRDF}"
        Format = "{format}"
        Width = "{width}"
        Height = "{height}"
        Levels = "1"
        />
        </RDF>'''

        open(rdfOut, "w").write(rdf)