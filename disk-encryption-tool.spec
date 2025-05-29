#
# spec file for package disk-encryption-tool
#
# Copyright (c) 2025 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#
# icecream 0

Name:           disk-encryption-tool
Version:        0
Release:        0
Summary:        Tool to reencrypt kiwi raw images
License:        MIT
URL:            https://github.com/openSUSE/disk-encryption-tool
Source:         disk-encryption-tool-%{version}.tar
Requires:       bash
Requires:       btrfsprogs
Requires:       coreutils
Requires:       cryptsetup
Requires:       keyutils
Requires:       sed
Requires:       systemd
Requires:       udev
Requires:       util-linux
Requires:       util-linux-systemd
ExclusiveArch:  aarch64 x86_64
BuildArch:      noarch

%description
Convert a plain text kiwi image into one with LUKS full disk
encryption. Supports both raw and qcow2 images. It assumes that the
third partition is the root fs using btrfs.
After encrypting the disk, the fs is mounted and a new initrd
created as well as the grub2 config adjusted.

%package dracut
Summary:        dracut module to reencrypt kiwi raw images
Requires:       %{name} = %{version}-%{release}
Requires:       dracut

%description dracut
dracut module to reencrypt kiwi raw images.

%package mkosi-initrd
Summary:        mkosi-initrd configuration to reencrypt kiwi raw images
Requires:       %{name} = %{version}-%{release}
Requires:       mkosi-initrd

%description mkosi-initrd
mkosi-initrd configuration to reencrypt kiwi raw images.

%prep
%setup -q

%build

%install
# common
install -D -m 0755 disk-encryption-tool %{buildroot}%{_sbindir}/disk-encryption-tool
install -D -m 0755 disk-encryption-tool-initrd %{buildroot}%{_libexecdir}/disk-encryption-tool-initrd
install -D -m 0644 disk-encryption-tool-initrd.service %{buildroot}%{_unitdir}/disk-encryption-tool-initrd.service

# dracut
install -D -m 0755 module-setup.sh %{buildroot}%{_prefix}/lib/dracut/modules.d/95disk-encryption-tool/module-setup.sh

# mkosi-initrd
install -D -m 0644 mkosi.conf %{buildroot}%{_prefix}/lib/mkosi-initrd/mkosi.conf.d/95-disk-encryption-tool.conf
install -D -m 0644 mkosi-extra.conf %{buildroot}%{_prefix}/lib/mkosi-initrd/mkosi.conf.d/95-disk-encryption-tool-options.conf
install -D -m 0644 mkosi.preset %{buildroot}%{_prefix}/lib/mkosi-initrd/mkosi.extra/usr/lib/systemd/system-preset/95-disk-encryption-tool.preset

%files
%license LICENSE
%doc README.md
%{_sbindir}/disk-encryption-tool
%{_libexecdir}/disk-encryption-tool-initrd
%{_unitdir}/disk-encryption-tool-initrd.service

%files dracut
%dir %{_prefix}/lib/dracut
%dir %{_prefix}/lib/dracut/modules.d
%{_prefix}/lib/dracut/modules.d/95disk-encryption-tool

%files mkosi-initrd
%dir %{_prefix}/lib/mkosi-initrd
%dir %{_prefix}/lib/mkosi-initrd/mkosi.conf.d
%{_prefix}/lib/mkosi-initrd/mkosi.conf.d/95-disk-encryption-tool.conf
%{_prefix}/lib/mkosi-initrd/mkosi.conf.d/95-disk-encryption-tool-options.conf
%dir %{_prefix}/lib/mkosi-initrd/mkosi.extra
%dir %{_prefix}/lib/mkosi-initrd/mkosi.extra/usr
%dir %{_prefix}/lib/mkosi-initrd/mkosi.extra/usr/lib
%dir %{_prefix}/lib/mkosi-initrd/mkosi.extra/usr/lib/systemd
%dir %{_prefix}/lib/mkosi-initrd/mkosi.extra/usr/lib/systemd/system-preset
%{_prefix}/lib/mkosi-initrd/mkosi.extra/usr/lib/systemd/system-preset/95-disk-encryption-tool.preset

%changelog
