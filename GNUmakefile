.PHONY: lilypond mingit phone web
.PHONY: default compilers TAGS help
sources = GNUmakefile $(filter-out %~, $(wildcard *.make bin/* gub/*.py gub/*/*.py gub/*/*/*.py gub/*/*/*/*.py test-lily/*.py))

ifeq ($(PLATFORMS),)
PLATFORMS=linux-x86 darwin-ppc darwin-x86 mingw linux-64 linux-ppc freebsd-x86 freebsd-64 # linux-mipsel
endif

default: compilers

include gub.make
include compilers.make

TAGS: $(sources)
	etags $^

MAKE_FILES = $(filter-out compilers.make gub.make local.make,$(wildcard *.make))
MAKE_BASES = $(MAKE_FILES:%.make=%)

help:
	@echo Usage: make [TAGS $(foreach a,$(MAKE_BASES),"| $(strip $(a))")]
	@echo
	@echo For more elaborate use, see README and bin/gub --help

$(MAKE_BASES):
	$(MAKE) -f $@.make

lily% cygwin%:
	$(MAKE) -f lilypond.make $@

denemo-%:
	$(MAKE) -f denemo.make $@

inkscape-%:
	$(MAKE) -f inkscape.make $@

openoffice-%:
	$(MAKE) -f openoffice.make $@

test:
	rm -rf target
	make -f lilypond.make tools LOCAL_GUB_OPTIONS=-vvv
	bin/gub -p $(BUILD_PLATFORM) --branch=lilypond=master:master lilypond -vvv

README: web/index.html web/basics.html web/lilypond.html web/denemo.html web/inkscape.html web/oo.o.html web/history.html web/links.html
	w3m -dump $^ | sed 's/website by.*$..//' > $@

web: README
	scp -p web/*.html web/*.css lilypond.org:/var/www/lilypond/gub

PYTHON_SOURCES = $$(git ls-files | grep -E '(^bin/|*.py$$)' | grep -Ev 'gub/(2|3)/')
python3:
ifeq (0,0) # a 2to3 crash fails to convert the remaining files
	2to3-3.0 -nw -x urllib -x next $(PYTHON_SOURCES) >/dev/null
else
	for i in $(PYTHON_SOURCES); do\
	    2to3-3.0 -nw -x urllib -x next $$i >/dev/null || :; \
	done
endif
# fix breakages
	sed -i -e 's@^\( *\)\t@\1        @g' \
	    -e 's@subprocess[.]\(AutogenMagic\|Chmod\|Conditional\|Copy\|CreateShar\|Dump\|ForcedAutogenMagic\|Func\|MapLocate\|Message\|Mkdir\|PackageGlobs\|Remove\|Rename\|Rmtree\|ShadowTree\|Substitute\|Symlink\|System\|UpdateSourceDir\)@commands.\1@g' \
		$(PYTHON_SOURCES)
# cleaning
	sed -i \
	     -e 's@\(for .* in\) list(\(.*[.]\(keys\|items\|values\)\) *()):@\1 \2 ():@' $(git ls-files | grep -E '(^bin/|*.py$)') \
	    -e 's@\(list\|next\|print\)(@\1 (@g' \
		$(PYTHON_SOURCES)

python3-stats:
	git diff origin p3 | grep -E '^(\+|X-) '| sed -e 's@^\(.\) *@\1@g' -e 's@^\(.\).*\(dbhash\|dbm\|md5\|0o\|new\|list (\|__self__\)@\1\2@g' | sort

python3-printf:
	sed -i \
	    -e 's@ print \([^(].*\)@ printf (\1)@g' \
	    -e 's@ print @ printf @g' \
		$(PYTHON_SOURCES)
	sed -i \
	    -e 's@#\nfrom gub import@#\nfrom gub.syntax import printf\nfrom gub import@' $$(grep -l printf $$(git diff --name-only))
# sed 4.0.1 is broken, what t[ext]t[tool] do you use?
	pytt '#\nfrom gub import' '#\nfrom gub.syntax import printf\nfrom gub import' $$(grep -l printf $$(git diff --name-only))
