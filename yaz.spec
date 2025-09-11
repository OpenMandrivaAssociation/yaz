%define major 5
%define libname %mklibname yaz %{major}
%define develname %mklibname yaz -d

Summary:	Z39.50 protocol support library
Name:		yaz
Version:	5.35.1
Release:	1
License:	BSD-like
Group:		System/Libraries
URL:		https://www.indexdata.dk/yaz/
Source0:	http://ftp.indexdata.dk/pub/yaz/%{name}-%{version}.tar.gz

BuildRequires:	bison
BuildRequires:	docbook-style-dsssl
BuildRequires:	docbook-style-xsl
BuildRequires:	pkgconfig 
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	libtool
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	readline-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(hiredis)

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
Obsoletes:	%{mklibname yaz 3 -d} <= %version

%description -n	%{develname}
Development libraries and includes for the libyaz package.

%prep
%autosetup -p1

%build
autoreconf -fi
%configure \
    --enable-shared \
    --enable-tcpd \
    --with-openssl \
    --with-xml2 \
    --with-xslt \
    --with-exslt \
    --with-icu

%make_build

%install

%make_install docdir=/installed-docs

# fix installed docs
rm -rf installed-docs
mv %{buildroot}/installed-docs .
mv %{buildroot}%{_docdir}/%name/* installed-docs/

%files
%defattr(644,root,root,755)
%doc README.md installed-docs/*.html installed-docs/*.png
%license LICENSE
%attr(755,root,root) %{_bindir}/%name-*
%attr(755,root,root) %{_bindir}/zoomsh
%{_mandir}/man1/%name-client*.*
%{_mandir}/man1/%name-iconv.1*
%{_mandir}/man1/%name-icu.1*
%{_mandir}/man1/%name-illclient.1*
%{_mandir}/man1/%name-json-parse.1*
%{_mandir}/man1/%name-marcdump.1*
%{_mandir}/man1/%name-record-conv.1*
%{_mandir}/man1/zoomsh.*
%{_mandir}/man1/%name-url.1.*
%{_mandir}/man8/%name-ztest*.*
# moved from lib pkg
%{_mandir}/man7/*
%{_datadir}/%name/etc

%files -n %{libname}
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(644,root,root,755)
%{_includedir}/%name
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/%name.m4
%{_datadir}/%name/z39.50
%{_datadir}/%name/ill
%{_mandir}/man1/%name-asncomp.*
%{_mandir}/man1/%name-config.*

