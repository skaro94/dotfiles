#!/bin/bash

FILEPATH=$PDF_FILE
IMG_SIZE=$HTML_IMG_WIDTH

DIR=$(echo $FILEPATH | rev | cut -d'/' -f2- | rev)"/"
HTMLDIR=$DIR"html/"
FILE=$(echo $FILEPATH | rev | cut -d'/' -f-1 | rev)
CUTNAME="$(echo $FILE | rev | cut -d'.' -f2- | rev)"
IMGPATH=$HTMLDIR

echo $FILEPATH
echo $DIR
echo $HTMLDIR
echo $FILE

rm -rf $HTMLDIR
rm -f $DIR$CUTNAME"s.post.html"

mkdir $HTMLDIR
cp $FILEPATH $HTMLDIR$FILE

pdftohtml -nomerge -nodrm "$HTMLDIR$FILE" > $TR_ROOT"/out.log"
python "$TR_UTIL/fix_div.py" -f $HTMLDIR$CUTNAME"s.html" -i $IMG_SIZE >> $TR_ROOT"/out.log"
mv $HTMLDIR$CUTNAME"s.post.html" $DIR$CUTNAME".html" >> $TR_ROOT"/out.log"

IMGS=$(find $IMGPATH -name '*.jpg' -o -name '*.png')

for img in $IMGS; do
    path=$(realpath $img)

    dir=$(echo $path | rev | cut -d'/' -f2- | rev)
    file=$(echo $path | rev | cut -d'/' -f-1 | rev)
    convert -resize $IMG_SIZE"x" $img $dir"/post_"$file >> $TR_ROOT"/out.log"
done
