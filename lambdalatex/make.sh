wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
docker build -t octech/lambdalatex .
docker run --rm -it -v $(pwd):/var/host octech/lambdalatex zip --symlinks -r -9 /var/host/latexlambda_v3.zip .
