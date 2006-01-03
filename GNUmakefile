
default: all

all: linux mingw mac


# local.make should set the following variables:
#
#  LILYPOND_CVSDIR - a CVS HEAD working directory
#

include local.make


include $(LILYPOND_CVSDIR)/VERSION

LILYPOND_VERSION=$(MAJOR_VERSION).$(MINOR_VERSION).$(PATCH_LEVEL)$(if $(strip $(MY_PATCH_LEVEL)),.$(MY_PATCH_LEVEL),)

INVOKE_DRIVER=python driver.py \
--platform $(1) \
--package-version=$(LILYPOND_VERSION) \
--package-build=1 \
$(LOCAL_DRIVER_OPTIONS)
INVOKE_XPM=python xpm-apt.py --platform $(1) 

BUILD_ALL=$(call INVOKE_DRIVER, $(1)) -t build all \
  && $(call INVOKE_XPM, $(1)) -t install all \
  && $(call INVOKE_DRIVER, $(1)) build all \
  && $(call INVOKE_XPM, $(1)) install all \
  && $(call INVOKE_DRIVER, $(1)) build-installer \
  && $(call INVOKE_DRIVER, $(1)) package-installer \

download:
	$(call INVOKE_DRIVER, darwin) download
	$(call INVOKE_DRIVER, freebsd) download
	$(call INVOKE_DRIVER, linux) download
	$(call INVOKE_DRIVER, mingw) download
	rm -f uploads/*/lilypond-HEAD*gub

all: linux freebsd mac mingw

linux:
	$(call BUILD_ALL, $@)

## FIXME: urg, why not using dependencies anymore?
freebsd:
	$(call BUILD_ALL, $@)

mac:
	$(call BUILD_ALL, darwin)

mingw:
	$(call BUILD_ALL, $@) 

distclean:
	rm -rf target uploads

sources = GNUmakefile $(wildcard *.py specs/*.py)

TAGS: $(sources)
	etags $^

cyg-apt.py: cyg-apt.py.in specs/cpm.py
	sed -e "/@CPM@/r specs/cpm.py" -e "s/@CPM@//" < $< > $@
	chmod +x $@

RUN_TEST=python test-gub.py --to hanwen@xs4all.nl --to janneke@gnu.org --smtp smtp.xs4all.nl "make $(1)" 
test:
	$(MAKE) distclean
	$(call RUN_TEST,mac)
	$(call RUN_TEST,mingw)
	$(call RUN_TEST,freebsd)
	$(call RUN_TEST,linux)
