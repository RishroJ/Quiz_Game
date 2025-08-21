import random
import os
import time

# ===================== THEME & UTILITIES =====================
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"


def color(txt, col):
    return f"{col}{txt}{RESET}"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def line(char="═", width=60):
    return char * width


def header(title: str):
    print(color(line(), BLUE))
    print(color(title.center(60), BOLD + CYAN))
    print(color(line(), BLUE))


def section(title: str):
    print("\n" + color(f"{title}", BOLD + MAGENTA))
    print(color(line("─"), MAGENTA))


# ===================== STORAGE (LEADERBOARD) =====================
LEADERBOARD_FILE = "leaderboard.txt"  # CSV: name,score


def load_leaderboard():
    leaderboard = []
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    name, score = parts
                    try:
                        leaderboard.append((name, int(score)))
                    except ValueError:
                        continue
    return leaderboard


def save_leaderboard(leaderboard):
    # only keep top 5
    leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)[:5]
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        for name, score in leaderboard:
            f.write(f"{name},{score}\n")
    return leaderboard


def update_leaderboard(name: str, score: int):
    board = load_leaderboard()
    board.append((name, score))
    return save_leaderboard(board)


def show_leaderboard(board):
    section("🏆 Leaderboard (Top 5)")
    if not board:
        print(color("No scores yet. Be the first!", YELLOW))
        return
    print(color(f"{'#':>2}  {'Player':<20}  {'Score':<5}", BOLD))
    for i, (name, score) in enumerate(board, start=1):
        print(f"{i:>2}  {name:<20}  {score:<5}")


# ===================== QUESTIONS BANK =====================
QUESTIONS = {
    "What does CPU stand for? ": "central processing unit",
    "What does GPU stand for? ": "graphics processing unit",
    "What does RAM stand for? ": "random access memory",
    "What does PSU stand for? ": "power supply unit",
    "What does ROM stand for? ": "read only memory",
    "What does BIOS stand for? ": "basic input output system",
    "What does URL stand for? ": "uniform resource locator",
    "What does HTTP stand for? ": "hypertext transfer protocol",
    "What does IP stand for in networking? ": "internet protocol",
    "What does LAN stand for? ": "local area network",
    "What does WAN stand for? ": "wide area network",
    "What does VPN stand for? ": "virtual private network",
    "What does USB stand for? ": "universal serial bus",
    "What does SSD stand for? ": "solid state drive",
    "What does DNS stand for? ": "domain name system",
}

# ===================== GAME LOGIC =====================


def ask_yes_no(prompt: str) -> bool:
    while True:
        ans = input(color(prompt + " (yes/no): ", CYAN)).strip().lower()
        if ans in {"y", "yes"}:
            return True
        if ans in {"n", "no"}:
            return False
        print(color("Please type yes or no.", YELLOW))


def choose_num_questions(total):
    section("⚙️  Settings")
    print(color(f"There are {total} questions available.", DIM))
    print(color("Tip: Press Enter for all questions.", DIM))
    while True:
        raw = input(
            color("How many questions do you want to attempt? ", CYAN)).strip()
        if raw == "":
            return total
        if raw.isdigit() and 1 <= int(raw) <= total:
            return int(raw)
        print(
            color(f"Enter a number between 1 and {total} or leave blank.", YELLOW))


def play_round(name: str):
    all_q = list(QUESTIONS.items())
    random.shuffle(all_q)

    q_count = choose_num_questions(len(all_q))
    asked = all_q[:q_count]

    section("🧠 Quiz Started")
    print(color("Type your answer (not case-sensitive).", DIM))

    score = 0
    start_time = time.time()

    for idx, (q, a) in enumerate(asked, start=1):
        print(color(f"\nQ{idx:02d}: {q}", BOLD))
        ans = input(color("Your answer: ", CYAN)).strip().lower()
        if ans == a:
            print(color("✅ Correct!", GREEN))
            score += 1
        else:
            print(color("❌ Incorrect!", RED), end=" ")
            print(color(f"Correct: {a.title()}", DIM))
        print(color(line("─"), MAGENTA))

    elapsed = time.time() - start_time
    percent = (score / q_count) * 100 if q_count else 0

    section("📊 Results")
    print(f"{name}, you answered {color(str(score), GREEN)}/{q_count} correctly.")
    print(f"Your score: {color(f'{percent:.2f}%', BOLD)}")
    print(color(f"Time taken: {elapsed:.1f} seconds", DIM))

    if percent >= 80:
        print(color("🎉 Excellent!", GREEN))
    elif percent >= 60:
        print(color("👍 Good job!", YELLOW))
    else:
        print(color("💪 Keep practicing!", RED))

    # update and show leaderboard
    board = update_leaderboard(name, score)
    show_leaderboard(board)


def main():
    clear_screen()
    header("COMPUTER QUIZ • Abbreviations Edition")

    name = input(color("Enter your name: ", CYAN)).strip() or "Player"

    print()
    print(color("Rules:", BOLD))
    print(color("• Answers are not case-sensitive.", DIM))
    print(color("• No negative marks.", DIM))
    print(color("• You can choose how many questions to attempt.", DIM))

    if not ask_yes_no("Ready to play?"):
        print(color("Maybe next time. Goodbye! 👋", YELLOW))
        return

    while True:
        clear_screen()
        header("COMPUTER QUIZ • Abbreviations Edition")
        print(color(f"Good luck, {name}!", BOLD))
        play_round(name)
        if not ask_yes_no("\nDo you want to play again?"):
            print(color("Thanks for playing! Goodbye 👋", CYAN))
            break


if __name__ == "__main__":
    main()
