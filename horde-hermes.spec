%define	module	hermes
%define	name	horde-%{module}
%define version 1.0
%define release %mkrel 2

%define _requires_exceptions pear(Horde.*)

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	The Horde file manager
License:	GPL
Group:		System/Servers
URL:		http://www.horde.org/%{module}
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.gz
Requires(post):	rpm-helper
Requires:	horde >= 3.0
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

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

# horde configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d
cat > %{buildroot}%{_sysconfdir}/horde/registry.d/%{module}.php <<'EOF'
<?php
//
// Hermes Horde configuration file
//
 
$this->applications['hermes'] = array(
    'fileroot' => \$this->applications['horde']['fileroot'] . '/hermes',
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
install -d -m 755 %{buildroot}%{_var}/www/horde/%{module}
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
install -d -m 755 %{buildroot}%{_sysconfdir}/horde
cp -pR *.php %{buildroot}%{_var}/www/horde/%{module}
cp -pR themes %{buildroot}%{_var}/www/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR scripts %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}

# use symlinks to recreate original structure
pushd %{buildroot}%{_var}/www/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
ln -s ../../../..%{_datadir}/horde/%{module}/lib .
ln -s ../../../..%{_datadir}/horde/%{module}/locale .
ln -s ../../../..%{_datadir}/horde/%{module}/templates .
popd
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

%files
%defattr(-,root,root)
%doc LICENSE README docs
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}
%{_var}/www/horde/%{module}

