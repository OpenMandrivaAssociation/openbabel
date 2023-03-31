%bcond_with perl
%bcond_with python
%bcond_with ruby
%bcond_without wx
%define major	5
%define libname	%mklibname %{name} %{major}
%define inchilib %mklibname inchi 0
%define devname	%mklibname %{name} -d
%define staticname %mklibname %{name} -d -s

Summary:	Chemistry software file format converter
Name:		openbabel
Version:	2.4.1
Release:	5
License:	GPLv2+
Group:		Sciences/Chemistry
Url:		http://openbabel.org
Source0:	https://github.com/openbabel/openbabel/archive/openbabel-%(echo %{version} |sed -e 's,\.,-,g').tar.gz

# fix perl modules install path
Patch1: %{name}-perl.patch
# fix plugin directory location (#680292, patch by lg)
Patch4: openbabel-plugindir.patch
# fix SWIG_init even when not using swig (#772149)
Patch6: openbabel-noswig-rubymethod.patch
# On F-17, directory for C ruby files changed to use vendorarch directory
Patch7: openbabel-ruby19-vendorarch.patch
# temporarily disable some tests on:
# - ppc64 and s390(x) to unblock other builds (#1108103)
# - ARM (#1094491)
# - aarch64 (#1094513)
# Upstream bugs: https://sourceforge.net/p/openbabel/bugs/927/ https://sourceforge.net/p/openbabel/bugs/945/
Patch8: openbabel-disable-tests.patch
Patch9: openbabel-narrowing-conversion.patch
# Fix path to libdir in .pc file
# https://bugzilla.redhat.com/show_bug.cgi?id=1669664
Patch10: openbabel-fix-libdir-in-pkgconfig.patch
# Math 4 test is failing on s390x only
Patch11: openbabel-disable-tests-s390x.patch
# Fix inconsistent whitespace
Patch12: openbabel-taberror.patch
# Fix import of dl module in python3.7
# https://github.com/openbabel/openbabel/pull/372
Patch13: openbabel-python-dl.patch

BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	eigen3
BuildRequires:	swig
BuildRequires:	libtool
BuildRequires:	perl-devel
%if %{with ruby}
BuildRequires:	ruby-devel
BuildRequires:	rubygems
%endif
%if %{with wx}
BuildRequires:	wxgtku3.0-devel
%endif
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(python)

%description
Open Babel is a project designed to pick up where Babel left off, 
as a cross-platform program and library designed to interconvert 
between many file formats used in molecular modeling and computational
chemistry.

%package -n	%{libname}
Summary:	Shared libraries of %{name}
Group:		System/Libraries

%description -n	%{libname}
Open Babel is a project designed to pick up where Babel left off, 
as a cross-platform program and library designed to interconvert 
between many file formats used in molecular modeling and computational
chemistry.

This package contains shared libraries of %{name}.

%package -n	%{inchilib}
Summary:	Shared libraries of inchi
Group:		System/Libraries

%description -n	%{inchilib}
The IUPAC International Chemical Identifier (InChITM) is a non-proprietary
identifier for chemical substances that can be used in printed and
electronic data sources thus enabling easier linking of diverse data
compilations. It was developed under IUPAC Project 2000-025-1-800 during
the period 2000-2004. Details of the project and the history of its
progress are available from the project web site.

This package contains shared libraries of inchi.

%package -n	%{devname}
Summary:	Development files of %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}
Requires:	%{inchilib} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{staticname} < 2.3.0

%description	-n %{devname}
Open Babel is a project designed to pick up where Babel left off, 
as a cross-platform program and library designed to interconvert 
between many file formats used in molecular modeling and computational
chemistry.

This package includes the header files and other development
related files necessary for developing or compiling programs
using the %{name} library.

%if %{with perl}
%package -n	perl-%{name}
Group:		Development/Perl
Summary:	Perl wrapper for the Open Babel library

%description -n	perl-%{name}
Perl wrapper for the Open Babel library.
%endif

%if %{with python}
%package -n	python-%{name}
Group: Development/Python
Summary: Python wrapper for the Open Babel library

%description -n	python-%{name}
Python wrapper for the Open Babel library.
%endif

%if %{with ruby}
%package -n	ruby-%{name}
Summary:	Ruby wrapper for the Open Babel library
Group:		Development/Ruby
Requires:	%{name} = %{version}-%{release}

%description -n	ruby-%{name}
Ruby wrapper for the Open Babel library.
%endif

%prep
%setup -qn %{name}-%{name}-%(echo %{version}|sed -e 's,\.,-,g')
%patch1 -p1 -b .perl_path
%patch4 -p1 -b .plugindir
%patch6 -p1 -b .noswig_ruby
%patch7 -p1 -b .ruby_vendor
%ifarch aarch64 %{arm} %{power64} s390 s390x
%patch8 -p1 -b .tests
%endif
%ifarch s390x
%patch11 -p1 -b .s390x
%endif
%patch9 -p1 -b .nc 
%patch10 -p1
%patch12 -p1 -b .taberr
%patch13 -p1 -b .py3dl

# remove hardcoded g++
sed -i 's!g++!%{__cxx}!g' scripts/perl/Makefile.PL

# Remove duplicate html files 
pushd doc
for man in *.1; do
 html=`basename $man .1`.html
 if [ -f $html ]; then
   rm $html
 fi
done
popd

%build
%global CXXFLAGS %CXXFLAGS -std=c++98
%cmake \
 -DBUILD_GUI:BOOL=ON \
 -DPYTHON_BINDINGS:BOOL=ON \
 -DPERL_BINDINGS:BOOL=ON \
 -DRUBY_BINDINGS:BOOL=ON \
 -DOPENBABEL_USE_SYSTEM_INCHI=OFF

%make_build

%install

%if %{with ruby}
mkdir -p %{buildroot}%ruby_sitearchdir
%endif

%make_install -C build 

%if 0
# Put Python bindings in the right place.
# See http://sourceforge.net/p/openbabel/bugs/837/
mkdir -p %{buildroot}%{python2_sitearch}
mv  %{buildroot}%{_libdir}/_openbabel.so \
    %{buildroot}%{_libdir}/openbabel.py* \
    %{buildroot}%{_libdir}/pybel.py* \
    %{buildroot}%{python2_sitearch}
%endif

%files
%doc AUTHORS COPYING THANKS
%doc doc/*.html doc/diox* doc/README*
%{_bindir}/*
%{_mandir}/man?/*
%{_datadir}/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%{_libdir}/%{name}/%{version}/*.so

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{inchilib}
%{_libdir}/libinchi.so.0*

%files -n %{devname}
%{_includedir}/*
%dir %{_libdir}/cmake/openbabel2
%{_libdir}/cmake/openbabel2/*.cmake
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so

%if %{with perl}
%files -n perl-%{name}
%{perl_vendorarch}/*
%endif

%if %{with python}
%files -n python-%{name}
%{python2_sitearch}/*
%endif

%if %{with ruby}
%files -n ruby-%{name}
%{ruby_sitearchdir}/openbabel.so
%endif
