Summary:	Edinburgh Speech Tools Library
Summary(pl):	Biblioteka narzêdzi mowy Edinburgh
Name:		speech_tools
Version:	1.2.2
Release:	1
License:	Distributable
Group:		Applications/Sound
Source0:	http://www.cstr.ed.ac.uk/download/festival/1.4.2/%{name}-%{version}-release.tar.gz
Patch0:		%{name}-termcap.patch
URL:		http://www.cstr.ed.ac.uk/projects/speech_tools.html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Edinburgh speech tools system is a library of C++ classes,
functions and utility programs that are frequently used in speech
software.

%description -l pl
Narzêdzia mowy Edinburgh s± bibliotek± klas C++, funkcji i programów
u¿ytkowych, które czêsto u¿ywa siê w syntezatorach mowy.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
%configure2_13
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldlags}" \
	OS_LIBS="-ldl -lncurses"

exit 1

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man6,%{_pixmapsdir},%{_applnkdir}/Amusements}
install oneko $RPM_BUILD_ROOT%{_bindir}
install oneko.man $RPM_BUILD_ROOT%{_mandir}/man6/oneko.6

gzip -9nf README README-NEW sample.resource

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Amusements
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man6/*
%{_pixmapsdir}/*
%{_applnkdir}/Amusements/*
