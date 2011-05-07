%define major 4
%define libname %mklibname %{name} %{major}
%define inchilib %mklibname inchi 0
%define develname %mklibname %{name} -d
%define staticname %mklibname %{name} -d -s

Name: openbabel
Version: 2.3.0
Release: %mkrel 1
Summary: Chemistry software file format converter
License: GPLv2+
Group: Sciences/Chemistry
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
URL: http://openbabel.org
Source: http://downloads.sourceforge.net/%name/%{name}-%{version}.tar.gz
Patch1: openbabel-rpm.patch
Patch3: openbabel-inchi.patch
Patch4: openbabel-2.3.0-plugindir.patch
Patch5: openbabel-2.3.0-obenergy-fflist.patch
BuildRequires: doxygen 
BuildRequires: wxgtku2.8-devel
BuildRequires: libtool
BuildRequires: libxml2-devel
BuildRequires: eigen2
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl-devel
BuildRequires: python-devel
BuildRequires: ruby-devel
BuildRequires: swig
BuildRequires: cmake
Requires: %{libname} = %{version}

%description
Open Babel is a project designed to pick up where Babel left off, 
as a cross-platform program and library designed to interconvert 
between many file formats used in molecular modeling and computational
chemistry.

%package	-n %{libname}
Summary:        Shared libraries of %{name}
Group:          System/Libraries

%description	-n %{libname}
Open Babel is a project designed to pick up where Babel left off, 
as a cross-platform program and library designed to interconvert 
between many file formats used in molecular modeling and computational
chemistry.

This package contains shared libraries of %{name}.

%package        -n %{inchilib}
Summary:        Shared libraries of inchi
Group:          System/Libraries

%description    -n %{inchilib}
The IUPAC International Chemical Identifier (InChITM) is a non-proprietary
identifier for chemical substances that can be used in printed and
electronic data sources thus enabling easier linking of diverse data
compilations. It was developed under IUPAC Project 2000-025-1-800 during
the period 2000-2004. Details of the project and the history of its
progress are available from the project web site.

This package contains shared libraries of inchi.

%package	-n %{develname}
Summary:        Development files of %{name}
Group:          Development/C++
Requires:	%{libname} = %{version}
Requires:	%{inchilib} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{staticname} < 2.3.0
Obsoletes: %mklibname %{name} 2 -d 
Obsoletes: %mklibname %{name} 3 -d 

%description	-n %{develname}
Open Babel is a project designed to pick up where Babel left off, 
as a cross-platform program and library designed to interconvert 
between many file formats used in molecular modeling and computational
chemistry.

This package includes the header files and other development
related files necessary for developing or compiling programs
using the %{name} library.

%package -n perl-%{name}
Group: Development/Perl
Summary: Perl wrapper for the Open Babel library

%description -n perl-%{name}
Perl wrapper for the Open Babel library.

%package -n python-%{name}
Group: Development/Python
Summary: Python wrapper for the Open Babel library

%description -n python-%{name}
Python wrapper for the Open Babel library.

%package -n ruby-%{name}
Summary: Ruby wrapper for the Open Babel library
Group: Development/Ruby
Requires: %{name} = %{version}-%{release}

%description -n ruby-%{name}
Ruby wrapper for the Open Babel library.

%prep
%setup -q
%patch1 -p1 -b .r
%patch3 -p1 -b .inchi
%patch4 -p1 -b .plugindir
%patch5 -p1 -b .obenergy-fflist

%build
%cmake \
 -DBUILD_GUI:BOOL=ON \
 -DPYTHON_BINDINGS:BOOL=ON \
 -DPERL_BINDINGS:BOOL=ON \
 -DRUBY_BINDINGS:BOOL=ON \
 -DOPENBABEL_USE_SYSTEM_INCHI=OFF
%make

%install
rm -rf %{buildroot}
export DESTDIR=%{buildroot}
%makeinstall_std -C build

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README THANKS
%doc doc/*.html doc/diox* doc/README*
%{_bindir}/*
%{_mandir}/man?/*
%{_datadir}/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%{_libdir}/%{name}/%{version}/*.so

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{inchilib}
%defattr(-, root, root)
%{_libdir}/libinchi.so.0.*
%{_libdir}/libinchi.so.0

%files -n %{develname}
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/%{name}/*.cmake
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so

%files -n perl-%{name}
%defattr(-,root,root,-)
%{perl_vendorarch}/*

%files -n python-%{name}
%defattr(-,root,root,-)
%{python_sitearch}/*

%files -n ruby-%{name}
%defattr(-, root, root, -)
%{ruby_sitearch}/openbabel.so
