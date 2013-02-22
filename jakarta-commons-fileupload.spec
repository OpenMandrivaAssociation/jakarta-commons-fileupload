# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%bcond_without	bootstrap
%define gcj_support	0
%define base_name fileupload
%define short_name commons-%{base_name}
%define section free

Name:           jakarta-%{short_name}
Epoch:          1
Version:        1.2.1
Release:        2.0.10
Summary:        Jakarta Commons Fileupload Package

Group:          Development/Java
License:        Apache License
URL:            http://jakarta.apache.org/commons/fileupload/
Source0:        http://www.apache.org/dist/jakarta/commons/fileupload/source/commons-fileupload-%{version}-src.tar.gz
Patch0:         %{name}-build_xml.patch

BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  ant
%if !%{with bootstrap}
BuildRequires:  ant-junit
BuildRequires:  junit >= 0:3.8.1
%endif
BuildRequires:  jakarta-commons-io
BuildRequires:  portlet-1.0-api
BuildRequires:  servlet6
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
Requires:       servlet6
Provides:       %{short_name}

%description
The javax.servlet package lacks support for rfc 1867, html file
upload.  This package provides a simple to use api for working with
such data.  The scope of this package is to create a package of Java
utility classes to read multipart/form-data within a
javax.servlet.http.HttpServletRequest

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{short_name}-%{version}-src
%patch0 -b .build.xml
#patch1 -p0 -b .servletapi5

%build
export CLASSPATH="$(build-classpath commons-io portlet-1.0-api \
    tomcat6-servlet-2.5-api):${PWD}/target/classes:${PWD}/target/test-classes"
%if !%{with bootstrap}
export CLASSPATH="$CLASSPATH:$(build-classpath junit)"
echo $CLASSPATH
%endif

%{ant} \
    -Dbuild.sysclasspath=only \
    -Dfinal.name=%{name}-%{version} \
%if %{with bootstrap}
    compile jar javadoc
%else
    dist
%endif

%install
%{__rm} -rf $RPM_BUILD_ROOT

# jars
%{__mkdir} -p $RPM_BUILD_ROOT%{_javadir}
%if %{with bootstrap}
%{__cp} -p target/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
%else
%{__cp} -p dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
%endif
(
    cd $RPM_BUILD_ROOT%{_javadir} && \
    for jar in *-%{version}*; do
        %{__ln_s} -f ${jar} `echo $jar | %{__sed} "s|jakarta-||g"`
    done
)
(
    cd $RPM_BUILD_ROOT%{_javadir} && \
    for jar in *-%{version}*; do
        %{__ln_s} -f ${jar} `echo $jar | %{__sed} "s|-%{version}||g"`
    done
)
%add_to_maven_depmap %{short_name} %{short_name} %{version} JPP %{short_name}

# javadoc
%{__mkdir} -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -m 644 pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{short_name}.pom

# fix end-of-line
%{__perl} -pi -e 's/\r$//g' *.txt

%{gcj_compile}

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt NOTICE.txt
%{_javadir}/*
%{_datadir}/maven2
%{_mavendepmapfragdir}
%{gcj_files}

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}


%changelog
* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.1-2.0.5mdv2011.0
+ Revision: 606054
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.1-2.0.4mdv2010.1
+ Revision: 522971
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1:1.2.1-2.0.3mdv2010.0
+ Revision: 425435
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 1:1.2.1-2.0.2mdv2009.1
+ Revision: 351276
- rebuild

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 1:1.2.1-2.0.1mdv2009.0
+ Revision: 264716
- rebuild early 2009.0 package (before pixel changes)

* Sun May 25 2008 Alexander Kurtakov <akurtakov@mandriva.org> 1:1.2.1-0.0.1mdv2009.0
+ Revision: 211135
- new version

* Thu Feb 21 2008 Alexander Kurtakov <akurtakov@mandriva.org> 1:1.1.1-3.0.1mdv2008.1
+ Revision: 173428
- fix requires
- new version

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sun Sep 16 2007 Anssi Hannula <anssi@mandriva.org> 1:1.0-5.5mdv2008.0
+ Revision: 87978
- use macros for rebuild-gcj-db

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 1:1.0-5.4mdv2008.0
+ Revision: 87408
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sun Sep 09 2007 Pascal Terjan <pterjan@mandriva.org> 1:1.0-5.3mdv2008.0
+ Revision: 82853
- rebuild


* Thu Mar 15 2007 Christiaan Welvaart <spturtle@mandriva.org> 1.0-5.2mdv2007.1
+ Revision: 143917
- rebuild for 2007.1
- Import jakarta-commons-fileupload

* Sun Jul 23 2006 David Walluck <walluck@mandriva.org> 1:1.0-5.1mdv2006.0
- bump release

* Fri Jun 02 2006 David Walluck <walluck@mandriva.org> 1:1.0-3.4mdv2006.0
- rebuild for libgcj.so.7

* Thu Dec 22 2005 David Walluck <walluck@mandriva.org> 1:1.0-3.3mdk
- export OPT_JAR_LIST

* Fri Nov 11 2005 David Walluck <walluck@mandriva.org> 1:1.0-3.2mdk
- aot compile

* Sun May 22 2005 David Walluck <walluck@mandriva.org> 1:1.0-3.1mdk
- release

* Sat Oct 23 2004 Fernando Nasser <fnasser@redhat.com> - 1:1.0-3jpp
- Patch to build with servletapi5
- Add missing dependency on ant-junit

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 1:1.0-2jpp
- Rebuild with ant-1.6.2

