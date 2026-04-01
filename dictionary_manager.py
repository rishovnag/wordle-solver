"""
DictionaryManager: Loads and manages the word dictionary for Wordle.
Supports loading from file with a built-in fallback word list.
"""

import os
import random
from collections import Counter
from typing import Optional


class DictionaryManager:
    DICT_FILE = "words.txt"
    WORD_LENGTH = 5

    def __init__(self):
        self._random = random.Random()
        self._valid_words: set[str] = set()
        self._answer_words: list[str] = []
        print("Loading dictionary...")
        self._load_dictionary()

    def _load_dictionary(self) -> None:
        if self._load_from_current_directory():
            print(f"SUCCESS: Loaded dictionary from current directory: {len(self._valid_words)} words")
        elif self._load_from_script_directory():
            print(f"SUCCESS: Loaded dictionary from script directory: {len(self._valid_words)} words")
        elif self._load_from_project_paths():
            print(f"SUCCESS: Loaded dictionary from project path: {len(self._valid_words)} words")
        else:
            self._load_fallback_words()
            print(f"SUCCESS: Using built-in fallback dictionary: {len(self._valid_words)} words")
            print("INFO: For full dictionary, place words.txt in your project directory")

        # Create answer list (filter for better gameplay)
        self._answer_words = [w for w in self._valid_words if self._is_good_answer_word(w)]
        if not self._answer_words:
            self._answer_words = list(self._valid_words)

        print(f"SUCCESS: Answer pool contains: {len(self._answer_words)} words")
        print("Dictionary loaded successfully!\n")

    def _load_from_current_directory(self) -> bool:
        try:
            path = self.DICT_FILE
            if os.path.isfile(path):
                print("Reading words.txt from current directory...")
                with open(path, "r") as f:
                    self._process_word_content(f.read())
                return bool(self._valid_words)
        except Exception as e:
            print(f"Could not load from current directory: {e}")
        return False

    def _load_from_script_directory(self) -> bool:
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(script_dir, self.DICT_FILE)
            if os.path.isfile(path):
                print("Reading words.txt from script directory...")
                with open(path, "r") as f:
                    self._process_word_content(f.read())
                return bool(self._valid_words)
        except Exception as e:
            print(f"Could not load from script directory: {e}")
        return False

    def _load_from_project_paths(self) -> bool:
        possible_paths = [
            "../words.txt",
            "../../words.txt",
            "./src/main/resources/words.txt",
        ]
        for path_str in possible_paths:
            try:
                if os.path.isfile(path_str):
                    print(f"Reading words.txt from: {path_str}")
                    with open(path_str, "r") as f:
                        self._process_word_content(f.read())
                    if self._valid_words:
                        return True
            except Exception:
                pass
        return False

    def _process_word_content(self, content: str) -> None:
        for line in content.splitlines():
            word = line.strip().upper()
            if len(word) == self.WORD_LENGTH and word.isalpha():
                self._valid_words.add(word)

    def _load_fallback_words(self) -> None:
        words = [
            "ABOUT", "ABOVE", "ABUSE", "ACTOR", "ACUTE", "ADMIT", "ADOPT", "ADULT", "AFTER", "AGAIN",
            "AGENT", "AGREE", "AHEAD", "ALARM", "ALBUM", "ALERT", "ALIEN", "ALIGN", "ALIKE", "ALIVE",
            "ALLOW", "ALONE", "ALONG", "ALTER", "AMONG", "ANGER", "ANGLE", "ANGRY", "APART", "APPLE",
            "APPLY", "ARENA", "ARGUE", "ARISE", "ARRAY", "ASIDE", "ASSET", "AVOID", "AWAKE", "AWARD",
            "AWARE", "BADLY", "BAKER", "BASES", "BASIC", "BATCH", "BEACH", "BEGAN", "BEGIN", "BEING",
            "BELLY", "BELOW", "BENCH", "BILLY", "BIRTH", "BLACK", "BLAME", "BLANK", "BLAST", "BLIND",
            "BLOCK", "BLOOD", "BLOOM", "BOARD", "BOAST", "BOOST", "BOOTH", "BOUND", "BRAIN", "BRAND",
            "BRASS", "BRAVE", "BREAD", "BREAK", "BREED", "BRIEF", "BRING", "BROAD", "BROKE", "BROWN",
            "BUILD", "BUILT", "BURST", "BUYER", "CABLE", "CARRY", "CATCH", "CAUSE", "CHAIN", "CHAIR",
            "CHAOS", "CHARM", "CHART", "CHASE", "CHEAP", "CHECK", "CHEST", "CHIEF", "CHILD", "CHINA",
            "CHOSE", "CIVIL", "CLAIM", "CLASS", "CLEAN", "CLEAR", "CLICK", "CLIMB", "CLOCK", "CLOSE",
            "CLOUD", "COACH", "COAST", "COULD", "COUNT", "COURT", "COVER", "CRAFT", "CRASH", "CRAZY",
            "CREAM", "CRIME", "CROSS", "CROWD", "CROWN", "CRUDE", "CURVE", "CYCLE", "DAILY", "DANCE",
            "DATED", "DEALT", "DEATH", "DEBUT", "DELAY", "DEPTH", "DOING", "DOUBT", "DOZEN", "DRAFT",
            "DRAMA", "DRANK", "DRAWN", "DREAM", "DRESS", "DRILL", "DRINK", "DRIVE", "DROVE", "DYING",
            "EAGER", "EARLY", "EARTH", "EIGHT", "ELITE", "EMPTY", "ENEMY", "ENJOY", "ENTER", "ENTRY",
            "EQUAL", "ERROR", "EVENT", "EVERY", "EXACT", "EXIST", "EXTRA", "FAITH", "FALSE", "FAULT",
            "FIBER", "FIELD", "FIFTH", "FIFTY", "FIGHT", "FINAL", "FIRST", "FIXED", "FLASH", "FLEET",
            "FLOOR", "FLUID", "FOCUS", "FORCE", "FORTH", "FORTY", "FORUM", "FOUND", "FRAME", "FRANK",
            "FRAUD", "FRESH", "FRONT", "FRUIT", "FULLY", "FUNNY", "GIANT", "GIVEN", "GLASS", "GLOBE",
            "GOING", "GRACE", "GRADE", "GRAND", "GRANT", "GRASS", "GRAVE", "GREAT", "GREEN", "GROSS",
            "GROUP", "GROWN", "GUARD", "GUESS", "GUEST", "GUIDE", "HAPPY", "HEART", "HEAVY", "HENCE",
            "HORSE", "HOTEL", "HOUSE", "HUMAN", "HURRY", "IMAGE", "INDEX", "INNER", "INPUT", "ISSUE",
            "JOINT", "JUDGE", "KNOWN", "LABEL", "LARGE", "LASER", "LATER", "LAUGH", "LAYER", "LEARN",
            "LEASE", "LEAST", "LEAVE", "LEGAL", "LEVEL", "LIGHT", "LIMIT", "LINKS", "LIVES", "LOCAL",
            "LOOSE", "LOWER", "LUCKY", "LUNCH", "LYING", "MAGIC", "MAJOR", "MAKER", "MARCH", "MATCH",
            "MAYBE", "MAYOR", "MEANT", "MEDAL", "MEDIA", "METAL", "MIGHT", "MINOR", "MINUS", "MIXED",
            "MODEL", "MONEY", "MONTH", "MORAL", "MOTOR", "MOUNT", "MOUSE", "MOUTH", "MOVED", "MOVIE",
            "MUSIC", "NEEDS", "NEVER", "NEWLY", "NIGHT", "NOISE", "NORTH", "NOTED", "NOVEL", "NURSE",
            "OCCUR", "OCEAN", "OFFER", "OFTEN", "ORDER", "OTHER", "OUGHT", "PAINT", "PANEL", "PAPER",
            "PARTY", "PEACE", "PHASE", "PHONE", "PHOTO", "PIANO", "PIECE", "PILOT", "PITCH", "PLACE",
            "PLAIN", "PLANE", "PLANT", "PLATE", "POINT", "POUND", "POWER", "PRESS", "PRICE", "PRIDE",
            "PRIME", "PRINT", "PRIOR", "PRIZE", "PROOF", "PROUD", "PROVE", "QUEEN", "QUICK", "QUIET",
            "QUITE", "RADIO", "RAISE", "RANGE", "RAPID", "RATIO", "REACH", "READY", "REALM", "REBEL",
            "REFER", "RELAX", "REPAY", "REPLY", "RIGHT", "RIGID", "RIVAL", "RIVER", "ROUGH", "ROUND",
            "ROUTE", "ROYAL", "RURAL", "SCALE", "SCENE", "SCOPE", "SCORE", "SENSE", "SERVE", "SETUP",
            "SEVEN", "SHALL", "SHAPE", "SHARE", "SHARP", "SHEET", "SHELF", "SHELL", "SHIFT", "SHINE",
            "SHIRT", "SHOCK", "SHOOT", "SHORT", "SHOWN", "SIGHT", "SILLY", "SINCE", "SIXTH", "SIXTY",
            "SIZED", "SKILL", "SLEEP", "SLIDE", "SMALL", "SMART", "SMILE", "SMITH", "SMOKE", "SOLID",
            "SOLVE", "SORRY", "SOUND", "SOUTH", "SPACE", "SPARE", "SPEAK", "SPEED", "SPEND", "SPENT",
            "SPLIT", "SPOKE", "SPORT", "STAFF", "STAGE", "STAKE", "STAND", "START", "STATE", "STEAM",
            "STEEL", "STEEP", "STEER", "STICK", "STILL", "STOCK", "STONE", "STOOD", "STORE", "STORM",
            "STORY", "STRIP", "STUCK", "STUDY", "STUFF", "STYLE", "SUGAR", "SUITE", "SUPER", "SWEET",
            "TABLE", "TAKEN", "TASTE", "TAXES", "TEACH", "TEETH", "TEXAS", "THANK", "THEFT", "THEIR",
            "THERE", "THESE", "THICK", "THING", "THINK", "THIRD", "THOSE", "THREE", "THREW", "THROW",
            "THUMB", "TIGHT", "TIRED", "TITLE", "TODAY", "TOPIC", "TOTAL", "TOUCH", "TOUGH", "TOWER",
            "TRACK", "TRADE", "TRAIN", "TREAT", "TREND", "TRIAL", "TRIBE", "TRICK", "TRIED", "TRIES",
            "TRUCK", "TRULY", "TRUNK", "TRUST", "TRUTH", "TWICE", "UNCLE", "UNDUE", "UNION", "UNITY",
            "UNTIL", "UPPER", "UPSET", "URBAN", "USAGE", "USUAL", "VALID", "VALUE", "VIDEO", "VIRUS",
            "VISIT", "VITAL", "VOCAL", "VOICE", "WASTE", "WATCH", "WATER", "WHEEL", "WHERE", "WHICH",
            "WHILE", "WHITE", "WHOLE", "WHOSE", "WOMAN", "WOMEN", "WORLD", "WORRY", "WORSE", "WORST",
            "WORTH", "WOULD", "WRITE", "WRONG", "WROTE", "YOUNG", "YOUTH", "SLATE", "CRANE", "ADIEU",
            "AUDIO", "TEARS", "ROAST", "STARE", "HOUSE", "MOUSE", "HEART", "SMART", "TRADE", "BLADE",
            "SHADE", "GAMES", "TALES", "WAVES", "BRAVE", "GRAVE", "FRAME", "SPACE", "PLACE", "TRACE",
        ]
        self._valid_words.update(words)

    def _is_good_answer_word(self, word: str) -> bool:
        """Filter for good answer words to ensure fair and enjoyable gameplay."""
        # 1. Exclude words with very rare letters
        very_rare = "QXZ"
        if any(c in word for c in very_rare):
            return False

        # 2. Limit words with multiple uncommon letters
        uncommon = "JFVW"
        uncommon_count = sum(1 for c in uncommon if c in word)
        if uncommon_count > 1:
            return False

        # 3. No letter should appear more than twice
        counts = Counter(word)
        if any(v > 2 for v in counts.values()):
            return False

        return True

    def is_valid_word(self, word: str) -> bool:
        return word.upper() in self._valid_words

    def get_random_answer(self) -> str:
        if not self._answer_words:
            return self._random.choice(list(self._valid_words))
        return self._random.choice(self._answer_words)

    def get_all_words(self) -> set[str]:
        return set(self._valid_words)

    @property
    def total_words_count(self) -> int:
        return len(self._valid_words)

    @property
    def answer_words_count(self) -> int:
        return len(self._answer_words)
