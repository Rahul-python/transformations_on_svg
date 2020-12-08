
**Author : _Rahul Jakkamsetty_**

The purpose of this project is to create four svg files with objects circle, square, triangle and polyline and read them and apply transformations
on objects like rotation, scale and translation.

The codes are present in **[src](https://github.com/Rahul-python/transformations_on_svg/tree/main/src)** folder.
## file_1: [create_svg.py](https://github.com/Rahul-python/transformations_on_svg/blob/main/src/create_svg.py)

The file 'create_svg.py' creates different objects with opencv, detects the contours and writes to svg file in binary mode.
These svg files are stored in data folder.
Four svg files will be created in **[data](https://github.com/Rahul-python/transformations_on_svg/tree/main/data)** folder: circle.svg, square.svg, triangle.svg and polyline.svg.

## file_2: [recognition_transform.py](https://github.com/Rahul-python/transformations_on_svg/blob/main/src/recognition_transform.py)

**Neither numpy nor opencv is used**.

The **ElementTree** module from **_xml.etree_** library is used for parsing svg files and doing transformations.

This code reads the saved files in data folder. If the code is run from src folder, the path is 'shape.svg' else,
else the whole path should be given. The shapes are stored in svg with path tag. So, these objects are detected
and corresponding images are written back to same file with object tags rather than path tag.

The **transform** method of class **'Image_Recog_Transform'** does the transformation on the objects.

The further documentation of the functions/methods can be found in the code file itself.

_Note: The transformation may go out of the viewBox._
