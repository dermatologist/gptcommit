
import subprocess
from transformers import pipeline
import re

summarizer = pipeline("summarization")

whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')

def is_git_repo() -> bool:
    try:
        subprocess.check_output(
            "git rev-parse --is-inside-work-tree", shell=True, stderr=subprocess.STDOUT
        )
        return True
    except subprocess.CalledProcessError:
        return False

def get_diff(diff_per_file: bool) -> str:
    if diff_per_file:
        diff = subprocess.check_output(
            "git diff --cached --name-only",
            shell=True,
            stderr=subprocess.STDOUT,
        ).decode("utf-8")

        files_changed = diff.split("\n")[:-1]
        diff_string = ""
        for file in files_changed:
            diff_string += subprocess.check_output(
                f"git diff --cached -- {file}",
                shell=True,
                stderr=subprocess.STDOUT,
            ).decode("utf-8")
    else:
        diff_string = subprocess.check_output(
            "git diff --cached .",
            shell=True,
            stderr=subprocess.STDOUT,
        ).decode("utf-8")

    return diff_string


def get_commit_message(prompt: str, language: str = "english", max_tokens=10) -> str:
    # prompt = f"What follows '-------' is a git diff for a potential commit. Reply with an appropriate git commit message(a Git commit message should be concise but also try to describe the important changes in the commit) and don't include any other text but the message in your response. ------- {prompt}, language={language}"
    # m = generator(prompt, max_new_tokens=max_tokens, num_return_sequences=1)
    # print(m)
    # return "Hello World"
    # prompt = ''.join(filter(whitelist.__contains__, prompt))
    prompt = re.sub('[^a-zA-Z]+', ' ', prompt)
    print(prompt)
    m = summarizer(prompt, max_length=100, min_length=10, do_sample=False)
    return m