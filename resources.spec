%bcond_without check

# Not packaged: crate(nparse/default) = 0.0.4
%global crates_io_deps 1

%global gtk4_version 4.10.0
%global libadwaita_version 1.6.0

%global tarball_version %%(echo %{version} | tr '~' '.')

Name:           resources
Version:        1.10.2
Release:        1%{?dist}
Summary:        Monitor your system resources and processes

License:        GPL-3.0-or-later
# LICENSE.dependencies contains a full license breakdown
URL:            https://github.com/nokyan/resources
# the given path has multiple possibilities: #<Git::Ref:0x00007fcb13731050>, #<Git::Ref:0x00007fcb13730b50>
%dnl Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  /usr/bin/appstream-util
BuildRequires:  /usr/bin/desktop-file-validate
BuildRequires:  cargo-rpm-macros
BuildRequires:  git-core
BuildRequires:  itstool
BuildRequires:  meson
BuildRequires:  pkgconfig(gtk4) >= %{gtk4_version}
BuildRequires:  pkgconfig(libadwaita-1) >= %{libadwaita_version}

Requires:       dmidecode
Requires:       hicolor-icon-theme
Requires:       polkit

%description
Resources is a simple yet powerful monitor for your system resources and
processes, written in Rust and using GTK 4 and libadwaita for its GUI. It's
capable of displaying usage and details of your CPU, memory, GPUs, network
interfaces and block devices. It's also capable of listing and terminating
running graphical applications as well as processes.


%prep
%autosetup -p1
%if ! 0%{?crates_io_deps}
echo "With crates.io deps"
%cargo_prep
%generate_buildrequires
%cargo_generate_buildrequires
%endif


%build
%meson \
    -Dprofile=default \
%meson_build

%if ! 0%{?crates_io_deps}
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
%endif


%install
%meson_install
%find_lang %{name} --with-gnome


%check
%if %{with check}
%meson_test
%endif

appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files -f %{name}.lang
%license LICENSE
%if ! 0%{?crates_io_deps}
%license LICENSE.dependencies
%endif
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/symbolic/apps/*-symbolic.svg
%{_datadir}/polkit-1/actions/net.nokyan.Resources.policy
%{_libexecdir}/%{name}/%{name}-*
%{_metainfodir}/*.metainfo.xml


%changelog
* Tue  May 5 2026 Rafał Rosner <kontakt@rafi67000.xyz> - 1.10.2-1
- chore: Update to latest release

* Sat Mar 29 2025 Artem Polishchuk <ego.cordatus@gmail.com> - 1.8.0-1
- chore: Update to latest release

* Mon Dec 09 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.7.1-1
- chore: Update to latest release

* Sun Dec 01 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.7.0-1
- chore: Update to latest release

* Sun Jul 07 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.5.1-1
- chore: Update to latest releaseT

* Sun Jun 23 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.5.0-1
- chore: Update to latest release

* Sun Apr 14 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.0-1
- chore: Update to latest release

* Mon Feb 26 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.3.0-2
- build: Switch to default profile

* Sun Dec 24 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.3.0-1
- chore: Update to latest release

* Tue Oct 31 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.2.0-1
- Update to latest version

* Mon Oct 16 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.1.0-1
- Initial
