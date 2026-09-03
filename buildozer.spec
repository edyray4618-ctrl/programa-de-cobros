[app]

title = Programa Cobros
package.name = programacobros
package.domain = org.nexus
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0

# Usamos la versión estable de KivyMD sin la dependencia problematica de materialyoucolor
requirements = python3,kivy==2.2.1,https://github.com/kivymd/KivyMD/archive/1.2.0.zip,plyer,openpyxl,sqlite3,pillow

p4a.branch = master

orientation = portrait
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

android.api = 34
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
