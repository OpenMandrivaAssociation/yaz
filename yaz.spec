%define major 4
%define libname %mklibname yaz %{major}
%define develname %mklibname yaz -d

Summary:	Z39.50 protocol support library
Name:		yaz
Version:	4.0.1
Release:	%mkrel 1
License:	BSD-like
Group:		System/Libraries
URL:		http://www.indexdata.dk/yaz/
Source0:	http://ftp.indexdata.dk/pub/yaz/%{name}-%{version}.tar.gz
Patch0:		yaz-config.diff
BuildRequires:	docbook-style-dsssl
BuildRequires:	docbook-style-xsl
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	openssl-devel
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
BuildRequires:	termcap-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	libicu-devel
BuildRequires:	bison
BuildRequires:	tcl
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*
perl -pi -e "s|/usr/lib/|%{_libdir}/|g" configure*

%build
#rm -f missing
#sh ./buildconf.sh

%if %mdkversion <= 200600
export LIBS="$LIBS -lnsl"
%endif

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std docdir=/installed-docs

# fix installed docs
rm -rf installed-docs
mv %{buildroot}/installed-docs .
mv %{buildroot}%{_docdir}/yaz/* installed-docs/

# fix yaz-config (weird stuff...)
perl -pi -e "s|^yaz_echo_source=.*|yaz_echo_source=yes|g" %{buildroot}%{_bindir}/yaz-config

%multiarch_binaries %{buildroot}%{_bindir}/yaz-config

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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
%{_mandir}/man8/yaz-ztest*.*
# moved from lib pkg
%{_mandir}/man7/*
%{_datadir}/yaz/etc

%files -n %{libname}
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.%{major}*

%files -n %{develname}
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


