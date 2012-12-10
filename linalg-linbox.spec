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


%changelog
* Wed Aug 15 2012 Paulo Andrade <pcpa@mandriva.com.br> 1.3.2-1
+ Revision: 814865
- Update to release matching http://pkgs.fedoraproject.org/cgit/linbox.git

* Tue Jan 24 2012 Paulo Andrade <pcpa@mandriva.com.br> 1.1.6-15
+ Revision: 767494
- Update and correct patch required by sagemath 4.8.

* Tue Jan 24 2012 Paulo Andrade <pcpa@mandriva.com.br> 1.1.6-14
+ Revision: 767465
- Rebuild with newer interface required by sagemath 4.8

* Wed Dec 07 2011 Paulo Andrade <pcpa@mandriva.com.br> 1.1.6-13
+ Revision: 738723
- Rebuild for .la file removal.

* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.6-12mdv2011.0
+ Revision: 612752
- the mass rebuild of 2010.1 packages

* Wed Feb 10 2010 Funda Wang <fwang@mandriva.org> 1.1.6-11mdv2010.1
+ Revision: 503621
- rebuild for new gmp

* Fri Jan 29 2010 Paulo Andrade <pcpa@mandriva.com.br> 1.1.6-10mdv2010.1
+ Revision: 498315
- Correct building of liblinboxsage.so
- Properly use atlas cblas library

* Fri Jan 29 2010 Paulo Andrade <pcpa@mandriva.com.br> 1.1.6-9mdv2010.1
+ Revision: 497858
- Update for build with givaro 3.3.1
- Remove _disable_ld_as_needed and _disable_ld_no_undefined

* Mon Aug 31 2009 Paulo Andrade <pcpa@mandriva.com.br> 1.1.6-8mdv2010.0
+ Revision: 423095
+ rebuild (emptylog)

* Tue Jun 02 2009 Paulo Andrade <pcpa@mandriva.com.br> 1.1.6-7mdv2010.0
+ Revision: 382074
- Correct linkage problems with liblinbox.so and liblinboxsage.so that
  caused sagemath to crash or give improper results.

* Fri May 22 2009 Paulo Andrade <pcpa@mandriva.com.br> 1.1.6-5mdv2010.0
+ Revision: 378829
+ rebuild (emptylog)

* Fri Apr 03 2009 Paulo Andrade <pcpa@mandriva.com.br> 1.1.6-4mdv2009.1
+ Revision: 363921
- o build with --enable-sage, and correct build for that option.
  o correct build with --with-ntl that was failing due to --Wl,as-needed

* Sat Feb 28 2009 Paulo Andrade <pcpa@mandriva.com.br> 1.1.6-3mdv2009.1
+ Revision: 345856
- Initial import of linalg-linbox, version 1.1.6
  linalg-linbox is a exact computational linear algebra C++ template library.
- linalg-linbox

