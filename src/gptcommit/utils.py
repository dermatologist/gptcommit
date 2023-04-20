
import subprocess
from transformers import pipeline
import re
import nltk
from nltk.corpus import stopwords
nltk.download('words')

stop_words = set(stopwords.words('english'))
summarizer = pipeline("summarization")
words = set(nltk.corpus.words.words())

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
    prompt = ' '.join(w for w in nltk.wordpunct_tokenize(prompt) if w.lower() in words or not w.isalpha())
    prompt = ' '.join(w for w in nltk.wordpunct_tokenize(prompt) if not w.lower() in stop_words)
    s = ' '.join(w for w in nltk.wordpunct_tokenize(
        prompt) if len(w) > 1 or w == 'i' or w == 'a' or w == 'I' or w == 'A')
    l = s.split()
    k = []
    for i in l:

        # If condition is used to store unique string
        # in another list 'k'
        if (s.count(i) >= 1 and (i not in k)):
            k.append(i)
    prompt = ' '.join(k)
    print(prompt)
    m = summarizer(prompt, max_length=max_tokens, min_length=3, do_sample=False)
    return m[0]['summary_text']