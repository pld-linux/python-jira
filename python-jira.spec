#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module jira
%define		pypi_name jira
%define		egg_name jira
Summary:	A library to ease use of the JIRA 5 REST APIs
Name:		python-%{pypi_name}
Version:	1.0.7
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/j/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	cb1d3f1e1b7a388932ad5d961bf2c56d
URL:		https://pypi.io/project/jira
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with python3}
BuildRequires:	python-devel
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%endif
Requires:	python-ipython-console
Requires:	python-magic
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A library to ease use of the JIRA 5 REST APIs.

%package -n python3-%{pypi_name}
Summary:	%{summary}
Group:		Libraries/Python
Requires:	python3-ipython-console
Requires:	python3-magic

%description -n python3-%{pypi_name}
A library to ease use of the JIRA 5 REST APIs.

%prep
%setup -q -n %{pypi_name}-%{version}

sed -i 's/tools.jirashell/jira.tools.jirashell/g' setup.py
sed -i "s/'ordereddict'//" setup.py

# Remove bundled egg-info in case it exists
rm -r %{pypi_name}.egg-info

# Remove shebang in the non-executable files
sed -i -e '/^#!\//, 1d' %{module}/{client,config,jirashell}.py

%build
%if %{with python2}
%py_build
%endif
%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
mv $RPM_BUILD_ROOT%{_bindir}/jirashell{,-%{py_ver}}
ln -sf jirashell-%{py_ver} $RPM_BUILD_ROOT%{_bindir}/jirashell-2
%endif

%if %{with python3}
%py3_install
mv $RPM_BUILD_ROOT%{_bindir}/jirashell{,-%{py3_ver}}
ln -s jirashell-%{py3_ver} $RPM_BUILD_ROOT%{_bindir}/jirashell-3
%endif

%if %{with python2}
ln -sf jirashell-2 $RPM_BUILD_ROOT%{_bindir}/jirashell
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc PKG-INFO LICENSE
%attr(755,root,root) %{_bindir}/jirashell
%attr(755,root,root) %{_bindir}/jirashell-2
%attr(755,root,root) %{_bindir}/jirashell-%{py_ver}
%{py_sitescriptdir}/%{module}/
%{py_sitescriptdir}/%{egg_name}-%{version}*
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc PKG-INFO LICENSE
%attr(755,root,root) %{_bindir}/jirashell-3
%attr(755,root,root) %{_bindir}/jirashell-%{py3_ver}
%{py3_sitescriptdir}/%{module}/
%{py3_sitescriptdir}/%{egg_name}-%{version}*
%endif
