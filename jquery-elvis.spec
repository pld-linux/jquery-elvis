# TODO
# - paths and deps for demo
%define		plugin	elvis
Summary:	jQuery plugin for ElvisAPI
Name:		jquery-%{plugin}
Version:	0.1
Release:	0.1
License:	MIT
Group:		Applications/WWW
Source0:	https://github.com/dutchsoftware/elvis-API-samples/tarball/master/%{name}-%{version}.tgz
# Source0-md5:	47551e2011b458f674f5e2dc2d695219
URL:		https://elvis.tenderapp.com/kb/api/javascript-library-elvisapi
BuildRequires:	closure-compiler
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	unzip
BuildRequires:	yuicompressor
Requires:	jquery >= 1.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/jquery/%{plugin}

%description
This class provides a thin layer around commonly used Elvis REST API
methods.

It streamlines the authentication process and underlying AJAX calls so
you can focus on coding your added functionality.

%package demo
Summary:	Demo for jQuery.%{plugin}
Summary(pl.UTF-8):	Pliki demonstracyjne dla pakietu jQuery.%{plugin}
Group:		Development
Requires:	%{name} = %{version}-%{release}

%description demo
Demonstrations and samples for jQuery.%{plugin}.

%prep
%setup -qc
mv *-%{plugin}-*/* .

install -d demo
mv action_plugins *_samples demo

%build
install -d build

# compress .js
for js in elvis_api/js/*.js; do
	out=build/${js#*/jquery.}
%if 0%{!?debug:1}
	yuicompressor --charset UTF-8 $js -o $out
	js -C -f $out
%else
	cp -a $js $out
%endif
done


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}
cp -p build/%{plugin}.js  $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.min.js
cp -p elvis_api/js/jquery.%{plugin}.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.js
ln -s %{plugin}-%{version}.min.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}.js

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a demo/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%{_appdir}

%files demo
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
