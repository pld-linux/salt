Summary:	Powerful remote config and execution manager.
Name:		salt
Version:	0.11.1
Release:	1
License:	Apache 2.0
Group:		Applications/System
Source0:	http://pypi.python.org/packages/source/s/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	0e96a361a5bfb9a208a6a30b2537a7c2
Source1:	%{name}-minion.service
Source2:	%{name}-master.service
URL:		http://saltstack.org/
BuildRequires:	gettext
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-Crypto
Requires:	python-M2Crypto
Requires:	python-PyYAML
Requires:	python-msgpack
Requires:	python-zmq
Suggests:	lsb-release
Suggests:	python-jinja2
%pyrequires_eq	python-modules
Obsoletes:	python-%{name}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Powerful remote execution manager that can be used to administer 
servers in a fast and efficient way.

%package minion
Summary:	Salt Minion
Summary(pl.UTF-8):	Salt Minion
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires(post):	systemd-units
Requires(preun):	systemd-units
Requires(postun):	systemd-units

%description minion
Salt Minion

%package master
Summary:	Salt Master
Summary(pl.UTF-8):	Salt Master
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires(post):	systemd-units
Requires(preun):	systemd-units
Requires(postun):	systemd-units

%description master
Salt Master

%prep
%setup

%build
export CFLAGS="%{rpmcflags}"
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/{etc,%{systemdunitdir}}
cp -r conf $RPM_BUILD_ROOT/etc/salt
cp %SOURCE1 $RPM_BUILD_ROOT/%{systemdunitdir}/%{name}-minion.service
cp %SOURCE2 $RPM_BUILD_ROOT/%{systemdunitdir}/%{name}-master.service
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post minion
%systemd_post %{name}-minion.service

%preun minion
%systemd_preun %{name}-minion.service

%postun minion
%systemd_reload

%post master
%systemd_post %{name}-master.service

%preun master
%systemd_preun %{name}-master.service

%postun master
%systemd_reload

%files
%defattr(644,root,root,755)
%dir /etc/%{name}
%attr(755,root,root) %{_bindir}/salt
%attr(755,root,root) %{_bindir}/salt-call
%attr(755,root,root) %{_bindir}/salt-cp
%attr(755,root,root) %{_bindir}/salt-key
%attr(755,root,root) %{_bindir}/salt-master
%attr(755,root,root) %{_bindir}/salt-minion
%attr(755,root,root) %{_bindir}/salt-run
%attr(755,root,root) %{_bindir}/salt-syndic
%dir %{py_sitescriptdir}/%{name}
%{py_sitescriptdir}/%{name}/*.py[co]
%dir %{py_sitescriptdir}/%{name}/auth
%{py_sitescriptdir}/%{name}/auth/*.py[co]
%dir %{py_sitescriptdir}/%{name}/cli
%{py_sitescriptdir}/%{name}/cli/*.py[co]
%dir %{py_sitescriptdir}/%{name}/ext
%{py_sitescriptdir}/%{name}/ext/*.py[co]
%dir %{py_sitescriptdir}/%{name}/grains
%{py_sitescriptdir}/%{name}/grains/*.py[co]
%dir %{py_sitescriptdir}/%{name}/modules
%{py_sitescriptdir}/%{name}/modules/*.py[co]
%dir %{py_sitescriptdir}/%{name}/modules/rh_ip
%{py_sitescriptdir}/%{name}/modules/rh_ip/*.jinja
%dir %{py_sitescriptdir}/%{name}/output
%{py_sitescriptdir}/%{name}/output/*.py[co]
%dir %{py_sitescriptdir}/%{name}/pillar
%{py_sitescriptdir}/%{name}/pillar/*.py[co]
%dir %{py_sitescriptdir}/%{name}/runners
%{py_sitescriptdir}/%{name}/runners/*.py[co]
%dir %{py_sitescriptdir}/%{name}/returners
%{py_sitescriptdir}/%{name}/returners/*.py[co]
%dir %{py_sitescriptdir}/%{name}/renderers
%{py_sitescriptdir}/%{name}/renderers/*.py[co]
%dir %{py_sitescriptdir}/%{name}/search
%{py_sitescriptdir}/%{name}/search/*.py[co]
%dir %{py_sitescriptdir}/%{name}/states
%{py_sitescriptdir}/%{name}/states/*.py[co]
%dir %{py_sitescriptdir}/%{name}/tops
%{py_sitescriptdir}/%{name}/tops/*.py[co]
%dir %{py_sitescriptdir}/%{name}/utils
%{py_sitescriptdir}/%{name}/utils/*.py[co]
%dir %{py_sitescriptdir}/%{name}/wheel
%{py_sitescriptdir}/%{name}/wheel/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{name}-*.egg-info
%endif
%{_mandir}/man1/*
%{_mandir}/man7/*

%files minion
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/%{name}/minion
%{systemdunitdir}/%{name}-minion.service

%files master
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/%{name}/master
%{systemdunitdir}/%{name}-master.service

