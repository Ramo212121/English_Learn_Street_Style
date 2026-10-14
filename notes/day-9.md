# Day 9 — React Native + Expo

**Date:** 2026-10-14
**Duration:** 4 hours
**Status:** ✅ Completed

## ✅ What I Did
- [x] Created Expo project (fuckinEnglishApp)
- [x] Installed expo-router, axios, react-native-web, expo-av
- [x] Created 5 screens: index, quiz, sohbet, istatistik, _layout
- [x] Created api/client.ts with auto IP detection
- [x] Added CORS to Flask
- [x] Flask runs on 0.0.0.0
- [x] Tested on phone (Expo Go) - WORKS
- [x] Tested on web (browser) - WORKS
- [x] Added sound playback to quiz
- [x] Fixed kufur_sayisi bug

## 📚 What I Learned
- Expo project structure
- expo-router (file-based navigation)
- React Native components (View, Text, TextInput, ScrollView)
- StyleSheet for styling
- Axios for API calls
- CORS (needed for web)
- Flask host='0.0.0.0' for network access
- Platform.OS detection (web vs mobile)
- expo-av for audio playback
- Constants.expoConfig.hostUri for auto IP

## 🐛 Problems I Faced
1. adaptive-icon.png missing → removed from app.json
2. expo-router plugin error → installed expo-router
3. axios not installed → installed
4. API connection failed → CORS + host='0.0.0.0'
5. IP changed (192.168.100.223 → 192.168.0.218) → updated client.ts
6. kufur_sayisi was incrementing on every wrong → removed line
7. Quiz no sound → added expo-av
8. `cat >` vs `cat |` confusion in terminal

## 💡 Tomorrow's Plan (Day 10)
- [ ] Better styling
- [ ] AI-powered answer checking
- [ ] Expanded variations
- [ ] More quiz features

## 🎯 Status
✅ Day 9 completed
