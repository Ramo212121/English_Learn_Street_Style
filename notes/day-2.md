# Day 2 — Groq Integration

**Date:** 2026-10-11
**Duration:** 2 hours
**Status:** ✅ Completed

## ✅ What I Did
- [x] Got Groq API key from console.groq.com
- [x] Added it to .env file
- [x] Added .env to .gitignore
- [x] Ran: pip install groq
- [x] Replaced ai_engine.py with Groq version
- [x] Changed model to openai/gpt-oss-120b
- [x] Added max_completion_tokens=512 and reasoning_effort="low"
- [x] Changed Flask port to 5001 (AirPlay uses 5000)
- [x] Tested with curl (4 different tests)

## 📚 What I Learned
- What an LLM is (Large Language Model)
- How to use the Groq API
- What a "system prompt" is
- What "temperature" means (0-1 creativity)
- What "max_completion_tokens" means
- What "reasoning_effort" means
- How to securely store API keys with .env
- How load_dotenv() and os.getenv() work
- Why macOS AirPlay uses port 5000 (conflict with Flask)
- How to kill a process using a port (lsof, kill -9)

## 🐛 Problems I Faced
1. venv + conda conflict → deleted .venv, use only conda
2. Groq model deprecated (llama-3.3-70b-versatile) → switched to openai/gpt-oss-120b
3. Empty AI response → added max_completion_tokens + reasoning_effort
4. Port 5000 used by AirTunes → switched to port 5001
5. Port already in use → killed old Flask process with lsof + kill

## 💡 Tomorrow's Plan (Day 3)
- [ ] Expand to 20 sentences for Day 1
- [ ] Add day system endpoint (/gun/<int:gun>)
- [ ] Add sentence categories (greeting, introduction, farewell)
- [ ] Add variations for each sentence

## 🤬 Curse Counter
- Curses received: 2 (wrong sentence + off-topic question)
- Curses given: 1 (correct sentence)

## 🎯 Status
✅ Day 2 completed