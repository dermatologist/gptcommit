
from nltk.tokenize import WordPunctTokenizer
import subprocess
from transformers import AutoTokenizer, AutoModelWithLMHead, SummarizationPipeline
import nltk
nltk.download('punkt')

pipeline = SummarizationPipeline(
    model=AutoModelWithLMHead.from_pretrained(
        "SEBIS/code_trans_t5_base_commit_generation_multitask"),
    tokenizer=AutoTokenizer.from_pretrained(
        "SEBIS/code_trans_t5_base_commit_generation_multitask", skip_special_tokens=True)
)


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
    tokenized_list = WordPunctTokenizer().tokenize(prompt)
    message = ' '.join(tokenized_list)
    message = pipeline([message])[0]['summary_text']

    # Testing commit messages using GPT
    return message