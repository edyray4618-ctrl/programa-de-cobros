[app]

# (str) Title of your application
title = Programa Cobros

# (str) Package name
package.name = programacobros

# (str) Package domain (needed for android/ios packaging)
package.domain = org.nexus

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy

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

# (list) Architectures to build for (solo 64 bits para evitar fallos de compilacion)
android.archs = arm64-v8a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
