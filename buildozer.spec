[app]
title = My Music Player
package.name = mymusicplayer
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3
version = 0.1
requirements = Cython==0.29.33,python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 23b
android.accept_sdk_license = True
android.entrypoint = org.kivy.android.PythonActivity
android.apptheme = "@android:style/Theme.NoTitleBar"
p4a.branch = master
