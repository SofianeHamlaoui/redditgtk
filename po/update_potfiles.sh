#!/bin/bash

APPNAME="redditgtk"

if [ -z $1 ]; then
    echo "Usage: $0 lang"
    exit
fi
lang="$1"

rm *.pot

version=$(fgrep "version: " ../meson.build | grep -v "meson" | grep -o "'.*'" | sed "s/'//g")

find ../$APPNAME -iname "*.py" | xargs xgettext --package-name=$APPNAME --package-version=$version --from-code=UTF-8 --output=$APPNAME-python.pot
find ../data/ui -iname "*.glade" -or -iname "*.xml" | xargs xgettext --package-name=$APPNAME --package-version=$version --from-code=UTF-8 --output=$APPNAME-glade.pot -L Glade
find ../data/ -iname "*.desktop.in" | xargs xgettext --package-name=$APPNAME --package-version=$version --from-code=UTF-8 --output=$APPNAME-desktop.pot -L Desktop
find ../data/ -iname "*.appdata.xml.in" | xargs xgettext --no-wrap --package-name=$APPNAME --package-version=$version --from-code=UTF-8 --output=$APPNAME-appdata.pot

msgcat --use-first $APPNAME-python.pot $APPNAME-glade.pot $APPNAME-desktop.pot $APPNAME-appdata.pot > $APPNAME.pot

sed 's/#: //g;s/:[0-9]*//g;s/\.\.\///g' <(fgrep "#: " $APPNAME.pot) | sort | uniq | grep -v " " > POTFILES.in

[ -f "${lang}.po" ] && mv "${lang}.po" "${lang}.po.old"
msginit --locale=$lang --input $APPNAME.pot
if [ -f "${lang}.po.old" ]; then
    mv "${lang}.po" "${lang}.po.new"
    msgmerge -N "${lang}.po.old" "${lang}.po.new" > ${lang}.po
    rm "${lang}.po.old" "${lang}.po.new"
fi
sed -i 's/ASCII/UTF-8/' "${lang}.po"
rm *.pot
