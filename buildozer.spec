[app]

title = Programa Cobros
package.name = programacobros
package.domain = org.nexus
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0

# Librerías exactas que utiliza tu main.py
requirements = python3,kivy,kivymd,plyer,openpyxl,sqlite3

p4a.branch = master

orientation = portrait
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
