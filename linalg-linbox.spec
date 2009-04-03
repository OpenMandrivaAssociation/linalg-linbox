# This causes configure to fail in "finding NTL" due to not finding
# libgmp symbols in libntl.so in the "try_build" configure program.
%define _disable_ld_as_needed		1

# A side effect of change above.
%define _disable_ld_no_undefined	1

Name:		linalg-linbox
Summary:	Exact computational linear algebra
Version:	1.1.6
Release:	%mkrel 4
License:	GPL
Group:		Sciences/Mathematics
Source0:	http://www.linalg.org/linbox-%{version}.tar.gz
URL:		http://www.linalg.org/

BuildRequires:	givaro-devel
BuildRequires:	libatlas-devel
BuildRequires:	libblas-devel
BuildRequires:	libgmpxx-devel
BuildRequires:	ntl-devel

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

# Wonder how people build sage interface, so, do a dirty hack to
# correct compilation here. Randoms numbers will be not so random
# as a side effect.
Patch0:		linbox-1.1.6-sage.diff

%description
LinBox is a C++ template library for exact, high-performance linear
algebra computation with dense, sparse, and structured matrices over
the integers and over finite fields.

%package	devel
Group:		Development/Other
Summary:	LinBox development files
Requires:	%{name}

%description	devel
This package contains the LinBox development files.

%prep
%setup -q -n linbox-%{version}

%patch0	-p1

%build
%configure2_5x					\
	--with-gmp=%{_prefix}			\
	--with-blas=%{_libdir}			\
	--with-givaro=%{_prefix}		\
	--with-ntl=%{_prefix}			\
	--enable-optimization			\
	--enable-sage
%make CFLAGS="%{optflags} -fPIC"

%install
%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/liblinbox.so.*
%{_libdir}/liblinboxsage.so.*

%files		devel
%defattr(-,root,root)
%{_bindir}/linbox-config
%dir %{_includedir}/linbox
%{_includedir}/linbox/*
%{_libdir}/liblinbox.a
%{_libdir}/liblinbox.la
%{_libdir}/liblinbox.so
%{_libdir}/liblinboxsage.a
%{_libdir}/liblinboxsage.la
%{_libdir}/liblinboxsage.so
%{_mandir}/man1/linbox-config.1*
