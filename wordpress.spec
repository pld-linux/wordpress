# TODO
# - gettext mo to system dir, add all possible languages?
# - merge changes from wpmu.spec
Summary:	Personal publishing system
Summary(pl.UTF-8):	Osobisty system publikacji
Name:		wordpress
Version:	3.0.1
Release:	0.2
License:	GPL v2
Group:		Applications/Publishing
Source0:	http://wordpress.org/%{name}-%{version}.tar.gz
# Source0-md5:	8fa5373ed805fb9a6ee56dfd236dcb64
Source1:	wp-secure.sh
Source2:	wp-setup.sh
Source3:	wp-setup.txt
Source4:	apache.conf
Source5:	lighttpd.conf
Source6:	http://svn.automattic.com/wordpress-i18n/et/tags/%{version}/messages/et.po
# Source6-md5:	7ee698806091573a534a4889f88d6d97
Source7:	http://svn.automattic.com/wordpress-i18n/pl_PL/tags/%{version}/messages/pl_PL.po
# Source7-md5:	795864c6eeeadcc74b8ea70d45f22e9f
# MagpieRSS upgrade (version 0.8a) from feedwordpress plugin: http://feedwordpress.radgeek.com/
Source10:	rss.php
Source11:	rss-functions.php
Patch0:		%{name}.patch
URL:		http://www.wordpress.org/
BuildRequires:	gettext-devel
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	php-gettext
Requires:	php-mysql
Requires:	php-pcre
Requires:	php-xml
Requires:	php-xmlrpc
Requires:	webapps
Requires:	webserver(php) >= 5.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
WordPress is a state-of-the-art semantic personal publishing platform
with a focus on aesthetics, web standards, and usability. WordPress
was born out of a desire for an elegant, well-architectured personal
publishing system (also called blog or weblog) built on PHP and MySQL
and licensed under the GPL. It is the official successor of
b2/cafelog. WordPress is fresh software, but its roots and development
go back to 2001.

%description -l pl.UTF-8
WordPress jest technologicznie dopracowaną, semantyczną, osobistą
platformą do publikacji kładącą nacisk na standardy WWW oraz
użyteczność. WordPress został stworzony w wyniku potrzeby
eleganckiego, dobrze zaprojektowanego, osobistego systemu publikacji
(nazywanego również blogiem czy weblogiem). Jest to system oparty o
PHP i MySQL oraz na licencji GPL. Jest oficjalnym następcą b2/cafelog.
WordPress jest nowym oprogramowaniem, ale jego korzenie i rozwój
sięgają 2001 roku.

%package setup
Summary:	Wordpress setup package
Summary(pl.UTF-8):	Pakiet do wstępnej konfiguracji Wordpress
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description setup
Install this package to configure initial WordPress installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl.UTF-8
Ten pakiet należy zainstalować w celu wstępnej konfiguracji WordPress
po pierwszej instalacji. Potem należy go odinstalować, jako że
pozostawienie plików instalacyjnych mogłoby być niebezpieczne.

%prep
%setup -qc
mv %{name}/* . && rmdir %{name}
%undos -f php,js,html
cp -a wp-config{-sample,}.php
%patch0 -p1
cp -a %{SOURCE3} .
rm -f license.txt

rm wp-content/themes/index.php
rm wp-content/plugins/index.php
rm wp-content/index.php

# Install new MagpieRSS
# NOTE: this is deprecated, simplepie should be used instead
cp -a %{SOURCE10} wp-includes/rss.php
cp -a %{SOURCE11} wp-includes/rss-functions.php

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
install -d wp-content/languages
msgfmt --statistics %{SOURCE6} -o wp-content/languages/et.mo
msgfmt --statistics %{SOURCE7} -o wp-content/languages/pl_PL.mo

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_sysconfdir},%{_appdir}/wp-content/languages}

cp -a . $RPM_BUILD_ROOT%{_appdir}
mv $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}/wp-config.php
rm -f $RPM_BUILD_ROOT%{_appdir}/readme.html
rm -f $RPM_BUILD_ROOT%{_appdir}/wp-setup.txt

install -p %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/wp-secure
install -p %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/wp-setup
ln -s %{_bindir}/wp-setup $RPM_BUILD_ROOT%{_appdir}/wp-setup.sh
ln -s %{_bindir}/wp-secure $RPM_BUILD_ROOT%{_appdir}/wp-secure.sh

cp -a %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
	%banner -e %{name} <<-EOF
	To finish your configuration DO NOT FORGET to:

	1) Create some MySQL database owned by some user
	2) Edit the file: %{_sysconfdir}/wp-config.php
	3) Install %{name}-setup
	4) Run a browser and visit: http://`hostname`/wordpress/wp-admin/install.php
EOF
fi

%post setup
chmod 660 %{_sysconfdir}/wp-config.php
chown root:http %{_sysconfdir}/wp-config.php

%postun setup
if [ "$1" = "0" ]; then
	chmod 640 %{_sysconfdir}/wp-config.php
	chown root:http %{_sysconfdir}/wp-config.php
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc readme.html wp-setup.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/wp-config.php

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/wp-includes
%dir %{_appdir}/wp-content
%dir %{_appdir}/wp-content/languages
%lang(et) %{_appdir}/wp-content/languages/et.mo
%lang(pl) %{_appdir}/wp-content/languages/pl_PL.mo
%dir %{_appdir}/wp-content/plugins
%{_appdir}/wp-content/plugins/*.php
%{_appdir}/wp-content/plugins/akismet

%dir %{_appdir}/wp-content/themes
%{_appdir}/wp-content/themes/twentyten

%files setup
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wp-secure
%attr(755,root,root) %{_bindir}/wp-setup
%{_appdir}/wp-secure.sh
%{_appdir}/wp-setup.sh
%{_appdir}/wp-admin
