%global debug_package %{nil}

%define vtag %(echo "$(curl -s https://api.github.com/repos/wez/wezterm/releases/latest | grep tag_name | cut -d \\" -f 4)")

Name:    wezterm
Version: %(echo "$(tr '-' '_' <<< %{vtag})")
Release: 1%{?dist}
Summary: WezTerm - a GPU-accelerated cross-platform terminal emulator and multiplexer written by @wez and implemented in Rust
Group:   System Environment/Shells
License: MIT
URL:     https://github.com/wez/%{name}
Source0: https://github.com/wez/%{name}/releases/download/%{vtag}/%{name}-%{vtag}-src.tar.gz
BuildRequires: desktop-file-utils
BuildRequires: rust
BuildRequires: cargo
BuildRequires: gcc-c++
BuildRequires: openssl-devel 
BuildRequires: wayland-devel
BuildRequires: egl-wayland-devel
BuildRequires: xorg-x11-server-Xwayland-devel
BuildRequires: libX11-devel
BuildRequires: libxkbcommon-devel
BuildRequires: libxkbcommon-x11-devel
BuildRequires: xcb-util-devel
BuildRequires: xcb-util-keysyms-devel
BuildRequires: xcb-util-wm-devel
BuildRequires: xcb-util-image-devel
BuildRequires: libpng-devel
BuildRequires: mesa-libEGL-devel
BuildRequires: dbus-devel
BuildRequires: fontconfig-devel
Requires: dbus, fontconfig, openssl, libxcb, libxkbcommon, libxkbcommon-x11, libwayland-client, libwayland-egl, libwayland-cursor, mesa-libEGL, xcb-util-keysyms, xcb-util-wm, xcb-util-image
%description
A GPU-accelerated cross-platform terminal emulator and multiplexer written by @wez and implemented in Rust
%prep
%setup -q -c
%build
export TAG_NAME=%{vtag}
export TAGNAME=%{vtag}
export WEZTERM_CI_TAG=%{vtag}
mv wezterm-$TAG_NAME/* .
mv wezterm-$TAG_NAME/.tag .
cp .tag ../
rm -rf wezterm-$TAG_NAME
ls -al
cargo build --all --release --features distro-defaults
# cargo build --all --release
%install
# Prepare asset files
set -x
mkdir -p %{buildroot}/etc/profile.d
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_metainfodir}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
mkdir -p %{buildroot}/usr/bin %{buildroot}/etc/profile.d
install -Dm755 assets/open-wezterm-here -t %{buildroot}/usr/bin
install -Dsm755 target/release/wezterm -t %{buildroot}/usr/bin
install -Dsm755 target/release/wezterm-mux-server -t %{buildroot}/usr/bin
install -Dsm755 target/release/wezterm-gui -t %{buildroot}/usr/bin
install -Dsm755 target/release/strip-ansi-escapes -t %{buildroot}/usr/bin
install -Dm644 assets/shell-integration/* -t %{buildroot}/etc/profile.d
install -Dm644 assets/shell-completion/zsh %{buildroot}/usr/share/zsh/site-functions/_wezterm
install -Dm644 assets/shell-completion/bash %{buildroot}/etc/bash_completion.d/wezterm
install -Dm644 assets/icon/terminal.png %{buildroot}/usr/share/icons/hicolor/128x128/apps/org.wezfurlong.wezterm.png
install -Dm644 assets/wezterm.desktop %{buildroot}/usr/share/applications/org.wezfurlong.wezterm.desktop
install -Dm644 assets/wezterm.appdata.xml %{buildroot}/usr/share/metainfo/org.wezfurlong.wezterm.appdata.xml
install -Dm644 assets/wezterm-nautilus.py %{buildroot}/usr/share/nautilus-python/extensions/wezterm-nautilus.py
%check
desktop-file-validate %{buildroot}/usr/share/applications/org.wezfurlong.wezterm.desktop
%files
%defattr(-,root,root,-)
%license LICENSE.md
%doc README.md
/usr/bin/open-wezterm-here
/usr/bin/wezterm
/usr/bin/wezterm-gui
/usr/bin/wezterm-mux-server
/usr/bin/strip-ansi-escapes
/usr/share/zsh/site-functions/_wezterm
/etc/bash_completion.d/wezterm
/usr/share/icons/hicolor/128x128/apps/org.wezfurlong.wezterm.png
/usr/share/applications/org.wezfurlong.wezterm.desktop
/usr/share/metainfo/org.wezfurlong.wezterm.appdata.xml
/usr/share/nautilus-python/extensions/wezterm-nautilus.py*
/etc/profile.d/*

%changelog %{vtag} 
* Mon Apr 24 2023 Stefan Maaßen <stefan.maassen@posteo.de> - %{vtag}
- built current release
