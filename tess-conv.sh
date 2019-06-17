convert -density 300 ea.pdf -depth 8 -strip -background white -alpha off file.tiff
tesseract file.tiff output.txt
cat output.txt
