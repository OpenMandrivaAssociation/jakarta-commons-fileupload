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

Summary:	Jakarta Commons Fileupload Package
Name:		jakarta-%{short_name}
Epoch:	1
Version:	1.2.2
Release:	1
Group:		Development/Java
License:	Apache License
Url:		http://jakarta.apache.org/commons/fileupload/
Source0:	http://www.apache.org/dist/jakarta/commons/fileupload/source/commons-fileupload-1.2.2-src.tar.gz
Patch0:		%{name}-build_xml.patch

%if !%{gcj_support}
BuildArch:	noarch
%else
BuildRequires:	java-gcj-compat-devel
%endif
BuildRequires:	java-rpmbuild >= 0:1.5
BuildRequires:	ant
%if !%{with bootstrap}
BuildRequires:	ant-junit
BuildRequires:	junit >= 0:3.8.1
%endif
BuildRequires:	jakarta-commons-io
BuildRequires:	portlet-1.0-api
BuildRequires:	servlet6
Requires:	servlet6
Provides:	%{short_name} = %{version}-%{release}

%description
The javax.servlet package lacks support for rfc 1867, html file
upload.  This package provides a simple to use api for working with
such data.  The scope of this package is to create a package of Java
utility classes to read multipart/form-data within a
javax.servlet.http.HttpServletRequest

%package        javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description    javadoc
Javadoc for %{name}.

%prep
%setup -qn %{short_name}-%{version}-src
%patch0 -b .build.xml
#patch1 -p0 -b .servletapi5

%build
export CLASSPATH="$(build-classpath commons-io portlet-1.0-api \
    tomcat6-servlet-2.5-api):${PWD}/target/classes:${PWD}/target/test-classes"
%if !%{with bootstrap}
export CLASSPATH="$CLASSPATH:$(build-classpath junit)"
echo $CLASSPATH
%endif

%ant \
	-Dbuild.sysclasspath=only \
	-Dfinal.name=%{name}-%{version} \
%if %{with bootstrap}
	compile jar javadoc
%else
	dist
%endif

%install
# jars
mkdir -p %{buildroot}%{_javadir}
%if %{with bootstrap}
cp -p target/%{name}-%{version}.jar %{buildroot}%{_javadir}
%else
cp -p dist/%{name}-%{version}.jar %{buildroot}%{_javadir}
%endif
(
    cd %{buildroot}%{_javadir} && \
    for jar in *-%{version}*; do
        ln -s -f ${jar} `echo $jar | %{__sed} "s|jakarta-||g"`
    done
)
(
    cd %{buildroot}%{_javadir} && \
    for jar in *-%{version}*; do
        ln -s -f ${jar} `echo $jar | %{__sed} "s|-%{version}||g"`
    done
)
%add_to_maven_depmap %{short_name} %{short_name} %{version} JPP %{short_name}

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# pom
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -m 644 pom.xml %{buildroot}%{_datadir}/maven2/poms/JPP-%{short_name}.pom

# fix end-of-line
sed -i -e 's/\r$//g' *.txt

%gcj_compile

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
%doc LICENSE.txt NOTICE.txt
%{_javadir}/*
%{_datadir}/maven2
%{_mavendepmapfragdir}
%{gcj_files}

%files javadoc
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}


