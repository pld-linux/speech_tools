# TODO:
# - fix libraries SONAME
# - some utils have too generic names
Summary:	Edinburgh Speech Tools Library
Summary(pl.UTF-8):	Biblioteka narzędzi mowy Edinburgh
Name:		speech_tools
Version:	2.1
Release:	1
License:	distributable
Group:		Applications/Sound
# also:		http://www.cstr.ed.ac.uk/download/festival/2.1/%{name}-%{version}-release.tar.gz
Source0:	http://www.festvox.org/packed/festival/latest/%{name}-%{version}-release.tar.gz
# Source0-md5:	6920ddc75b042910a3bcfee3ab106938
Patch0:		%{name}-shared.patch
Patch1:		%{name}-soname.patch
Patch2:		%{name}-bin_printf.patch
Patch3:		%{name}-rateconvtrivialbug.patch
Patch4:		%{name}-as-needed.patch
Patch5:		%{name}-gcc42.patch
Patch6:		%{name}-gcc44.patch
URL:		http://www.cstr.ed.ac.uk/projects/speech_tools/
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	coreutils >= 5.0-7
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	rpmbuild(macros) >= 1.583
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         skip_post_check_so      libestools.so.*

%description
The Edinburgh speech tools system is a library of C++ classes,
functions and utility programs that are frequently used in speech
software.

%description -l pl.UTF-8
Narzędzia mowy Edinburgh są biblioteką klas C++, funkcji i programów
użytkowych, które często używa się w syntezatorach mowy.

%package devel
Summary:	Developement files for speech tools
Summary(pl.UTF-8):	Pliki nagłówkowe do narzędzi mowy
Group:		Applications/Sound
Requires:	libstdc++-devel
Requires:	%{name} = %{version}-%{release}

%description devel
Developement files for speech tools.

%description devel -l pl.UTF-8
Pliki nagłówkowe do narzędzi mowy.

%package static
Summary:	Static libraries for speech tools
Summary(pl.UTF-8):	Statyczne biblioteki narzędzi mowy
Group:		Applications/Sound
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libraries for speech tools.

%description static -l pl.UTF-8
Statyczne biblioteki narzędzi mowy.

%package utils
Summary:	Speech tools utils
Summary(pl.UTF-8):	Programy użytkowe narzędzi mowy Edinburgh
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description utils
Speech tools utils.

%description utils -l pl.UTF-8
Programy użytkowe narzędzi mowy Edinburgh.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p2
%patch4 -p1
%patch5 -p1
%patch6 -p1
%if "%{_lib}" == "lib64"
# fix regression output for 64-bit archs (sizeof(ptr)==8 instead of 4).
%{__sed} -i 's:20 bytes:24 bytes:' testsuite/correct/matrix_regression.out
%{__sed} -i 's:28 bytes:32 bytes:' testsuite/correct/matrix_regression.out
%endif

%build
cp -f /usr/share/automake/config.* .
%{__aclocal}
%{__autoconf}
%configure
%{__make} all test -j1 \
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
	grep -v est_string_config\.h $file.tmp > $file
	rm -f $file.tmp
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
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/testsuite/*.o
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
%attr(755,root,root) %{_libdir}/libestbase.so.*.*.*
%attr(755,root,root) %{_libdir}/libestools.so.*.*.*
%attr(755,root,root) %{_libdir}/libeststring.so.*.*
%{_datadir}/%{name}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libestbase.so
%attr(755,root,root) %{_libdir}/libestools.so
%attr(755,root,root) %{_libdir}/libeststring.so
%{_includedir}/EST
%{_libdir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/libestbase.a
%{_libdir}/libestools.a
%{_libdir}/libeststring.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/align
%attr(755,root,root) %{_bindir}/bcat
%attr(755,root,root) %{_bindir}/build_docbook_index
%attr(755,root,root) %{_bindir}/ch_lab
%attr(755,root,root) %{_bindir}/ch_track
%attr(755,root,root) %{_bindir}/ch_utt
%attr(755,root,root) %{_bindir}/ch_wave
%attr(755,root,root) %{_bindir}/cxx_to_docbook
%attr(755,root,root) %{_bindir}/design_filter
%attr(755,root,root) %{_bindir}/dp
%attr(755,root,root) %{_bindir}/est_examples
%attr(755,root,root) %{_bindir}/est_gdb
%attr(755,root,root) %{_bindir}/est_program
%attr(755,root,root) %{_bindir}/example_to_doc++
%attr(755,root,root) %{_bindir}/fringe_client
%attr(755,root,root) %{_bindir}/make_wagon_desc
%attr(755,root,root) %{_bindir}/na_play
%attr(755,root,root) %{_bindir}/na_record
%attr(755,root,root) %{_bindir}/ngram_build
%attr(755,root,root) %{_bindir}/ngram_test
%attr(755,root,root) %{_bindir}/ols
%attr(755,root,root) %{_bindir}/ols_test
%attr(755,root,root) %{_bindir}/pda
%attr(755,root,root) %{_bindir}/pitchmark
%attr(755,root,root) %{_bindir}/pm
%attr(755,root,root) %{_bindir}/raw_to_xgraph
%attr(755,root,root) %{_bindir}/resynth
%attr(755,root,root) %{_bindir}/scfg_make
%attr(755,root,root) %{_bindir}/scfg_parse
%attr(755,root,root) %{_bindir}/scfg_test
%attr(755,root,root) %{_bindir}/scfg_train
%attr(755,root,root) %{_bindir}/sig2fv
%attr(755,root,root) %{_bindir}/sigfilter
%attr(755,root,root) %{_bindir}/siod
%attr(755,root,root) %{_bindir}/spectgen
%attr(755,root,root) %{_bindir}/tex_to_images
%attr(755,root,root) %{_bindir}/tilt_analysis
%attr(755,root,root) %{_bindir}/tilt_synthesis
%attr(755,root,root) %{_bindir}/viterbi
%attr(755,root,root) %{_bindir}/wagon
%attr(755,root,root) %{_bindir}/wagon_test
%attr(755,root,root) %{_bindir}/wfst_build
%attr(755,root,root) %{_bindir}/wfst_run
%attr(755,root,root) %{_bindir}/wfst_train
%attr(755,root,root) %{_bindir}/xml_parser
