%define major 4
%define libname %mklibname yaz %{major}
%define develname %mklibname yaz -d

Summary:	Z39.50 protocol support library
Name:		yaz
Version:	4.2.30
Release:	6
License:	BSD-like
Group:		System/Libraries
URL:		http://www.indexdata.dk/yaz/
Source0:	http://ftp.indexdata.dk/pub/yaz/%{name}-%{version}.tar.gz
Source1:	yaz-config.in
Patch0:		yaz-4.2.0-external_libstemmer.diff
BuildRequires:	bison
BuildRequires:	docbook-style-dsssl
BuildRequires:	docbook-style-xsl
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	libstemmer-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	readline-devel
BuildRequires:	tcl
BuildRequires:	tcp_wrappers-devel
# BuildRequires:	termcap-devel

%description
This package contains both a test-server and clients (normal & ssl) for the
ANSI/NISO Z39.50 protocol for Information Retrieval.

%package -n %{libname}
Summary:	Z39.50 Library
Group:		System/Libraries
Requires:	openssl
Requires:	tcp_wrappers
Requires:	%{name} = %{version}-%{release}

%description -n	%{libname}
YAZ is a library for the ANSI/NISO Z39.50 protocol for Information Retrieval.

%package -n %{develname}
Summary:	Z39.50 Library - development package
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel
Provides:	lib%{name}-devel
Conflicts:	%{mklibname yaz 2 -d}
Obsoletes:	%{mklibname yaz 3 -d}

%description -n	%{develname}
Development libraries and includes for the libyaz package.

%prep

%setup -q
%patch0 -p0

# nuke the bundled libstemmer_c just in case
rm -rf libstemmer_c

# i'm sick an dtired of patching this stupid file over and over...
rm -rf yaz-config.in
cp %{SOURCE1} yaz-config.in

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*
perl -pi -e "s|/usr/lib/|%{_libdir}/|g" configure*

%build
autoreconf -fi
%configure2_5x \
    --enable-shared \
    --enable-tcpd \
    --with-openssl \
    --with-xml2 \
    --with-xslt \
    --with-exslt \
    --with-icu

%make

%check
make check

%install

%makeinstall_std docdir=/installed-docs

# fix installed docs
rm -rf installed-docs
mv %{buildroot}/installed-docs .
mv %{buildroot}%{_docdir}/yaz/* installed-docs/

%multiarch_binaries %{buildroot}%{_bindir}/yaz-config

%files
%defattr(644,root,root,755)
%doc README LICENSE installed-docs/*.html installed-docs/*.png
%attr(755,root,root) %{_bindir}/yaz-*
%attr(755,root,root) %{_bindir}/zoomsh
%{_mandir}/man1/yaz-client*.*
%{_mandir}/man1/yaz-iconv.1*
%{_mandir}/man1/yaz-icu.1*
%{_mandir}/man1/yaz-illclient.1*
%{_mandir}/man1/yaz-json-parse.1*
%{_mandir}/man1/yaz-marcdump.1*
%{_mandir}/man1/zoomsh.*
%{_mandir}/man1/yaz-url.1.*
%{_mandir}/man8/yaz-ztest*.*
# moved from lib pkg
%{_mandir}/man7/*
%{_datadir}/yaz/etc

%files -n %{libname}
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(644,root,root,755)
%attr(755,root,root) %{multiarch_bindir}/yaz-config
%{_includedir}/yaz
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/yaz.m4
%{_datadir}/yaz/z39.50
%{_datadir}/yaz/ill
%{_mandir}/man1/yaz-asncomp.*
%{_mandir}/man1/yaz-config.*


%changelog
* Mon Apr 23 2012 Alexander Khrukin <akhrukin@mandriva.org> 4.2.30-1mdv2012.0
+ Revision: 792807
- version update 4.2.30

* Sun Jun 05 2011 Funda Wang <fwang@mandriva.org> 4.2.0-2
+ Revision: 682807
- rebuild for new icu

* Sun May 29 2011 Oden Eriksson <oeriksson@mandriva.com> 4.2.0-1
+ Revision: 681632
- 4.2.0
- fix the friggin multiarch changes
- use the system libstemmer library
- 4.0.12
- provide our own simplified yaz-config.in file (S1) instead of patching the stupid file over and over again....

* Mon Mar 14 2011 Funda Wang <fwang@mandriva.org> 4.0.1-5
+ Revision: 644579
- rebuild for new icu

* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 4.0.1-4mdv2011.0
+ Revision: 615760
- the mass rebuild of 2010.1 packages

* Mon Apr 19 2010 Funda Wang <fwang@mandriva.org> 4.0.1-3mdv2010.1
+ Revision: 536634
- rebuild

* Sun Mar 21 2010 Funda Wang <fwang@mandriva.org> 4.0.1-2mdv2010.1
+ Revision: 526124
- rebuild for new icu

* Thu Feb 18 2010 Oden Eriksson <oeriksson@mandriva.com> 4.0.1-1mdv2010.1
+ Revision: 507482
- 4.0.1

* Mon Nov 09 2009 Frederik Himpe <fhimpe@mandriva.org> 3.0.50-1mdv2010.1
+ Revision: 463704
- update to new version 3.0.50

* Mon Sep 14 2009 Frederik Himpe <fhimpe@mandriva.org> 3.0.48-1mdv2010.0
+ Revision: 440780
- update to new version 3.0.48

* Mon Jul 13 2009 Frederik Himpe <fhimpe@mandriva.org> 3.0.47-1mdv2010.0
+ Revision: 395462
- update to new version 3.0.47

* Wed Jun 10 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0.46-1mdv2010.0
+ Revision: 384871
- 3.0.46
- rediffed patches
- nuke obsolete options

* Tue Mar 03 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.0.41-2mdv2009.1
+ Revision: 347885
- rebuild for latest readline

* Mon Feb 02 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0.41-1mdv2009.1
+ Revision: 336358
- fix build (duh!)
- 3.0.41
- rediffed patches

* Fri Dec 05 2008 Adam Williamson <awilliamson@mandriva.org> 3.0.36-1mdv2009.1
+ Revision: 310408
- rebuild with new tcl
- new release 3.0.36

* Thu Jul 17 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.34-1mdv2009.0
+ Revision: 237499
- rediffed P0

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - update to new version 3.0.34

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri May 16 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.26-1mdv2009.0
+ Revision: 208164
- 3.0.26

* Fri Feb 15 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.24-1mdv2008.1
+ Revision: 168741
- second try (bork bork bork!)
- 3.0.24
- rediffed P0
- make that strange doc install work

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag

* Thu Dec 27 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 3.0.18-2mdv2008.1
+ Revision: 138524
- reintroduce patch 0

* Thu Dec 27 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 3.0.18-1mdv2008.1
+ Revision: 138494
- add bunch of missing buildrequires, and remove not needed ones
- fix file list
- drop patch 0
- new version

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Nov 13 2007 Oden Eriksson <oeriksson@mandriva.com> 3.0.14-2mdv2008.1
+ Revision: 108417
- make it build on cs4

* Tue Oct 23 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 3.0.14-1mdv2008.1
+ Revision: 101377
- new version

* Mon Oct 01 2007 Oden Eriksson <oeriksson@mandriva.com> 3.0.10-2mdv2008.0
+ Revision: 94147
- rebuilt due to missing packages

* Fri Sep 07 2007 Oden Eriksson <oeriksson@mandriva.com> 3.0.10-1mdv2008.0
+ Revision: 81705
- 3.0.10
- drop obolete patches
- new devel naming

* Wed Aug 29 2007 Pixel <pixel@mandriva.com> 3.0.6-3mdv2008.0
+ Revision: 74638
- better conflict on older lib

* Wed Aug 29 2007 Pixel <pixel@mandriva.com> 3.0.6-2mdv2008.0
+ Revision: 74631
- add explicit conflict from libyaz3-devel on libyaz2-devel

* Thu Jun 07 2007 Oden Eriksson <oeriksson@mandriva.com> 3.0.6-1mdv2008.0
+ Revision: 36505
- 3.0.6

* Tue May 08 2007 Oden Eriksson <oeriksson@mandriva.com> 3.0.2-1mdv2008.0
+ Revision: 25052
- 3.0.2
- rediffed P0
- new major (3)

* Sat Apr 21 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.1.54-2mdv2008.0
+ Revision: 16550
- regenerate P0 one more time

* Sat Apr 21 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.1.54-1mdv2008.0
+ Revision: 16497
- new version
- regenerate P0 and P1
- own missing files

