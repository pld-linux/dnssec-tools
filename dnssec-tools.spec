# TODO:
#	- fix linking, it should link with just built, not with system, libs
#
# Conditional build:
%bcond_without	qt	# Qt-based GUI tools
#
Summary:	DNSSEC tools
Summary(pl.UTF-8):	Narzędzia DNSSEC
Name:		dnssec-tools
Version:	2.2.3
Release:	10
License:	BSD
Group:		Applications/Networking
#Source0Download: https://github.com/DNSSEC-Tools/DNSSEC-Tools/releases
Source0:	https://github.com/DNSSEC-Tools/DNSSEC-Tools/archive/%{name}-%{version}.tar.gz
# Source0-md5:	235bfa9bf059b2f5502db2877444646b
Patch0:		%{name}-link.patch
Patch1:		%{name}-qt.patch
Patch2:		build.patch
URL:		https://dnssec-tools.org/
BuildRequires:	openssl-devel
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	perl-Net-DNS
BuildRequires:	perl-Net-DNS-SEC
BuildRequires:	perl-TimeDate
BuildRequires:	perl-base
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.745
%if %{with qt}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Declarative-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Network-devel >= 5
BuildRequires:	Qt5Qml-devel >= 5
BuildRequires:	Qt5Quick-devel >= 5
BuildRequires:	Qt5Svg-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	Qt5Xml-devel >= 5
BuildRequires:	qt5-qmake >= 5
%endif
Requires:	%{name}-libs = %{version}-%{release}
Requires:	perl-%{name} = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The goal of the DNSSEC-Tools project is to create a set of tools,
patches, applications, wrappers, extensions, and plugins that will
help ease the deployment of DNSSEC-related technologies.

%description -l pl.UTF-8
Celem projektu DNSSEC-Tools jest stworzenie zbioru narzędzi, łatek,
aplikacji, wrapperów, rozszerzeń i wtyczek pomagających przy wdrażaniu
technologii związanych z DNSSEC.

%package gui
Summary:	DNSSEC tools with GUI
Summary(pl.UTF-8):	Narzędzia DNSSEC z GUI
Group:		X11/Applications
Requires:	%{name}-libs = %{version}-%{release}

%description gui
DNSSEC tools with Qt-based GUI: dnssec-check, dnssec-nodes,
dnssec-system-tray and lookup.

%description gui -l pl.UTF-8
Narzędzia DNSSEC z opartym na Qt graficznym interfejsem użytkownika:
dnssec-check, dnssec-nodes, dnssec-system-tray oraz lookup.

%package libs
Summary:	DNSSEC libraries
Summary(pl.UTF-8):	Biblioteki DNSSEC
Group:		Libraries

%description libs
DNSSEC libraries.

%description libs -l pl.UTF-8
Biblioteki DNSSEC.

%package devel
Summary:	Header files for DNSSEC libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek DNSSEC
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	openssl-devel

%description devel
Header files for DNSSEC libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek DNSSEC.

%package static
Summary:	Static DNSSEC libraries
Summary(pl.UTF-8):	Statyczne biblioteki DNSSEC
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static DNSSEC libraries.

%description static -l pl.UTF-8
Statyczne biblioteki DNSSEC.

%package -n perl-%{name}
Summary:	Perl modules supporting DNSSEC
Summary(pl.UTF-8):	Moduły Perla wspierające DNSSEC
Group:		Development/Languages/Perl
Requires:	%{name}-libs = %{version}-%{release}
Requires:	perl-Net-DNS
Requires:	perl-Net-DNS-SEC

%description -n perl-%{name}
Perl modules supporting DNSSEC.

%description -n perl-%{name} -l pl.UTF-8
Moduły Perla wspierające DNSSEC.

%prep
%setup -q -n DNSSEC-Tools-dnssec-tools-%{version}
cd dnssec-tools
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
cd dnssec-tools
%configure \
	ac_cv_lib_nsl_inet_ntop=no \
	--disable-bind-checks \
	--with-dlv \
	--with-ipv6 \
	--with-nsec3 \
	--with-perl-build-args='INSTALLDIRS=vendor'
%{__make} -j1

%if %{with qt}
cd validator/apps
for d in dnssec-check dnssec-nodes dnssec-system-tray lookup ; do
	cd $d
	qmake-qt5 \
		PREFIX=%{_prefix} \
		QMAKE_CXX="%{__cxx}" \
		QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
		QMAKE_LFLAGS_RELEASE="%{rpmldflags}"
	%{__make}
	cd ..
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

cd dnssec-tools
%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with qt}
for d in dnssec-check dnssec-nodes dnssec-system-tray lookup ; do
	%{__make} install -C validator/apps/$d \
		DESTDIR=$RPM_BUILD_ROOT \
		INSTALL_ROOT=$RPM_BUILD_ROOT
done

# omitted from make install
install -Dp validator/apps/dnssec-check/images/dnssec-check-32x32.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/dnssec-check.png
install -Dp validator/apps/dnssec-check/images/dnssec-check-48x48.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/dnssec-check.png
install -Dp validator/apps/dnssec-check/images/dnssec-check-64x64.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/64x64/apps/dnssec-check.png
install -Dp validator/apps/dnssec-check/images/dnssec-check-512.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/512x512/apps/dnssec-check.png
install -Dp validator/apps/dnssec-check/images/dnssec-check.svg $RPM_BUILD_ROOT%{_iconsdir}/hicolor/scalable/apps/dnssec-check.svg
sed -e 's,^Exec=.*,Exec=%{_bindir}/dnssec-check,' validator/apps/dnssec-check/dnssec-check.desktop >$RPM_BUILD_ROOT%{_desktopdir}/dnssec-check.desktop
%endif

%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/Net/DNS/SEC/examples.pl \
	$RPM_BUILD_ROOT%{_mandir}/man3/Net::DNS::SEC::examples.3pm
find $RPM_BUILD_ROOT%{perl_vendorarch}/auto -name .packlist | xargs -r %{__rm}
find $RPM_BUILD_ROOT%{perl_vendorarch} -name '*.pod' | xargs -r %{__rm}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc dnssec-tools/{COPYING,ChangeLog,NEWS,README.md}
%attr(755,root,root) %{_bindir}/blinkenlights
%attr(755,root,root) %{_bindir}/bubbles
%attr(755,root,root) %{_bindir}/buildrealms
%attr(755,root,root) %{_bindir}/check-zone-expiration
%attr(755,root,root) %{_bindir}/cleanarch
%attr(755,root,root) %{_bindir}/cleankrf
%attr(755,root,root) %{_bindir}/convertar
%attr(755,root,root) %{_bindir}/dnspktflow
%attr(755,root,root) %{_bindir}/donuts
%attr(755,root,root) %{_bindir}/donutsd
%attr(755,root,root) %{_bindir}/drawvalmap
%attr(755,root,root) %{_bindir}/dt-danechk
%attr(755,root,root) %{_bindir}/dt-getaddr
%attr(755,root,root) %{_bindir}/dt-gethost
%attr(755,root,root) %{_bindir}/dt-getname
%attr(755,root,root) %{_bindir}/dt-getquery
%attr(755,root,root) %{_bindir}/dt-getrrset
%attr(755,root,root) %{_bindir}/dt-libval_check_conf
%attr(755,root,root) %{_bindir}/dt-validate
%attr(755,root,root) %{_bindir}/dtck
%attr(755,root,root) %{_bindir}/dtconf
%attr(755,root,root) %{_bindir}/dtconfchk
%attr(755,root,root) %{_bindir}/dtdefs
%attr(755,root,root) %{_bindir}/dtinitconf
%attr(755,root,root) %{_bindir}/dtrealms
%attr(755,root,root) %{_bindir}/expchk
%attr(755,root,root) %{_bindir}/fixkrf
%attr(755,root,root) %{_bindir}/genkrf
%attr(755,root,root) %{_bindir}/getdnskeys
%attr(755,root,root) %{_bindir}/getds
%attr(755,root,root) %{_bindir}/grandvizier
%attr(755,root,root) %{_bindir}/keyarch
%attr(755,root,root) %{_bindir}/keymod
%attr(755,root,root) %{_bindir}/krfcheck
%attr(755,root,root) %{_bindir}/lights
%attr(755,root,root) %{_bindir}/lsdnssec
%attr(755,root,root) %{_bindir}/lskrf
%attr(755,root,root) %{_bindir}/lsrealm
%attr(755,root,root) %{_bindir}/lsroll
%attr(755,root,root) %{_bindir}/maketestzone
%attr(755,root,root) %{_bindir}/mapper
%attr(755,root,root) %{_bindir}/realmchk
%attr(755,root,root) %{_bindir}/realmctl
%attr(755,root,root) %{_bindir}/realminit
%attr(755,root,root) %{_bindir}/realmset
%attr(755,root,root) %{_bindir}/rollchk
%attr(755,root,root) %{_bindir}/rollctl
%attr(755,root,root) %{_bindir}/rollerd
%attr(755,root,root) %{_bindir}/rollinit
%attr(755,root,root) %{_bindir}/rolllog
%attr(755,root,root) %{_bindir}/rollrec-editor
%attr(755,root,root) %{_bindir}/rollset
%attr(755,root,root) %{_bindir}/signset-editor
%attr(755,root,root) %{_bindir}/tachk
%attr(755,root,root) %{_bindir}/timetrans
%attr(755,root,root) %{_bindir}/trustman
%attr(755,root,root) %{_bindir}/zonesigner
%dir %{_sysconfdir}/dnssec-tools
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dnssec-tools/dnssec-tools.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dnssec-tools/validator-testcases
%{_datadir}/%{name}
%{_mandir}/man1/blinkenlights.1p*
%{_mandir}/man1/buildrealms.1p*
%{_mandir}/man1/bubbles.1p*
%{_mandir}/man1/check-zone-expiration.1p*
%{_mandir}/man1/cleanarch.1p*
%{_mandir}/man1/cleankrf.1p*
%{_mandir}/man1/convertar.1p*
%{_mandir}/man1/dnspktflow.1p*
%{_mandir}/man1/dnssec-tools.1*
%{_mandir}/man1/donuts.1p*
%{_mandir}/man1/donutsd.1p*
%{_mandir}/man1/drawvalmap.1p*
%{_mandir}/man1/dt-danechk.1*
%{_mandir}/man1/dt-libval_check_conf.1*
%{_mandir}/man1/dt-getaddr.1*
%{_mandir}/man1/dt-gethost.1*
%{_mandir}/man1/dt-getname.1*
%{_mandir}/man1/dt-getquery.1*
%{_mandir}/man1/dt-getrrset.1*
%{_mandir}/man1/dt-validate.1*
%{_mandir}/man1/dtck.1p*
%{_mandir}/man1/dtconf.1p*
%{_mandir}/man1/dtconfchk.1p*
%{_mandir}/man1/dtdefs.1p*
%{_mandir}/man1/dtinitconf.1p*
%{_mandir}/man1/dtrealms.1p*
%{_mandir}/man1/expchk.1p*
%{_mandir}/man1/fixkrf.1p*
%{_mandir}/man1/genkrf.1p*
%{_mandir}/man1/getdnskeys.1p*
%{_mandir}/man1/getds.1p*
%{_mandir}/man1/grandvizier.1p*
%{_mandir}/man1/keyarch.1p*
%{_mandir}/man1/keymod.1p*
%{_mandir}/man1/krfcheck.1p*
%{_mandir}/man1/lights.1p*
%{_mandir}/man1/lsdnssec.1p*
%{_mandir}/man1/lskrf.1p*
%{_mandir}/man1/lsrealm.1p*
%{_mandir}/man1/lsroll.1p*
%{_mandir}/man1/maketestzone.1p*
%{_mandir}/man1/mapper.1p*
%{_mandir}/man1/realmchk.1p*
%{_mandir}/man1/realmctl.1p*
%{_mandir}/man1/realminit.1p*
%{_mandir}/man1/realmset.1p*
%{_mandir}/man1/rollchk.1p*
%{_mandir}/man1/rollctl.1p*
%{_mandir}/man1/rollerd.1p*
%{_mandir}/man1/rollinit.1p*
%{_mandir}/man1/rolllog.1p*
%{_mandir}/man1/rollrec-editor.1p*
%{_mandir}/man1/rollset.1p*
%{_mandir}/man1/signset-editor.1p*
%{_mandir}/man1/tachk.1p*
%{_mandir}/man1/timetrans.1p*
%{_mandir}/man1/trustman.1p*
%{_mandir}/man1/zonesigner.1p*

%if %{with qt}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dnssec-check
%attr(755,root,root) %{_bindir}/dnssec-nodes
%attr(755,root,root) %{_bindir}/dnssec-system-tray
%attr(755,root,root) %{_bindir}/lookup
%{_desktopdir}/dnssec-check.desktop
%{_desktopdir}/dnssec-nodes.desktop
%{_desktopdir}/lookup.desktop
%{_iconsdir}/hicolor/48x48/apps/lookup.png
%{_iconsdir}/hicolor/*x*/apps/dnssec-check.png
%{_iconsdir}/hicolor/scalable/apps/dnssec-check.svg
%{_pixmapsdir}/lookup.xpm
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsres.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsres.so.15
%attr(755,root,root) %{_libdir}/libval-threads.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libval-threads.so.15
%attr(755,root,root) %{_libdir}/libval_shim.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libval_shim.so.15

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/libval-config
%attr(755,root,root) %{_libdir}/libsres.so
%attr(755,root,root) %{_libdir}/libval-threads.so
%attr(755,root,root) %{_libdir}/libval_shim.so
%{_libdir}/libsres.la
%{_libdir}/libval-threads.la
%{_libdir}/libval_shim.la
%{_includedir}/validator
%{_mandir}/man3/dnsval.conf.3*
%{_mandir}/man3/dnsval_conf*.3*
%{_mandir}/man3/libsres.3*
%{_mandir}/man3/libval.3*
%{_mandir}/man3/libval_async.3*
%{_mandir}/man3/libval_shim.3*
%{_mandir}/man3/p_ac_status.3*
%{_mandir}/man3/p_dane_error.3*
%{_mandir}/man3/p_val_status.3*
%{_mandir}/man3/resolv_conf_*.3*
%{_mandir}/man3/root_hints_*.3*
%{_mandir}/man3/val_*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libsres.a
%{_libdir}/libval-threads.a
%{_libdir}/libval_shim.a

%files -n perl-%{name}
%defattr(644,root,root,755)
%dir %{perl_vendorarch}/Net/DNS
%dir %{perl_vendorarch}/Net/DNS/SEC
%{perl_vendorarch}/Net/DNS/SEC/Tools
%{perl_vendorarch}/Net/DNS/SEC/Validator.pm
%{perl_vendorarch}/Net/DNS/SEC/defines.pl
%{perl_vendorarch}/Net/DNS/ZoneFile
%{perl_vendorarch}/Net/addrinfo.pm
%dir %{perl_vendorarch}/auto/Net/DNS
%dir %{perl_vendorarch}/auto/Net/DNS/SEC
%{perl_vendorarch}/auto/Net/DNS/SEC/Tools
%dir %{perl_vendorarch}/auto/Net/DNS/SEC/Validator
%{perl_vendorarch}/auto/Net/DNS/SEC/Validator/Validator.so
%dir %{perl_vendorarch}/auto/Net/addrinfo
%attr(755,root,root) %{perl_vendorarch}/auto/Net/addrinfo/addrinfo.so
%dir %{perl_vendorlib}/Net/DNS/SEC
%{perl_vendorlib}/Net/DNS/SEC/Tools
%{_mandir}/man3/Net::DNS::SEC::Tools::*.3pm*
%{_mandir}/man3/Net::DNS::SEC::Validator.3pm*
%{_mandir}/man3/Net::DNS::ZoneFile::Fast.3pm*
%{_mandir}/man3/Net::addrinfo.3pm*
