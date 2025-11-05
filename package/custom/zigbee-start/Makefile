include $(TOPDIR)/rules.mk

PKG_NAME:=zigbee-start
PKG_VERSION:=1.0
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/zigbee-start
	SECTION:=utils
	CATEGORY:=Utilities
	TITLE:=Zigbee Start Script
	DEPENDS:=+python3-zigpy
	PKGARCH:=all
endef

define Package/zigbee-start/description
	Startup script for zigpy Zigbee application.
endef

define Build/Compile
endef

define Package/zigbee-start/install
	$(INSTALL_DIR) $(1)/root
	$(INSTALL_BIN) ./files/zigbee_start.py $(1)/root/zigbee_start.py
	$(INSTALL_DIR) $(1)/etc/init.d
	echo '#!/bin/sh /etc/rc.common' > $(1)/etc/init.d/zigbee
	echo 'START=99' >> $(1)/etc/init.d/zigbee
	echo 'PYTHONPATH=/zigpy /root/zigbee_start.py &' >> $(1)/etc/init.d/zigbee
	chmod 755 $(1)/etc/init.d/zigbee
endef

$(eval $(call BuildPackage,zigbee-start))
