#
# Copyright 2005 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
#ident	"@(#)Makefile 1.7 09/02/17 SMI"
#

# Master hcts packaging Makefile, top level
#!/bin/sh

ARCH	:sh = uname -p
i386_dir	= bat_detect
sparc_dir	=

SUBDIRS=all_devices dmi hd_detect $($(ARCH)_dir)
PKGDIR=$(SRC)/pkg/pkgarchive
PKGDEF=$(SRC)/pkg/pkgdef
PKGNAME=SUNWddu

all :=          TARGET= all
clean :=        TARGET= clean 
lint :=         TARGET= lint
check :=        TARGET= check

all clean lint check: $(SUBDIRS)

$(SUBDIRS): FRC	
	@cd $@; pwd; $(MAKE) $(TARGET) 
FRC:

packages:
	@echo "Building packages"
	cd $(PKGDEF) ; \
	pkgmk -o -r . -d . -f prototype ; \
	cp -r $(PKGNAME) $(PKGDIR) ; \
	cd $(PKGDIR) ; \
	chmod 755 $(PKGNAME) ; \
	tar cvfpe $(PKGNAME).tar $(PKGNAME) ; \
	gzip $(PKGNAME).tar ; \
	chmod 755 $(PKGNAME).tar.gz

pkgclean:
	cd $(PKGDEF); rm -rf SUNW*; \
	cd $(PKGDIR); rm -rf SUNW*
