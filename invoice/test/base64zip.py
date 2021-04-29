import base64
import zipfile
import os
import io



def zipdir(path, ziph):
    cwd = os.getcwd()
    os.chdir(path)
    # ziph is zipfile handle
    for root, dirs, files in os.walk('./'):
        for file in files:
            ziph.write(os.path.join(root, file))
    os.chdir(cwd)      
            
if __name__ == '__main__':
    
    zipf = zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('./lol/', zipf)
    zipf.close()



#zip file to base64
if False:
    zfile = "testtex.zip"

    with open(zfile, "rb") as f:
        bytes = f.read()
        encoded = base64.b64encode(bytes)

# Base64 to zip file
if False:
    bytes = base64.b64decode(encoded)
    z = zipfile.ZipFile(io.BytesIO(bytes))
    z.extractall(path="./lol/")
    # Decode back 

