%global pkg_name nekohtml
%{?scl:%scl_package %{pkg_name}}
%{?java_common_find_provides_and_requires}

# Copyright (c) 2000-2009, JPackage Project
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

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.9.14
Release:        13.14%{?dist}
Epoch:          0
Summary:        HTML scanner and tag balancer
License:        ASL 2.0
URL:            http://nekohtml.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{pkg_name}/%{pkg_name}-%{version}.tar.gz
# http://www.jpackage.org/cgi-bin/viewvc.cgi/*checkout*/rpms/devel/nekohtml/nekohtml-filter.sh?root=jpackage&content-type=text%2Fplain
Source1:        %{pkg_name}-filter.sh
Source2:        nekohtml-component-info.xml
Source3:        http://repo1.maven.org/maven2/net/sourceforge/nekohtml/nekohtml/1.9.14/nekohtml-1.9.14.pom
Patch0:         %{pkg_name}-crosslink.patch
Patch1:         %{pkg_name}-jars.patch
# Add proper attributes to MANIFEST.MF file so bundle can be used by other OSGI bundles.
Patch2:         %{pkg_name}-osgi.patch
Requires:       %{?scl_prefix}bcel
Requires:       %{?scl_prefix}javapackages-tools >= 0:1.6
Requires:       %{?scl_prefix}xerces-j2 >= 0:2.7.1
Requires:       %{?scl_prefix}xml-commons-apis
BuildRequires:  %{?scl_prefix}javapackages-tools
BuildRequires:  %{?scl_prefix}ant
BuildRequires:  %{?scl_prefix}ant-junit
BuildRequires:  %{?scl_prefix}bcel
BuildRequires:  %{?scl_prefix}bcel-javadoc
BuildRequires:  %{?scl_prefix}xerces-j2 >= 0:2.7.1
BuildRequires:  %{?scl_prefix}xerces-j2-javadoc
BuildRequires:  %{?scl_prefix}xml-commons-apis
BuildArch:      noarch

%description
NekoHTML is a simple HTML scanner and tag balancer that enables
application programmers to parse HTML documents and access the
information using standard XML interfaces. The parser can scan HTML
files and "fix up" many common mistakes that human (and computer)
authors make in writing HTML documents.  NekoHTML adds missing parent
elements; automatically closes elements with optional end tags; and
can handle mismatched inline element tags.
NekoHTML is written using the Xerces Native Interface (XNI) that is
the foundation of the Xerces2 implementation. This enables you to use
the NekoHTML parser with existing XNI tools without modification or
rewriting code.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
Javadoc for %{pkg_name}.

%package demo
Summary:        Demo for %{pkg_name}
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%patch0 -p1
%patch1 -p1
%patch2
find . -name "*.jar" | xargs -t %{__rm}
%{__perl} -pi -e 's/\r$//g' *.txt doc/*.html
%{__rm} -r doc/javadoc
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
export CLASSPATH=$(build-classpath bcel xerces-j2)
%{ant} \
    -Dbuild.sysclasspath=first \
    -Dlib.dir=%{_javadir} \
    -Djar.file=%{pkg_name}.jar \
    -Djar.xni.file=%{pkg_name}-xni.jar \
    -Djar.samples.file=%{pkg_name}-samples.jar \
    -Dbcel.javadoc=%{_javadocdir}/bcel \
    -Dj2se.javadoc=%{_javadocdir}/java \
    -Dxni.javadoc=%{_javadocdir}/xerces-j2-xni \
    -Dxerces.javadoc=%{_javadocdir}/xerces-j2-impl \
    clean jar jar-xni doc 
# test - disabled because it makes the build failing
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
# Jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 644 %{pkg_name}{,-samples,-xni}.jar $RPM_BUILD_ROOT%{_javadir}/

# Scripts
install -Dpm 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/%{pkg_name}-filter

# POM
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{pkg_name}.pom
%add_maven_depmap -a nekohtml:nekohtml

# Javadocs
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -a build/doc/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE.txt README.txt doc/*.html
%attr(755,root,root) %{_bindir}/%{pkg_name}-filter
%{_javadir}/%{pkg_name}-xni.jar

%files javadoc
%{_javadocdir}/%{name}

%files demo
%{_javadir}/%{pkg_name}-samples.jar

%changelog
* Fri Jan 16 2015 Mat Booth <mat.booth@redhat.com> - 0:1.9.14-13.14
- Add osgi manifest patch from Fedora

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 0:1.9.14-13.13
- Mass rebuild 2015-01-13

* Fri Jan 09 2015 Michal Srb <msrb@redhat.com> - 0:1.9.14-13.12
- Mass rebuild 2015-01-09

* Wed Jan 07 2015 Michal Srb <msrb@redhat.com> - 1.9.14-13.11
- Migrate to .mfiles

* Tue Dec 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.14-13.10
- Migrate requires and build-requires to rh-java-common

* Mon Dec 15 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.14-13.9
- Mass rebuild 2014-12-15

* Mon Dec 15 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.14-13.8
- Rebuild for rh-java-common collection

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.14-13.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.14-13.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.14-13.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.14-13.4
- Remove requires on java

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.14-13.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.14-13.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.14-13.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 01.9.14-13
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.14-12
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.9.14-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.14-10
- Add addiotional depmap

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.9.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Bill Nottingham <notting@redhat.com> 0:1.9.14-7
- Update buildreqs to packages that currently exist

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.9.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 1 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.9.14-6
- Adapt to current guidelines.

* Mon Oct 10 2011 Andy Grimm <agrimm@gmail.com> - 0:1.9.14-5
- Add POM file (BZ #735521)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.9.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 6 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.9.14-3
- Drop gcj support and rpeolib.

* Mon Jul 19 2010 James Laska <jlaska@redhat.com> 0:1.9.14-2
- Disable gcj_support
- Updated nekohtml-jars.patch

* Mon Jul 15 2010 James Laska <jlaska@redhat.com> 0:1.9.14-1
- Update to 1.9.14

* Wed May 13 2009 Martha Benitez <mbenitez@redhat.com> 0:1.9.11-2.2
- Build without aot-compile

* Thu Mar 19 2009 David Walluck <dwalluck@redhat.com> 0:1.9.11-2.1
- BuildRequires: bcel
- force use of xalan-j2

* Wed Feb 11 2009 David Walluck <dwalluck@redhat.com> 0:1.9.11-2
- add repolib

* Wed Feb 11 2009 David Walluck <dwalluck@redhat.com> 0:1.9.11-1
- 1.9.6.1

* Mon Feb 12 2007 Jeff Johnston <jjohnstn@redhat.com> - 0:0.9.5-4jpp.1
- Update to address Fedora review comments.

* Mon May 08 2006 Ralph Apel <r.apel at r-apel.de> - 0:0.9.5-4jpp
- First JPP-1.7 release

* Tue Oct 11 2005 Ralph Apel <r.apel at r-apel.de> - 0:0.9.5-3jpp
- Patch to JAXP13

* Mon Aug  1 2005 Ville SkyttÃ¤ <scop at jpackage.org> - 0:0.9.5-2jpp
- Fix unversioned xni jar symlink (#10).

* Wed Jul  6 2005 Ville SkyttÃ¤ <scop at jpackage.org> - 0:0.9.5-1jpp
- 0.9.5.

* Wed Dec 15 2004 Ville SkyttÃ¤ <scop at jpackage.org> - 0:0.9.4-1jpp
- Update to 0.9.4.

* Tue Aug 24 2004 Fernando Nasser <fnasser@redhat.com> - 0:0.9.3-2jpp
- Rebuild with Ant 1.6.2

* Sat Jul  3 2004 Ville SkyttÃ¤ <scop at jpackage.org> - 0:0.9.3-1jpp
- Update to 0.9.3.
- Add nekohtml-filter script.

* Thu Apr  1 2004 Ville SkyttÃ¤ <scop at jpackage.org> - 0:0.9.2-1jpp
- Update to 0.9.2.

* Sat Dec 13 2003 Ville SkyttÃ¤ <scop at jpackage.org> - 0:0.8.3-1jpp
- Update to 0.8.3.

* Sat Nov 15 2003 Ville SkyttÃ¤ <scop at jpackage.org> - 0:0.8.2-1jpp
- Update to 0.8.2.

* Wed Oct  1 2003 Ville SkyttÃ¤ <scop at jpackage.org> - 0:0.8.1-1jpp
- Update to 0.8.1.
- Crosslink with local J2SE and XNI javadocs.
- Save .spec in UTF-8.

* Thu Jun 26 2003 Ville SkyttÃ¤ <scop at jpackage.org> - 0:0.7.7-1jpp
- Update to 0.7.7.

* Sun May 11 2003 David Walluck <david@anti-microsoft.org> 0:0.7.6-1jpp
- 0.7.6
- update for JPackage 1.5

* Sat Mar 29 2003 Ville SkyttÃ¤ <scop at jpackage.org> - 0.7.4-2jpp
- Rebuilt for JPackage 1.5.

* Tue Mar  4 2003 Ville SkyttÃ¤ <scop at jpackage.org> - 0.7.4-1jpp
- Update to 0.7.4.

* Mon Feb 24 2003 Ville SkyttÃ¤ <scop at jpackage.org> - 0.7.3-1jpp
- Update to 0.7.3.
- Built with IBM's 1.3.1 SR3 and xerces-j2 2.3.0.

* Sat Jan 11 2003 Ville SkyttÃ¤ <scop at jpackage.org> - 0.7.2-1jpp
- Update to 0.7.2.
- Run unit tests when building.

* Tue Dec 10 2002 Ville SkyttÃ¤ <scop at jpackage.org> - 0.7.1-1jpp
- Update to 0.7.1.

* Sun Nov  3 2002 Ville SkyttÃ¤ <scop at jpackage.org> - 0.6.8-1jpp
- 0.6.8, first JPackage release.
