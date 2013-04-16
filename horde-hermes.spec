%define	module	hermes

Name:		horde-%{module}
Version:	1.0.1
Release:	3
Summary:	The Horde file manager
License:	GPL
Group:		System/Servers
URL:		http://www.horde.org/%{module}
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.gz
Requires:	horde >= 3.3.8
BuildArch:	noarch

%description
Hermes is a time-tracking application integrated with the Horde Framework. It
ties into Turba (to retrieve clients) and Nag and Whups (to retrieve cost
objects). It comes with a stop watch, search and reporting capabilities, and an
invoice interface

%prep
%setup -q -n %{module}-h3-%{version}

%build

%install
rm -rf %{buildroot}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration file

<Directory %{_datadir}/horde/%{module}/lib>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
    Order allow,deny
    Deny from all
</Directory>
EOF

# horde configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d
cat > %{buildroot}%{_sysconfdir}/horde/registry.d/%{module}.php <<'EOF'
<?php
//
// Hermes Horde configuration file
//
 
$this->applications['hermes'] = array(
    'fileroot' => $this->applications['horde']['fileroot'] . '/hermes',
    'webroot' => $this->applications['horde']['webroot'] . '/hermes',
    'name' => _("Time Tracking"),
    'status' => 'active',
    'menu_parent' => 'office',
    'provides' => 'time'
);

$this->applications['hermes-stopwatch'] = array(
    'status' => 'block',
    'app' => 'hermes',
    'blockname' => 'tree_stopwatch',
    'menu_parent' => 'hermes',
);

$this->applications['hermes-menu'] = array(
    'status' => 'block',
    'app' => 'hermes',
    'blockname' => 'tree_menu',
    'menu_parent' => 'hermes',
);
EOF

# remove .htaccess files
find . -name .htaccess -exec rm -f {} \;

# install files
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
cp -pR *.php %{buildroot}%{_datadir}/horde/%{module}
cp -pR themes %{buildroot}%{_datadir}/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR scripts %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}

install -d -m 755 %{buildroot}%{_sysconfdir}/horde
pushd %{buildroot}%{_datadir}/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
popd

# activate configuration files
for file in %{buildroot}%{_sysconfdir}/horde/%{module}/*.dist; do
	mv $file ${file%.dist}
done

%clean
rm -rf %{buildroot}

%post
if [ $1 = 1 ]; then
	# configuration
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php apache apache 644
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php.bak apache apache 644
fi
%if %mdkversion < 201010
%_post_webapp
%endif


%files
%defattr(-,root,root)
%doc LICENSE README docs
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}


%changelog
* Sun Aug 08 2010 Thomas Spuhler <tspuhler@mandriva.org> 1.0.1-1mdv2011.0
+ Revision: 567489
- Updated to version 1.0.1
- added version 1.0.1 source file

* Mon Aug 02 2010 Thomas Spuhler <tspuhler@mandriva.org> 1.0-7mdv2011.0
+ Revision: 564910
- Increased release for rebuild

* Mon Jan 18 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-6mdv2010.1
+ Revision: 493345
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise
- restrict default access permissions to localhost only, as per new policy

* Sun Sep 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-4mdv2010.0
+ Revision: 446018
- new setup (simpler is better)

* Wed Aug 19 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-3mdv2010.0
+ Revision: 418309
- fix registry file (fix #52696)

* Wed Nov 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-2mdv2009.1
+ Revision: 304683
- fix automatic dependencies

* Sun Oct 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-1mdv2009.1
+ Revision: 295347
- import horde-hermes


* Sun Oct 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-1mdv2009.1
- first mdv release
