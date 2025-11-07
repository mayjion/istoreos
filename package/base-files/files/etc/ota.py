#!/usr/bin/env python3
import os
import json
import time
import hashlib
import requests
import jwt
import subprocess

# ==== 基本配置 ====
APP_ID = 2238607
INSTALLATION_ID = 93175630
PRIVATE_KEY_PATH = "/rom/etc/myfirmwareupdater.2025-11-05.private-key.pem"
OWNER = "mayjion"
REPO = "ota"

INDEX_FILE = "index.json"
LOCAL_AUTH_CACHE = "/boot/.authorized_devices.json"
VERSION_FILE = "/rom/etc/version"
TMP_FW_PATH = "/tmp/new_firmware.bin"
CHECK_INTERVAL = 300  # 每5分钟检测一次
SALT = "MySecretSalt1234"

# ==== 工具函数 ====
def get_mac(interface="eth0"):
    """获取设备MAC"""
    try:
        with open(f"/sys/class/net/{interface}/address", "r") as f:
            return f.read().strip().upper().replace(":", "")
    except:
        return None

def md5sum(file_path):
    """计算文件MD5"""
    h = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def reboot_system():
    print("⚠️ 授权无效，系统将在5秒后重启...")
    time.sleep(5)
    os.system("reboot")

# ==== GitHub访问 ====
def get_installation_token():
    """生成 GitHub Installation Token"""
    with open(PRIVATE_KEY_PATH, "r") as f:
        private_key = f.read()

    payload = {
        "iat": int(time.time()) - 60,
        "exp": int(time.time()) + (10 * 60),
        "iss": APP_ID
    }
    jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }

    url = f"https://api.github.com/app/installations/{INSTALLATION_ID}/access_tokens"
    r = requests.post(url, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()["token"]

def get_remote_json(token, file_path):
    """从 GitHub 获取 JSON 文件"""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{file_path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.raw"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return json.loads(r.text)
        else:
            print(f"❌ 无法访问 {file_path}: {r.status_code}")
            return None
    except requests.RequestException as e:
        print(f"🌐 网络错误: {e}")
        return None

# ==== 授权逻辑 ====
def update_local_auth_cache(data):
    """更新本地授权缓存"""
    try:
        with open(LOCAL_AUTH_CACHE, "w") as f:
            json.dump(data, f)
        print(f"💾 已更新本地授权缓存: {LOCAL_AUTH_CACHE}")
    except Exception as e:
        print("⚠️ 无法写入本地授权缓存:", e)

def load_local_auth_cache():
    """加载本地授权缓存"""
    if not os.path.exists(LOCAL_AUTH_CACHE):
        print("⚠️ 本地授权缓存不存在")
        return None
    try:
        with open(LOCAL_AUTH_CACHE, "r") as f:
            return json.load(f)
    except Exception as e:
        print("⚠️ 无法读取本地授权缓存:", e)
        return None

def check_authorization(token):
    """从云端验证授权，无网时回退本地"""
    mac = get_mac("eth0")
    if not mac:
        print("❌ 无法获取MAC地址")
        return False

    data = get_remote_json(token, "authorized_devices.json")
    if data:
        update_local_auth_cache(data)
    else:
        print("🌐 无法连接云端，使用本地授权缓存")
        data = load_local_auth_cache()
        if not data:
            print("❌ 无法验证授权（无网络且无缓存）")
            return False

    authorized = data.get("devices", [])
    for dev in authorized:
        if dev.get("mac", "").upper() == mac:
            print("✅ 授权验证通过")
            return True

    print("❌ 当前设备未被授权")
    return False

# ==== 版本管理 ====
def get_local_version():
    """读取本地版本信息"""
    try:
        with open(VERSION_FILE, "r") as f:
            data = json.load(f)
        return {"model": data.get("model"), "version": data.get("version")}
    except Exception as e:
        print("❌ 读取本地版本失败:", e)
        return None

def download_file(url, path):
    """下载文件"""
    try:
        r = requests.get(url, stream=True, timeout=120)
        if r.status_code == 200:
            with open(path, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            print(f"📦 固件下载完成: {path}")
            return True
        else:
            print(f"❌ 下载失败，状态码 {r.status_code}")
            return False
    except requests.RequestException as e:
        print("🌐 下载异常:", e)
        return False

def perform_sysupgrade(firmware_path):
    """执行 sysupgrade"""
    print("⚙️ 开始系统升级...")
    try:
        subprocess.run(["sysupgrade", firmware_path], check=True)
    except subprocess.CalledProcessError as e:
        print("❌ 系统升级失败:", e)

def check_for_update(local, remote_index, token):
    """检查更新并执行升级"""
    model = local["model"]
    gateway_data = remote_index.get("gateway", {})
    if model not in gateway_data:
        print(f"❌ 未在 index.json 中找到型号 {model}")
        return

    version_url = gateway_data[model]["version_file"]
    version_path = version_url.split("main/")[-1]
    remote_info = get_remote_json(token, version_path)
    if not remote_info:
        print("🌐 无法获取远程版本信息")
        return

    remote_ver = remote_info.get("version", "")
    checksum = remote_info.get("checksum", "")
    ctype = remote_info.get("checksum_type", "md5")
    fw_url = remote_info.get("url", "")

    if not fw_url:
        print("❌ 远程文件缺少 url 字段")
        return

    if remote_ver != local["version"]:
        print(f"⬆️ 检测到新版本 {remote_ver} (当前 {local['version']})")
        if download_file(fw_url, TMP_FW_PATH):
            # 校验文件
            if ctype.lower() == "md5":
                file_md5 = md5sum(TMP_FW_PATH)
                if file_md5 != checksum:
                    print(f"❌ MD5 校验失败: {file_md5} != {checksum}")
                    return
            print("✅ 校验通过，执行 sysupgrade")
            perform_sysupgrade(TMP_FW_PATH)
        else:
            print("❌ 固件下载失败")
    else:
        print("✅ 当前已是最新版本")

# ==== 主循环 ====
def main_loop():
    while True:
        print("\n===== OTA 检查开始 =====")

        # 获取 GitHub Token
        try:
            token = get_installation_token()
        except Exception as e:
            print("🌐 无法获取 GitHub Token:", e)
            print("💤 等待下次检测...")
            time.sleep(CHECK_INTERVAL)
            continue

        # 授权校验
        if not check_authorization(token):
            reboot_system()
            return

        # 获取 index.json
        remote_index = get_remote_json(token, INDEX_FILE)
        if not remote_index:
            print("🌐 无法获取 index.json，跳过此次检测")
            time.sleep(CHECK_INTERVAL)
            continue

        # 获取本地版本
        local_version = get_local_version()
        if not local_version:
            print("❌ 无法读取本地版本信息")
            time.sleep(CHECK_INTERVAL)
            continue

        # 检查更新
        check_for_update(local_version, remote_index, token)

        print("===== 检查结束，等待下次执行 =====")
        time.sleep(CHECK_INTERVAL)

# ==== 启动 ====
if __name__ == "__main__":
    main_loop()
