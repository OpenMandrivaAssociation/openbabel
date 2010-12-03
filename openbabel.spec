%define major 3
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define staticname %mklibname %{name} -d -s

Name: openbabel
Version: 2.2.3
Release: %mkrel 4
Summary: Chemistry software file format converter
License: GPLv2+
Group: Sciences/Chemistry
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
URL: http://openbabel.sourceforge.net/
Source: %{name}-%{version}.tar.gz
BuildRequires: doxygen 
BuildRequires: wxGTK-devel
BuildRequires: libtool
BuildRequires: libxml2-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: python-devel
BuildRequires: ruby-devel
BuildRequires: swig

Requires: %{libname} = %{version}

%description
Open Babel is a project designed to pick up where Babel left off, 
as a cross-platform program and library designed to interconvert 
between many file formats used in molecular modeling and computational
chemistry.

%package	-n %{libname}
Summary:        Shared libraries of %{name}
Group:          System/Libraries
Provides:	%{name} = %{version}-%{release}
Conflicts:      %{develname} <  2.2.0-4

%description	-n %{libname}
Open Babel is a project designed to pick up where Babel left off, 
as a cross-platform program and library designed to interconvert 
between many file formats used in molecular modeling and computational
chemistry.

This package contains shared libraries of %{name}.

%package	-n %{develname}
Summary:        Development files of %{name}
Group:          Development/C++
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
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

%package	-n %{staticname}
Summary:        Static library of %{name}
Group:          System/Libraries
Requires:	%{develname} = %{version}
Provides:	%{name}-static-devel = %{version}-%{release}
Obsoletes:	%{_lib}%{name}33-static-devel

%description	-n %{staticname}
Open Babel is a project designed to pick up where Babel left off, 
as a cross-platform program and library designed to interconvert 
between many file formats used in molecular modeling and computational
chemistry.

This package contains static library of %{name}.

%prep
%setup -q

%build
%configure2_5x  --enable-shared=yes --enable-static=no --disable-inchi --enable-maintainer-mode

%make

%install
rm -rf %{buildroot}
%makeinstall_std

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
%{_libdir}/%{name}/%{version}/*.so
#%{_libdir}/%{name}/%{version}/*.la

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-, root, root)
%{_includedir}/%name-2.0
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so
%{_includedir}/inchi102/inchi_api.h
#%{_libdir}/lib*.la

%files -n %{staticname}
%{_libdir}/lib*.la
%{_libdir}/%{name}/%{version}/*.la

