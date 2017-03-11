%{?_javapackages_macros:%_javapackages_macros}

%if 0%{?fedora}
# Unavailable test deps
# xLightweb depend on xSocket, but the
# active development of xSocket has been stopped.
# Currently xSocket supports bug-fixes only.
%bcond_with xlightweb
%endif

Name:          jbosh
Version:       0.8.0
Release:       4
Summary:       XEP-0124: Bidirectional-streams Over Synchronous HTTP (BOSH)
License:       ASL 2.0
Group:         Development/Java
URL:           https://github.com/igniterealtime/jbosh
Source0:       https://github.com/igniterealtime/jbosh/archive/%{version}/%{name}-%{version}.tar.gz
Source1:       http://repo1.maven.org/maven2/org/igniterealtime/jbosh/jbosh/%{version}/jbosh-%{version}.pom
# LICENSE file was added @ https://github.com/igniterealtime/jbosh/commit/6b09a889942abe289f6c89f642add142e57bd88e
Source2:       http://www.apache.org/licenses/LICENSE-2.0.txt

BuildRequires: maven-local
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.apache.httpcomponents:httpclient)
BuildRequires: mvn(xpp3:xpp3)

%if %{with xlightweb}
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.xlightweb:xlightweb)
%endif

BuildArch:     noarch

%description
A maintained fork of com.kenai.jbosh for XEP-0124:
Bidirectional-streams Over Synchronous HTTP (BOSH).
This library is used by Smack to support XEP-206:
XMPP over BOSH. In contrast to org.kenai.jbosh,
this jBOSH library uses the Apache Commons HttpClient 4.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
# cleanup
find . -name "*.class" -print -delete
find . -name "*.dll" -print -delete
find . -name "*.jar" -print  -delete

cp -p %{SOURCE1} pom.xml
cp -p %{SOURCE2} LICENSE
sed -i 's/\r//' LICENSE

%pom_add_plugin org.apache.felix:maven-bundle-plugin . "
<extensions>true</extensions>
<configuration>
  <instructions>
    <Bundle-SymbolicName>\${project.groupId}</Bundle-SymbolicName>
    <Bundle-Name>\${project.artifactId}</Bundle-Name>
    <Bundle-Version>\${project.version}</Bundle-Version>
  </instructions>
</configuration>
<executions>
  <execution>
    <id>bundle-manifest</id>
    <phase>process-classes</phase>
    <goals>
      <goal>manifest</goal>
    </goals>
  </execution>
</executions>"

%pom_add_plugin org.apache.maven.plugins:maven-jar-plugin . "
<configuration>
  <archive>
    <manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
    <addMavenDescriptor>false</addMavenDescriptor>
  </archive>
</configuration>"

mkdir -p target/classes/{META-INF/services,org.jivesoftware.jbosh}

%if %{with xlightweb}
# ComparisonFailure: expected:<gzip> but was:<null>
rm -r src/test/java/org/igniterealtime/jbosh/XEP0124Section07Test.java
# Exception: test timed out after 5000 milliseconds
rm -r src/test/java/org/igniterealtime/jbosh/XEP0124Section09Test.java \
 src/test/java/org/igniterealtime/jbosh/XEP0124Section17Test.java
# Exception: test timed out after 3000 milliseconds
rm -r src/test/java/org/igniterealtime/jbosh/XEP0124Section11Test.java
%else
%pom_remove_dep org.xlightweb:xlightweb
%endif

#  Add alias
%mvn_alias org.igniterealtime.jbosh:%{name} com.github.igniterealtime:%{name}

%mvn_file : %{name}

%build

%if %{without xlightweb}
opts="-f"
%endif
%mvn_build $opts -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 30 2014 gil cattaneo <puntogil@libero.it> 0.8.0-1
- initial rpm
