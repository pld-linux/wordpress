Summary:	Personal publishing system
Summary(pl):	Osobisty system publikacji
Name:		wordpress
Version:	1.5
Release:	2
License:	GPL
Group:		Applications/Publishing
Source0:	http://wordpress.org/latest.tar.gz
# Source0-md5:	df6dc18a7a0d93fa6bb187eb48b41612
Source1:	wp-secure.sh
Source2:	wp-setup.sh
Source3:	wp-setup.txt
URL:		http://wordpress.org/
Requires:	php >= 4.1
Requires:	php-gettext >= 5.0
Requires:	php-mysql >= 5.0
Requires:	php-pcre >= 5.0
Requires:	php-xml >= 5.0
Requires:	php-xmlrpc >= 5.0
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	wordpressdir	/home/services/httpd/html/wordpress

%description
WordPress is a state-of-the-art semantic personal publishing platform
with a focus on aesthetics, web standards, and usability. WordPress
was born out of a desire for an elegant, well-architectured personal
publishing system (also called blog or weblog) built on PHP and MySQL
and licensed under the GPL. It is the official successor of
b2/cafelog. WordPress is fresh software, but its roots and development
go back to 2001.

%description -l pl
WordPress jest technologicznie dopracowan±, semantyczn±, osobist±
platform± do publikacji k³ad±c± nacisk na standardy WWW oraz
u¿yteczno¶æ. WordPress zosta³ stworzony w wyniku potrzeby
eleganckiego, dobrze zaprojektowanego, osobistego systemu publikacji
(nazywanego równie¿ blogiem czy weblogiem). Jest to system oparty
o PHP i MySQL oraz na licencji GPL. Jest oficjalnym nastêpc± b2/cafelog.
WordPress jest nowym oprogramowaniem, ale jego korzenie i rozwój
siêgaj± 2001 roku.

%prep
%setup -q -n %{name}
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{wordpressdir} $RPM_BUILD_ROOT%{_bindir}

rm -f license.txt
cp -R * $RPM_BUILD_ROOT%{wordpressdir}
ln -s %{wordpressdir}/wp-setup.sh $RPM_BUILD_ROOT%{_bindir}/wp-setup
ln -s %{wordpressdir}/wp-secure.sh $RPM_BUILD_ROOT%{_bindir}/wp-secure

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{wordpressdir}/wp-config.php ]; then
	touch %{wordpressdir}/wp-config.php
	chmod 0640 %{wordpressdir}/wp-config.php
	chown root:http %{wordpressdir}/wp-config.php
	cat %{wordpressdir}/wp-config-sample.php > %{wordpressdir}/wp-config.php
	echo "To finish your configuration DO NOT FORGET to:"
	echo
	echo "0.) Create some MySQL database owned by some user"
	echo "1.) Edit the file: %{wordpressdir}/wp-config.php"
	echo "2.) Run a browser and visit: http://`hostname`/wordpress/wp-admin/install.php"
fi

%files
%defattr(644,root,root,755)
%doc readme.html wp-setup.txt
%dir %{wordpressdir}
%dir %attr(750,root,http) %{wordpressdir}/wp-content
%attr(640,root,http) %{wordpressdir}/wp-content/plugins/*.php
%attr(640,root,http) %{wordpressdir}/wp-content/themes/classic/*
%attr(640,root,http) %{wordpressdir}/wp-content/themes/default/*.php
%attr(640,root,http) %{wordpressdir}/wp-content/themes/default/*.css
%attr(640,root,http) %{wordpressdir}/wp-content/themes/default/images/*
%{wordpressdir}/wp-admin
%{wordpressdir}/wp-images
%{wordpressdir}/wp-includes
%{wordpressdir}/*.php
%{wordpressdir}/wp-secure.sh
%{wordpressdir}/wp-setup.sh
%{_bindir}/wp-secure
%{_bindir}/wp-setup
