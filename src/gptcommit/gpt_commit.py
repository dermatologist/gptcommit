import os
import subprocess
import sys
from . import utils




def gpt_commit():
    utils.is_git_repo()
    diff = utils.get_diff(diff_per_file=True)
    print(diff)
