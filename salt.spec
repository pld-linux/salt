%define	appname	salt
Summary:	Powerful remote config and execution manager.
Name:		python-%{appname}
Version:	0.9.9
Release:	1
License:	Apache 2.0
Group:		Libraries/Python
Source0:	https://github.com/downloads/saltstack/%{appname}/%{appname}-%{version}.tar.gz
# Source0-md5:	fa223f1abe5b80a5226bc987ff7735c5
Patch0:		%{name}-grains.patch
URL:		http://saltstack.org/
BuildRequires:	gettext
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-Crypto
Requires:	python-M2Crypto
Requires:	python-PyYAML
Requires:	python-msgpack
Requires:	python-pyzmq
Suggests:	python-jinja2
%pyrequires_eq	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Powerful remote execution manager that can be used to administer 
servers in a fast and efficient way.

%prep
%setup -q -n %{appname}-%{version}
%patch0 -p1

%build
export CFLAGS="%{rpmcflags}"
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir /etc/%{appname}
/etc/%{appname}/*.template
%attr(755,root,root) %{_bindir}/salt
%attr(755,root,root) %{_bindir}/salt-call
%attr(755,root,root) %{_bindir}/salt-cp
%attr(755,root,root) %{_bindir}/salt-key
%attr(755,root,root) %{_bindir}/salt-master
%attr(755,root,root) %{_bindir}/salt-minion
%attr(755,root,root) %{_bindir}/salt-run
%attr(755,root,root) %{_bindir}/salt-syndic
%dir %{py_sitescriptdir}/%{appname}
%{py_sitescriptdir}/%{appname}/*.py[co]
%dir %{py_sitescriptdir}/%{appname}/ext
%{py_sitescriptdir}/%{appname}/ext/*.py[co]
%dir %{py_sitescriptdir}/%{appname}/cli
%{py_sitescriptdir}/%{appname}/cli/*.py[co]
%dir %{py_sitescriptdir}/%{appname}/grains
%{py_sitescriptdir}/%{appname}/grains/*.py[co]
%dir %{py_sitescriptdir}/%{appname}/modules
%{py_sitescriptdir}/%{appname}/modules/*.py[co]
%dir %{py_sitescriptdir}/%{appname}/utils
%{py_sitescriptdir}/%{appname}/utils/*.py[co]
%dir %{py_sitescriptdir}/%{appname}/states
%{py_sitescriptdir}/%{appname}/states/*.py[co]
%dir %{py_sitescriptdir}/%{appname}/runners
%{py_sitescriptdir}/%{appname}/runners/*.py[co]
%dir %{py_sitescriptdir}/%{appname}/returners
%{py_sitescriptdir}/%{appname}/returners/*.py[co]
%dir %{py_sitescriptdir}/%{appname}/renderers
%{py_sitescriptdir}/%{appname}/renderers/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{appname}-*.egg-info
%endif
%{_mandir}/man1/*
%{_mandir}/man7/*
