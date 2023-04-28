import os
import subprocess
import sys
from .utils import is_git_repo, get_diff, get_commit_message
import inquirer

from gptcommit import __version__

def gpt_commit():
    is_git_repo()

    diff_per_file = False
    commit_conventional = True
    commit_language = "en"
    commit_tokens = 15

    # Check for flags
    if len(sys.argv) > 1:
        if "--help" in sys.argv:
            print(
                "Usage: python gpt_commit.py [--diff-per-file] [--conventional] [--language <language>] [--choice <choice>]\n"
            )
            print("Flags:")
            print("  --diff-per-file     Generate commit message per changed file")
            print("  --conventional      Use conventional commit format")
            print(
                "  --language          Language for generated commit message (default: en)"
            )
            print(
                "  --tokens            Choose number of tokens (default: 200)\n"
            )
            sys.exit(0)

        flags = sys.argv[1:]

        if "--diff-per-file" in flags:
            diff_per_file = True

        if "--conventional" in flags:
            commit_conventional = True

        if "--language" in flags:
            language_index = flags.index("--language")
            commit_language = flags[language_index + 1]

        if "--tokens" in flags:
            tokens_index = flags.index("--tokens")
            commit_tokens = int(flags[tokens_index + 1])

    diff = get_diff(diff_per_file)

    if not diff:
        print(
            "No staged changes found. Make sure there are changes and run `git add .`"
        )
        sys.exit(1)

    # Accounting for GPT-3's input requirement of 4k tokens (approx 8k chars)
    if len(diff) > 8000:
        print(
            "The diff is too large to write a commit message for. Please split your changes into multiple commits."
        )
        sys.exit(1)
    selected_message = get_commit_message(diff, commit_language, commit_tokens)

    if commit_conventional:
        conventional_choices = [
            "feat",
            "fix",
            "docs",
            "style",
            "refactor",
            "test",
            "chore",
        ]
        commit_type = inquirer.prompt(
        [
            inquirer.List(
                "conventional_choice",
                message="What type of change are you making?",
                choices=conventional_choices,
            )
        ]
        )

    if commit_type:
        selected_message = f"{commit_type['conventional_choice']}: {selected_message}"

    print(f"Commit Message:\n{selected_message}")

    confirmation_message = inquirer.prompt(
        [
            inquirer.List(
                "use_commit_message",
                message="Would you like to use this commit message?",
                choices=["y", "n"],
                default="y",
            )
        ]
    )




    if confirmation_message["use_commit_message"] == "n":
        print("Commit message has not been committed.")
        sys.exit(1)

    subprocess.run(["git", "commit", "-m", f"{str(selected_message)}"])


if __name__ == "__main__":
    gpt_commit()