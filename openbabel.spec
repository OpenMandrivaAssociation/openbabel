%define major	4
%define libname	%mklibname %{name} %{major}
%define inchilib %mklibname inchi 0
%define devname	%mklibname %{name} -d
%define staticname %mklibname %{name} -d -s

Summary:	Chemistry software file format converter
Name:		openbabel
Version:	2.3.1
Release:	3
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

BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	eigen2
BuildRequires:	swig
BuildRequires:	libtool
BuildRequires:	perl-devel
BuildRequires:	ruby-devel
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

%build
%cmake \
 -DBUILD_GUI:BOOL=ON \
 -DPYTHON_BINDINGS:BOOL=ON \
 -DPERL_BINDINGS:BOOL=ON \
 -DRUBY_BINDINGS:BOOL=ON \
 -DOPENBABEL_USE_SYSTEM_INCHI=OFF
%make

%install
%makeinstall_std -C build

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
%{python_sitearch}/*

%files -n ruby-%{name}
%{ruby_sitearchdir}/openbabel.so


%changelog
* Wed Feb 15 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.3.1-1
+ Revision: 774603
- drop explicit dependency on library package
- cleanup spec
- fix library dirs used for linking of python module
- new version
- mass rebuild of ruby packages against ruby 1.9.1

* Sun Jan 22 2012 Oden Eriksson <oeriksson@mandriva.com> 2.3.0-2
+ Revision: 765939
- rebuilt for perl-5.14.2

* Sat May 07 2011 Funda Wang <fwang@mandriva.org> 2.3.0-1
+ Revision: 672299
- update file list
- export destdir
- fix install
- fix libdir
- New version 2.3.0
- add fedora patches to make it build correctly

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2.2.3-6
+ Revision: 666948
- mass rebuild

* Fri Mar 18 2011 John Balcaen <mikala@mandriva.org> 2.2.3-5
+ Revision: 646278
- %libname should not provide %%name

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.3-4mdv2011.0
+ Revision: 607013
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.3-3mdv2010.1
+ Revision: 523516
- rebuilt for 2010.1

* Wed Aug 05 2009 Funda Wang <fwang@mandriva.org> 2.2.3-2mdv2010.0
+ Revision: 409924
- add virtual provides

* Tue Aug 04 2009 Frederik Himpe <fhimpe@mandriva.org> 2.2.3-1mdv2010.0
+ Revision: 409361
- Fix file list
- Don't use unrecognized --enable-doxygen configure option
- Unbreak the static-devel package name
- Update to new version 2.3.3

* Sun Jul 12 2009 Frederik Himpe <fhimpe@mandriva.org> 2.2.2-1mdv2010.0
+ Revision: 395300
- Update to new version 2.2.2

* Wed Apr 01 2009 Antoine Ginies <aginies@mandriva.com> 2.2.1-2mdv2009.1
+ Revision: 363406
- add missing file (remove by error)
- restore the static-devel package

* Mon Mar 02 2009 Emmanuel Andry <eandry@mandriva.org> 2.2.1-1mdv2009.1
+ Revision: 347008
- New version 2.2.1
- drop redundant BR

* Fri Aug 29 2008 Helio Chissini de Castro <helio@mandriva.com> 2.2.0-5mdv2009.0
+ Revision: 277286
- There's still devel packages with soname installed in some boxes

* Wed Aug 27 2008 Nicolas Lécureuil <nlecureuil@mandriva.com> 2.2.0-4mdv2009.0
+ Revision: 276620
- Fix file list
  Fix configure
- Enhance configure
  fix file list  ( Bug #42549 )

* Wed Aug 27 2008 Nicolas Lécureuil <nlecureuil@mandriva.com> 2.2.0-3mdv2009.0
+ Revision: 276462
- Add libxml2-devel As buildrequire

* Sun Aug 10 2008 Emmanuel Andry <eandry@mandriva.org> 2.2.0-2mdv2009.0
+ Revision: 270542
- New version
- fix license
- apply devel policy
- fix major
- major check
- static-devel is not built anymore

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 2.2.0-2.b5.1mdv2009.0
+ Revision: 265231
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Jun 05 2008 Helio Chissini de Castro <helio@mandriva.com> 2.2.0-0.b5.1mdv2009.0
+ Revision: 216196
- New upstream beta version required for current kdeedu4

* Fri Apr 18 2008 Nicolas Lécureuil <nlecureuil@mandriva.com> 2.2.0-0.b4.1mdv2009.0
+ Revision: 195522
- Update tp 2.2.0 Beta4 (needed by kdeedu4)

* Fri Dec 21 2007 Olivier Blin <blino@mandriva.org> 2.1.1-1mdv2008.1
+ Revision: 136634
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Jul 09 2007 Austin Acton <austin@mandriva.org> 2.1.1-1mdv2008.0
+ Revision: 50762
- new version

* Wed May 09 2007 Austin Acton <austin@mandriva.org> 2.1.0-2mdv2008.0
+ Revision: 25785
- fix major

* Tue Apr 17 2007 Laurent Montel <lmontel@mandriva.org> 2.1.0-1mdv2007.1
+ Revision: 13613
- 2.1.0 (need by kalzium4)


* Sun Feb 25 2007 Emmanuel Andry <eandry@mandriva.org> 2.0.2-1mdv2007.0
+ Revision: 125461
- New version 2.0.2

  + Jérôme Soyer <saispo@mandriva.org>
    - Import openbabel

* Wed Jun 21 2006 Lenny Cartier <lenny@mandriva.com> 2.0.1-2mdv2007.0
- rebuild

* Wed Apr 19 2006 Lenny Cartier <lenny@mandriva.com> 2.0.1-1mdk
- 2.0.1
- remove patch merged upstream

* Tue Jan 17 2006 Lenny Cartier <lenny@mandriva.com> 2.0.0-1mdk
- 2.0.0
- used patch from website to fix gcc4 compilation

* Fri Jul 08 2005 Lenny Cartier <lenny@mandriva.com> 1.100.2-3mdk
- rebuild

* Sat Jun 05 2004 Abel Cheung <deaddog@deaddog.org> 1.100.2-2mdk
- Drop patch0 (not needed)
- Rebuild with new gcc

* Tue May 04 2004 Austin Acton <austin@mandrake.org> 1.100.2-1mdk
- 1.100.2

