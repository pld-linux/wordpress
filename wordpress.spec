# TODO
# - gettext mo to system dir, add all possible languages?
# - merge changes from wpmu.spec
%include	/usr/lib/rpm/macros.php
%define		php_min_version 5.2.1
Summary:	Personal publishing system
Summary(pl.UTF-8):	Osobisty system publikacji
Name:		wordpress
Version:	3.5.2
Release:	2
License:	GPL v2
Group:		Applications/Publishing
Source0:	http://wordpress.org/%{name}-%{version}.tar.gz
# Source0-md5:	90acae65199db7b33084ef36860d7f22
Source1:	wp-secure.sh
Source2:	wp-setup.sh
Source3:	wp-setup.txt
Source4:	apache.conf
Source5:	lighttpd.conf
# no 3.5.1 tag
Source6:	http://svn.automattic.com/wordpress-i18n/et/tags/3.5/messages/et.po
# Source6-md5:	e6fbcf1940701ce6f1f91c0ad4ed5a99
# no messages under 3.5 tag
Source7:	http://svn.automattic.com/wordpress-i18n/pl_PL/tags/3.2.1/messages/pl_PL.po
# Source7-md5:	a0f5d65b7d4e5d53209edc595a19ff49
Patch0:		configpath.patch
Patch1:		multisite.patch
Patch2:		%{name}.patch
Patch3:		simplepie.patch
Patch4:		pear-text-diff.patch
Patch6:		swfobject.patch
Patch7:		phpmailer.patch
URL:		http://www.wordpress.org/
BuildRequires:	gettext-devel
BuildRequires:	rpm-php-pearprov
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	js-swfobject >= 2.2
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)
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
Requires:	php-pear-Text_Diff
Requires:	php-phpmailer >= 2.0.4
Requires:	php-simplepie >= 1.2
Requires:	webapps
Requires:	webserver(php)
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
Summary:	WordPress setup package
Summary(pl.UTF-8):	Pakiet do wstępnej konfiguracji WordPress
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
Summary:	WordPress Akismet Plugin
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description plugin-akismet
Akismet checks your comments against the Akismet web service to see if
they look like spam or not and lets you review the spam it catches
under your blog's "Comments" admin screen.

%package theme-twentyeleven
Summary:	WordPress Twenty Eleven theme
Group:		Applications/WWW
URL:		http://wordpress.org/extend/themes/twentyeleven
Requires:	%{name} = %{version}-%{release}

%description theme-twentyeleven
The 2011 theme for WordPress is sophisticated, lightweight, and
adaptable.

Make it yours with a custom menu, header image, and background -- then
go further with available theme options for light or dark color
scheme, custom link colors, and three layout choices. Twenty Eleven
comes equipped with a Showcase page template that transforms your
front page into a showcase to show off your best content, widget
support galore (sidebar, three footer areas, and a Showcase page
widget area), and a custom "Ephemera" widget to display your Aside,
Link, Quote, or Status posts. Included are styles for print and for
the admin editor, support for featured images (as custom header images
on posts and pages and as large images on featured "sticky" posts),
and special styles for six different post formats.

%package theme-twentytwelve
Summary:	WordPress Twenty Twelve theme
Group:		Applications/WWW
URL:		http://wordpress.org/extend/themes/twentytwelve
Requires:	%{name} = %{version}-%{release}

%description theme-twentytwelve
The 2012 theme for WordPress is a fully responsive theme that looks
great on any device.

Features include a front page template with its own widgets, an
optional display font, styling for post formats on both index and
single views, and an optional no-sidebar page template. Make it yours
with a custom menu, header image, and background.

%prep
%setup -qc
mv %{name}/* . && rmdir %{name}
%undos -f php,js,html
%patch0 -p1
%patch1 -p1
cp -p wp-config{-sample,}.php
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1
%patch7 -p1
cp -p %{SOURCE3} .

%{__rm} license.txt
%{__rm} wp-content/themes/index.php
%{__rm} wp-content/plugins/index.php
%{__rm} wp-content/index.php

# remove .js/.css with matching minified file
find -name '*.min.js' | while read min; do
	js=${min%.min.js}.js
	test -e $js && echo $js
done | xargs rm -v

find -name '*.min.css' | while read min; do
	css=${min%.min.css}.css
	test -e $css && echo $css
done | xargs rm -v

# sample plugin
%{__rm} wp-content/plugins/hello.php

# system swfobject
%{__rm} wp-includes/js/swfobject.js

# system simplepie
%{__rm} wp-includes/class-simplepie.php

# system php-pear-Text_Diff
%{__rm} -r wp-includes/Text/Diff*
rmdir wp-includes/Text

# system atomlib
%{__rm} wp-includes/atomlib.php

# system phpmailer
%{__rm} wp-includes/class-phpmailer.php
%{__rm} wp-includes/class-smtp.php

# php 5.2 + json ext satisfies this compat
%{__rm} wp-includes/class-json.php

%{__rm} wp-content/plugins/akismet/.htaccess

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

cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

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
%{_appdir}/wp-content/plugins/akismet/*.css
%{_appdir}/wp-content/plugins/akismet/*.gif
%{_appdir}/wp-content/plugins/akismet/*.js
%{_appdir}/wp-content/plugins/akismet/*.php

%files theme-twentyeleven
%defattr(644,root,root,755)
%{_appdir}/wp-content/themes/twentyeleven

%files theme-twentytwelve
%defattr(644,root,root,755)
%{_appdir}/wp-content/themes/twentytwelve
