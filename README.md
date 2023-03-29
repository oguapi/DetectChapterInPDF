# OCR-with-Tesseract
Text Detector + Draw bbox!

## Requirements
    * Python 3.9
    * requirements.txt

## PyMuPDF
https://github.com/pymupdf/PyMuPDF

## Text Detector
This project is a text detector with Tesseract, official repository [here](https://github.com/tesseract-ocr/tessdoc).
After detect the texts and the position, we draw a box where encapsulate the words. The Mannheim University Library (UB Mannheim) uses Tesseract to perform text recognition (OCR = optical character recognition). We need install Tesseract before use it in python with a library, the installers for windows can be access [here](https://github.com/UB-Mannheim/tesseract/wiki). I use the version of tesseract v5.0.0.

## Pytesseract
In Python we need use Python-tesseract which is a wrapper for Google's Tesseract-OCR Engine. Tt can read all image types supported by the Pillow and Leptonica imaging libraries, including jpeg, png, gif, bmp, tiff, and others. For more information, you can see the official repository [here](https://pypi.org/project/pytesseract/).

This process is implemented python, and the following libraries:
  * Pytesseract (text detector)
  * OpenCV (For draw bbox)
  * Os (For manage path)
  * Csv (For manage csv file)

## Outputs
Some pages where we detecting characters:

![Pag1][lil-pag1-url]

Page 2:

![Pag2][lil-pag2-url]

Page 3:

![Pag3][lil-pag3-url]

The output csv is:

![Csv File][lil-csv-url]

In the detecting numbers we didn't get good results maybe because we don't use any image preprocessing as recommendend in the official repository. For more information, visit [here](https://github.com/tesseract-ocr/tessdoc/blob/main/ImproveQuality.md#binarisation).

[lil-pag1-url]: https://raw.githubusercontent.com/oguapi/DetectChapterInPDF/master/assets/IndiceLibroOpencv_page1OCR.png
[lil-pag2-url]: https://raw.githubusercontent.com/oguapi/DetectChapterInPDF/master/assets/IndiceLibroOpencv_page2OCR.png
[lil-pag3-url]: https://raw.githubusercontent.com/oguapi/DetectChapterInPDF/master/assets/IndiceLibroOpencv_page3OCR.png
[lil-csv-url]: https://raw.githubusercontent.com/oguapi/DetectChapterInPDF/master/assets/newCsv.csv