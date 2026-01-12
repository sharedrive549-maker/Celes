[app]
title = Celes

package.name = celes
package.domain = org.celes.ai

source.dir = .
source.include_exts = py,kv,png,jpg,json,ttf

version = 0.1

entrypoint = main.py

requirements = python3,kivy,requests,openai

orientation = portrait
fullscreen = 1

android.permissions = INTERNET,RECORD_AUDIO

android.minapi = 23
android.api = 33
android.archs = arm64-v8a

log_level = 2
