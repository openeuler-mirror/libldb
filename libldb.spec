%global with_lmdb 1
%global with_python3 1
%global talloc_version 2.2.0
%global tdb_version 1.4.1
%global tevent_version 0.10.0

Name:          libldb
Version:       2.0.12
Release:       2
Summary:       A schema-less, ldap like, API and database
Requires:      libtalloc%{?_isa} >= %{talloc_version}
Requires:      libtdb%{?_isa} >= %{tdb_version}
Requires:      libtevent%{?_isa} >= %{tevent_version}
License:       LGPLv3+
URL:           http://ldb.samba.org/
Source0:       https://www.samba.org/ftp/ldb/ldb-%{version}.tar.gz

Patch0:        Skip-ldb_lmdb_free_list_test-on-ppc64el-ppc64-and-sp.patch

BuildRequires: gcc libtalloc-devel >= %{talloc_version} libtdb-devel >= %{tdb_version}
BuildRequires: libtevent-devel >= %{tevent_version} lmdb-devel >= 0.9.16 popt-devel
BuildRequires: libxslt docbook-style-xsl python3-devel python3-tdb python3-talloc-devel
BuildRequires: python3-tevent doxygen openldap-devel libcmocka-devel gdb

Provides:      bundled(libreplace) ldb-tools
Obsoletes:     python2-ldb < 2.0.5-1 python2-ldb-devel < 2.0.5-1 pyldb < 1.1.26-2 ldb-tools

%description
An extensible library that implements an LDAP like API to access remote LDAP
servers, or use local tdb databases.

%package       devel
Summary:       Developer tools for the LDB library
Requires:      libldb%{?_isa} = %{version}-%{release} libtdb-devel%{?_isa} >= %{tdb_version}
Requires:      libtalloc-devel%{?_isa} >= %{talloc_version} libtevent-devel%{?_isa} >= %{tevent_version}

%description   devel
Header files needed to develop programs that link against the LDB library.

%package -n    python-ldb-devel-common
Summary:       Common development files for the Python bindings for the LDB library

Provides:      pyldb-devel%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-ldb-devel}

%description -n python-ldb-devel-common
Development files for the Python bindings for the LDB library.
This package includes files that aren't specific to a Python version.

%package -n    python3-ldb
Summary:       Python bindings for the LDB library
Requires:      libldb%{?_isa} = %{version}-%{release} python3-tdb%{?_isa} >= %{tdb_version}

%{?python_provide:%python_provide python3-ldb}

%description -n python3-ldb
Python bindings for the LDB library

%package -n    python3-ldb-devel
Summary:       Development files for the Python bindings for the LDB library
Requires:      python3-ldb%{?_isa} = %{version}-%{release}
Requires:      python-ldb-devel-common%{?_isa} = %{version}-%{release}

%{?python_provide:%python_provide python3-ldb-devel}

%description -n python3-ldb-devel
Development files for the Python bindings for the LDB library

%package_help

%prep
%autosetup -n ldb-%{version} -p1

%build

export python_LDFLAGS=""

%configure --disable-rpath \
           --disable-rpath-install \
           --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --with-modulesdir=%{_libdir}/ldb/modules \
           %{?without_lmdb_flags} \
           --with-privatelibdir=%{_libdir}/ldb

make %{?_smp_mflags} V=1
doxygen Doxyfile

%check
echo disabling one assertion in tests/python/repack.py
sed -e '/test_guid_indexed_v1_db/,+18{/toggle_guidindex_check_pack/d}' -i tests/python/repack.py
make %{?_smp_mflags} check

%install
make install DESTDIR=$RPM_BUILD_ROOT
cp -a apidocs/man/* $RPM_BUILD_ROOT/%{_mandir}
rm -f $RPM_BUILD_ROOT/%{_mandir}/man3/_*

%ldconfig_scriptlets

%files
%{_bindir}/ldbadd
%{_bindir}/ldbdel
%{_bindir}/ldbedit
%{_bindir}/ldbmodify
%{_bindir}/ldbrename
%{_bindir}/ldbsearch
%dir %{_libdir}/ldb
%{_libdir}/libldb.so.*
%{_libdir}/ldb/libldb-key-value.so
%{_libdir}/ldb/libldb-tdb-err-map.so
%{_libdir}/ldb/libldb-tdb-int.so
%{_libdir}/ldb/libldb-mdb-int.so
%dir %{_libdir}/ldb/modules
%dir %{_libdir}/ldb/modules/ldb
%{_libdir}/ldb/modules/ldb/*.so
%{_libdir}/ldb/libldb-cmdline.so

%files devel
%{_includedir}/ldb_module.h
%{_includedir}/ldb_handlers.h
%{_includedir}/ldb_errors.h
%{_includedir}/ldb_version.h
%{_includedir}/ldb.h
%{_libdir}/libldb.so
%{_libdir}/pkgconfig/ldb.pc

%files -n python-ldb-devel-common
%{_includedir}/pyldb.h

%files -n python3-ldb
%{python3_sitearch}/ldb.cpython-*.so
%{_libdir}/libpyldb-util.cpython-*.so.2*
%{python3_sitearch}/_ldb_text.py
%{python3_sitearch}/__pycache__/_ldb_text.cpython-*.py*

%files -n python3-ldb-devel
%{_libdir}/libpyldb-util.cpython-*.so
%{_libdir}/pkgconfig/pyldb-util.cpython-*.pc

%ldconfig_scriptlets -n python3-ldb

%files help
%{_mandir}/man*/Py*.gz
%{_mandir}/man3/ldb*.gz
%{_mandir}/man3/ldif*.gz
%{_mandir}/man1/ldbadd.1.*
%{_mandir}/man1/ldbdel.1.*
%{_mandir}/man1/ldbedit.1.*
%{_mandir}/man1/ldbmodify.1.*
%{_mandir}/man1/ldbrename.1.*
%{_mandir}/man1/ldbsearch.1.*

%changelog
* Tue Mar 23 2021 gaihuiying <gaihuiying1@huawei.com> - 2.0.12-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix tests failed when build with rpmbuild command

* Mon Aug 31 2020 gaihuiying <gaihuiying1@huawei.com> - 2.0.12-1
- Type:requirement
- ID:NA
- SUG:NA
- DESC:update to 2.0.12

* Fri Aug 21 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.0.8-3
- Type:rebuild
- ID:NA
- SUG:NA
- DESC:rebuild for requirement package update

* Fri Mar 20 2020 songnannan <songnannan2@huawei.com> - 2.0.8-2
- add gdb in buildrequires

* Wed Feb 12 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.0.8-1
- Type:update
- ID:NA
- SUG:NA
- DESC:update to 2.0.8

* Thu Dec 26 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.4.2-3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:remove rpath and runpath of exec files and libraries

* Wed Sep 11 2019 liyongqiang<liyongqiang10@huawei.com> - 1.4.2-2
- Package init

