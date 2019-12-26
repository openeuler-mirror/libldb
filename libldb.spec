Name:            libldb
Version:         1.4.2
Release:         3
Summary:         A LDAP-like embedded database
License:         LGPLv3+
URL:             http://ldb.samba.org/
Source:          http://samba.org/ftp/ldb/ldb-%{version}.tar.gz
#Patch0001 and patch6000 are come from upstream community
Patch0001:       0002-ldb-Run-at-least-some-tests-on-32-bit-machines.patch
Patch6000:       0003-ldb-Out-ouf-bound-read-in-ldb_wildcard_compare.patch

BuildRequires:   gcc popt-devel libxslt docbook-style-xsl python2-devel python2-tdb python2-talloc-devel python2-tevent
BuildRequires:   libtalloc-devel >= 2.1.11 doxygen openldap-devel libcmocka-devel
BuildRequires:   libtdb-devel >= 1.3.14 libtevent-devel >= 0.9.36 chrpath
BuildRequires:   lmdb-devel >= 0.9.16 python3-devel python3-tdb python3-talloc-devel python3-tevent
Requires:        libtalloc%{?_isa} >= 2.1.11 libtdb%{?_isa} >= 1.3.14 libtevent%{?_isa} >= 0.9.36

Provides:        bundled(libreplace) ldb-tools
Obsoletes:       ldb-tools

%description
ldb is a LDAP-like embedded database and is not at all LDAP standards compliant.It provide a
fast database with an LDAP-like API designed to be used within an application.

%package devel
Summary: Developer files for ldb
Requires: libldb%{?_isa} = %{version}-%{release} pkgconfig libtevent-devel%{?_isa} >= 0.9.36
Requires: libtdb-devel%{?_isa} >= 1.3.14 libtalloc-devel%{?_isa} >= 2.1.11

%description devel
Develop files for use LDB library.

%package -n python2-ldb
Summary: Python2 bindings for ldb
Requires: libldb%{?_isa} = %{version}-%{release} python2-tdb%{?_isa} >= 1.3.14

Provides: pyldb = %{version}-%{release} pyldb%{?_isa} = %{version}-%{release}
Obsoletes: pyldb < 1.1.26-2
%{?python_provide:%python_provide python2-ldb}

%description -n python2-ldb
Python2 bindings for ldb.

%package -n python2-ldb-devel
Summary: Develop files for python2 bindings for ldb
Requires: python2-ldb%{?_isa} = %{version}-%{release} python-ldb-devel-common%{?_isa} = %{version}-%{release}

Provides: pyldb-devel = %{version}-%{release} pyldb-devel%{?_isa} = %{version}-%{release}
Obsoletes: pyldb-devel < 1.1.26-2
%{?python_provide:%python_provide python2-ldb-devel}

%description -n python2-ldb-devel
Develop files for python2 bindings for ldb.

%package -n python-ldb-devel-common
Summary: Common develop files for python bindings for ldb

Provides: pyldb-devel%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-ldb-devel}

%description -n python-ldb-devel-common
This packages provides develop files for python bindings for ldb.

%package -n python3-ldb
Summary: Python3 bindings for ldb
Requires: libldb%{?_isa} = %{version}-%{release} python3-tdb%{?_isa} >= %{tdb_version}
%{?python_provide:%python_provide python3-ldb}

%description -n python3-ldb
Python3 bindings for ldb.

%package -n python3-ldb-devel
Summary: Develop files for python3 bindings for ldb
Requires: python3-ldb%{?_isa} = %{version}-%{release} python-ldb-devel-common%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python3-ldb-devel}

%description -n python3-ldb-devel
Develop files for the python3 bindings for ldb.

%package help
Summary: Document files for libldb

%description help
Document files for libldb.

%prep
%autosetup -n ldb-%{version} -p1

%build
pathfix.py -n -p -i %{__python2} buildtools/bin/waf
%configure --disable-rpath --disable-rpath-install --bundled-libraries=NONE \
           --builtin-libraries=replace --with-modulesdir=%{_libdir}/ldb/modules \
           --extra-python=%{__python3} --with-privatelibdir=%{_libdir}/ldb

%make_build V=1
doxygen Doxyfile

%install
%make_install
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;
cp -a apidocs/man/* $RPM_BUILD_ROOT/%{_mandir}

chrpath -d $RPM_BUILD_ROOT%{_libdir}/ldb/modules/ldb/*.so*
chrpath -d $RPM_BUILD_ROOT%{_libdir}/ldb/*.so*

mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo "%{_libdir}/ldb" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf
rm -f $RPM_BUILD_ROOT%{_libdir}/libldb.a

%check
%if %{?_with_check:1}%{!?_with_check:0}
%make_build check
%endif

%post
ldconfig
%post -n python2-ldb
ldconfig
%post -n python3-ldb
ldconfig
%postun
ldconfig
%postun -n python2-ldb
ldconfig
%postun -n python3-ldb
ldconfig

%files
%{_libdir}/libldb.so.*
%{_libdir}/ldb/lib*.so
%{_libdir}/ldb/modules/ldb/*.so
%{_bindir}/ldb*
%config(noreplace) /etc/ld.so.conf.d/*
%exclude %{_libdir}/libldb.a

%files devel
%{_includedir}/ldb*.h
%{_libdir}/libldb.so
%{_libdir}/pkgconfig/ldb.pc

%files -n python2-ldb
%{python2_sitearch}/ldb.so
%{_libdir}/libpyldb-util.so.1*
%{python2_sitearch}/_ldb_text.py*

%files -n python2-ldb-devel
%{_libdir}/libpyldb-util.so
%{_libdir}/pkgconfig/pyldb-util.pc

%files -n python-ldb-devel-common
%{_includedir}/pyldb.h

%files -n python3-ldb
%{python3_sitearch}/ldb.cpython-*.so
%{_libdir}/libpyldb-util.cpython-*.so.1*
%{python3_sitearch}/_ldb_text.py
%{python3_sitearch}/__pycache__/_ldb_text.cpython-*.py*

%files -n python3-ldb-devel
%{_libdir}/libpyldb-util.cpython-*.so
%{_libdir}/pkgconfig/pyldb-util.cpython-*.pc

%files help
%{_mandir}/man1/ldb*.1.*
%{_mandir}/man3/ldb*.gz
%{_mandir}/man3/ldif*.gz
%{_mandir}/man*/Py*.gz
%exclude /%{_mandir}/man3/_*

%changelog
* Thu Dec 26 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.4.2-3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:remove rpath and runpath of exec files and libraries

* Wed Sep 11 2019 liyongqiang<liyongqiang10@huawei.com> - 1.4.2-2
- Package init

