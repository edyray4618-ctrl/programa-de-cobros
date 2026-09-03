[app]

# (str) Title of your application
title = Programa Cobros

# (str) Package name
package.name = programacobros

# (str) Package domain
package.domain = org.nexus

# (str) Source code directory
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 1.0.0

# (list) Application requirements (Forzar Python 3.11 estable)
requirements = hostpython3==3.11.5,python3==3.11.5,kivy

# (str) Supported orientation
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API supported
android.minapi = 21

# (str) NDK version
android.ndk = 25b

# (bool) Accept SDK license agreement
android.accept_sdk_license = True

# (list) Architectures to build for
android.archs = arm64-v8a

[buildozer]

# (int) Log level
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
