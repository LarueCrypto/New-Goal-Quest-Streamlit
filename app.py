"""
🎮 GOAL QUEST - Gamified Habit Tracking App
Streamlit Version with Full AI Integration
Solo Leveling Inspired Dark Theme

Deploy from GitHub to Streamlit Cloud
"""

import streamlit as st
import sqlite3
import json
import hashlib
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple, Any
import os

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION & THEME
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Goal Quest",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Solo Leveling dark theme
CUSTOM_CSS = """
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(180deg, #0A0A0A 0%, #111111 100%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0A0A0A;
        border-right: 1px solid #1A1A1A;
    }
    
    /* Cards */
    .quest-card {
        background: #1A1A1A;
        border: 1px solid #252525;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        transition: all 0.3s ease;
    }
    .quest-card:hover {
        border-color: #D4AF37;
        transform: translateY(-2px);
    }
    
    /* Gold accent text */
    .gold-text {
        color: #D4AF37 !important;
        font-weight: 600;
    }
    
    /* XP Progress bar */
    .xp-bar {
        background: #252525;
        border-radius: 6px;
        height: 12px;
        overflow: hidden;
    }
    .xp-fill {
        background: linear-gradient(90deg, #D4AF37 0%, #F4D03F 100%);
        height: 100%;
        border-radius: 6px;
        transition: width 0.5s ease-out;
    }
    
    /* Stat boxes */
    .stat-box {
        background: #1A1A1A;
        border: 1px solid #252525;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    
    /* Streak fire */
    .streak-badge {
        background: linear-gradient(135deg, #F97316 0%, #EF4444 100%);
        padding: 4px 12px;
        border-radius: 12px;
        color: white;
        font-weight: 600;
    }
    
    /* Difficulty badges */
    .diff-trivial { background: rgba(156, 163, 175, 0.2); color: #9CA3AF; }
    .diff-easy { background: rgba(34, 197, 94, 0.2); color: #22C55E; }
    .diff-medium { background: rgba(59, 130, 246, 0.2); color: #3B82F6; }
    .diff-hard { background: rgba(245, 158, 11, 0.2); color: #F59E0B; }
    .diff-expert { background: rgba(239, 68, 68, 0.2); color: #EF4444; }
    .diff-legendary { background: rgba(168, 85, 247, 0.2); color: #A855F7; }
    
    /* Category colors */
    .cat-fitness { border-left: 4px solid #EF4444; }
    .cat-health { border-left: 4px solid #22C55E; }
    .cat-learning { border-left: 4px solid #3B82F6; }
    .cat-career { border-left: 4px solid #6366F1; }
    .cat-finance { border-left: 4px solid #F59E0B; }
    .cat-creative { border-left: 4px solid #EC4899; }
    .cat-mindfulness { border-left: 4px solid #A855F7; }
    .cat-productivity { border-left: 4px solid #F97316; }
    .cat-social { border-left: 4px solid #06B6D4; }
    .cat-personal { border-left: 4px solid #FBBF24; }
    .cat-spiritual { border-left: 4px solid #8B5CF6; }
    .cat-home { border-left: 4px solid #84CC16; }
    .cat-environment { border-left: 4px solid #10B981; }
    .cat-relationships { border-left: 4px solid #F472B6; }
    .cat-life_goals { border-left: 4px solid #D4AF37; }
    .cat-skills { border-left: 4px solid #64748B; }
    
    /* Rarity glows */
    .rarity-common { border: 1px solid #9CA3AF; }
    .rarity-uncommon { border: 2px solid #22C55E; box-shadow: 0 0 10px rgba(34, 197, 94, 0.3); }
    .rarity-rare { border: 2px solid #3B82F6; box-shadow: 0 0 15px rgba(59, 130, 246, 0.4); }
    .rarity-epic { border: 2px solid #A855F7; box-shadow: 0 0 20px rgba(168, 85, 247, 0.5); }
    .rarity-legendary { border: 2px solid #F59E0B; box-shadow: 0 0 25px rgba(245, 158, 11, 0.6); }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
        color: #000000;
        border: none;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        color: #D4AF37;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS & GAME DATA
# ═══════════════════════════════════════════════════════════════════════════════

CATEGORIES = {
    "fitness": {"name": "Fitness", "emoji": "💪", "color": "#EF4444"},
    "health": {"name": "Health", "emoji": "❤️", "color": "#22C55E"},
    "learning": {"name": "Learning", "emoji": "🧠", "color": "#3B82F6"},
    "career": {"name": "Career", "emoji": "💼", "color": "#6366F1"},
    "finance": {"name": "Finance", "emoji": "💰", "color": "#F59E0B"},
    "creative": {"name": "Creative", "emoji": "🎨", "color": "#EC4899"},
    "mindfulness": {"name": "Mindfulness", "emoji": "🧘", "color": "#A855F7"},
    "productivity": {"name": "Productivity", "emoji": "⚡", "color": "#F97316"},
    "social": {"name": "Social", "emoji": "👥", "color": "#06B6D4"},
    "personal": {"name": "Personal", "emoji": "🌟", "color": "#FBBF24"},
    "spiritual": {"name": "Spiritual", "emoji": "🙏", "color": "#8B5CF6"},
    "home": {"name": "Home", "emoji": "🏠", "color": "#84CC16"},
    "environment": {"name": "Environment", "emoji": "🌍", "color": "#10B981"},
    "relationships": {"name": "Relationships", "emoji": "💑", "color": "#F472B6"},
    "life_goals": {"name": "Life Goals", "emoji": "🎯", "color": "#D4AF37"},
    "skills": {"name": "Skills", "emoji": "🔧", "color": "#64748B"},
}

DIFFICULTIES = {
    1: {"name": "Trivial", "color": "#9CA3AF", "xp_range": (25, 50), "stars": 1},
    2: {"name": "Easy", "color": "#22C55E", "xp_range": (50, 100), "stars": 2},
    3: {"name": "Medium", "color": "#3B82F6", "xp_range": (100, 200), "stars": 3},
    4: {"name": "Hard", "color": "#F59E0B", "xp_range": (200, 400), "stars": 4},
    5: {"name": "Expert", "color": "#EF4444", "xp_range": (400, 600), "stars": 5},
    6: {"name": "Legendary", "color": "#A855F7", "xp_range": (600, 1000), "stars": 6},
}

STATS = {
    "strength": {"name": "Strength", "abbr": "STR", "emoji": "⚔️", "color": "#EF4444"},
    "intelligence": {"name": "Intelligence", "abbr": "INT", "emoji": "🧠", "color": "#3B82F6"},
    "vitality": {"name": "Vitality", "abbr": "VIT", "emoji": "❤️", "color": "#22C55E"},
    "agility": {"name": "Agility", "abbr": "AGI", "emoji": "⚡", "color": "#F59E0B"},
    "sense": {"name": "Sense", "abbr": "SEN", "emoji": "👁️", "color": "#A855F7"},
    "willpower": {"name": "Willpower", "abbr": "WIL", "emoji": "🔥", "color": "#EC4899"},
}

TIERS = {
    1: {"name": "Novice Adventurer", "level_range": (1, 10), "color": "#9CA3AF"},
    2: {"name": "Skilled Warrior", "level_range": (11, 25), "color": "#22C55E"},
    3: {"name": "Elite Champion", "level_range": (26, 50), "color": "#3B82F6"},
    4: {"name": "Master Guardian", "level_range": (51, 75), "color": "#A855F7"},
    5: {"name": "Legendary Hero", "level_range": (76, 99), "color": "#F59E0B"},
    6: {"name": "Shadow Monarch", "level_range": (100, 999), "color": "#EF4444"},
}

RARITIES = {
    "common": {"name": "Common", "color": "#9CA3AF"},
    "uncommon": {"name": "Uncommon", "color": "#22C55E"},
    "rare": {"name": "Rare", "color": "#3B82F6"},
    "epic": {"name": "Epic", "color": "#A855F7"},
    "legendary": {"name": "Legendary", "color": "#F59E0B"},
}

PHILOSOPHY_TRADITIONS = {
    "stoic": {"name": "Stoicism", "emoji": "🏛️"},
    "biblical": {"name": "Biblical", "emoji": "✝️"},
    "eastern": {"name": "Eastern", "emoji": "☯️"},
    "samurai": {"name": "Samurai", "emoji": "⚔️"},
    "hermetic": {"name": "Hermetic", "emoji": "🔮"},
    "quranic": {"name": "Quranic", "emoji": "☪️"},
}


# ═══════════════════════════════════════════════════════════════════════════════
# AI SERVICE
# ═══════════════════════════════════════════════════════════════════════════════

class AIService:
    """AI Service using Anthropic Claude API"""
    
    def __init__(self):
        self.api_key = self._get_api_key()
        self.client = None
        if self.api_key:
            self._init_client()
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from Streamlit secrets or environment"""
        try:
            return st.secrets["ANTHROPIC_API_KEY"]
        except:
            return os.environ.get("ANTHROPIC_API_KEY", "")
    
    def _init_client(self):
        """Initialize Anthropic client"""
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            st.warning("⚠️ Anthropic package not installed. AI features will use fallback logic.")
        except Exception as e:
            st.warning(f"⚠️ Could not initialize AI: {e}")
    
    def is_available(self) -> bool:
        return self.client is not None
    
    def assess_habit_difficulty(self, habit_description: str, user_stats: Dict = None) -> Dict:
        """AI-powered difficulty assessment for habits"""
        if not self.is_available():
            return self._fallback_difficulty(habit_description)
        
        prompt = f"""Analyze this habit and assess its difficulty. Return ONLY valid JSON.

Habit: "{habit_description}"

User's current stats: {json.dumps(user_stats) if user_stats else "New user"}

Return this exact JSON structure:
{{
    "difficulty": <1-6 integer>,
    "difficulty_name": "<Trivial|Easy|Medium|Hard|Expert|Legendary>",
    "xp_reward": <integer 25-1000>,
    "category": "<fitness|health|learning|career|finance|creative|mindfulness|productivity|social|personal|spiritual|home|environment|relationships|life_goals|skills>",
    "target_stat": "<strength|intelligence|vitality|agility|sense|willpower>",
    "time_estimate": "<X minutes|X hours>",
    "tip": "<helpful personalized tip for building this habit>",
    "reasoning": {{
        "time_factor": <1-5>,
        "mental_effort": <1-5>,
        "physical_effort": <1-5>,
        "skill_required": <1-5>,
        "consistency_need": <1-5>
    }}
}}

Difficulty scale:
1 = Trivial: <5 min, no prep (drink water, make bed)
2 = Easy: 5-15 min, minimal effort (quick stretch, gratitude)
3 = Medium: 15-30 min, focus needed (meditation, reading)
4 = Hard: 30-60 min, significant effort (workout, study)
5 = Expert: 1+ hour, high commitment (deep work, training)
6 = Legendary: Major undertaking (marathon training, mastery)"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            result_text = response.content[0].text.strip()
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
            return json.loads(result_text)
        except Exception as e:
            st.warning(f"AI analysis failed: {e}")
            return self._fallback_difficulty(habit_description)
    
    def _fallback_difficulty(self, habit_description: str) -> Dict:
        """Fallback difficulty assessment"""
        desc_lower = habit_description.lower()
        
        # Keyword-based assessment
        if any(kw in desc_lower for kw in ["drink", "water", "make bed", "5 min", "quick"]):
            difficulty = 2
        elif any(kw in desc_lower for kw in ["workout", "gym", "hour", "run", "study"]):
            difficulty = 4
        elif any(kw in desc_lower for kw in ["marathon", "master", "expert", "intensive"]):
            difficulty = 5
        else:
            difficulty = 3
        
        # Category detection
        category = "personal"
        if any(w in desc_lower for w in ["workout", "gym", "run", "exercise", "fitness"]):
            category = "fitness"
        elif any(w in desc_lower for w in ["read", "learn", "study", "course"]):
            category = "learning"
        elif any(w in desc_lower for w in ["meditate", "journal", "gratitude", "mindful"]):
            category = "mindfulness"
        elif any(w in desc_lower for w in ["pray", "devotion", "scripture", "spiritual"]):
            category = "spiritual"
        elif any(w in desc_lower for w in ["budget", "save", "invest", "money"]):
            category = "finance"
        elif any(w in desc_lower for w in ["sleep", "water", "health", "vitamin"]):
            category = "health"
        
        stat_map = {
            "fitness": "strength", "health": "vitality", "learning": "intelligence",
            "career": "intelligence", "finance": "sense", "mindfulness": "willpower",
            "spiritual": "willpower", "productivity": "agility", "personal": "willpower",
        }
        
        diff_info = DIFFICULTIES[difficulty]
        xp = (diff_info["xp_range"][0] + diff_info["xp_range"][1]) // 2
        
        return {
            "difficulty": difficulty,
            "difficulty_name": diff_info["name"],
            "xp_reward": xp,
            "category": category,
            "target_stat": stat_map.get(category, "willpower"),
            "time_estimate": "15-20 minutes",
            "tip": "Start small and build consistency. You can always increase the challenge later!",
            "reasoning": {"time_factor": difficulty, "mental_effort": difficulty, 
                         "physical_effort": 2, "skill_required": difficulty, "consistency_need": 4}
        }
    
    def generate_goal_steps(self, goal_description: str, target_weeks: int = 12) -> Dict:
        """Generate 7-10 actionable steps for a goal"""
        if not self.is_available():
            return self._fallback_goal_steps(goal_description, target_weeks)
        
        prompt = f"""Create a detailed action plan for this goal. Return ONLY valid JSON.

Goal: "{goal_description}"
Target timeline: {target_weeks} weeks

Return this exact JSON structure:
{{
    "title": "<cleaned up goal title>",
    "difficulty": <1-6>,
    "difficulty_name": "<Trivial|Easy|Medium|Hard|Expert|Legendary>",
    "total_xp": <integer 1000-10000>,
    "category": "<category key>",
    "target_stat": "<stat key>",
    "estimated_weeks": {target_weeks},
    "steps": [
        {{
            "title": "<step title>",
            "description": "<detailed description>",
            "estimated_duration": "<e.g., '1 week', '3-5 days'>",
            "xp_reward": <integer>,
            "suggested_habit": "<optional daily/weekly habit to support this step>" or null
        }}
    ],
    "suggested_habits": [
        {{
            "title": "<habit title>",
            "description": "<brief description>",
            "frequency": "<daily|weekly>",
            "category": "<category>"
        }}
    ]
}}

Generate 7-10 steps that are specific, actionable, progressive, and achievable within the timeline.
Also suggest 2-3 supporting habits."""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            result_text = response.content[0].text.strip()
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
            return json.loads(result_text)
        except Exception as e:
            st.warning(f"AI goal generation failed: {e}")
            return self._fallback_goal_steps(goal_description, target_weeks)
    
    def _fallback_goal_steps(self, goal_description: str, target_weeks: int) -> Dict:
        """Fallback goal steps"""
        return {
            "title": goal_description[:50],
            "difficulty": 3,
            "difficulty_name": "Medium",
            "total_xp": 2500,
            "category": "personal",
            "target_stat": "willpower",
            "estimated_weeks": target_weeks,
            "steps": [
                {"title": "Research and plan", "description": "Gather information and create a detailed plan", "estimated_duration": "1 week", "xp_reward": 200, "suggested_habit": None},
                {"title": "Set up foundation", "description": "Prepare everything you need to get started", "estimated_duration": "1 week", "xp_reward": 250, "suggested_habit": None},
                {"title": "Begin practice", "description": "Start with basic exercises and activities", "estimated_duration": "2 weeks", "xp_reward": 300, "suggested_habit": "Daily practice - 15 minutes"},
                {"title": "Build consistency", "description": "Establish a regular routine", "estimated_duration": "2 weeks", "xp_reward": 350, "suggested_habit": None},
                {"title": "Increase challenge", "description": "Push beyond comfort zone", "estimated_duration": "2 weeks", "xp_reward": 300, "suggested_habit": None},
                {"title": "Refine technique", "description": "Focus on quality and improvement", "estimated_duration": "2 weeks", "xp_reward": 350, "suggested_habit": None},
                {"title": "Final push", "description": "Complete the goal with excellence", "estimated_duration": "2 weeks", "xp_reward": 500, "suggested_habit": None},
            ],
            "suggested_habits": [
                {"title": "Daily Progress Review", "description": "Spend 5 minutes reviewing progress", "frequency": "daily", "category": "productivity"},
                {"title": "Weekly Planning", "description": "Plan the week ahead", "frequency": "weekly", "category": "productivity"},
            ]
        }
    
    def analyze_document(self, text: str, max_chars: int = 50000) -> Dict:
        """Analyze document text and extract habits, goals, and quotes"""
        if not self.is_available():
            return self._fallback_document_analysis()
        
        if len(text) > max_chars:
            text = text[:max_chars] + "...[truncated]"
        
        prompt = f"""Analyze this document and extract actionable habits, goals, and memorable quotes.
Return ONLY valid JSON.

Document text:
\"\"\"
{text}
\"\"\"

Return this exact JSON structure:
{{
    "title": "<detected document title or 'Imported Document'>",
    "summary": "<brief 2-3 sentence summary>",
    "habits": [
        {{
            "title": "<habit title>",
            "description": "<from the text>",
            "category": "<category key>",
            "difficulty": <1-6>
        }}
    ],
    "goals": [
        {{
            "title": "<goal title>",
            "description": "<from the text>",
            "category": "<category key>",
            "steps": ["<step 1>", "<step 2>", ...]
        }}
    ],
    "quotes": [
        {{
            "quote": "<the quote>",
            "author": "<author if known>" or null,
            "context": "<brief context>"
        }}
    ],
    "key_concepts": ["<concept 1>", "<concept 2>", ...]
}}

Extract 5-15 habits, 1-5 goals, 5-10 quotes, and 3-7 key concepts."""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}]
            )
            result_text = response.content[0].text.strip()
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
            return json.loads(result_text)
        except Exception as e:
            st.warning(f"Document analysis failed: {e}")
            return self._fallback_document_analysis()
    
    def _fallback_document_analysis(self) -> Dict:
        return {
            "title": "Imported Document",
            "summary": "Document imported. AI analysis unavailable.",
            "habits": [], "goals": [], "quotes": [], "key_concepts": []
        }
    
    def chat(self, message: str, user_data: Dict, chat_history: List[Dict] = None) -> str:
        """AI coach chat"""
        if not self.is_available():
            return self._fallback_chat()
        
        user_context = f"""
User Profile:
- Name: {user_data.get('name', 'Hunter')}
- Level: {user_data.get('level', 1)}
- Current Streak: {user_data.get('current_streak', 0)} days
- Stats: STR {user_data.get('strength', 1)}, INT {user_data.get('intelligence', 1)}, VIT {user_data.get('vitality', 1)}, AGI {user_data.get('agility', 1)}, SEN {user_data.get('sense', 1)}, WIL {user_data.get('willpower', 1)}
"""
        
        system_prompt = f"""You are an AI Life Coach in Goal Quest - a gamified habit tracking app inspired by Solo Leveling anime.

{user_context}

Your personality:
- Motivating but not cheesy
- Reference their stats and progress naturally
- Use their name occasionally
- Give practical, actionable advice
- Keep responses concise (2-4 paragraphs max)
- Encourage them to create habits or goals when appropriate"""

        messages = []
        if chat_history:
            for msg in chat_history[-10:]:
                messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                system=system_prompt,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            return self._fallback_chat()
    
    def _fallback_chat(self) -> str:
        return """I'm currently in offline mode. Here's what you can do:
• Create a new habit to build your streak
• Work on your active goals
• Check your progress in Analytics
• Browse the Shop for power-ups

When AI is available, I'll give you personalized coaching!"""


# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════════════════════════════════════

class Database:
    """SQLite database handler"""
    
    def __init__(self, db_path: str = "goal_quest.db"):
        self.db_path = db_path
        self.conn = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
    
    def _create_tables(self):
        cursor = self.conn.cursor()
        
        # User table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                display_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                level INTEGER DEFAULT 1,
                current_xp INTEGER DEFAULT 0,
                total_xp INTEGER DEFAULT 0,
                gold INTEGER DEFAULT 100,
                gems INTEGER DEFAULT 10,
                strength INTEGER DEFAULT 1,
                intelligence INTEGER DEFAULT 1,
                vitality INTEGER DEFAULT 1,
                agility INTEGER DEFAULT 1,
                sense INTEGER DEFAULT 1,
                willpower INTEGER DEFAULT 1,
                current_streak INTEGER DEFAULT 0,
                best_streak INTEGER DEFAULT 0,
                last_activity_date DATE,
                philosophy_traditions TEXT DEFAULT '["stoic"]',
                onboarding_complete INTEGER DEFAULT 0,
                dreams_text TEXT
            )
        """)
        
        # Habits table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT DEFAULT 'personal',
                difficulty INTEGER DEFAULT 3,
                xp_reward INTEGER DEFAULT 100,
                target_stat TEXT DEFAULT 'willpower',
                frequency TEXT DEFAULT 'daily',
                streak INTEGER DEFAULT 0,
                best_streak INTEGER DEFAULT 0,
                total_completions INTEGER DEFAULT 0,
                is_priority INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ai_tip TEXT,
                FOREIGN KEY (user_id) REFERENCES user(id)
            )
        """)
        
        # Habit completions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habit_completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completion_date DATE NOT NULL,
                xp_earned INTEGER DEFAULT 0,
                streak_bonus INTEGER DEFAULT 0,
                FOREIGN KEY (habit_id) REFERENCES habits(id),
                UNIQUE(habit_id, completion_date)
            )
        """)
        
        # Goals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT DEFAULT 'personal',
                difficulty INTEGER DEFAULT 3,
                xp_reward INTEGER DEFAULT 2000,
                target_stat TEXT DEFAULT 'intelligence',
                due_date DATE,
                estimated_weeks INTEGER,
                is_completed INTEGER DEFAULT 0,
                completed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(id)
            )
        """)
        
        # Goal steps
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS goal_steps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_id INTEGER NOT NULL,
                step_number INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                estimated_duration TEXT,
                xp_reward INTEGER DEFAULT 200,
                is_completed INTEGER DEFAULT 0,
                completed_at TIMESTAMP,
                FOREIGN KEY (goal_id) REFERENCES goals(id)
            )
        """)
        
        # Shop items
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shop_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                item_type TEXT,
                rarity TEXT DEFAULT 'common',
                gold_cost INTEGER DEFAULT 0,
                gem_cost INTEGER DEFAULT 0,
                level_required INTEGER DEFAULT 1,
                effects TEXT,
                is_available INTEGER DEFAULT 1
            )
        """)
        
        # User inventory
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (item_id) REFERENCES shop_items(id)
            )
        """)
        
        # Wisdom quotes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wisdom_quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quote TEXT NOT NULL,
                author TEXT,
                source TEXT,
                tradition TEXT,
                is_user_saved INTEGER DEFAULT 0,
                user_id INTEGER
            )
        """)
        
        # Notes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                is_pinned INTEGER DEFAULT 0,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(id)
            )
        """)
        
        # Achievements
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT,
                tier TEXT DEFAULT 'bronze',
                xp_reward INTEGER DEFAULT 100,
                requirement_type TEXT,
                requirement_value INTEGER
            )
        """)
        
        # User achievements
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                achievement_id INTEGER NOT NULL,
                unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (achievement_id) REFERENCES achievements(id),
                UNIQUE(user_id, achievement_id)
            )
        """)
        
        self.conn.commit()
        self._init_default_data()
    
    def _init_default_data(self):
        """Initialize default data"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM shop_items")
        if cursor.fetchone()[0] == 0:
            shop_items = [
                ("XP Boost (Minor)", "Gain 25% more XP for 1 hour", "consumable", "common", 100, 0, 1, '{"xp_multiplier": 1.25, "duration_hours": 1}'),
                ("XP Boost (Major)", "Gain 50% more XP for 2 hours", "consumable", "uncommon", 250, 0, 5, '{"xp_multiplier": 1.5, "duration_hours": 2}'),
                ("Streak Shield", "Protect your streak for one missed day", "consumable", "rare", 500, 0, 10, '{"streak_protection": 1}'),
                ("Motivation Elixir", "Double XP for next habit completion", "consumable", "uncommon", 150, 0, 5, '{"next_habit_multiplier": 2}'),
                ("XP Boost (Legendary)", "Double XP for 24 hours", "consumable", "legendary", 0, 50, 25, '{"xp_multiplier": 2, "duration_hours": 24}'),
                ("Strength Elixir", "+5 temporary Strength for 24h", "boost", "rare", 300, 0, 15, '{"stat": "strength", "boost": 5}'),
                ("Wisdom Scroll", "+5 temporary Intelligence for 24h", "boost", "rare", 300, 0, 15, '{"stat": "intelligence", "boost": 5}'),
            ]
            cursor.executemany("""
                INSERT INTO shop_items (name, description, item_type, rarity, gold_cost, gem_cost, level_required, effects)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, shop_items)
        
        cursor.execute("SELECT COUNT(*) FROM wisdom_quotes")
        if cursor.fetchone()[0] == 0:
            quotes = [
                ("The impediment to action advances action. What stands in the way becomes the way.", "Marcus Aurelius", "Meditations", "stoic"),
                ("We suffer more in imagination than in reality.", "Seneca", "Letters", "stoic"),
                ("No man is free who is not master of himself.", "Epictetus", "Discourses", "stoic"),
                ("I can do all things through Christ who strengthens me.", "Philippians 4:13", "Bible", "biblical"),
                ("Trust in the Lord with all your heart.", "Proverbs 3:5", "Bible", "biblical"),
                ("The journey of a thousand miles begins with a single step.", "Lao Tzu", "Tao Te Ching", "eastern"),
                ("The mind is everything. What you think you become.", "Buddha", "Dhammapada", "eastern"),
                ("Today is victory over yourself of yesterday.", "Miyamoto Musashi", "Book of Five Rings", "samurai"),
                ("Think lightly of yourself and deeply of the world.", "Miyamoto Musashi", "Book of Five Rings", "samurai"),
            ]
            cursor.executemany("""
                INSERT INTO wisdom_quotes (quote, author, source, tradition)
                VALUES (?, ?, ?, ?)
            """, quotes)
        
        cursor.execute("SELECT COUNT(*) FROM achievements")
        if cursor.fetchone()[0] == 0:
            achievements = [
                ("first_flame", "First Flame", "Complete your first habit", "streaks", "bronze", 100, "count", 1),
                ("kindling", "Kindling", "Maintain a 7-day streak", "streaks", "bronze", 200, "streak", 7),
                ("bonfire", "Bonfire", "Maintain a 14-day streak", "streaks", "silver", 400, "streak", 14),
                ("inferno", "Inferno", "Maintain a 30-day streak", "streaks", "gold", 800, "streak", 30),
                ("awakened", "Awakened", "Reach Level 5", "levels", "bronze", 150, "level", 5),
                ("novice_hunter", "Novice Hunter", "Reach Level 10", "levels", "bronze", 300, "level", 10),
                ("habit_former", "Habit Former", "Create 5 habits", "habits", "bronze", 100, "count", 5),
                ("goal_setter", "Goal Setter", "Create your first goal", "goals", "bronze", 100, "count", 1),
            ]
            cursor.executemany("""
                INSERT INTO achievements (key, title, description, category, tier, xp_reward, requirement_type, requirement_value)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, achievements)
        
        self.conn.commit()
    
    # User methods
    def get_user(self) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user LIMIT 1")
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def create_user(self, name: str, **kwargs) -> int:
        cursor = self.conn.cursor()
        columns = ["name"] + list(kwargs.keys())
        placeholders = ["?"] * len(columns)
        values = [name] + list(kwargs.values())
        cursor.execute(f"INSERT INTO user ({', '.join(columns)}) VALUES ({', '.join(placeholders)})", values)
        self.conn.commit()
        return cursor.lastrowid
    
    def update_user(self, user_id: int, **kwargs) -> bool:
        if not kwargs:
            return False
        cursor = self.conn.cursor()
        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values()) + [user_id]
        cursor.execute(f"UPDATE user SET {set_clause} WHERE id = ?", values)
        self.conn.commit()
        return cursor.rowcount > 0
    
    def add_xp(self, user_id: int, xp: int) -> Dict:
        user = self.get_user()
        if not user:
            return {"error": "User not found"}
        
        new_xp = user["current_xp"] + xp
        new_total = user["total_xp"] + xp
        new_level = user["level"]
        leveled_up = False
        
        xp_needed = self.xp_for_level(new_level)
        while new_xp >= xp_needed:
            new_xp -= xp_needed
            new_level += 1
            leveled_up = True
            xp_needed = self.xp_for_level(new_level)
        
        self.update_user(user_id, current_xp=new_xp, total_xp=new_total, level=new_level)
        return {"xp_gained": xp, "new_xp": new_xp, "new_level": new_level, "leveled_up": leveled_up, "xp_to_next": xp_needed}
    
    @staticmethod
    def xp_for_level(level: int) -> int:
        return int(100 * (level ** 1.5))
    
    # Habit methods
    def create_habit(self, user_id: int, title: str, **kwargs) -> int:
        cursor = self.conn.cursor()
        columns = ["user_id", "title"] + list(kwargs.keys())
        placeholders = ["?"] * len(columns)
        values = [user_id, title] + list(kwargs.values())
        cursor.execute(f"INSERT INTO habits ({', '.join(columns)}) VALUES ({', '.join(placeholders)})", values)
        self.conn.commit()
        return cursor.lastrowid
    
    def get_habits(self, user_id: int, active_only: bool = True) -> List[Dict]:
        cursor = self.conn.cursor()
        query = "SELECT * FROM habits WHERE user_id = ?"
        if active_only:
            query += " AND is_active = 1"
        query += " ORDER BY is_priority DESC, created_at DESC"
        cursor.execute(query, (user_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_habit(self, habit_id: int) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM habits WHERE id = ?", (habit_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def update_habit(self, habit_id: int, **kwargs) -> bool:
        if not kwargs:
            return False
        cursor = self.conn.cursor()
        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values()) + [habit_id]
        cursor.execute(f"UPDATE habits SET {set_clause} WHERE id = ?", values)
        self.conn.commit()
        return cursor.rowcount > 0
    
    def delete_habit(self, habit_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM habit_completions WHERE habit_id = ?", (habit_id,))
        cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def complete_habit(self, habit_id: int, user_id: int) -> Dict:
        today = date.today().isoformat()
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT id FROM habit_completions WHERE habit_id = ? AND completion_date = ?", (habit_id, today))
        if cursor.fetchone():
            return {"error": "Already completed today"}
        
        habit = self.get_habit(habit_id)
        if not habit:
            return {"error": "Habit not found"}
        
        new_streak = habit["streak"] + 1
        streak_bonus = min(int(habit["xp_reward"] * 0.1 * new_streak), habit["xp_reward"])
        total_xp = habit["xp_reward"] + streak_bonus
        
        cursor.execute("""
            INSERT INTO habit_completions (habit_id, completion_date, xp_earned, streak_bonus)
            VALUES (?, ?, ?, ?)
        """, (habit_id, today, total_xp, streak_bonus))
        
        best_streak = max(habit["best_streak"], new_streak)
        self.update_habit(habit_id, streak=new_streak, best_streak=best_streak, total_completions=habit["total_completions"] + 1)
        
        xp_result = self.add_xp(user_id, total_xp)
        gold_earned = int(habit["xp_reward"] * 0.1)
        
        user = self.get_user()
        self.update_user(user_id, gold=user["gold"] + gold_earned)
        
        # Update user streak
        user_streak = user["current_streak"] + 1
        user_best = max(user["best_streak"], user_streak)
        self.update_user(user_id, current_streak=user_streak, best_streak=user_best, last_activity_date=today)
        
        # Update target stat
        stat = habit.get("target_stat", "willpower")
        current_stat = user.get(stat, 1)
        self.update_user(user_id, **{stat: current_stat + 1})
        
        self.conn.commit()
        return {"success": True, "xp_earned": total_xp, "streak_bonus": streak_bonus, "gold_earned": gold_earned, "new_streak": new_streak, **xp_result}
    
    def is_habit_completed_today(self, habit_id: int) -> bool:
        today = date.today().isoformat()
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM habit_completions WHERE habit_id = ? AND completion_date = ?", (habit_id, today))
        return cursor.fetchone() is not None
    
    def get_today_completions(self, user_id: int) -> List[int]:
        today = date.today().isoformat()
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT hc.habit_id FROM habit_completions hc
            JOIN habits h ON hc.habit_id = h.id
            WHERE h.user_id = ? AND hc.completion_date = ?
        """, (user_id, today))
        return [row[0] for row in cursor.fetchall()]
    
    # Goal methods
    def create_goal(self, user_id: int, title: str, steps: List[Dict] = None, **kwargs) -> int:
        cursor = self.conn.cursor()
        columns = ["user_id", "title"] + list(kwargs.keys())
        placeholders = ["?"] * len(columns)
        values = [user_id, title] + list(kwargs.values())
        cursor.execute(f"INSERT INTO goals ({', '.join(columns)}) VALUES ({', '.join(placeholders)})", values)
        goal_id = cursor.lastrowid
        
        if steps:
            for i, step in enumerate(steps, 1):
                cursor.execute("""
                    INSERT INTO goal_steps (goal_id, step_number, title, description, estimated_duration, xp_reward)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (goal_id, i, step.get("title", f"Step {i}"), step.get("description", ""), step.get("estimated_duration", "1 week"), step.get("xp_reward", 200)))
        
        self.conn.commit()
        return goal_id
    
    def get_goals(self, user_id: int, include_completed: bool = False) -> List[Dict]:
        cursor = self.conn.cursor()
        query = "SELECT * FROM goals WHERE user_id = ?"
        if not include_completed:
            query += " AND is_completed = 0"
        query += " ORDER BY due_date ASC, created_at DESC"
        cursor.execute(query, (user_id,))
        goals = [dict(row) for row in cursor.fetchall()]
        
        for goal in goals:
            goal["steps"] = self.get_goal_steps(goal["id"])
            goal["progress"] = self.get_goal_progress(goal["id"])
        return goals
    
    def get_goal(self, goal_id: int) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM goals WHERE id = ?", (goal_id,))
        row = cursor.fetchone()
        if not row:
            return None
        goal = dict(row)
        goal["steps"] = self.get_goal_steps(goal_id)
        goal["progress"] = self.get_goal_progress(goal_id)
        return goal
    
    def get_goal_steps(self, goal_id: int) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM goal_steps WHERE goal_id = ? ORDER BY step_number", (goal_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_goal_progress(self, goal_id: int) -> Dict:
        steps = self.get_goal_steps(goal_id)
        if not steps:
            return {"completed": 0, "total": 0, "percentage": 0}
        completed = sum(1 for s in steps if s["is_completed"])
        return {"completed": completed, "total": len(steps), "percentage": int((completed / len(steps)) * 100)}
    
    def complete_goal_step(self, step_id: int, user_id: int) -> Dict:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM goal_steps WHERE id = ?", (step_id,))
        step = cursor.fetchone()
        if not step:
            return {"error": "Step not found"}
        step = dict(step)
        if step["is_completed"]:
            return {"error": "Step already completed"}
        
        cursor.execute("UPDATE goal_steps SET is_completed = 1, completed_at = ? WHERE id = ?", (datetime.now().isoformat(), step_id))
        xp_result = self.add_xp(user_id, step["xp_reward"])
        
        progress = self.get_goal_progress(step["goal_id"])
        goal_completed = progress["percentage"] == 100
        
        if goal_completed:
            goal = self.get_goal(step["goal_id"])
            cursor.execute("UPDATE goals SET is_completed = 1, completed_at = ? WHERE id = ?", (datetime.now().isoformat(), step["goal_id"]))
            goal_xp = self.add_xp(user_id, goal["xp_reward"])
            xp_result["goal_xp"] = goal["xp_reward"]
        
        self.conn.commit()
        return {"success": True, "step_xp": step["xp_reward"], "goal_completed": goal_completed, **xp_result}
    
    def delete_goal(self, goal_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM goal_steps WHERE goal_id = ?", (goal_id,))
        cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    # Shop methods
    def get_shop_items(self, user_level: int = 1) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM shop_items WHERE is_available = 1 ORDER BY level_required, gold_cost")
        items = []
        for row in cursor.fetchall():
            item = dict(row)
            item["meets_level"] = item["level_required"] <= user_level
            items.append(item)
        return items
    
    def purchase_item(self, user_id: int, item_id: int) -> Dict:
        user = self.get_user()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM shop_items WHERE id = ?", (item_id,))
        item = cursor.fetchone()
        if not item:
            return {"error": "Item not found"}
        item = dict(item)
        
        if user["level"] < item["level_required"]:
            return {"error": f"Requires level {item['level_required']}"}
        if item["gold_cost"] > 0 and user["gold"] < item["gold_cost"]:
            return {"error": "Not enough gold"}
        if item["gem_cost"] > 0 and user["gems"] < item["gem_cost"]:
            return {"error": "Not enough gems"}
        
        new_gold = user["gold"] - item["gold_cost"]
        new_gems = user["gems"] - item["gem_cost"]
        self.update_user(user_id, gold=new_gold, gems=new_gems)
        
        cursor.execute("SELECT id, quantity FROM user_inventory WHERE user_id = ? AND item_id = ?", (user_id, item_id))
        existing = cursor.fetchone()
        if existing:
            cursor.execute("UPDATE user_inventory SET quantity = quantity + 1 WHERE id = ?", (existing[0],))
        else:
            cursor.execute("INSERT INTO user_inventory (user_id, item_id, quantity) VALUES (?, ?, 1)", (user_id, item_id))
        
        self.conn.commit()
        return {"success": True, "item": item, "new_gold": new_gold, "new_gems": new_gems}
    
    def get_inventory(self, user_id: int) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT ui.*, si.name, si.description, si.item_type, si.rarity, si.effects
            FROM user_inventory ui
            JOIN shop_items si ON ui.item_id = si.id
            WHERE ui.user_id = ?
        """, (user_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    # Quote methods
    def get_random_quote(self, traditions: List[str] = None) -> Optional[Dict]:
        cursor = self.conn.cursor()
        if traditions:
            placeholders = ", ".join(["?"] * len(traditions))
            cursor.execute(f"SELECT * FROM wisdom_quotes WHERE tradition IN ({placeholders}) ORDER BY RANDOM() LIMIT 1", traditions)
        else:
            cursor.execute("SELECT * FROM wisdom_quotes ORDER BY RANDOM() LIMIT 1")
        row = cursor.fetchone()
        return dict(row) if row else None
    
    # Notes methods
    def create_note(self, user_id: int, title: str, content: str = "", **kwargs) -> int:
        cursor = self.conn.cursor()
        columns = ["user_id", "title", "content"] + list(kwargs.keys())
        placeholders = ["?"] * len(columns)
        values = [user_id, title, content] + list(kwargs.values())
        cursor.execute(f"INSERT INTO notes ({', '.join(columns)}) VALUES ({', '.join(placeholders)})", values)
        self.conn.commit()
        return cursor.lastrowid
    
    def get_notes(self, user_id: int) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM notes WHERE user_id = ? ORDER BY is_pinned DESC, updated_at DESC", (user_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def update_note(self, note_id: int, **kwargs) -> bool:
        kwargs["updated_at"] = datetime.now().isoformat()
        cursor = self.conn.cursor()
        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        cursor.execute(f"UPDATE notes SET {set_clause} WHERE id = ?", list(kwargs.values()) + [note_id])
        self.conn.commit()
        return cursor.rowcount > 0
    
    def delete_note(self, note_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    # Analytics
    def get_habit_stats(self, user_id: int, days: int = 30) -> Dict:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT hc.completion_date, COUNT(*) as count, SUM(hc.xp_earned) as xp
            FROM habit_completions hc
            JOIN habits h ON hc.habit_id = h.id
            WHERE h.user_id = ? AND hc.completion_date >= date('now', ?)
            GROUP BY hc.completion_date
            ORDER BY hc.completion_date
        """, (user_id, f"-{days} days"))
        daily = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute("""
            SELECT h.category, COUNT(*) as count
            FROM habit_completions hc
            JOIN habits h ON hc.habit_id = h.id
            WHERE h.user_id = ? AND hc.completion_date >= date('now', ?)
            GROUP BY h.category
        """, (user_id, f"-{days} days"))
        by_category = {row[0]: row[1] for row in cursor.fetchall()}
        
        return {"daily": daily, "by_category": by_category}


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_greeting(name: str = "") -> str:
    hour = datetime.now().hour
    day = datetime.now().strftime("%A")
    
    if day == "Monday":
        greeting = "New week energy"
    elif day == "Friday":
        greeting = "Finish strong"
    elif 5 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 17:
        greeting = "Good afternoon"
    elif 17 <= hour < 21:
        greeting = "Good evening"
    else:
        greeting = "Burning the midnight oil"
    
    return f"{greeting}, {name}!" if name else f"{greeting}!"


def get_tier_for_level(level: int) -> Dict:
    for tier_num, tier_data in TIERS.items():
        min_lvl, max_lvl = tier_data["level_range"]
        if min_lvl <= level <= max_lvl:
            return {"tier": tier_num, **tier_data}
    return {"tier": 6, **TIERS[6]}


def render_difficulty_badge(difficulty: int) -> str:
    diff = DIFFICULTIES.get(difficulty, DIFFICULTIES[3])
    stars = "⭐" * diff["stars"]
    return f'<span class="diff-{diff["name"].lower()}" style="padding: 4px 8px; border-radius: 4px; font-size: 12px;">{stars} {diff["name"]}</span>'


def render_xp_bar(current: int, needed: int) -> str:
    percentage = min((current / needed) * 100, 100) if needed > 0 else 0
    return f'''
    <div class="xp-bar">
        <div class="xp-fill" style="width: {percentage}%;"></div>
    </div>
    '''


# ═══════════════════════════════════════════════════════════════════════════════
# INITIALIZE SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def get_database():
    return Database()

@st.cache_resource
def get_ai_service():
    return AIService()

def init_session_state():
    if "db" not in st.session_state:
        st.session_state.db = get_database()
    if "ai" not in st.session_state:
        st.session_state.ai = get_ai_service()
    if "user" not in st.session_state:
        st.session_state.user = st.session_state.db.get_user()
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

init_session_state()


# ═══════════════════════════════════════════════════════════════════════════════
# ONBOARDING
# ═══════════════════════════════════════════════════════════════════════════════

def show_onboarding():
    st.markdown("# ⚔️ GOAL QUEST")
    st.markdown("### Level Up Your Life")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Welcome, Future Legend!")
        st.markdown("""
        Goal Quest transforms your habits and goals into an epic adventure:
        
        - 🔥 **Build streaks** and earn XP for consistency
        - 🎯 **AI-powered goals** with auto-generated action steps  
        - 📊 **Track 6 stats**: Strength, Intelligence, Vitality, Agility, Sense, Willpower
        - 🏆 **Unlock achievements** and shop for power-ups
        - 📖 **Daily wisdom** from philosophy traditions you choose
        """)
        
        st.markdown("---")
        
        name = st.text_input("What should we call you?", placeholder="Enter your name...")
        display_name = st.text_input("Choose your title (optional)", placeholder="e.g., Shadow, Phoenix, Titan...")
        
        st.markdown("#### Choose Your Wisdom Traditions")
        selected_traditions = []
        cols = st.columns(3)
        for i, (key, trad) in enumerate(PHILOSOPHY_TRADITIONS.items()):
            with cols[i % 3]:
                if st.checkbox(f"{trad['emoji']} {trad['name']}", value=(key == "stoic")):
                    selected_traditions.append(key)
        
        st.markdown("---")
        dreams = st.text_area("What are your dreams and goals? (optional)", placeholder="Tell us what you want to achieve...")
        
        if st.button("⚔️ Begin Your Journey", type="primary", use_container_width=True):
            if name.strip():
                user_id = st.session_state.db.create_user(
                    name=name.strip(),
                    display_name=display_name.strip() or name.strip(),
                    philosophy_traditions=json.dumps(selected_traditions or ["stoic"]),
                    dreams_text=dreams,
                    onboarding_complete=1,
                )
                st.session_state.user = st.session_state.db.get_user()
                st.balloons()
                st.rerun()
            else:
                st.error("Please enter your name!")
    
    with col2:
        st.markdown("#### Features")
        st.info("🔥 Streak System")
        st.info("🤖 AI Difficulty Assessment")
        st.info("🎯 Auto-Generated Goal Steps")
        st.info("📄 Document Import (PDF)")
        st.info("🏪 In-Game Shop")
        st.info("📈 Progress Analytics")


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════════

def render_sidebar():
    user = st.session_state.user
    tier = get_tier_for_level(user["level"])
    
    with st.sidebar:
        st.markdown(f"### ⚔️ Goal Quest")
        st.markdown("---")
        
        # User info
        st.markdown(f"**{user['display_name'] or user['name']}**")
        st.markdown(f"<span style='color: {tier['color']};'>{tier['name']}</span>", unsafe_allow_html=True)
        
        # Level and XP
        xp_needed = Database.xp_for_level(user["level"])
        st.markdown(f"**Level {user['level']}** • {user['current_xp']:,}/{xp_needed:,} XP")
        st.progress(user["current_xp"] / xp_needed if xp_needed > 0 else 0)
        
        # Currency
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💰 Gold", f"{user['gold']:,}")
        with col2:
            st.metric("💎 Gems", user['gems'])
        
        st.markdown("---")
        
        # Navigation
        pages = {
            "dashboard": "🏠 Dashboard",
            "habits": "⚡ Habits",
            "goals": "🎯 Goals",
            "shop": "🛒 Shop",
            "analytics": "📊 Analytics",
            "notes": "📝 Notes",
            "coach": "🤖 AI Coach",
            "settings": "⚙️ Settings",
        }
        
        for key, label in pages.items():
            if st.button(label, key=f"nav_{key}", use_container_width=True, type="secondary" if st.session_state.page != key else "primary"):
                st.session_state.page = key
                st.rerun()
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("#### Your Stats")
        stats_cols = st.columns(3)
        stat_keys = list(STATS.keys())
        for i, stat_key in enumerate(stat_keys):
            stat = STATS[stat_key]
            with stats_cols[i % 3]:
                st.markdown(f"**{stat['emoji']} {user.get(stat_key, 1)}**")


# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def render_dashboard():
    user = st.session_state.user
    db = st.session_state.db
    
    st.markdown(f"## {get_greeting(user['name'])}")
    
    # Quick stats row
    col1, col2, col3, col4 = st.columns(4)
    
    tier = get_tier_for_level(user["level"])
    with col1:
        st.metric("Level", user["level"], delta=f"{tier['name']}")
    with col2:
        st.metric("🔥 Streak", f"{user['current_streak']} days", delta=f"Best: {user['best_streak']}")
    with col3:
        habits = db.get_habits(user["id"])
        completions = db.get_today_completions(user["id"])
        st.metric("Today's Habits", f"{len(completions)}/{len(habits)}")
    with col4:
        goals = db.get_goals(user["id"])
        st.metric("Active Goals", len(goals))
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Today's habits
        st.markdown("### ⚡ Today's Quests")
        
        habits = db.get_habits(user["id"])
        completions = db.get_today_completions(user["id"])
        
        if not habits:
            st.info("No habits yet! Create your first habit to start your journey.")
            if st.button("➕ Create First Habit", key="dash_create_habit"):
                st.session_state.page = "habits"
                st.rerun()
        else:
            # Progress bar
            progress = len(completions) / len(habits) if habits else 0
            st.progress(progress)
            st.caption(f"{len(completions)}/{len(habits)} completed")
            
            for habit in habits:
                is_done = habit["id"] in completions
                cat = CATEGORIES.get(habit["category"], CATEGORIES["personal"])
                diff = DIFFICULTIES.get(habit["difficulty"], DIFFICULTIES[3])
                
                with st.container():
                    cols = st.columns([0.5, 3, 1, 1])
                    
                    with cols[0]:
                        st.markdown(f"### {cat['emoji']}")
                    
                    with cols[1]:
                        title_style = "text-decoration: line-through; color: #666;" if is_done else ""
                        st.markdown(f"<span style='{title_style}'><b>{habit['title']}</b></span>", unsafe_allow_html=True)
                        st.caption(f"{'⭐' * diff['stars']} {diff['name']} • +{habit['xp_reward']} XP")
                    
                    with cols[2]:
                        if habit["streak"] > 0:
                            st.markdown(f"🔥 {habit['streak']}")
                    
                    with cols[3]:
                        if is_done:
                            st.markdown("✅")
                        else:
                            if st.button("Complete", key=f"complete_{habit['id']}", type="primary"):
                                result = db.complete_habit(habit["id"], user["id"])
                                if result.get("success"):
                                    st.session_state.user = db.get_user()
                                    st.toast(f"🎉 +{result['xp_earned']} XP!")
                                    if result.get("leveled_up"):
                                        st.balloons()
                                        st.toast(f"⬆️ Level Up! You're now level {result['new_level']}!")
                                    st.rerun()
                    
                    st.markdown("---")
    
    with col2:
        # Wisdom quote
        st.markdown("### 📖 Daily Wisdom")
        
        traditions = user.get("philosophy_traditions", '["stoic"]')
        if isinstance(traditions, str):
            traditions = json.loads(traditions)
        
        quote = db.get_random_quote(traditions)
        if quote:
            st.markdown(f"*\"{quote['quote']}\"*")
            st.markdown(f"— **{quote['author']}**")
        
        if st.button("🔄 New Quote", key="new_quote"):
            st.rerun()
        
        st.markdown("---")
        
        # Stats overview
        st.markdown("### 📊 Your Stats")
        
        for stat_key, stat_info in STATS.items():
            value = user.get(stat_key, 1)
            st.markdown(f"{stat_info['emoji']} **{stat_info['abbr']}**: {value}")


# ═══════════════════════════════════════════════════════════════════════════════
# HABITS PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def render_habits():
    user = st.session_state.user
    db = st.session_state.db
    ai = st.session_state.ai
    
    st.markdown("## ⚡ Habits")
    
    # Add habit form
    with st.expander("➕ Create New Habit", expanded=False):
        habit_title = st.text_area("What habit do you want to build?", placeholder="e.g., Meditate for 10 minutes every morning")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🤖 Analyze with AI", use_container_width=True):
                if habit_title.strip():
                    with st.spinner("Analyzing..."):
                        analysis = ai.assess_habit_difficulty(habit_title, {
                            "level": user["level"],
                            "strength": user["strength"],
                            "willpower": user["willpower"],
                        })
                        st.session_state.habit_analysis = analysis
                else:
                    st.warning("Please enter a habit description first!")
        
        # Show analysis if available
        if "habit_analysis" in st.session_state:
            analysis = st.session_state.habit_analysis
            diff = DIFFICULTIES.get(analysis.get("difficulty", 3))
            cat = CATEGORIES.get(analysis.get("category", "personal"))
            
            st.markdown("---")
            st.markdown("#### AI Analysis")
            
            cols = st.columns(4)
            with cols[0]:
                st.markdown(f"**Difficulty**")
                st.markdown(f"{'⭐' * diff['stars']} {diff['name']}")
            with cols[1]:
                st.markdown(f"**Category**")
                st.markdown(f"{cat['emoji']} {cat['name']}")
            with cols[2]:
                st.markdown(f"**XP Reward**")
                st.markdown(f"+{analysis.get('xp_reward', 100)} XP")
            with cols[3]:
                st.markdown(f"**Time**")
                st.markdown(analysis.get("time_estimate", "~15 min"))
            
            if analysis.get("tip"):
                st.info(f"💡 **Tip**: {analysis['tip']}")
            
            with col2:
                if st.button("✅ Create Habit", type="primary", use_container_width=True):
                    habit_id = db.create_habit(
                        user_id=user["id"],
                        title=habit_title.strip(),
                        category=analysis.get("category", "personal"),
                        difficulty=analysis.get("difficulty", 3),
                        xp_reward=analysis.get("xp_reward", 100),
                        target_stat=analysis.get("target_stat", "willpower"),
                        ai_tip=analysis.get("tip", ""),
                    )
                    del st.session_state.habit_analysis
                    st.success("✅ Habit created!")
                    st.rerun()
    
    st.markdown("---")
    
    # Habit list
    habits = db.get_habits(user["id"])
    completions = db.get_today_completions(user["id"])
    
    if not habits:
        st.info("No habits yet. Create your first habit above!")
    else:
        # Filter tabs
        tab1, tab2 = st.tabs(["📋 Active", "✅ Completed Today"])
        
        with tab1:
            active_habits = [h for h in habits if h["id"] not in completions]
            if not active_habits:
                st.success("🎉 All habits completed for today!")
            else:
                for habit in active_habits:
                    cat = CATEGORIES.get(habit["category"], CATEGORIES["personal"])
                    diff = DIFFICULTIES.get(habit["difficulty"], DIFFICULTIES[3])
                    
                    with st.container():
                        cols = st.columns([0.5, 3, 1, 1, 0.5])
                        
                        with cols[0]:
                            st.markdown(f"### {cat['emoji']}")
                        
                        with cols[1]:
                            st.markdown(f"**{habit['title']}**")
                            st.caption(f"{'⭐' * diff['stars']} {diff['name']} • +{habit['xp_reward']} XP • {cat['name']}")
                            if habit.get("ai_tip"):
                                st.caption(f"💡 {habit['ai_tip'][:50]}...")
                        
                        with cols[2]:
                            if habit["streak"] > 0:
                                st.markdown(f"🔥 **{habit['streak']}** streak")
                        
                        with cols[3]:
                            if st.button("✅ Complete", key=f"h_complete_{habit['id']}", type="primary"):
                                result = db.complete_habit(habit["id"], user["id"])
                                if result.get("success"):
                                    st.session_state.user = db.get_user()
                                    st.toast(f"🎉 +{result['xp_earned']} XP!")
                                    st.rerun()
                        
                        with cols[4]:
                            if st.button("🗑️", key=f"h_delete_{habit['id']}"):
                                db.delete_habit(habit["id"])
                                st.rerun()
                        
                        st.markdown("---")
        
        with tab2:
            completed_habits = [h for h in habits if h["id"] in completions]
            if not completed_habits:
                st.info("No habits completed yet today.")
            else:
                for habit in completed_habits:
                    cat = CATEGORIES.get(habit["category"], CATEGORIES["personal"])
                    st.markdown(f"✅ ~~{habit['title']}~~ {cat['emoji']} +{habit['xp_reward']} XP")


# ═══════════════════════════════════════════════════════════════════════════════
# GOALS PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def render_goals():
    user = st.session_state.user
    db = st.session_state.db
    ai = st.session_state.ai
    
    st.markdown("## 🎯 Goals")
    
    # Create goal form
    with st.expander("➕ Create New Goal", expanded=False):
        goal_title = st.text_area("What do you want to achieve?", placeholder="e.g., Learn to play guitar")
        target_weeks = st.slider("Target timeline (weeks)", 1, 52, 12)
        
        if st.button("🤖 Generate Quest with AI", use_container_width=True):
            if goal_title.strip():
                with st.spinner("Crafting your quest..."):
                    result = ai.generate_goal_steps(goal_title, target_weeks)
                    st.session_state.goal_generation = result
            else:
                st.warning("Please enter a goal description first!")
        
        # Show generated quest
        if "goal_generation" in st.session_state:
            gen = st.session_state.goal_generation
            diff = DIFFICULTIES.get(gen.get("difficulty", 3))
            
            st.markdown("---")
            st.markdown(f"### 🎯 {gen.get('title', goal_title)}")
            
            cols = st.columns(4)
            with cols[0]:
                st.markdown(f"**{'⭐' * diff['stars']} {diff['name']}**")
            with cols[1]:
                st.markdown(f"**{gen.get('estimated_weeks', target_weeks)} weeks**")
            with cols[2]:
                st.markdown(f"**+{gen.get('total_xp', 2500)} XP**")
            with cols[3]:
                cat = CATEGORIES.get(gen.get("category", "personal"))
                st.markdown(f"**{cat['emoji']} {cat['name']}**")
            
            st.markdown("#### Quest Steps")
            for i, step in enumerate(gen.get("steps", []), 1):
                st.markdown(f"**{i}.** {step.get('title')} • {step.get('estimated_duration', '1 week')} • +{step.get('xp_reward', 200)} XP")
            
            if gen.get("suggested_habits"):
                st.markdown("#### Suggested Supporting Habits")
                for habit in gen.get("suggested_habits", []):
                    st.markdown(f"• {habit.get('title')} ({habit.get('frequency', 'daily')})")
            
            if st.button("✅ Start This Quest", type="primary", use_container_width=True):
                due_date = (datetime.now() + timedelta(weeks=gen.get("estimated_weeks", target_weeks))).date().isoformat()
                goal_id = db.create_goal(
                    user_id=user["id"],
                    title=gen.get("title", goal_title),
                    description=goal_title,
                    category=gen.get("category", "personal"),
                    difficulty=gen.get("difficulty", 3),
                    xp_reward=gen.get("total_xp", 2500),
                    target_stat=gen.get("target_stat", "willpower"),
                    due_date=due_date,
                    estimated_weeks=gen.get("estimated_weeks", target_weeks),
                    steps=gen.get("steps", []),
                )
                
                # Create suggested habits
                for habit in gen.get("suggested_habits", []):
                    db.create_habit(
                        user_id=user["id"],
                        title=habit.get("title"),
                        description=habit.get("description", ""),
                        category=habit.get("category", "personal"),
                        frequency=habit.get("frequency", "daily"),
                    )
                
                del st.session_state.goal_generation
                st.success("🎯 Quest started!")
                st.rerun()
    
    st.markdown("---")
    
    # Goals list
    tab1, tab2 = st.tabs(["📋 Active Goals", "✅ Completed"])
    
    with tab1:
        goals = db.get_goals(user["id"], include_completed=False)
        
        if not goals:
            st.info("No active goals. Create a new goal above!")
        else:
            for goal in goals:
                cat = CATEGORIES.get(goal["category"], CATEGORIES["personal"])
                progress = goal.get("progress", {"completed": 0, "total": 0, "percentage": 0})
                
                with st.container():
                    cols = st.columns([0.5, 3, 1, 0.5])
                    
                    with cols[0]:
                        st.markdown(f"### {cat['emoji']}")
                    
                    with cols[1]:
                        st.markdown(f"**{goal['title']}**")
                        st.progress(progress["percentage"] / 100)
                        st.caption(f"{progress['completed']}/{progress['total']} steps • +{goal['xp_reward']} XP total")
                    
                    with cols[2]:
                        if goal.get("due_date"):
                            days_left = (datetime.fromisoformat(goal["due_date"]) - datetime.now()).days
                            if days_left < 0:
                                st.error("Overdue!")
                            elif days_left <= 7:
                                st.warning(f"{days_left} days left")
                            else:
                                st.info(f"{days_left} days left")
                    
                    with cols[3]:
                        if st.button("🗑️", key=f"g_delete_{goal['id']}"):
                            db.delete_goal(goal["id"])
                            st.rerun()
                    
                    # Show steps
                    with st.expander("View Steps"):
                        for step in goal.get("steps", []):
                            cols2 = st.columns([0.5, 4, 1])
                            with cols2[0]:
                                if step["is_completed"]:
                                    st.markdown("✅")
                                else:
                                    st.markdown("⬜")
                            with cols2[1]:
                                title_style = "text-decoration: line-through;" if step["is_completed"] else ""
                                st.markdown(f"<span style='{title_style}'>{step['title']}</span>", unsafe_allow_html=True)
                                st.caption(f"+{step['xp_reward']} XP")
                            with cols2[2]:
                                if not step["is_completed"]:
                                    if st.button("Complete", key=f"step_{step['id']}"):
                                        result = db.complete_goal_step(step["id"], user["id"])
                                        if result.get("success"):
                                            st.session_state.user = db.get_user()
                                            st.toast(f"🎉 +{result.get('step_xp', 200)} XP!")
                                            if result.get("goal_completed"):
                                                st.balloons()
                                                st.toast("🏆 Goal Complete!")
                                            st.rerun()
                    
                    st.markdown("---")
    
    with tab2:
        completed_goals = db.get_goals(user["id"], include_completed=True)
        completed_goals = [g for g in completed_goals if g.get("is_completed")]
        
        if not completed_goals:
            st.info("No completed goals yet.")
        else:
            for goal in completed_goals:
                cat = CATEGORIES.get(goal["category"], CATEGORIES["personal"])
                st.markdown(f"✅ **{goal['title']}** {cat['emoji']} +{goal['xp_reward']} XP")


# ═══════════════════════════════════════════════════════════════════════════════
# SHOP PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def render_shop():
    user = st.session_state.user
    db = st.session_state.db
    
    st.markdown("## 🛒 Shop")
    
    # Currency display
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.metric("💰 Gold", f"{user['gold']:,}")
    with col2:
        st.metric("💎 Gems", user['gems'])
    
    st.markdown("---")
    
    # Shop items
    items = db.get_shop_items(user["level"])
    
    tab1, tab2 = st.tabs(["🛍️ Shop", "🎒 Inventory"])
    
    with tab1:
        cols = st.columns(3)
        for i, item in enumerate(items):
            with cols[i % 3]:
                rarity = RARITIES.get(item["rarity"], RARITIES["common"])
                
                with st.container():
                    st.markdown(f"**{item['name']}**")
                    st.caption(f"<span style='color: {rarity['color']};'>{rarity['name'].upper()}</span>", unsafe_allow_html=True)
                    st.markdown(item["description"])
                    
                    # Price
                    if item["gold_cost"] > 0:
                        st.markdown(f"💰 {item['gold_cost']}")
                    if item["gem_cost"] > 0:
                        st.markdown(f"💎 {item['gem_cost']}")
                    
                    # Level requirement
                    if not item["meets_level"]:
                        st.warning(f"🔒 Requires Level {item['level_required']}")
                    else:
                        can_afford = (item["gold_cost"] == 0 or user["gold"] >= item["gold_cost"]) and \
                                     (item["gem_cost"] == 0 or user["gems"] >= item["gem_cost"])
                        
                        if st.button("Buy", key=f"buy_{item['id']}", disabled=not can_afford):
                            result = db.purchase_item(user["id"], item["id"])
                            if result.get("success"):
                                st.session_state.user = db.get_user()
                                st.success(f"✅ Purchased {item['name']}!")
                                st.rerun()
                            else:
                                st.error(result.get("error", "Purchase failed"))
                    
                    st.markdown("---")
    
    with tab2:
        inventory = db.get_inventory(user["id"])
        
        if not inventory:
            st.info("Your inventory is empty. Buy items from the shop!")
        else:
            for item in inventory:
                rarity = RARITIES.get(item["rarity"], RARITIES["common"])
                cols = st.columns([3, 1, 1])
                
                with cols[0]:
                    st.markdown(f"**{item['name']}**")
                    st.caption(f"<span style='color: {rarity['color']};'>{rarity['name']}</span>", unsafe_allow_html=True)
                
                with cols[1]:
                    st.markdown(f"Qty: **{item['quantity']}**")
                
                with cols[2]:
                    if st.button("Use", key=f"use_{item['id']}"):
                        st.toast(f"Used {item['name']}!")
                
                st.markdown("---")


# ═══════════════════════════════════════════════════════════════════════════════
# ANALYTICS PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def render_analytics():
    user = st.session_state.user
    db = st.session_state.db
    
    st.markdown("## 📊 Analytics")
    
    # Overview stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total XP", f"{user['total_xp']:,}")
    with col2:
        st.metric("Current Level", user['level'])
    with col3:
        st.metric("Best Streak", f"{user['best_streak']} days")
    with col4:
        habits = db.get_habits(user["id"])
        total_completions = sum(h.get("total_completions", 0) for h in habits)
        st.metric("Total Completions", total_completions)
    
    st.markdown("---")
    
    # Stats breakdown
    st.markdown("### 📈 Your Stats")
    
    cols = st.columns(6)
    for i, (stat_key, stat_info) in enumerate(STATS.items()):
        with cols[i]:
            value = user.get(stat_key, 1)
            st.metric(f"{stat_info['emoji']} {stat_info['abbr']}", value)
    
    st.markdown("---")
    
    # Habit stats by category
    st.markdown("### 📊 Habits by Category")
    
    stats = db.get_habit_stats(user["id"], 30)
    
    if stats["by_category"]:
        for cat_key, count in stats["by_category"].items():
            cat = CATEGORIES.get(cat_key, CATEGORIES["personal"])
            st.markdown(f"{cat['emoji']} **{cat['name']}**: {count} completions")
    else:
        st.info("Complete some habits to see your stats!")
    
    st.markdown("---")
    
    # Tier progress
    st.markdown("### 🏆 Tier Progress")
    
    tier = get_tier_for_level(user["level"])
    st.markdown(f"**Current Tier**: <span style='color: {tier['color']};'>{tier['name']}</span>", unsafe_allow_html=True)
    
    for tier_num, tier_data in TIERS.items():
        min_lvl, max_lvl = tier_data["level_range"]
        is_current = tier_num == tier["tier"]
        is_achieved = user["level"] >= min_lvl
        
        status = "✅" if is_achieved else "🔒"
        style = f"color: {tier_data['color']}; font-weight: bold;" if is_current else ""
        
        st.markdown(f"{status} <span style='{style}'>{tier_data['name']}</span> (Level {min_lvl}-{max_lvl})", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# NOTES PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def render_notes():
    user = st.session_state.user
    db = st.session_state.db
    
    st.markdown("## 📝 Notes")
    
    # Create note
    with st.expander("➕ Create New Note"):
        note_title = st.text_input("Title", placeholder="Note title...")
        note_content = st.text_area("Content", placeholder="Write your note...", height=200)
        
        if st.button("💾 Save Note", type="primary"):
            if note_title.strip():
                db.create_note(user["id"], note_title.strip(), note_content)
                st.success("Note saved!")
                st.rerun()
            else:
                st.warning("Please enter a title!")
    
    st.markdown("---")
    
    # Notes list
    notes = db.get_notes(user["id"])
    
    if not notes:
        st.info("No notes yet. Create your first note above!")
    else:
        for note in notes:
            with st.expander(f"{'📌 ' if note['is_pinned'] else ''}{note['title']}"):
                st.markdown(note["content"] or "*No content*")
                st.caption(f"Created: {note['created_at'][:10]}")
                
                cols = st.columns([1, 1, 1])
                with cols[0]:
                    pin_label = "Unpin" if note["is_pinned"] else "📌 Pin"
                    if st.button(pin_label, key=f"pin_{note['id']}"):
                        db.update_note(note["id"], is_pinned=0 if note["is_pinned"] else 1)
                        st.rerun()
                with cols[2]:
                    if st.button("🗑️ Delete", key=f"del_note_{note['id']}"):
                        db.delete_note(note["id"])
                        st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# AI COACH PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def render_coach():
    user = st.session_state.user
    ai = st.session_state.ai
    
    st.markdown("## 🤖 AI Coach")
    st.markdown("Your personal life coach powered by AI")
    
    if not ai.is_available():
        st.warning("⚠️ AI is currently unavailable. Please check your API key in secrets.")
    
    st.markdown("---")
    
    # Chat history display
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**You**: {msg['content']}")
        else:
            st.markdown(f"**Coach**: {msg['content']}")
        st.markdown("---")
    
    # Chat input
    user_message = st.text_input("Ask your coach...", placeholder="e.g., How can I stay motivated?", key="coach_input")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Send", type="primary", use_container_width=True):
            if user_message.strip():
                st.session_state.chat_history.append({"role": "user", "content": user_message})
                
                with st.spinner("Thinking..."):
                    response = ai.chat(user_message, user, st.session_state.chat_history)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                st.rerun()
    
    with col2:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Quick prompts
    st.markdown("### 💡 Quick Prompts")
    quick_prompts = [
        "How can I build better habits?",
        "I'm struggling with motivation today",
        "Help me set a meaningful goal",
        "What should I focus on this week?",
        "Give me some wisdom for the day",
    ]
    
    cols = st.columns(3)
    for i, prompt in enumerate(quick_prompts):
        with cols[i % 3]:
            if st.button(prompt, key=f"quick_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                
                with st.spinner("Thinking..."):
                    response = ai.chat(prompt, user, st.session_state.chat_history)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# SETTINGS PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def render_settings():
    user = st.session_state.user
    db = st.session_state.db
    
    st.markdown("## ⚙️ Settings")
    
    # Profile settings
    st.markdown("### 👤 Profile")
    
    new_name = st.text_input("Name", value=user["name"])
    new_display = st.text_input("Display Name", value=user.get("display_name", ""))
    
    if st.button("Save Profile", type="primary"):
        db.update_user(user["id"], name=new_name, display_name=new_display)
        st.session_state.user = db.get_user()
        st.success("Profile updated!")
        st.rerun()
    
    st.markdown("---")
    
    # Philosophy traditions
    st.markdown("### 📖 Philosophy Traditions")
    st.markdown("Choose traditions to guide your daily wisdom")
    
    current_traditions = user.get("philosophy_traditions", '["stoic"]')
    if isinstance(current_traditions, str):
        current_traditions = json.loads(current_traditions)
    
    selected = []
    cols = st.columns(3)
    for i, (key, trad) in enumerate(PHILOSOPHY_TRADITIONS.items()):
        with cols[i % 3]:
            if st.checkbox(f"{trad['emoji']} {trad['name']}", value=(key in current_traditions), key=f"trad_{key}"):
                selected.append(key)
    
    if st.button("Save Traditions"):
        db.update_user(user["id"], philosophy_traditions=json.dumps(selected or ["stoic"]))
        st.session_state.user = db.get_user()
        st.success("Traditions updated!")
        st.rerun()
    
    st.markdown("---")
    
    # Document Import
    st.markdown("### 📄 Import Document")
    st.markdown("Upload a document to extract habits, goals, and quotes using AI")
    
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf"])
    
    if uploaded_file:
        if st.button("🤖 Analyze Document"):
            with st.spinner("Analyzing document..."):
                # For simplicity, only handling text files in this version
                if uploaded_file.type == "text/plain":
                    text = uploaded_file.read().decode("utf-8")
                    ai = st.session_state.ai
                    result = ai.analyze_document(text)
                    st.session_state.doc_analysis = result
                else:
                    st.warning("PDF support requires additional libraries. Text files work best!")
    
    if "doc_analysis" in st.session_state:
        analysis = st.session_state.doc_analysis
        
        st.markdown(f"#### {analysis.get('title', 'Document Analysis')}")
        st.markdown(analysis.get("summary", ""))
        
        if analysis.get("habits"):
            st.markdown("**Extracted Habits:**")
            for h in analysis["habits"][:5]:
                st.markdown(f"• {h.get('title')}")
        
        if analysis.get("goals"):
            st.markdown("**Extracted Goals:**")
            for g in analysis["goals"][:3]:
                st.markdown(f"• {g.get('title')}")
        
        if analysis.get("quotes"):
            st.markdown("**Notable Quotes:**")
            for q in analysis["quotes"][:3]:
                st.markdown(f"*\"{q.get('quote')}\"*")
    
    st.markdown("---")
    
    # Danger zone
    st.markdown("### ⚠️ Danger Zone")
    
    if st.button("🗑️ Reset All Data", type="secondary"):
        st.warning("This will delete all your data. Type 'RESET' to confirm.")
        confirm = st.text_input("Type RESET to confirm", key="reset_confirm")
        if confirm == "RESET":
            # Delete database file and recreate
            import os
            if os.path.exists("goal_quest.db"):
                os.remove("goal_quest.db")
            st.session_state.clear()
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    # Check if user exists
    if st.session_state.user is None:
        show_onboarding()
        return
    
    # Render sidebar
    render_sidebar()
    
    # Render current page
    page = st.session_state.page
    
    if page == "dashboard":
        render_dashboard()
    elif page == "habits":
        render_habits()
    elif page == "goals":
        render_goals()
    elif page == "shop":
        render_shop()
    elif page == "analytics":
        render_analytics()
    elif page == "notes":
        render_notes()
    elif page == "coach":
        render_coach()
    elif page == "settings":
        render_settings()
    else:
        render_dashboard()


if __name__ == "__main__":
    main()
