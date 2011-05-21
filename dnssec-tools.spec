%include	/usr/lib/rpm/macros.perl
Summary:	DNSSEC tools
Summary(pl.UTF-8):	Narzędzia DNSSEC
Name:		dnssec-tools
Version:	1.9
Release:	1
License:	BSD
Group:		Applications/Network
Source0:	http://www.dnssec-tools.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	f8bb8dcc3cd9d7f466045291e331a92b
Patch0:		%{name}-link.patch
URL:		http://www.dnssec-tools.org/
BuildRequires:	openssl-devel
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	perl-Net-DNS
BuildRequires:	perl-Net-DNS-SEC
BuildRequires:	perl-TimeDate
BuildRequires:	perl-base
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
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
%setup -q
%patch0 -p1

%build
%configure \
	--disable-bind-checks \
	--with-dlv \
	--with-ipv6 \
	--with-nsec3 \
	--with-perl-build-args='INSTALLDIRS=vendor'
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{perl_vendorarch}/auto -name .packlist | xargs -r %{__rm}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/blinkenlights
%attr(755,root,root) %{_bindir}/bubbles
%attr(755,root,root) %{_bindir}/cleanarch
%attr(755,root,root) %{_bindir}/cleankrf
%attr(755,root,root) %{_bindir}/convertar
%attr(755,root,root) %{_bindir}/dnspktflow
%attr(755,root,root) %{_bindir}/donuts
%attr(755,root,root) %{_bindir}/donutsd
%attr(755,root,root) %{_bindir}/drawvalmap
%attr(755,root,root) %{_bindir}/dtck
%attr(755,root,root) %{_bindir}/dtconf
%attr(755,root,root) %{_bindir}/dtconfchk
%attr(755,root,root) %{_bindir}/dtdefs
%attr(755,root,root) %{_bindir}/dtinitconf
%attr(755,root,root) %{_bindir}/expchk
%attr(755,root,root) %{_bindir}/fixkrf
%attr(755,root,root) %{_bindir}/genkrf
%attr(755,root,root) %{_bindir}/getaddr
%attr(755,root,root) %{_bindir}/getdnskeys
%attr(755,root,root) %{_bindir}/getds
%attr(755,root,root) %{_bindir}/gethost
%attr(755,root,root) %{_bindir}/getname
%attr(755,root,root) %{_bindir}/getquery
%attr(755,root,root) %{_bindir}/getrrset
%attr(755,root,root) %{_bindir}/keyarch
%attr(755,root,root) %{_bindir}/krfcheck
%attr(755,root,root) %{_bindir}/libval_check_conf
%attr(755,root,root) %{_bindir}/lights
%attr(755,root,root) %{_bindir}/lsdnssec
%attr(755,root,root) %{_bindir}/lskrf
%attr(755,root,root) %{_bindir}/lsroll
%attr(755,root,root) %{_bindir}/maketestzone
%attr(755,root,root) %{_bindir}/mapper
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
%attr(755,root,root) %{_bindir}/validate
%attr(755,root,root) %{_bindir}/zonesigner
%dir %{_sysconfdir}/dnssec-tools
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dnssec-tools/dnssec-tools.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dnssec-tools/validator-testcases
%{_datadir}/%{name}
%{_mandir}/man1/blinkenlights.1p*
%{_mandir}/man1/bubbles.1p*
%{_mandir}/man1/cleanarch.1p*
%{_mandir}/man1/cleankrf.1p*
%{_mandir}/man1/convertar.1p*
%{_mandir}/man1/dnspktflow.1p*
%{_mandir}/man1/dnssec-tools.1*
%{_mandir}/man1/donuts.1p*
%{_mandir}/man1/donutsd.1p*
%{_mandir}/man1/drawvalmap.1p*
%{_mandir}/man1/dtck.1p*
%{_mandir}/man1/dtconf.1p*
%{_mandir}/man1/dtconfchk.1p*
%{_mandir}/man1/dtdefs.1p*
%{_mandir}/man1/dtinitconf.1p*
%{_mandir}/man1/expchk.1p*
%{_mandir}/man1/fixkrf.1p*
%{_mandir}/man1/genkrf.1p*
%{_mandir}/man1/getaddr.1*
%{_mandir}/man1/getdnskeys.1p*
%{_mandir}/man1/getds.1p*
%{_mandir}/man1/gethost.1*
%{_mandir}/man1/getname.1*
%{_mandir}/man1/getquery.1*
%{_mandir}/man1/getrrset.1*
%{_mandir}/man1/keyarch.1p*
%{_mandir}/man1/krfcheck.1p*
%{_mandir}/man1/libval_check_conf.1*
%{_mandir}/man1/lights.1p*
%{_mandir}/man1/lsdnssec.1p*
%{_mandir}/man1/lskrf.1p*
%{_mandir}/man1/lsroll.1p*
%{_mandir}/man1/maketestzone.1p*
%{_mandir}/man1/mapper.1p*
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
%{_mandir}/man1/validate.1*
%{_mandir}/man1/zonesigner.1p*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsres.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsres.so.9
%attr(755,root,root) %{_libdir}/libval-threads.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libval-threads.so.9
%attr(755,root,root) %{_libdir}/libval_shim.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libval_shim.so.9

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
%{_mandir}/man3/libval_shim.3*
%{_mandir}/man3/p_ac_status.3*
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
%dir %{perl_vendorarch}/Net/DNS/SEC
%{perl_vendorarch}/Net/DNS/SEC/Tools
%{perl_vendorarch}/Net/DNS/SEC/Validator.pm
%{perl_vendorarch}/Net/DNS/SEC/defines.pl
%{perl_vendorarch}/Net/DNS/ZoneFile
%{perl_vendorarch}/Net/addrinfo.pm
%dir %{perl_vendorarch}/auto/Net/DNS/SEC
%dir %{perl_vendorarch}/auto/Net/DNS/SEC/Validator
%{perl_vendorarch}/auto/Net/DNS/SEC/Validator/Validator.bs
%attr(755,root,root) %{perl_vendorarch}/auto/Net/DNS/SEC/Validator/Validator.so
%{perl_vendorarch}/auto/Net/addrinfo/addrinfo.bs
%attr(755,root,root) %{perl_vendorarch}/auto/Net/addrinfo/addrinfo.so
%{perl_vendorlib}/Net/DNS/SEC/Tools
%{_mandir}/man3/Net::DNS::SEC::Tools::*.3pm*
%{_mandir}/man3/Net::DNS::SEC::Validator.3pm*
%{_mandir}/man3/Net::DNS::ZoneFile::Fast.3pm*
%{_mandir}/man3/Net::addrinfo.3pm*
