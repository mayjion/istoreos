include $(TOPDIR)/rules.mk

PKG_NAME:=python3-bellows
PKG_VERSION:=0.46.2
PKG_RELEASE:=1

PKG_SOURCE:=bellows-0.46.2.tar.gz
PKG_SOURCE_URL:=https://files.pythonhosted.org/packages/source/b/bellows/
PKG_HASH:=4f0579032c7a8fa16e43da6fe0e1831dbc417b7f9062c5ac51ec89053ef0bc3c
PKG_LICENSE:=GPL-3.0-only
PKG_LICENSE_FILES:=LICENSE

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)
PKG_USE_MIPS16:=0

include $(INCLUDE_DIR)/package.mk

define Package/python3-bellows
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Python3 Bellows Library for EZSP (EmberZNet Serial Protocol)
  URL:=https://github.com/zigpy/bellows
  DEPENDS:=+python3 +python3-zigpy +python3-click +python3-voluptuous +python3-async-timeout
endef

define Package/python3-bellows/description
  Bellows is a Python 3 library implementing the EmberZNet Serial Protocol (EZSP)
  for Silicon Labs Zigbee radios like EFR32MG24.
endef

# 手动提取源 tar.gz
define Build/Prepare
	$(call Build/Prepare/Default)
	$(TAR) -C $(PKG_BUILD_DIR) --strip-components=1 -xzf $(DL_DIR)/$(PKG_SOURCE)
endef

# 空编译：纯 Python
define Build/Compile
endef

# 直接复制源代码到 site-packages
define Package/python3-bellows/install
	$(INSTALL_DIR) $(1)$(PYTHON3_PKG_DIR)
	$(CP) $(PKG_BUILD_DIR)/bellows $(1)$(PYTHON3_PKG_DIR)/
	[ -d $(PKG_BUILD_DIR)/*.egg-info ] && $(CP) $(PKG_BUILD_DIR)/*.egg-info $(1)$(PYTHON3_PKG_DIR)/ || true
endef

$(eval $(call BuildPackage,python3-bellows))
