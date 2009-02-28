Name:		linalg-linbox
Summary:	Exact computational linear algebra
Version:	1.1.6
Release:	%mkrel 3
License:	GPL
Group:		Sciences/Mathematics
Source0:	http://www.linalg.org/linbox-%{version}.tar.gz
URL:		http://www.linalg.org/

BuildRequires:	libatlas-devel libgmpxx-devel givaro-devel libblas-devel

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%build
%configure2_5x --with-gmp=%{_prefix} --with-blas=%{_libdir}
%make

%install
%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/liblinbox.so.*

%files		devel
%defattr(-,root,root)
%{_bindir}/linbox-config
%dir %{_includedir}/linbox
%{_includedir}/linbox/*
%{_libdir}/liblinbox.a
%{_libdir}/liblinbox.la
%{_libdir}/liblinbox.so
%{_mandir}/man1/linbox-config.1*
