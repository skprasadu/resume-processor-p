convert -density 300 $1 -depth 8 -strip -background white -alpha off $1.tiff
tesseract $1.tiff $1
cat $1.txt
rm $1.t*
