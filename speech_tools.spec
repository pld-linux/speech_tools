Summary:	Edinburgh Speech Tools Library
Summary(pl):	Biblioteka narzêdzi mowy Edinburgh
Name:		speech_tools
Version:	1.2.2
Release:	5
License:	distributable
Group:		Applications/Sound
Source0:	http://www.cstr.ed.ac.uk/download/festival/1.4.2/%{name}-%{version}-release.tar.gz
# Source0-md5:	34c7e43480612ef8ecc5d3bdf1b46668
Patch0:		%{name}-termcap.patch
Patch1:		%{name}-shared.patch
Patch2:		%{name}-soname.patch
URL:		http://www.cstr.ed.ac.uk/projects/speech_tools.html
BuildRequires:	automake
BuildRequires:  libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Edinburgh speech tools system is a library of C++ classes,
functions and utility programs that are frequently used in speech
software.

%description -l pl
Narzêdzia mowy Edinburgh s± bibliotek± klas C++, funkcji i programów
u¿ytkowych, które czêsto u¿ywa siê w syntezatorach mowy.

%package devel
Summary:	Developement files for speech tools
Summary(pl):	Pliki nag³ówkowe do narzêdzi mowy
Group:		Applications/Sound
Requires:	%{name} = %{version}

%description devel
Developement files for speech tools.

%description devel -l pl
Pliki nag³ówkowe do narzêdzi mowy.

%package static
Summary:	Static libraries for speech tools
Summary(pl):	Statyczne biblioteki narzêdzi mowy
Group:		Applications/Sound
Requires:	%{name}-devel = %{version}

%description static
Static libraries for speech tools.

%description static -l pl
Statyczne biblioteki narzêdzi mowy.

%package utils
Summary:	Speech tools utils
Summary(pl):	Programy u¿ytkowe narzêdzi mowy Edinburgh
Group:		Applications/Sound
Requires:	%{name} = %{version}

%description utils
Speech tools utils.

%description utils -l pl
Programy u¿ytkowe narzêdzi mowy Edinburgh.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cp -f /usr/share/automake/config.* .
%configure2_13
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPTIMISE_CCFLAGS="%{rpmcflags}" \
	OPTIMISE_CXXFLAGS="%{rpmcflags}" \
	OPTIMISE_LINKFLAGS="%{rpmldflags}" \
	OS_LIBS="-ldl -lncurses"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir}/EST,%{_datadir}/%{name}/example_data} \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/{scripts,siod,stats/wagon,grammar/{scfg,wfst}}

# includes
cp -r include/* $RPM_BUILD_ROOT%{_includedir}/EST
find $RPM_BUILD_ROOT%{_includedir}/EST -name Makefile -exec rm \{\} \;
for file in `find $RPM_BUILD_ROOT%{_includedir}/EST -type f`
do
	sed 's/\"\(.*h\)\"/\<EST\/\1\>/g' $file > $file.tmp
	mv $file.tmp $file
done
sed 's/\<EST\//&rxp\//g' $RPM_BUILD_ROOT%{_includedir}/EST/rxp/rxp.h > bzzz
mv bzzz $RPM_BUILD_ROOT%{_includedir}/EST/rxp/rxp.h
for i in $RPM_BUILD_ROOT%{_includedir}/EST/rxp/*
do
	ln -s %{_includedir}/EST/rxp/`basename $i` $RPM_BUILD_ROOT%{_includedir}/EST/`basename $i`
done
ln -s /usr/include/EST $RPM_BUILD_ROOT%{_libdir}/%{name}/include

# libraries
install lib/lib* $RPM_BUILD_ROOT%{_libdir}
for i in $RPM_BUILD_ROOT%{_libdir}/*.so
do
	rm $i
	ln -s `basename $i*` $i
done

# binaries
install `find bin -type f -perm +1` $RPM_BUILD_ROOT%{_bindir}

# scripts
install scripts/{example_to_doc++.prl,make_wagon_desc.sh,resynth.sh,shared_script,shared_setup_prl,shared_setup_sh} \
		$RPM_BUILD_ROOT%{_libdir}/%{name}/scripts

# example data
install lib/example_data/* $RPM_BUILD_ROOT%{_datadir}/%{name}/example_data
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/example_data/Makefile

# more shit
cp -r config $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -r testsuite $RPM_BUILD_ROOT%{_libdir}/%{name}
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/testsuite/*.o
install siod/siod.mak $RPM_BUILD_ROOT%{_libdir}/%{name}/siod
install lib/siod/*.scm $RPM_BUILD_ROOT%{_libdir}/%{name}/siod
install stats/ols.mak $RPM_BUILD_ROOT%{_libdir}/%{name}/stats
install stats/wagon/wagon.mak $RPM_BUILD_ROOT%{_libdir}/%{name}/stats/wagon
install grammar/scfg/scfg.mak $RPM_BUILD_ROOT%{_libdir}/%{name}/grammar/scfg
install grammar/wfst/wfst.mak $RPM_BUILD_ROOT%{_libdir}/%{name}/grammar/wfst

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_datadir}/%{name}

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib*.so
%{_includedir}/EST
%{_libdir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
