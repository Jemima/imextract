README
======

Usage
-------
search.py -i in\_file -o out\_folder
Searches in\_file for images, and extracts them if found.

Summary
-------
Have a big list of magic values for image formats (see appendix A), create an Aho-Corasick FSM at compile-time, and then use said FSM to search input file for instances of magic values. Whenever a magic value is found hand off to a specialised helper which will do additional validation, and if it looks like a valid image, export it to a file.

All the fancy searching stuff is TBD, at the moment it's a brute-force approach.


Appendices
==========
Magic Values
--------------

Format    | Sequence (BE)
------    | ---------------------------
Bitmap    | 42 4D
GIF       | 47 49 46 38 39 61
GIF       | 47 49 46 38 37 61
JPEG      | FF D8
JPEG/JFIF | 4A 46 49 46 00
JPEG/EXIF | 45 78 69 66 00
PNG       | 89 50 4E 47 0D 0A 1A 0A
TIFF (LE) | 49 49 2A 00
TIFF (BE) | 4D 4D 00 2A

