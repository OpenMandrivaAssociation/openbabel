%define major	4
%define libname	%mklibname %{name} %{major}
%define inchilib %mklibname inchi 0
%define devname	%mklibname %{name} -d
%define staticname %mklibname %{name} -d -s

Summary:	Chemistry software file format converter
Name:		openbabel
Version:	2.3.2
Release:	4
License:	GPLv2+
Group:		Sciences/Chemistry
Url:		http://openbabel.org
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch1:		openbabel-2.3.1-rpm.patch
Patch2:		openbabel-2.3.1-gcc47-darwin.patch
Patch3:		openbabel-2.3.1-noswig-rubymethod.patch
Patch4:		openbabel-2.3.0-plugindir.patch
Patch5:		openbabel-2.3.1-python-library_dirs-lame-workaround.patch
Patch6:		openbabel-2.3.1-pkgconfig.patch
Patch7:		openbabel-2.3.1-ruby-path.patch
Patch8:		openbabel-2.3.2-cmake.patch

BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	eigen3
BuildRequires:	swig
BuildRequires:	libtool
BuildRequires:	perl-devel
BuildRequires:	ruby-devel
BuildRequires:	rubygems
BuildRequires:	wxgtku2.8-devel
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

%package -n	perl-%{name}
Group:		Development/Perl
Summary:	Perl wrapper for the Open Babel library

%description -n	perl-%{name}
Perl wrapper for the Open Babel library.

%package -n	python-%{name}
Group: Development/Python
Summary: Python wrapper for the Open Babel library

%description -n	python-%{name}
Python wrapper for the Open Babel library.

%package -n	ruby-%{name}
Summary:	Ruby wrapper for the Open Babel library
Group:		Development/Ruby
Requires:	%{name} = %{version}-%{release}

%description -n	ruby-%{name}
Ruby wrapper for the Open Babel library.

%prep
%setup -q
%patch1 -p1 -b .r
%patch2 -p1 -b .gcc4.7~
%patch3 -p1 -b .ruby~
%patch4 -p1 -b .plugindir
%patch5 -p1 -b .py_libdirs~
%patch6 -p0 -b .pkgconfig
%patch7 -p1 -b .ruby
%patch8 -p1 -b .cmake

%build
%cmake \
 -DBUILD_GUI:BOOL=ON \
 -DPYTHON_BINDINGS:BOOL=ON \
 -DPERL_BINDINGS:BOOL=ON \
 -DRUBY_BINDINGS:BOOL=ON \
 -DOPENBABEL_USE_SYSTEM_INCHI=OFF
%make

%install

mkdir -p %{buildroot}%ruby_sitearchdir

%makeinstall_std -C build 

# Put Python bindings in the right place.
# See http://sourceforge.net/p/openbabel/bugs/837/
mkdir -p %{buildroot}%{python2_sitearch}
mv  %{buildroot}%{_libdir}/_openbabel.so \
    %{buildroot}%{_libdir}/openbabel.py* \
    %{buildroot}%{_libdir}/pybel.py* \
    %{buildroot}%{python2_sitearch}

%files
%doc AUTHORS COPYING ChangeLog README THANKS
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

%files -n perl-%{name}
%{perl_vendorarch}/*

%files -n python-%{name}
%{python2_sitearch}/*

%files -n ruby-%{name}
%{ruby_sitearchdir}/openbabel.so
