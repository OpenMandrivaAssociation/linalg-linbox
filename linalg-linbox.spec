# Avoid find requires problem with atlas*-devel packages
%define __noautoreq	'devel\\(|libcblas\\.so\\..*|libclapack\\.so\\..*'

Name:           linalg-linbox
Version:        1.3.2
Release:        4
Summary:        C++ Library for High-Performance Exact Linear Algebra
License:        LGPLv2+
URL:            http://www.linalg.org/
Source0:        http://www.linalg.org/linbox-%{version}.tar.gz
Source1:        %{name}.rpmlintrc
# Sent upstream 2 Nov 2011.  Fix double frees that crash all tests.
Patch0:         linbox-destructor.patch
Patch1:         linbox-gcc47.patch
# Correct missing semicollon
Patch2:		linbox-int64.patch
# Force linkage to mpfr and iml to avoid unresolved symbols
Patch3:		linbox-underlink.patch
# Upstream: 3 Jan 2013.  Fix driver compilation, which has bitrotted somewhat.
Patch4:         linbox-driver.patch
# Upstream: 3 Jan 2013.  Fix detection of LAPACK support in FFLAS-FFPACK.
Patch5:         linbox-lapack.patch
# Upstream: 3 Jan 2013.  Adapt to FPLLL 4.x.
Patch6:         linbox-fplll.patch
# Upstream: 3 Jan 2013.  Fix build when size_t is unsigned long (eg. on s390).
Patch7:         linbox-size_t.patch

BuildRequires:  fflas-ffpack-devel
BuildRequires:  givaro-devel
BuildRequires:  iml-devel
BuildRequires:  libatlas-devel
BuildRequires:  m4ri-devel
BuildRequires:  m4rie-devel
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
Requires:       %{name} = %{version}-%{release}
Requires:       fflas-ffpack-devel


%description    devel
Headers and libraries for development with linbox.


%package        doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch


%description    doc
Documentation for %{name}.


%prep
%setup -q -n linbox-%{version}
%patch0
%patch1
%patch2
%patch3
%patch4
%patch5
%patch6
%patch7 -p1

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

%configure2_5x --enable-shared --disable-static --enable-drivers --enable-sage \
  --enable-optimization --enable-doc --with-ntl

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


#%#check
#LD_LIBRARY_PATH=`pwd`/linbox/.libs make %{?_smp_mflags} check


%files
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_libdir}/*.so.*

%files doc
%doc doc/linbox-html/*

%files devel
%{_includedir}/linbox
%{_libdir}/*.so
%{_bindir}/linbox-config
%{_mandir}/man1/linbox-config.1*
