# ⚔️ Goal Quest - Gamified Habit Tracking

A Solo Leveling-inspired gamified habit tracking app with AI-powered features.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Claude AI](https://img.shields.io/badge/Claude_AI-191919?style=for-the-badge&logo=anthropic&logoColor=white)

## ✨ Features

- 🔥 **Habit Tracking** with streaks and XP rewards
- 🎯 **AI-Powered Goals** with auto-generated action steps
- 🤖 **AI Difficulty Assessment** - no manual difficulty selection
- 📊 **16 Life Categories** (Fitness, Learning, Finance, Spiritual, etc.)
- 📈 **6 Character Stats**: Strength, Intelligence, Vitality, Agility, Sense, Willpower
- 🏪 **In-Game Shop** with items and boosts
- 📖 **Daily Wisdom** from 6 philosophy traditions
- 🤖 **AI Life Coach** for personalized guidance
- 💾 **SQLite Database** for persistent storage

---

## 🚀 Deploy to Streamlit Cloud (FREE)

### Step 1: Fork/Upload to GitHub

1. Create a new GitHub repository
2. Upload these files:
   ```
   your-repo/
   ├── app.py
   ├── requirements.txt
   ├── .gitignore
   ├── README.md
   └── .streamlit/
       ├── config.toml
       └── secrets.toml.example
   ```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Connect your GitHub account
4. Select your repository
5. Set **Main file path**: `app.py`
6. Click **"Deploy!"**

### Step 3: Add Your API Key (IMPORTANT!)

1. In Streamlit Cloud, go to your app's **Settings**
2. Click **"Secrets"**
3. Add your Anthropic API key:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-your-actual-api-key-here"
   ```
4. Click **"Save"**

Your app will automatically restart with AI features enabled!

---

## 🔐 Keeping Your API Key Secret

### ❌ NEVER do this:
- Commit `secrets.toml` to GitHub
- Put API keys directly in `app.py`
- Share your API key publicly

### ✅ ALWAYS do this:
- Use Streamlit Cloud's Secrets management
- Keep `secrets.toml` in `.gitignore`
- Use environment variables for local development

---

## 💻 Run Locally

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# 1. Clone your repo
git clone https://github.com/YOUR_USERNAME/goal-quest.git
cd goal-quest

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create secrets file
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# 5. Edit secrets.toml and add your API key
# (Use any text editor)

# 6. Run the app
streamlit run app.py
```

Open http://localhost:8501 in your browser!

---

## 🎮 How It Works

### XP & Leveling System
- Complete habits → Earn XP
- XP needed per level: `100 × level^1.5`
- Streak bonuses: +10% XP per day (capped at 100%)

### 6 Character Stats
| Stat | Abbr | Boosted By |
|------|------|-----------|
| Strength | STR | Fitness habits |
| Intelligence | INT | Learning, Career |
| Vitality | VIT | Health habits |
| Agility | AGI | Productivity |
| Sense | SEN | Finance, Awareness |
| Willpower | WIL | Mindfulness, Spiritual |

### Difficulty Levels
| Level | Stars | XP Range |
|-------|-------|----------|
| Trivial | ⭐ | 25-50 |
| Easy | ⭐⭐ | 50-100 |
| Medium | ⭐⭐⭐ | 100-200 |
| Hard | ⭐⭐⭐⭐ | 200-400 |
| Expert | ⭐⭐⭐⭐⭐ | 400-600 |
| Legendary | ⭐⭐⭐⭐⭐⭐ | 600-1000 |

### Evolution Tiers
| Tier | Level Range |
|------|-------------|
| Novice Adventurer | 1-10 |
| Skilled Warrior | 11-25 |
| Elite Champion | 26-50 |
| Master Guardian | 51-75 |
| Legendary Hero | 76-99 |
| Shadow Monarch | 100+ |

---

## 🤖 AI Features

All AI features use **Claude** by Anthropic:

1. **Auto Difficulty Assessment**
   - Analyzes habit descriptions
   - Assigns difficulty, category, XP, target stat
   - Provides personalized tips

2. **Goal Step Generation**
   - Creates 7-10 actionable steps
   - Estimates timelines
   - Suggests supporting habits

3. **Document Analysis**
   - Extracts habits from text
   - Identifies goals
   - Pulls memorable quotes

4. **AI Coach Chat**
   - Personalized guidance
   - Context-aware responses
   - Motivational support

---

## 📁 File Structure

```
GoalQuest_Streamlit/
├── app.py                 # Main application (single file)
├── requirements.txt       # Python dependencies
├── .gitignore            # Files to ignore in git
├── README.md             # This file
└── .streamlit/
    ├── config.toml       # Streamlit theme config
    └── secrets.toml.example  # API key template
```

---

## 🛠️ Troubleshooting

### "AI features not working"
- Check that your API key is set in Streamlit Cloud Secrets
- Verify the key starts with `sk-ant-`
- Make sure you have API credits

### "Database resets on redeploy"
- Streamlit Cloud doesn't persist SQLite files
- For production, consider using a cloud database
- Local development keeps data in `goal_quest.db`

### "App won't load"
- Check the Streamlit Cloud logs
- Verify `requirements.txt` is correct
- Make sure `app.py` is the main file

---

## 🔮 Future Enhancements

- [ ] Cloud database integration (PostgreSQL/Supabase)
- [ ] User authentication
- [ ] Social features (leaderboards, challenges)
- [ ] Mobile-responsive improvements
- [ ] PDF document import
- [ ] Voice input for habits

---

## 📜 License

MIT License - Feel free to use, modify, and distribute.

---

## 🙏 Credits

- Built with [Streamlit](https://streamlit.io)
- AI powered by [Anthropic Claude](https://anthropic.com)
- Inspired by Solo Leveling manhwa

---

**Happy Questing!** ⚔️🎮
