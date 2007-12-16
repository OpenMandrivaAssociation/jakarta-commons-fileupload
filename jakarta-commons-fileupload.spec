%define gcj_support	1
%define base_name       fileupload
%define short_name      commons-%{base_name}
%define name            jakarta-%{short_name}
%define version         1.0
%define section         free

Name:           %{name}
Version:        %{version}
Release:        %mkrel 5.6
Summary:        Jakarta Commons Fileupload Package
License:        Apache License
Group:          Development/Java
#Vendor:         JPackage Project
#Distribution:   JPackage
Epoch:          1
Source0:        http://www.apache.org/dist/jakarta/commons/fileupload/source/commons-fileupload-%{version}-src.tar.bz2
Patch0:         %{name}-crosslink.patch
Patch1:         %{name}-servletapi5.patch
URL:            http://jakarta.apache.org/commons/fileupload/
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  junit >= 0:3.8.1
BuildRequires:  servlet24
BuildRequires:  servletapi5-javadoc
Requires:       servletapi5
%if %{gcj_support}
BuildRequires:	java-gcj-compat
%else
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides:       %{short_name}
Obsoletes:      %{short_name}

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

# -----------------------------------------------------------------------------

%prep
%setup -q -n %{short_name}-%{version}
%patch0 -p0
%patch1 -p0

# -----------------------------------------------------------------------------

%build
export CLASSPATH="$(build-classpath servletapi5 junit \
jakarta-commons-beanutils):$PWD/target/classes:$PWD/target/test-classes"
export OPT_JAR_LIST="ant/ant-junit"

%ant \
  -Dbuild.sysclasspath=only \
  -Dfinal.name=%{name}-%{version} \
  -Dservletapi.javadoc=%{_javadocdir}/servletapi5 \
  dist

# -----------------------------------------------------------------------------

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

# fix end-of-line
%{__perl} -pi -e 's/\r$//g' *.txt

%if %{gcj_support}
aot-compile-rpm
%endif

# -----------------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT

# -----------------------------------------------------------------------------

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
  rm -f %{_javadocdir}/%{name}
fi

# -----------------------------------------------------------------------------

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt
%{_javadir}/*
%if %{gcj_support}
%{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

# -----------------------------------------------------------------------------


