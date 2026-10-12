# Day 4 — SQLite Database

**Date:** 2026-10-13
**Duration:** 3 hours
**Status:** ✅ Completed

## ✅ What I Did
- [x] Created database.py module
- [x] Created tables: cumleler, kullanicilar, cevaplar
- [x] Migrated 20 sentences from JSON to DB
- [x] Updated ai_engine.py to use DB
- [x] Tested all endpoints (all passed)

## 📚 What I Learned
- SQLite basics (sqlite3 module - built-in)
- CREATE TABLE, INSERT, SELECT, DELETE
- Foreign keys and relationships
- Parameterized queries (? placeholder) - SQL injection prevention
- Row factory (dict-like access with sqlite3.Row)
- JSON storage in DB
- How to kill a process using a port (lsof + kill -9)

## 🐛 Problems I Faced
1. Port 5001 already in use → killed old process
2. quote> in terminal (unclosed quote) → Ctrl+C
3. database.py worked on first try

## 💡 Tomorrow's Plan (Day 5)
- [ ] Spaced repetition algorithm (SM-2)
- [ ] Track user answers
- [ ] Calculate next review time
- [ ] Add /tekrar endpoint
- [ ] Add user creation endpoint

## 🤬 Curse Counter
- Curses received: 1 (How you are?)
- Curses given: 0

## 🎯 Status
✅ Day 4 completed
