#
# Copyright (C) 2025 OpenWrt.org
#
include $(TOPDIR)/rules.mk

PKG_NAME:=aic8800-firmware
PKG_VERSION:=1.0
PKG_RELEASE:=1

PKG_MAINTAINER:=Your Name <your.email@example.com>
PKG_LICENSE:=Proprietary

include $(INCLUDE_DIR)/package.mk

define Package/aic8800-firmware
  SECTION:=firmware
  CATEGORY:=Firmware
  TITLE:=AIC8800 Wi-Fi and Bluetooth Firmware
  DEPENDS:=
endef

define Package/aic8800-firmware/description
  Firmware files for the AIC8800 Wi-Fi and Bluetooth chipset.
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	$(CP) ./files/* $(PKG_BUILD_DIR)/
endef

define Build/Compile
	# Nothing to compile, just firmware
endef

define Package/aic8800-firmware/install
	$(INSTALL_DIR) $(1)/lib/firmware/aic8800
	$(CP) $(PKG_BUILD_DIR)/*.bin $(PKG_BUILD_DIR)/*.txt $(1)/lib/firmware/aic8800/
endef

$(eval $(call BuildPackage,aic8800-firmware))