[app]

# (str) Title of your application
title = Video Editor

# (str) Package name
package.name = videoeditor

# (str) Package domain (needed for android/ios packaging)
package.domain = com.yourname

# (str) Source code where the main.py lives
source.dir = src

# (list) Source files to include (let everything)
source.include_exts = py,png,jpg,kv,atlas,txt

# (list) Application requirements
requirements = python3,kivy,moviepy,numpy,Pillow,android

# (str) Application versioning
version = 0.1

# (str) Presplash of the application
presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/data/icon.png

# (list) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (int) Android API to use
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android NDK version to use
android.ndk = 23b

# (bool) Enable AndroidX support
android.enable_androidx = True

# (str) Android SDK directory (if not set, buildozer will download)
# android.sdk = 20

# (str) Android NDK directory (if not set, buildozer will download)
# android.ndk = 

# (str) Android ANT directory (if not set, buildozer will download)
# android.ant = 

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (str) Path to build artifact in the bin directory (format = 'app-{version}-{debug/release}.apk')
warn_on_root = 1