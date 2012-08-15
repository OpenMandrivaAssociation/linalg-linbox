# Avoid find requires problem with atlas*-devel packages
%define __noautoreq	'devel\\('

Name:           linalg-linbox
Version:        1.3.2
Release:        1
Summary:        C++ Library for High-Performance Exact Linear Algebra
Group:          Sciences/Mathematics
License:        LGPLv2+
URL:            http://www.linalg.org/
Source0:        http://www.linalg.org/linbox-%{version}.tar.gz
# Sent upstream 2 Nov 2011.  Fix double frees that crash all tests.
Patch0:         linbox-destructor.patch
Patch1:         linbox-gcc47.patch
# Correct missing semicollon
Patch2:		linbox-int64.patch
# Force linkage to mpfr and iml to avoid unresolved symbols
Patch3:		linbox-underlink.patch

BuildRequires:  fflas-ffpack-devel
BuildRequires:  givaro-devel
BuildRequires:  iml-devel
BuildRequires:  libatlas-devel
BuildRequires:  libm4ri-devel
BuildRequires:  libm4rie-devel
BuildRequires:  mpfr-devel
BuildRequires:  ntl-devel

BuildRequires:  doxygen
BuildRequires:  ghostscript
BuildRequires:  gnuplot
BuildRequires:  texlive

%description
LinBox is a C++ template library for exact, high-performance linear
algebra computation with dense, sparse, and structured matrices over
the integers and over finite fields.


%package        devel
Summary:        Development libraries/headers for linbox
Group:          Development/C++
Requires:       %{name} = %{version}-%{release}
Requires:       fflas-ffpack-devel


%description    devel
Headers and libraries for development with linbox.


%prep
%setup -q -n linbox-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# Fix up missing and extraneous library linkage
sed -e "s|\$(GMP_LIBS) \$(NTL_LIBS) \$(BLAS_LIBS)|-L%{_libdir}/atlas \$(NTL_LIBS) -lcblas|" \
    -i interfaces/driver/Makefile.in
sed -e "s|\$(GIVARO_LIBS) \$(GMP_LIBS) \$(NTL_LIBS) \$(BLAS_LIBS)|-L%{_libdir}/atlas ../../linbox/liblinbox.la \$(GIVARO_LIBS) \$(NTL_LIBS) -lcblas|" \
    -i interfaces/sage/Makefile.in

# Fix libtool
sed -i "s/func_apped/func_append/g" build-aux/ltmain.sh

%build
CFLAGS="%{optflags}"
%ifarch x86_64 ppc64
    CFLAGS="$CFLAGS -D__LINBOX_HAVE_INT64=1"
%endif
export CFLAGS
CXXFLAGS=$CFLAGS
export CXXFLAGS
CPPFLAGS="$CPPFLAGS -I%{_includedir}/m4rie"
export CPPFLAGS

%configure2_5x --enable-shared --disable-static --enable-sage \
  --enable-doc --with-ntl

# Remove hardcoded rpaths
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -i libtool

# Don't try to optimize the tests; the build takes gargantuan amounts of memory
sed -i 's|-O2||g' tests/Makefile

make # %%{?_smp_mflags}

# Don't want these files in with the HTML files
rm -f doc/linbox-html/{AUTHORS,COPYING,INSTALL}


%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la

# Remove docs that are installed in the wrong place
rm -rf %{buildroot}%{_prefix}/doc


%check
LD_LIBRARY_PATH=`pwd`/linbox/.libs make %{?_smp_mflags} check


%files
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_libdir}/*.so.*


%files devel
%doc doc/linbox-html/*
%{_includedir}/linbox
%{_libdir}/*.so
%{_bindir}/linbox-config
%{_mandir}/man1/linbox-config.1*
