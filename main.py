#!/usr/bin/env python3
import argparse, subprocess, sys

def choose_language(cli_lang):
    if cli_lang in ("en", "pl"):
        return cli_lang
    while True:
        lang = input("Choose language [en/pl]: ").strip().lower()
        if lang in ("en", "pl"):
            return lang
        print("Please enter 'en' or 'pl'.")

def main():
    p = argparse.ArgumentParser(description="Run English or Polish Solitaire")
    p.add_argument("-l", "--lang", choices=("en", "pl"),
                   help="language: en or pl")
    args = p.parse_args()

    lang = choose_language(args.lang)
    script = f"game_{lang}.py"   # make sure your files are named game_en.py / game_pl.py

    # Spawn a fresh Python interpreter to run the chosen script:
    rc = subprocess.call([sys.executable, script])
    sys.exit(rc)

if __name__ == "__main__":
    main()
