%define version 2.0.2
%define release %mkrel 1

%define major 	1
%define libname %mklibname %{name}

Summary: 	Chemistry software file format converter
Name: 		openbabel
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Sciences/Chemistry
BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot
URL: 		http://openbabel.sourceforge.net/
Source: 	%{name}-%{version}.tar.bz2

BuildRequires:	doxygen
Requires:	%{libname}%{major} = %{version}

%description
Open Babel is a project designed to pick up where Babel left off, 
as a cross-platform program and library designed to interconvert 
between many file formats used in molecular modeling and computational
chemistry.

%package	-n %{libname}%{major}
Summary:        Shared libraries of %{name}
Group:          System/Libraries
Provides:	%{libname} = %{version}-%{release}

%description	-n %{libname}%{major}
Open Babel is a project designed to pick up where Babel left off, 
as a cross-platform program and library designed to interconvert 
between many file formats used in molecular modeling and computational
chemistry.

This package contains shared libraries of %{name}.

%package	-n %{libname}%{major}-devel
Summary:        Development files of %{name}
Group:          Development/C++
Requires:	%{libname}%{major} = %{version}
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{libname}-devel = %{version}-%{release}

%description	-n %{libname}%{major}-devel
Open Babel is a project designed to pick up where Babel left off, 
as a cross-platform program and library designed to interconvert 
between many file formats used in molecular modeling and computational
chemistry.

This package includes the header files and other development
related files necessary for developing or compiling programs
using the %{name} library.

%package	-n %{libname}%{major}-static-devel
Summary:        Static library of %{name}
Group:          System/Libraries
Requires:	%{libname}%{major}-devel = %{version}

%description	-n %{libname}%{major}-static-devel
Open Babel is a project designed to pick up where Babel left off, 
as a cross-platform program and library designed to interconvert 
between many file formats used in molecular modeling and computational
chemistry.

This package contains static library of %{name}.

%prep
%setup -q

%build
%configure2_5x --enable-doxygen --enable-shared
%make

%install
rm -rf %{buildroot}
%makeinstall_std
#install -d -m 0755 %{buildroot}%{_includedir}/openbabel/math
#install -m 0644 src/math/*.h %{buildroot}%{_includedir}/openbabel/math/ 

%post -n %{libname}%{major} -p /sbin/ldconfig
%postun -n %{libname}%{major} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README THANKS
%doc doc/*.html doc/diox* doc/README*
%{_bindir}/*
%{_mandir}/man?/*
%{_datadir}/%{name}

%files -n %{libname}%{major}
%defattr(-, root, root)
%{_libdir}/lib*.so.*

%files -n %{libname}%{major}-devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so
%{_libdir}/lib*.la

%files -n %{libname}%{major}-static-devel
%defattr(-, root, root)
%{_libdir}/lib*.a
%{_libdir}/%name


