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
# Copyright 2007 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
#ident	"@(#)Makefile 1.6 09/02/17 SMI"
#
include $(SRC)/include/Makefile.master

DBX		=
CFLAGS		+= $(DBX) -D_SunOS_
LDFLAGS		+= 
LDLIBS		= -ldevinfo

BINDIR		= ../../bin/i386
TARGETS		= $(BINDIR)/dmi_info

SRCS1		=		\
		bios_info.c	\
		cpuid_info.c	\
		dev_scan.c	\
		dmi_info.c	\
		mem_info.c	\
		cpu_info.c	\
		dev_info.c	\
		dmi.c		\
		mb_info.c	\
		sys_info.c

SRCS2		= cpuid.s
SRCS		= $(SRCS1) $(SRCS2)

HDRS		=		\
		bios_info.h	\
		cpuid_info.h	\
		dmi_info.h	\
		mem_info.h	\
		cpu_info.h	\
		dev_info.h	\
		dmi.h		\
		mb_info.h	\
		sys_info.h

OBJS1		= $(SRCS1:.c=.o)
OBJS2		= $(SRCS2:.s=.o)
ALWAYS_LINT_DEFS        += -erroff=E_STATIC_UNUSED
##### beginning of dependency lines #####
all: $(TARGETS)
 
$(TARGETS): $(OBJS1) $(OBJS2)
	    $(LINK.c) $(OBJS1) $(OBJS2) -o $@ $(LDLIBS) ; \
	    strip $(TARGETS)

include $(SRC)/include/Makefile.targ
