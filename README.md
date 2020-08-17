# sentenceAlignmentTool
A semi-automatic English-Vietnamese sentence alignment tool.

# Python version 3.7 (We use python version 3.7.4)

# Library needed to be installed:
- nltk
- underthesea
- Flask
- googletrans
- sklearn
- numpy
- Werkzeug

# How to use it
- First choose "Chọn tệp"
- You have 2 options:
 + Choose 2 files, 1 file is in English and the other is in Vietnamese. Note that the English file has to have "el" in the file's name, and the Vietnamese file has to have "vn" in the file's name.
 + Choose 1 file which contains the previous works of yours (This file has to have our format). If you want to recreate this specific file (wait, there is no way you wanna do that, but I'm gonna explain the format anyway),
 the format is:
    "+(en)This is English sentence INSERT_NEW_LINE This is English sentence INSERT_NEW_LINE ...
    (vi)This is Vietnamese sentence INSERT_NEW_LINE This is Vietnamese sentence INSERT_NEW_LINE ...
    INSERT_NEW_LINE
    INSERT_NEW_LINE
    +(en)..."
    The cycle continues. Notice the "+" at the beginning, it represents for unchecked box or unfinished work. If it's removed then that pair is clean data.
- Choose "Gửi", if you have 2 files chosen then it might take a while (about 10s) to translate so be patient. On the other hand, loading 1 file is so much faster, literally 1s. That's why I recommend you to save the file after the first time you load it and work with that file.
- Begin or continue your works. Check the box if you finish a pair
- Finally, press download if you need to save your works
