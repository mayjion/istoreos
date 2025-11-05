include $(TOPDIR)/rules.mk

PKG_NAME:=python3-zigpy
PKG_VERSION:=0.85.0
PKG_RELEASE:=1

PYPI_NAME:=zigpy
PKG_HASH:=8c4a1dec729e3a76be184e7b88af9dce87ef802ccf0a2e5d81ee2800c8eae449

PKG_MAINTAINER:=OpenWrt community <community@openwrt.org>
PKG_LICENSE:=GPL-3.0-or-later
PKG_LICENSE_FILES:=LICENSE

PKG_BUILD_DIR:=$(BUILD_DIR)/pypi/$(PYPI_NAME)-$(PKG_VERSION)

include $(TOPDIR)/feeds/packages/lang/python/pypi.mk
include $(INCLUDE_DIR)/package.mk

define Build/Prepare
	$(call Build/Prepare/Default)
	sed -i 's/from typing import Self//g' $(PKG_BUILD_DIR)/zigpy/types/basic.py
	sed -i 's/Self/object/g' $(PKG_BUILD_DIR)/zigpy/types/basic.py
endef

define Package/python3-zigpy
	SECTION:=lang
	CATEGORY:=Languages
	SUBMENU:=Python
	TITLE:=Zigbee Protocol Stack for Python
	URL:=https://github.com/zigpy/zigpy
	DEPENDS:=+python3 +python3-pyserial +python3-cryptography
endef

define Package/python3-zigpy/description
	A pure-python implementation of the Zigbee radio protocol.
endef

define Build/Compile
	cd $(PKG_BUILD_DIR); $(STAGING_DIR_HOSTPKG)/bin/python3 setup.py build
endef

define Package/python3-zigpy/install
	$(INSTALL_DIR) $(1)$(PYTHON3_PKG_USR_LIB_DIR)
	$(CP) $(PKG_BUILD_DIR)/build/lib/zigpy $(1)$(PYTHON3_PKG_USR_LIB_DIR)/zigpy/
endef

$(eval $(call BuildPackage,python3-zigpy))
