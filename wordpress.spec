# TODO
# - gettext mo to system dir, add all possible languages?
# - merge changes from wpmu.spec
%include	/usr/lib/rpm/macros.php
%define		php_min_version 5.2.1
Summary:	Personal publishing system
Summary(pl.UTF-8):	Osobisty system publikacji
Name:		wordpress
Version:	3.0.4
Release:	4
License:	GPL v2
Group:		Applications/Publishing
Source0:	http://wordpress.org/%{name}-%{version}.tar.gz
# Source0-md5:	a455e0834eb2c8994c35acf3c13ddc11
Source1:	wp-secure.sh
Source2:	wp-setup.sh
Source3:	wp-setup.txt
Source4:	apache.conf
Source5:	lighttpd.conf
Source6:	http://svn.automattic.com/wordpress-i18n/et/tags/%{version}/messages/et.po
# Source6-md5:	faccf42481d5bf742b019c24a3c6251a
Source7:	http://svn.automattic.com/wordpress-i18n/pl_PL/tags/%{version}/messages/pl_PL.po
# Source7-md5:	8c9038410b596f9c705cc006dcdd5960
Source8:	httpd.conf
Patch0:		configpath.patch
Patch1:		multisite.patch
Patch2:		%{name}.patch
Patch3:		simplepie.patch
Patch4:		pear-text-diff.patch
Patch5:		atomlib.patch
Patch6:		swfobject.patch
Patch7:		phpmailer.patch
URL:		http://www.wordpress.org/
BuildRequires:	gettext-devel
BuildRequires:	rpm-php-pearprov
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	js-swfobject >= 2.1
Requires:	php(core) >= %{php_min_version}
Requires:	php(dom)
Requires:	php(gettext)
Requires:	php(hash)
Requires:	php(iconv)
Requires:	php(json)
Requires:	php(mbstring)
Requires:	php(mysql)
Requires:	php(pcre)
Requires:	php(spl)
Requires:	php(tokenizer)
Requires:	php(xml)
Requires:	php-atomlib >= 0.4
Requires:	php-date
Requires:	php-pear-Text_Diff
Requires:	php-phpmailer >= 2.0.4
Requires:	php-simplepie >= 1.2
Requires:	webapps
Requires:	webserver(php)
Conflicts:	apache-base < 2.4.0-1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# no pear deps
%define		_noautopear	pear

%define		_noautophp	php-ftp php-gd php-openssl php-simplexml

# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

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

%package plugin-akismet
Summary:	Wordpress Akismet Plugin
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description plugin-akismet
Akismet checks your comments against the Akismet web service to see if
they look like spam or not and lets you review the spam it catches
under your blog's "Comments" admin screen.

%package theme-twentyten
Summary:	Wordpress MU default theme
Group:		Applications/WWW
URL:		http://wordpress.org/extend/themes/twentyten
Requires:	%{name} = %{version}-%{release}

%description theme-twentyten
The 2010 theme for WordPress is stylish, customizable, simple, and
readable.

Make it yours with a custom menu, header image, and background. Twenty
Ten supports six widgetized areas (two in the sidebar, four in the
footer) and featured images (thumbnails for gallery posts and custom
header images for posts and pages). It includes stylesheets for print
and the admin Visual Editor, special styles for posts in the "Asides"
and "Gallery" categories, and has an optional one-column page template
that removes the sidebar.

%prep
%setup -qc
mv %{name}/* . && rmdir %{name}
%undos -f php,js,html
%patch0 -p1
%patch1 -p1
cp -a wp-config{-sample,}.php
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
cp -a %{SOURCE3} .

rm license.txt
rm wp-content/themes/index.php
rm wp-content/plugins/index.php
rm wp-content/index.php

# remove *.dev js/.css
find -name *.dev.js | xargs rm -v
find -name *.dev.css | xargs rm -v

# sample plugin
rm wp-content/plugins/hello.php

# system swfobject
rm wp-includes/js/swfobject.js

# system simplepie
rm wp-includes/class-simplepie.php

# system php-pear-Text_Diff
rm -r wp-includes/Text/Diff*
rmdir wp-includes/Text

# system atomlib
rm wp-includes/atomlib.php

# system phpmailer
rm wp-includes/class-phpmailer.php
rm wp-includes/class-smtp.php

# php 5.2 + json ext satisfies this compat
rm wp-includes/class-json.php

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
install -d wp-content/languages
msgfmt --statistics %{SOURCE6} -o wp-content/languages/et.mo
msgfmt --statistics %{SOURCE7} -o wp-content/languages/pl_PL.mo

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_sysconfdir},%{_appdir}/wp-content/{languages,mu-plugins},/var/{lib,log}/%{name}}

cp -a . $RPM_BUILD_ROOT%{_appdir}
mv $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}/wp-config.php
rm -f $RPM_BUILD_ROOT%{_appdir}/readme.html
rm -f $RPM_BUILD_ROOT%{_appdir}/wp-setup.txt

install -p %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/wp-secure
install -p %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/wp-setup
ln -s %{_bindir}/wp-setup $RPM_BUILD_ROOT%{_appdir}/wp-setup.sh
ln -s %{_bindir}/wp-secure $RPM_BUILD_ROOT%{_appdir}/wp-secure.sh

cp -a %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
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

%triggerin -- apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache-base
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
%dir %{_appdir}/wp-content/mu-plugins
%dir %{_appdir}/wp-content/themes

# needed for daily moderation
%{_appdir}/wp-admin

%attr(775,root,http) /var/lib/%{name}
%attr(775,root,http) /var/log/%{name}

%files setup
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wp-secure
%attr(755,root,root) %{_bindir}/wp-setup
%{_appdir}/wp-secure.sh
%{_appdir}/wp-setup.sh

%files plugin-akismet
%defattr(644,root,root,755)
%dir %{_appdir}/wp-content/plugins/akismet
%doc %{_appdir}/wp-content/plugins/akismet/readme.txt
%{_appdir}/wp-content/plugins/akismet/*.php
%{_appdir}/wp-content/plugins/akismet/*.gif

%files theme-twentyten
%defattr(644,root,root,755)
%{_appdir}/wp-content/themes/twentyten
