
import subprocess
# get transformers
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
import re

# get large GPT2 tokenizer and GPT2 model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2-large")
GPT2 = TFGPT2LMHeadModel.from_pretrained(
    "gpt2-large", pad_token_id=tokenizer.eos_token_id)
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
    input_ids = tokenizer.encode(prompt, return_tensors='tf')
    greedy_output = GPT2.generate(input_ids, max_length=max_tokens, num_return_sequences=1)
    m = tokenizer.decode(greedy_output[0], skip_special_tokens=True)
    return m