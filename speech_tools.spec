Summary:	Edinburgh Speech Tools Library
Summary(pl):	Biblioteka narzêdzi mowy Edinburgh
Name:		speech_tools
Version:	1.2.2
Release:	1
License:	Distributable
Group:		Applications/Sound
Source0:	http://www.cstr.ed.ac.uk/download/festival/1.4.2/%{name}-%{version}-release.tar.gz
Patch0:		%{name}-termcap.patch
Patch1:		%{name}-shared.patch
URL:		http://www.cstr.ed.ac.uk/projects/speech_tools.html
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
Group:		Applications/Sound

%description devel
Developement files for speech tools.

%package static
Summary:	Static libraries for speech tools
Group:		Applications/Sound

%description static
Static libraries for speech tools.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
%configure2_13
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldlags}" \
	OS_LIBS="-ldl -lncurses"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir}/EST,%{_libdir}}

cp -r include/* $RPM_BUILD_ROOT%{_includedir}/EST
find $RPM_BUILD_ROOT%{_includedir}/EST -name Makefile -exec rm \{\} \;

for file in `find $RPM_BUILD_ROOT%{_includedir}/EST -type f`
do
	sed 's/\"\(.*h\)\"/\<EST\/\1\>/g' $file > $file.tmp
	mv $file.tmp $file
done

install lib/lib* $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib*.so
%{_includedir}/EST

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
