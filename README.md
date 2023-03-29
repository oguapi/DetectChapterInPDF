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

## Outputs
Detecting characters:

![Output1][lil-out1-url]

Detecting words:

![Output2][lil-out2-url]

Detecting numbers:

![Output3][lil-out3-url]

In the detecting numbers we didn't get good results maybe because we don't use any image preprocessing as recommendend in the official repository. For more information, visit [here](https://github.com/tesseract-ocr/tessdoc/blob/main/ImproveQuality.md#binarisation).

[lil-out1-url]: https://raw.githubusercontent.com/oguapi/OCRWithTesseract/master/assets/output1.jpg
[lil-out2-url]: https://raw.githubusercontent.com/oguapi/OCRWithTesseract/master/assets/output2.jpg
[lil-out3-url]: https://raw.githubusercontent.com/oguapi/OCRWithTesseract/master/assets/output3.jpg
