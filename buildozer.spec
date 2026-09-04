[app]

title = Programa Cobros
package.name = programacobros
package.domain = org.nexus
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0

# Usamos la combinación probada para p4a y Android 14/15:
requirements = python3,kivy,kivymd==1.2.0,materialyoucolor,plyer,openpyxl,sqlite3,pillow

p4a.branch = develop

orientation = portrait
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# Compatibilidad con Android 14/15
android.api = 34
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
