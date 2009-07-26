#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License, Version 1.0 only
# (the "License").  You may not use this file except in compliance
# with the License.
#
# You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at usr/src/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#
# Copyright 2005 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
#ident	"@(#)Makefile 1.5 09/02/17 SMI"
#

# Makefile for programs kvars and all_devices which
# are used by system_info.sh
#

include $(SRC)/include/Makefile.master

DBX		=
CFLAGS		+= $(DBX)
LDFLAGS		+= 
LDLIBS		= -ldevinfo

BINDIR		= ../bin/$(ARCH)
TARGETS		= $(BINDIR)/all_devices 

SRCS		=		\
		all_devices.c	\
		pci.c		\
		usb.c

HDRS		=		\
		all_devices.h	\
		pci_info.h	\
		usb_info.h

OBJS		= $(SRCS:.c=.o)

##### beginning of dependency lines #####
all: $(TARGETS)
 
$(TARGETS): $(OBJS)
	    $(LINK.c) $(OBJS) -o $@ $(LDLIBS) ; \
	    strip $(TARGETS)

include $(SRC)/include/Makefile.targ

