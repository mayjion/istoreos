include $(TOPDIR)/rules.mk

PKG_NAME:=python3-aiosqlite
PKG_VERSION:=0.19.0
PKG_RELEASE:=1

PYPI_NAME:=aiosqlite
PKG_HASH:=95ee77b91c8d2808bd08a59fbebf66270e9090c3d92ffbf260dc0db0b979577d

PKG_MAINTAINER:=OpenWrt community <community@openwrt.org>
PKG_LICENSE:=Apache-2.0
PKG_LICENSE_FILES:=LICENSE

include $(TOPDIR)/feeds/packages/lang/python/pypi.mk
include $(INCLUDE_DIR)/package.mk

define Package/python3-aiosqlite
	SECTION:=lang
	CATEGORY:=Languages
	SUBMENU:=Python
	TITLE:=asyncio wrapper for sqlite3
	URL:=https://pypi.org/project/aiosqlite/
	DEPENDS:=+python3 +python3-sqlite3
endef

define Package/python3-aiosqlite/description
	aiosqlite is an asynchronous wrapper for sqlite3.
endef

define Build/Compile
endef

define Package/python3-aiosqlite/install
	$(INSTALL_DIR) $(1)$(PYTHON3_PKG_USR_LIB_DIR)
	$(CP) $(PKG_BUILD_DIR)/aiosqlite $(1)$(PYTHON3_PKG_USR_LIB_DIR)/
endef

$(eval $(call BuildPackage,python3-aiosqlite))

