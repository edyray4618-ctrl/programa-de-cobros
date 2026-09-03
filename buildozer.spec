[app]

title = Programa Cobros
package.name = programacobros
package.domain = org.nexus
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0

requirements = python3,kivy

p4a.branch = v2024.01.21

orientation = portrait
android.permissions = INTERNET

# Modificado a 31 para compatibilidad perfecta con Gradle
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
