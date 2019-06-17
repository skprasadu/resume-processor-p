convert $1 -colorspace Gray ocr.tif 
tesseract ocr.tif $1
cat $1.txt
