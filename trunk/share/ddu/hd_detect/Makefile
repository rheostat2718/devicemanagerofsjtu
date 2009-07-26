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
#ident	"@(#)Makefile 1.2 09/02/17 SMI"
#

include $(SRC)/include/Makefile.master

DBX		=
CFLAGS		+= $(DBX)
LDFLAGS		+= 
LDLIBS		= -ldevinfo -lMPAPI

BINDIR		= ../bin/$(ARCH)
TARGETS		= $(BINDIR)/hd_detect

SRCS		=		\
		hd_detect.c	\
		disk_info.c	\
		mpath.c

HDRS		=		\
		hd_detect.h	\
		disk_info.h	\
		mpath.h

OBJS		= $(SRCS:.c=.o)
ALWAYS_LINT_DEFS        += -erroff=E_NAME_USED_NOT_DEF2
##### beginning of dependency lines #####
all: $(TARGETS)
 
$(TARGETS): $(OBJS)
	    $(LINK.c) $(OBJS) -o $@ $(LDLIBS) ; \
	    strip $(TARGETS)

include $(SRC)/include/Makefile.targ
