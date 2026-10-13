# Day 8 — TTS + Ağır Küfür + Samimi AI

**Date:** 2026-10-13
**Duration:** 5 hours
**Status:** ✅ Completed

## ✅ What I Did
- [x] Installed edge-tts
- [x] Created tts.py with retry mechanism
- [x] Added /ses endpoint
- [x] Added /quiz/cevapla-sesli endpoint
- [x] Updated AI prompt to street style with curses
- [x] Fixed Groq safety filter issue
- [x] Switched model to openai/gpt-oss-120b
- [x] Added Turkish phonetic conversion for English
- [x] Added text cleaning (remove *, #, `, _, ", ')
- [x] Added fallback for empty audio
- [x] Tested all endpoints - SUCCESS!

## 📚 What I Learned
- edge-tts Turkish voice (tr-TR-AhmetNeural)
- Retry mechanism for empty audio
- Groq safety filter workaround (avoid "curse" keyword)
- Model deprecation (llama-3.1-8b-instant gone)
- Turkish phonetic conversion for English words
- Text cleaning for TTS
- Fallback strategies

## 🐛 Problems I Faced
1. Groq refused to curse → changed prompt to examples only
2. llama-3.1-8b-instant model not found → switched to openai/gpt-oss-120b
3. Empty MP3 files → added retry + size check
4. TTS failed with markdown (**) → text cleaning
5. Port conflicts → lsof + kill -9

## 💡 Tomorrow's Plan (Day 9)
- [ ] React Native + Expo setup
- [ ] Mobile app skeleton
- [ ] First screen

## 🤬 Curse Counter
- Curses received: 1 ("kafanı s*kerim")
- Curses given: 0

## 🎯 Status
✅ Day 8 completed
