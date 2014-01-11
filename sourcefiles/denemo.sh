#!/bin/bash 
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PREFIX=$DIR/../Resources

export LD_LIBRARY_PATH=$PREFIX/lib:$LD_LIBRARY_PATH
export DYLD_FALLBACK_LIBRARY_PATH=$PREFIX/lib:$HOME/lib:/usr/local/lib:/usr/lib
export LILYPOND_PATH=$PREFIX/bin/lilypond
export GUILE_LOAD_PATH=$PREFIX/share/guile/1.8:$PREFIX/share/denemo/actions/denemo-modules/

export PANGO_RC_FILE=$PREFIX/etc/pango/pangorc
export PANGO_PREFIX=$PREFIX
export PANGO_MODULE_VERSION="1.6.0"
export PANGO_SO_EXTENSION=".so"

export EVINCE_MODULE_PATH=$PREFIX/lib/evince/2/backends

export FONTCONFIG_PATH=$PREFIX/etc/fonts
export FONTCONFIG_FILE=$PREFIX/etc/fonts/fonts.conf 
if [ ! -d "~/Library/Fonts" ]; then
    mkdir -p ~/Library/Fonts
fi
cp -r $PREFIX/share/fonts/* ~/Library/Fonts/
$PREFIX/bin/fc-cache -fv ~/Library/Fonts/
$PREFIX/bin/pango-querymodules > $PREFIX/etc/pango/pango.modules
$PREFIX/bin/denemo
