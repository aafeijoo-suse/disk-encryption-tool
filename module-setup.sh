#!/bin/bash

# called by dracut
check() {
	require_binaries \
		blkid \
		btrfs \
		cat \
		cryptsetup \
		dd \
		findmnt \
		getopt \
		keyctl \
		kill \
		mkdir \
		mkswap \
		mktemp \
		mount \
		mountpoint \
		partx \
		readlink \
		sed \
		sfdisk \
		tac \
		udevadm \
		umount \
		|| return 1

	return 0
}

# called by dracut
depends() {
	echo "crypt"
	return 0
}

# called by dracut
installkernel() {
	# for systemd credentials via smbios
	instmods dmi_sysfs
}

# called by dracut
install() {
	inst_multiple \
		"$systemdsystemunitdir"/disk-encryption-tool-initrd.service \
		/usr/libexec/disk-encryption-tool-initrd \
		disk-encryption-tool \
		blkid \
		btrfs \
		cat \
		cryptsetup \
		dd \
		findmnt \
		getopt \
		keyctl \
		kill \
		mkdir \
		mkswap \
		mktemp \
		mount \
		mountpoint \
		partx \
		readlink \
		sed \
		sfdisk \
		tac \
		udevadm \
		umount

	$SYSTEMCTL -q --root "$initdir" enable disk-encryption-tool-initrd.service

	: "${ENCRYPTION_CONFIG:=/etc/encrypt_options}"
	[ -e "$ENCRYPTION_CONFIG" ] && inst_simple "$ENCRYPTION_CONFIG" "/etc/encrypt_options"
}
