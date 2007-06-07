%define major 3
%define libname	%mklibname yaz %{major}

Summary:	Z39.50 protocol support library
Name:		yaz
Version:	3.0.6
Release:	%mkrel 1
License:	BSD-like
Group:		System/Libraries
URL:		http://www.indexdata.dk/yaz/
Source0:	http://ftp.indexdata.dk/pub/yaz/%{name}-%{version}.tar.gz
Patch0:		yaz-config.diff
Patch1:		%{name}-2.1.54-shared_pcap_libs.patch
BuildRequires:	autoconf2.5
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-dsssl
BuildRequires:	docbook-utils
BuildRequires:	jade
BuildRequires:	jadetex
BuildRequires:	libgcrypt-devel
BuildRequires:	libgpg-error-devel
BuildRequires:	libpcap-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This package contains both a test-server and clients (normal &
ssl) for the ANSI/NISO Z39.50 protocol for Information Retrieval.

%package -n	%{libname}
Summary:	Z39.50 Library
Group:		System/Libraries
Requires:	openssl
Requires:	tcp_wrappers
Requires:	%{name} = %{version}-%{release}

%description -n	%{libname}
YAZ is a library for the ANSI/NISO Z39.50 protocol for Information
Retrieval.

%package -n	%{libname}-devel
Summary:	Z39.50 Library - development package
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel
Provides:	lib%{name}-devel

%description -n %{libname}-devel
Development libraries and includes for the libyaz package.

%prep

%setup -q
%patch0 -p0
%patch1 -p0

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*
perl -pi -e "s|/usr/lib/|%{_libdir}/|g" configure*

%build
export WANT_AUTOCONF_2_5=1
rm -f missing
#libtoolize --copy --force; aclocal -I m4; autoconf; automake --add-missing

sh ./buildconf.sh

%configure2_5x \
    --enable-shared \
    --enable-tcpd \
    --with-openssl \
    --with-pic \
    --with-xml2 \
    --with-xslt \
    --with-exslt

%make

%check
make check

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

# fix installed docs
rm -rf installed-docs
cp -rf %{buildroot}%{_docdir}/yaz installed-docs
rm -rf %{buildroot}%{_docdir}/yaz

# fix yaz-config (weird stuff...)
perl -pi -e "s|^yaz_echo_source=.*|yaz_echo_source=yes|g" %{buildroot}%{_bindir}/yaz-config

%multiarch_binaries %{buildroot}%{_bindir}/yaz-config

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc README LICENSE TODO installed-docs/*.html installed-docs/*.png
%attr(755,root,root) %{_bindir}/yaz-*
%attr(755,root,root) %{_bindir}/zoomsh
%attr(755,root,root) %{_bindir}/ziffy
%{_mandir}/man1/yaz-client*.*
%{_mandir}/man1/yaz-iconv.1*
%{_mandir}/man1/yaz-illclient.1*
%{_mandir}/man1/yaz-marcdump.1*
%{_mandir}/man1/ziffy.1*
%{_mandir}/man1/zoomsh.*
%{_mandir}/man8/yaz-ztest*.*
# moved from lib pkg
%{_mandir}/man7/*
%{_datadir}/yaz/etc

%files -n %{libname}
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.%{major}*

%files -n %{libname}-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/yaz-config
%multiarch %attr(755,root,root) %{multiarch_bindir}/yaz-config
%attr(755,root,root) %{_bindir}/yaz-asncomp
%{_includedir}/yaz
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/yaz.m4
%{_datadir}/yaz/z39.50
%{_datadir}/yaz/ill
%{_mandir}/man1/yaz-asncomp.*
%{_mandir}/man8/yaz-config.*
