include $(TOPDIR)/rules.mk

PKG_NAME:=python3-crccheck
PKG_VERSION:=1.3.1
PKG_RELEASE:=1

PYPI_NAME:=crccheck
PKG_HASH:=1544c0110bf0a697d875d4f29dc40d7079f9d4d402a9317383f55f90ca72563a

PKG_MAINTAINER:=OpenWrt community <community@openwrt.org>
PKG_LICENSE:=MIT
PKG_LICENSE_FILES:=LICENSE

include $(TOPDIR)/feeds/packages/lang/python/pypi.mk
include $(INCLUDE_DIR)/package.mk

define Package/python3-crccheck
	SECTION:=lang
	CATEGORY:=Languages
	SUBMENU:=Python
	TITLE:=Python CRC Checksum library
	URL:=https://pypi.org/project/crccheck/
	DEPENDS:=+python3
endef

define Package/python3-crccheck/description
	crccheck is a Python library for checksums and error-correcting codes.
endef

define Build/Compile
	cd $(PKG_BUILD_DIR); $(STAGING_DIR_HOSTPKG)/bin/python3 -m build --no-isolation --wheel --outdir $(PKG_BUILD_DIR)/dist
endef

define Package/python3-crccheck/install
	$(INSTALL_DIR) $(1)$(PYTHON3_PKG_USR_LIB_DIR)
	$(CP) $(PKG_BUILD_DIR)/build/lib/crccheck $(1)$(PYTHON3_PKG_USR_LIB_DIR)/
endef

$(eval $(call BuildPackage,python3-crccheck))
