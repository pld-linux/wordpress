# TODO
# - put config files to %{_sysconfdir}!
Summary:	Personal publishing system
Summary(pl.UTF-8):	Osobisty system publikacji
Name:		wordpress
Version:	2.0.7
Release:	1
License:	GPL
Group:		Applications/Publishing
Source0:	http://wordpress.org/latest.tar.gz
# Source0-md5:	e377fa9389d1a06a700ac349582f498c
Source1:	wp-secure.sh
Source2:	wp-setup.sh
Source3:	wp-setup.txt
Source4:	%{name}.conf
URL:		http://wordpress.org/
Requires:	php(gettext)
Requires:	php(mysql)
Requires:	php(pcre)
Requires:	php(xml)
Requires:	php(xmlrpc)
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

%prep
%setup -q -n %{name}
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} .
rm -f license.txt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_sysconfdir}}

cp -R * $RPM_BUILD_ROOT%{_appdir}
rm -f $RPM_BUILD_ROOT%{_appdir}/readme.html
rm -f $RPM_BUILD_ROOT%{_appdir}/wp-setup.txt
ln -sf %{_appdir}/wp-setup.sh $RPM_BUILD_ROOT%{_bindir}/wp-setup
ln -sf %{_appdir}/wp-secure.sh $RPM_BUILD_ROOT%{_bindir}/wp-secure

install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_appdir}/wp-config.php ]; then
	install -uroot -ghttp -m640 %{_appdir}/wp-config-sample.php > %{_appdir}/wp-config.php

	%banner -e %{name} <<-EOF
	To finish your configuration DO NOT FORGET to:

	1) Create some MySQL database owned by some user
	2) Edit the file: %{_appdir}/wp-config.php
	3) Run a browser and visit: http://`hostname`/wordpress/wp-admin/install.php
EOF
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc readme.html wp-setup.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf

%dir %{_appdir}
%dir %attr(750,root,http) %{_appdir}/wp-content
%dir %attr(750,root,http) %{_appdir}/wp-content/plugins
%dir %attr(750,root,http) %{_appdir}/wp-content/themes
%dir %attr(750,root,http) %{_appdir}/wp-content/themes/classic
%dir %attr(750,root,http) %{_appdir}/wp-content/themes/default
%attr(640,root,http) %{_appdir}/wp-content/plugins/*.php
%attr(640,root,http) %{_appdir}/wp-content/plugins/akismet
%attr(640,root,http) %{_appdir}/wp-content/themes/classic/*
%attr(640,root,http) %{_appdir}/wp-content/themes/default/*.php
%attr(640,root,http) %{_appdir}/wp-content/themes/default/*.css
%attr(640,root,http) %{_appdir}/wp-content/themes/default/images/*
%{_appdir}/wp-admin
%{_appdir}/wp-includes
%{_appdir}/*.php
%{_appdir}/wp-secure.sh
%{_appdir}/wp-setup.sh
%attr(755,root,root) %{_bindir}/wp-secure
%attr(755,root,root) %{_bindir}/wp-setup
