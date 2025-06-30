# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#    WhisperNet - The Definitive Profiling Wordlister    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import itertools
import re
import sys
import configparser
import random
from datetime import datetime
from colorama import Fore, Style, init
from tqdm import tqdm

# --- Setup ---
init(autoreset=True)
CONFIG_FILE = "config.cfg"

# --- Color & Style Definitions ---
G, R, B, Y, W, C = Fore.GREEN, Fore.RED, Fore.BLUE, Fore.YELLOW, Fore.WHITE, Fore.CYAN
BO = Style.BRIGHT
p_prompt = f"{G}[+]{W}"
p_info = f"{B}[*]{W}"
p_ok = f"{G}[SUCCESS]{W}"
p_err = f"{R}[ERROR]{W}"
p_warn = f"{Y}[WARN]{W}"


def print_banner():
    """Prints a randomly selected WhisperNet banner."""

    # A list of available ASCII art banners. Add more here!
    banner_options = [
        # Banner 1: The Original
        f"""
{BO}{G}

 /$$      /$$ /$$       /$$                                         /$$   /$$             /$$    
| $$  /$ | $$| $$      |__/                                        | $$$ | $$            | $$    
| $$ /$$$| $$| $$$$$$$  /$$  /$$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$ | $$$$| $$  /$$$$$$  /$$$$$$  
| $$/$$ $$ $$| $$__  $$| $$ /$$_____/ /$$__  $$ /$$__  $$ /$$__  $$| $$ $$ $$ /$$__  $$|_  $$_/  
| $$$$_  $$$$| $$  \ $$| $$|  $$$$$$ | $$  \ $$| $$$$$$$$| $$  \__/| $$  $$$$| $$$$$$$$  | $$    
| $$$/ \  $$$| $$  | $$| $$ \____  $$| $$  | $$| $$_____/| $$      | $$\  $$$| $$_____/  | $$ /$$
| $$/   \  $$| $$  | $$| $$ /$$$$$$$/| $$$$$$$/|  $$$$$$$| $$      | $$ \  $$|  $$$$$$$  |  $$$$/
|__/     \__/|__/  |__/|__/|_______/ | $$____/  \_______/|__/      |__/  \__/ \_______/   \___/  
                                     | $$                                                        
                                     | $$                                                        
                                     |__/                                                        

""",
        # Banner 2: The "Signal"
        f"""
{BO}{G}


 █     █░ ██░ ██  ██▓  ██████  ██▓███  ▓█████  ██▀███   ███▄    █ ▓█████▄▄▄█████▓
▓█░ █ ░█░▓██░ ██▒▓██▒▒██    ▒ ▓██░  ██▒▓█   ▀ ▓██ ▒ ██▒ ██ ▀█   █ ▓█   ▀▓  ██▒ ▓▒
▒█░ █ ░█ ▒██▀▀██░▒██▒░ ▓██▄   ▓██░ ██▓▒▒███   ▓██ ░▄█ ▒▓██  ▀█ ██▒▒███  ▒ ▓██░ ▒░
░█░ █ ░█ ░▓█ ░██ ░██░  ▒   ██▒▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█▄  ▓██▒  ▐▌██▒▒▓█  ▄░ ▓██▓ ░ 
░░██▒██▓ ░▓█▒░██▓░██░▒██████▒▒▒██▒ ░  ░░▒████▒░██▓ ▒██▒▒██░   ▓██░░▒████▒ ▒██▒ ░ 
░ ▓░▒ ▒   ▒ ░░▒░▒░▓  ▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒░   ▒ ▒ ░░ ▒░ ░ ▒ ░░   
  ▒ ░ ░   ▒ ░▒░ ░ ▒ ░░ ░▒  ░ ░░▒ ░      ░ ░  ░  ░▒ ░ ▒░░ ░░   ░ ▒░ ░ ░  ░   ░    
  ░   ░   ░  ░░ ░ ▒ ░░  ░  ░  ░░          ░     ░░   ░    ░   ░ ░    ░    ░      
    ░     ░  ░  ░ ░        ░              ░  ░   ░              ░    ░  ░        
                                                                                 
                                                   
                          
""",
        # Banner 3: The "Modern"
        rf"""
{BO}{G}
 __      __.__    .__                             _______          __   
/  \    /  \  |__ |__| ____________   ___________ \      \   _____/  |_ 
\   \/\/   /  |  \|  |/  ___/\____ \_/ __ \_  __ \/   |   \_/ __ \   __\
 \        /|   Y  \  |\___ \ |  |_> >  ___/|  | \/    |    \  ___/|  |  
  \__/\  / |___|  /__/____  >|   __/ \___  >__|  \____|__  /\___  >__|  
       \/       \/        \/ |__|        \/              \/     \/      

""",
        # Banner 4"
        f"""
{BO}{G}


 ▄█     █▄     ▄█    █▄     ▄█     ▄████████    ▄███████▄    ▄████████    ▄████████ ███▄▄▄▄      ▄████████     ███     
███     ███   ███    ███   ███    ███    ███   ███    ███   ███    ███   ███    ███ ███▀▀▀██▄   ███    ███ ▀█████████▄ 
███     ███   ███    ███   ███▌   ███    █▀    ███    ███   ███    █▀    ███    ███ ███   ███   ███    █▀     ▀███▀▀██ 
███     ███  ▄███▄▄▄▄███▄▄ ███▌   ███          ███    ███  ▄███▄▄▄      ▄███▄▄▄▄██▀ ███   ███  ▄███▄▄▄         ███   ▀ 
███     ███ ▀▀███▀▀▀▀███▀  ███▌ ▀███████████ ▀█████████▀  ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   ███   ███ ▀▀███▀▀▀         ███     
███     ███   ███    ███   ███           ███   ███          ███    █▄  ▀███████████ ███   ███   ███    █▄      ███     
███ ▄█▄ ███   ███    ███   ███     ▄█    ███   ███          ███    ███   ███    ███ ███   ███   ███    ███     ███     
 ▀███▀███▀    ███    █▀    █▀    ▄████████▀   ▄████▀        ██████████   ███    ███  ▀█   █▀    ██████████    ▄████▀   
                                                                         ███    ███                                    
      
""",
        # Banner 5"
        f"""
{BO}{G}
 _       ____    _                      _   __     __ 
| |     / / /_  (_)________  ___  _____/ | / /__  / /_
| | /| / / __ \/ / ___/ __ \/ _ \/ ___/  |/ / _ \/ __/
| |/ |/ / / / / (__  ) /_/ /  __/ /  / /|  /  __/ /_  
|__/|__/_/ /_/_/____/ .___/\___/_/  /_/ |_/\___/\__/  
                   /_/                                

""",
    ]

    # Randomly select one banner from the list
    chosen_banner = random.choice(banner_options)

    print(chosen_banner)
    # The version and disclaimer are printed separately to work with any banner
    print(f"{W}                       v1.0 - The Definitive Profiling Wordlister")
    print(f"\n{'='*60}")
    print(f"Disclaimer: For legal and ethical security testing only.")
    print(f"{'='*60}\n")


# =================== START OF REPLACEMENT BLOCK ===================


def load_config():
    """Loads settings from config.cfg."""
    # This function remains the same, but is included for context.
    config = configparser.ConfigParser()
    if not config.read(CONFIG_FILE):
        print(
            f"{p_err} '{CONFIG_FILE}' not found! Please ensure it's in the same directory."
        )
        sys.exit(1)
    try:
        settings = {
            "behavior": {
                k: config.getboolean("BEHAVIOR", k) for k in config["BEHAVIOR"]
            },
            "affixes": {
                "prefixes": [
                    p.strip()
                    for p in config.get(
                        "AFFIXES", "default_prefixes", fallback=""
                    ).split(",")
                    if p
                ],
                "suffixes": [
                    s.strip()
                    for s in config.get(
                        "AFFIXES", "default_suffixes", fallback=""
                    ).split(",")
                    if s
                ],
                "years": [
                    y.strip()
                    for y in config.get("AFFIXES", "extra_years", fallback="").split(
                        ","
                    )
                    if y
                ],
            },
            "leet_map": {
                k: [v.strip() for v in val.split(",")]
                for k, val in config.items("LEETSPEAK")
            },
            "special_chars": [
                c.strip()
                for c in config.get("SPECIAL_CHARS", "all", fallback="").split(",")
                if c
            ],
            # --- ADD THIS NEW KEY ---
            "email_filter": {
                "domain_blacklist": config.get(
                    "EMAIL_FILTER", "domain_blacklist", fallback=""
                )
            },
            # --- END OF ADDITION ---
        }
        return settings
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(
            f"{p_err} Configuration file is corrupted or missing a section/option: {e}"
        )
        sys.exit(1)


# --- NEW HELPER FUNCTIONS FOR INTERACTIVE INPUT ---


def _prompt_yes_no(question):
    """A standardized yes/no prompt."""
    return input(f"{p_prompt} {question} (y/n): ").lower().strip() == "y"


def _prompt_for_person(role):
    """Prompts for a standardized set of details for a single person."""
    print(f"\n{BO}{Y}--- Enter details for {role} ---{W}")

    # Get the first name
    name = input(f"{p_prompt} Name: ").lower()
    if not name:
        print(f"{p_warn} Name is required for a person. Skipping this entry.")
        return None

    surname = ""
    # 2. Only ask for the surname if the role is the "Target".
    if role == "Target":
        surname = input(f"{p_prompt} Surname (optional): ").lower()

    # Get the other details
    nickname = input(f"{p_prompt} Nickname (optional): ").lower()
    dob = input(f"{p_prompt} Date of Birth (YYYY-MM-DD, optional): ")

    return {
        "role": role,
        "name": name,
        "surname": surname,
        "nickname": nickname,
        "dob": dob,
    }


def _prompt_for_list(prompt_text):
    """Prompts for a list of items until the user is done."""
    items = []
    while True:
        item = input(f"{p_prompt} {prompt_text} (or press Enter to finish): ").lower()
        if not item:
            break
        items.append(item)
    return items


# --- COMPLETELY REWRITTEN get_user_info FUNCTION ---


def get_user_info():
    """Gathers all personal information using an interactive, looping flow."""
    info = {"people": [], "emails": [], "phones": [], "vehicles": [], "keywords": {}}

    # --- Target ---
    target_details = _prompt_for_person("Target")
    if target_details:
        info["people"].append(target_details)

    # --- Family ---
    if _prompt_yes_no("Add Father's details?"):
        details = _prompt_for_person("Father")
        if details:
            info["people"].append(details)

    if _prompt_yes_no("Add Mother's details?"):
        details = _prompt_for_person("Mother")
        if details:
            info["people"].append(details)

    if _prompt_yes_no("Add Partner/Spouse's details?"):
        details = _prompt_for_person("Partner")
        if details:
            info["people"].append(details)

    while _prompt_yes_no("Add a Child?"):
        details = _prompt_for_person("Child")
        if details:
            info["people"].append(details)

    # --- Identifiers & Keywords ---
    print(f"\n{BO}{Y}--- Enter Identifiers & Keywords ---{W}")
    if _prompt_yes_no("Add Email address(es)?"):
        info["emails"] = _prompt_for_list("Email address")

    if _prompt_yes_no("Add Phone number(s)?"):
        info["phones"] = _prompt_for_list("Phone number")

    if _prompt_yes_no("Add Vehicle plate(s)?"):
        info["vehicles"] = _prompt_for_list("Vehicle plate")

    # My "Good Addition" -> Address details are critical
    info["keywords"]["house_no"] = input(
        f"{p_prompt} House Number (optional): "
    ).lower()
    info["keywords"]["street_name"] = input(
        f"{p_prompt} Street Name (optional): "
    ).lower()
    info["keywords"]["city"] = input(f"{p_prompt} City/Town (optional): ").lower()
    info["keywords"]["company"] = input(f"{p_prompt} Company Name (optional): ").lower()

    if _prompt_yes_no("Add other custom keywords (pets, hobbies, etc.)?"):
        info["keywords"]["custom"] = _prompt_for_list("Keyword")

    return info


# --- COMPLETELY WRITTEN parse_data FUNCTION ---


def parse_data(info, config):
    """Parses the new, structured info into clean lists of base words and numbers."""
    base_words = set()
    base_numbers = set()

    # Contextual relationship keywords
    relationship_keywords = {
        "Father": ["dad", "papa", "father"],
        "Mother": ["mom", "mama", "mother"],
        "Partner": ["love", "baby"],
        "Child": ["son", "daughter", "kid"],
    }

    # 1. Parse People (This section already handles adding the DOB year)
    for person in info["people"]:
        if person.get("name"):
            base_words.add(person["name"])
        if person.get("surname"):
            base_words.add(person["surname"])
        if person.get("nickname"):
            base_words.add(person["nickname"])

        role = person.get("role")
        if role in relationship_keywords:
            base_words.update(relationship_keywords[role])

        # This part already adds the specific year from the date of birth entered
        if person.get("dob"):
            try:
                dt = datetime.strptime(person["dob"], "%Y-%m-%d")
                base_numbers.update(
                    [
                        str(dt.year),
                        str(dt.year)[-2:],
                        f"{dt.day:02d}",
                        f"{dt.month:02d}",
                        f"{dt.day:02d}{dt.month:02d}",
                        f"{dt.day:02d}{dt.month:02d}{dt.year}",
                    ]
                )
            except ValueError:
                print(
                    f"{p_warn} Invalid date format for {person['name']}'s DOB. Skipping."
                )

    # 2. Parse Emails, Phones, Vehicles (This part remains the same)
    for email in info.get("emails", []):
        base_words.update(p for p in re.split(r"[@._-]", email) if p)

    for phone in info.get("phones", []):
        num = re.sub(r"\D", "", phone)
        if len(num) >= 4:
            base_numbers.add(num[-4:])
        if len(num) > 4:
            base_numbers.add(num)

    for plate in info.get("vehicles", []):
        parts = re.findall(r"[a-zA-Z]+|\d+", plate)
        base_words.update(p for p in parts if not p.isdigit())
        base_numbers.update(p for p in parts if p.isdigit())

    # 3. Parse Other Keywords (This part remains the same)
    for value in info.get("keywords", {}).values():
        if isinstance(value, list):
            base_words.update(v for v in value if v)
        elif isinstance(value, str) and value:
            base_words.add(value)

    # --- NEW: DYNAMIC YEAR GENERATION ---
    # 4. Add dynamic years based on the current date
    current_year = datetime.now().year
    dynamic_years = [
        str(current_year - 2),
        str(current_year - 1),
        str(current_year),
        str(current_year + 1),
        str(current_year + 2),
    ]
    base_numbers.update(dynamic_years)

    # 5. Add any years manually set in config.cfg as a fallback
    base_numbers.update(config["affixes"]["years"])

    # 6. Clean up and return
    base_words.discard("")
    base_numbers.discard("")

    return list(base_words), list(base_numbers)


def get_generation_options(config):
    """Asks the user for dynamic generation options."""
    options = {}
    print(f"\n{BO}{C}{'='*20} [ Generation Options ] {'='*19}{W}")

    # Special Chars
    use_all_specials = (
        input(f"{p_prompt} Use ALL special characters for affixes? (y/n): ").lower()
        == "y"
    )
    if use_all_specials:
        options["prefixes"] = config["special_chars"]
        options["suffixes"] = config["special_chars"]
        print(f"{p_info} Using all special characters.")
    else:
        options["prefixes"] = config["affixes"]["prefixes"]
        options["suffixes"] = config["affixes"]["suffixes"]
        print(
            f"{p_info} Using default prefixes: {BO}{', '.join(options['prefixes'])}{W}"
        )
        print(
            f"{p_info} Using default suffixes: {BO}{', '.join(options['suffixes'])}{W}"
        )

    # Blank Spaces
    options["space_range"] = None
    if input(f"{p_prompt} Generate blank space passwords? (y/n): ").lower() == "y":
        options["space_range"] = input(
            f"{p_prompt}   Enter length or range for spaces (e.g., 8 or 8-12): "
        )

    # Length Filter  (REMOVED)
    # options['length_filter'] = None
    # if input(f"{p_prompt} Filter final wordlist by length? (y/n): ").lower() == 'y':
    #    options['length_filter'] = input(f"{p_prompt}   Enter length or range (e.g., 8 or 8-16): ")

    # NEW: Desired Password Length
    options["desired_length"] = input(
        f"{p_prompt} Enter desired password length (or leave blank for no length restriction): "
    )

    return options


# --- MODIFIED FUNCTION ---
def generate_combinations(base_words, base_numbers, config):
    """
    Generates a base wordlist by combining the user's full words and numbers.
    Length filtering will be applied later, after all mutations.
    """
    combinations = set(base_words + base_numbers)

    # 1. Word + Number combinations
    print(f"{p_info} Combining base words and numbers...")
    for word in base_words:
        for num in base_numbers:
            combinations.add(word + num)
            combinations.add(num + word)

    # 2. Word + Word combinations (if enabled)
    if config["behavior"]["combine_base_words"] and len(base_words) > 1:
        print(f"{p_info} Combining words with other words...")
        # Use permutations to get all ordered pairs (e.g., john+smith and smith+john)
        for combo in itertools.permutations(base_words, 2):
            combinations.add("".join(combo))

    return combinations


def parse_range(range_str):
    """Parses a string like '8' or '8-12' into min, max integers."""
    if not range_str:
        return None, None
    if "-" in range_str:
        parts = range_str.split("-")
        try:
            return int(parts[0].strip()), int(parts[1].strip())
        except (ValueError, IndexError):
            return None, None
    else:
        try:
            val = int(range_str.strip())
            return val, val
        except ValueError:
            return None, None


def parse_data(info, config):
    """Parses the new, structured info into clean lists of base words and numbers."""
    base_words = set()
    base_numbers = set()

    # Contextual relationship keywords
    relationship_keywords = {
        "Father": ["dad", "papa", "father"],
        "Mother": ["mom", "mama", "mother"],
        "Partner": ["love", "baby"],
        "Child": ["son", "daughter"],
    }

    # 1. Parse People
    for person in info["people"]:
        if person.get("name"):
            base_words.add(person["name"])
        if person.get("surname"):
            base_words.add(person["surname"])
        if person.get("nickname"):
            base_words.add(person["nickname"])

        # Add relationship keywords based on the person's role
        role = person.get("role")
        if role in relationship_keywords:
            base_words.update(relationship_keywords[role])

        # Parse Date of Birth
        if person.get("dob"):
            try:
                dt = datetime.strptime(person["dob"], "%Y-%m-%d")
                base_numbers.update(
                    [
                        str(dt.year),
                        str(dt.year)[-2:],
                        f"{dt.day:02d}",
                        f"{dt.month:02d}",
                        f"{dt.day:02d}{dt.month:02d}",
                        f"{dt.day:02d}{dt.month:02d}{dt.year}",
                    ]
                )
            except ValueError:
                print(
                    f"{p_warn} Invalid date format for {person['name']}'s DOB. Skipping."
                )

    # 2. Parse Emails, Phones, Vehicles
    # Access the blacklist from the config DICTIONARY.
    # The .get() calls prevent errors if the keys don't exist.
    blacklist_str = config.get("email_filter", {}).get("domain_blacklist", "")
    domain_blacklist = {
        item.strip() for item in blacklist_str.split(",") if item.strip()
    }

    for email in info.get("emails", []):
        # Split the email into parts
        parts = re.split(r"[@._-]", email)
        # Add only the parts that are NOT in our blacklist
        base_words.update(p for p in parts if p and p.lower() not in domain_blacklist)

    for phone in info.get("phones", []):
        num = re.sub(r"\D", "", phone)
        if len(num) >= 4:
            base_numbers.add(num[-4:])
        if len(num) > 4:
            base_numbers.add(num)

    for plate in info.get("vehicles", []):
        parts = re.findall(r"[a-zA-Z]+|\d+", plate)
        base_words.update(p for p in parts if not p.isdigit())
        base_numbers.update(p for p in parts if p.isdigit())

    # 3. Parse Other Keywords (This is the critical fix for your keyword issue)
    for value in info.get("keywords", {}).values():
        if isinstance(value, list):
            base_words.update(v for v in value if v)
        elif isinstance(value, str) and value:
            base_words.add(value)

    # 4. Add config years and clean up
    base_numbers.update(config["affixes"]["years"])
    base_words.discard("")
    base_numbers.discard("")

    return list(base_words), list(base_numbers)


def apply_leetspeak(word, leet_map):
    """
    Generates leetspeak variations one at a time using a generator.
    This avoids building the entire set of variations in memory.
    """
    options = []
    for char in word:
        options.append([char] + leet_map.get(char, []))

    for leetspeak_tuple in itertools.product(*options):
        yield "".join(leetspeak_tuple)


# --- START OF NEW FUNCTION ---


def generate_custom_patterns(info, config):
    """
    Generates a wordlist based on a specific, fixed set of common password patterns
    for ALL individuals entered by the user.
    """
    print(f"\n{BO}{C}{'='*15} [ Custom Pattern Generation ] {'='*14}{W}")
    custom_wordlist = set()

    # Relationship keywords, similar to parse_data, for targeted words
    relationship_keywords = {
        "Father": ["dad", "papa"],
        "Mother": ["mom", "mama"],
        "Partner": ["love", "baby"],
    }

    # Get the default signs for patterns like name@bday
    default_signs = config.get("affixes", {}).get("prefixes", ["@"])

    # --- THE MAIN LOOP: Process EVERY person ---
    print(f"{p_info} Generating specific patterns for all individuals...")
    for person in info["people"]:
        name = person.get("name")
        surname = person.get("surname")
        role = person.get("role")

        # Helper to get date formats
        try:
            dt = datetime.strptime(person.get("dob", ""), "%Y-%m-%d")
            dates = {"year": str(dt.year), "mmdd": f"{dt.month:02d}{dt.day:02d}"}
        except ValueError:
            dates = None

        # --- PATTERN 1: Name and Surname combinations ---
        if name and surname:
            custom_wordlist.add(name + surname)
            custom_wordlist.add(surname + name)

        # --- PATTERN 2: Name and Birth Year ---
        if name and dates:
            custom_wordlist.add(name + dates["year"])

        # --- PATTERN 3: Name and Relationship Keywords ---
        if name and role in relationship_keywords:
            for keyword in relationship_keywords[role]:
                custom_wordlist.add(name + keyword)
                custom_wordlist.add(keyword + name)

        # --- PATTERN 4: Birthday and Name with signs (name@bday, etc.) ---
        if name and dates:
            for sign in default_signs:
                custom_wordlist.add(name + sign + dates["mmdd"])
                custom_wordlist.add(dates["mmdd"] + sign + name)

    print(
        f"{p_ok} Custom pattern generation complete. Added {BO}{len(custom_wordlist)}{W} unique passwords."
    )
    return custom_wordlist


def main():
    """Main function to drive the tool."""
    print_banner()
    config = load_config()
    user_info = get_user_info()

    # This will hold ALL passwords from all methods
    final_wordlist = set()

    # --- NEW LOGIC: Ask to ADD custom patterns ---
    print(f"\n{BO}{C}{'='*19} [ Generation Mode ] {'='*20}{W}")
    if _prompt_yes_no(
        "Add specific custom patterns (e.g., name@bday) to the wordlist?"
    ):
        # Run the custom generator and UPDATE the main list
        custom_patterns = generate_custom_patterns(user_info, config)
        final_wordlist.update(custom_patterns)

    # --- ALWAYS RUN THE FULL MUTATION ENGINE ---
    print(f"\n{BO}{Y}--- Starting Full Mutation Engine ---{W}")
    gen_options = get_generation_options(config)

    # Stage 1: Data Parsing
    print(f"\n{BO}{C}{'='*20} [ Stage 1: Data Parsing ] {'='*20}{W}")
    base_words, base_numbers = parse_data(user_info, config)
    print(
        f"{p_info} Found {BO}{len(base_words)}{W} unique base words and {BO}{len(base_numbers)}{W} unique numbers."
    )

    # Stage 2: Combination Generation
    print(f"\n{BO}{C}{'='*15} [ Stage 2: Combination Generation ] {'='*14}{W}")
    # Generate standard combinations and add them to our list
    standard_combinations = generate_combinations(base_words, base_numbers, config)
    final_wordlist.update(standard_combinations)
    print(f"{p_info} Wordlist size after combinations: {BO}{len(final_wordlist)}{W}")

    # Stage 3: Mutations
    print(f"\n{BO}{C}{'='*22} [ Stage 3: Mutations ] {'='*23}{W}")
    current_passwords = list(final_wordlist)
    mutations_to_add = set()

    print(f"{p_info} Applying Case & Leetspeak mutations...")
    for word in tqdm(
        current_passwords, desc=f"{C}Case & Leet{W}     ", unit="word", ncols=100
    ):
        if config["behavior"]["use_case_mutations"]:
            mutations_to_add.add(word.capitalize())
        if config["behavior"]["use_leetspeak"] and any(
            c in config["leet_map"] for c in word
        ):
            mutations_to_add.update(apply_leetspeak(word, config["leet_map"]))
    final_wordlist.update(mutations_to_add)
    print(f"{p_info} After case & leetspeak mutations: {BO}{len(final_wordlist)}{W}")

    if config["behavior"]["add_affixes"]:
        print(f"{p_info} Applying Affixes...")
        current_passwords = list(final_wordlist)
        affixes_to_add = set()
        for word in tqdm(
            current_passwords, desc=f"{C}Applying Affixes{W} ", unit="word", ncols=100
        ):
            for prefix in gen_options["prefixes"]:
                affixes_to_add.add(prefix + word)
            for suffix in gen_options["suffixes"]:
                affixes_to_add.add(word + suffix)
        final_wordlist.update(affixes_to_add)
        print(f"{p_info} After affixes: {BO}{len(final_wordlist)}{W}")

    # Stage 4: Final Touches (Length filter, etc.)
    print(f"\n{BO}{C}{'='*20} [ Stage 4: Final Touches ] {'='*21}{W}")
    desired_length_str = gen_options.get("desired_length")
    if desired_length_str:
        try:
            desired_length = int(desired_length_str)
            print(
                f"{p_info} Filtering wordlist to a fixed length of {BO}{desired_length}{W} characters..."
            )
            initial_count = len(final_wordlist)
            final_wordlist = {w for w in final_wordlist if len(w) == desired_length}
            removed_count = initial_count - len(final_wordlist)
            print(f"{p_info} Length filter removed {BO}{removed_count}{W} words.")
        except ValueError:
            print(f"{p_warn} Invalid desired length provided. Skipping length filter.")

    min_s, max_s = parse_range(gen_options["space_range"])
    if min_s is not None:
        print(f"{p_info} Adding space-only passwords from length {min_s} to {max_s}.")
        for length in range(min_s, max_s + 1):
            final_wordlist.add(" " * length)

    # Stage 5: Output
    print(f"\n{p_ok} Total unique words generated: {BO}{len(final_wordlist)}{W}")
    print(f"\n{BO}{C}{'='*23} [ Stage 5: Output ] {'='*24}{W}")
    output_filename = (
        input(f"{p_prompt} Enter the name for the output file (e.g., wordlist.txt): ")
        or "wordlist.txt"
    )

    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            sorted_wordlist = sorted(list(final_wordlist))
            f.write("\n".join(sorted_wordlist))
        print(
            f"\n{p_ok} Wordlist with {BO}{len(final_wordlist)}{W} passwords saved to '{BO}{output_filename}{W}'"
        )
    except Exception as e:
        print(f"\n{p_err} Could not write to file: {e}")


if __name__ == "__main__":
    main()
