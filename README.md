# Python Internship Tasks - Datheon

Four beginner-friendly Python projects (standard library only).

| # | Task | Run |
|---|------|-----|
| 1 | Hangman (ASCII art, 6 attempts, duplicate-guess protection) | `python task1_hangman/hangman.py` |
| 2 | File Organizer (auto category folders, collision + permission handling) | `python task2_file_organizer/organizer.py [folder] [--dry-run]` |
| 3 | Rule-based Chatbot (keywords + regex, fallback, exit commands) | `python task3_chatbot/chatbot.py` |
| 4 | Portfolio Tracker (P/L per holding, CSV log) | `python task4_portfolio_tracker/portfolio.py` |

## Notes
- Requires Python 3.8+. Task 4 optionally uses `yfinance` for live prices (`pip install yfinance`); otherwise it falls back to `sample_prices.csv`.
- Task 1 uses `words.txt` (10k English word list); Task 4 validates tickers using `constituents.csv` (S&P 500).
- Task 3 also answers extra questions from `sample_faq.json`.
- Tip: run Task 2 with `--dry-run` first to preview.
