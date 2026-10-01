[app]
title = PixelMed Studio
package.name = pixelmedstudio
package.domain = com.pixelmed.studio

source.dir =.
source.include_exts = py,png,jpg,kv,atlas,ico,ttf
source.include_patterns = image/*,*.ttf

version = 1.0
requirements = hostpython3==3.11.9,python3==3.11.9,kivy==2.3.0,pillow,pyjnius,android,arabic-reshaper,python-bidi

orientation = portrait
fullscreen = 0

# ايقوناتك الجديدة
icon.filename = %(source.dir)s/image/icon.png
presplash.filename = %(source.dir)s/image/icmd.png
presplash.color = #87CEEB

# نفس الصلاحيات اللي اشتغلت معك + زيادة للصور
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,CHANGE_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_MEDIA_IMAGES

# نفس اعداداتك القديمة المضمونة
android.api = 33
android.minapi = 21
android.sdk = 33
android.build_tools_version = 33.0.2
android.ndk = 25b
android.accept_sdk_license_agreements = True
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.request_legacy_external_storage = True
android.manifest.application_attributes = android:usesCleartextTraffic="true"

p4a.branch = v2024.01.21
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1