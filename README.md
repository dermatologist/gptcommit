# gptcommit

The gptcommit is a command-line tool that generates commit messages for your Git commits. This tool uses [this model](https://huggingface.co/SEBIS/code_trans_t5_base_commit_generation_multitask) to analyze your code changes and suggest relevant commit messages, and is a modification of [this repository](https://github.com/Nneji123/aicommit). Yes, you guessed it right, ChatGPT wrote this README :)

## Installation

To use the gptcommit, you will need to have Python 3 installed on your computer. You can then install the tool using pip:

```

pip install git+https://github.com/dermatologist/gptcommit

```

## Usage

Once installed, you can use the tool by navigating to the directory containing your Git repository and running the following command:

```
gptcommit
```

The tool will then analyze your code changes and suggest a relevant commit message. You can then choose to accept the suggestion or generate a new message.


```
gptcommit --help
```

## Contributing

If you would like to contribute to the gptcommit, feel free to open a pull request on GitHub.

## Give us a star ⭐️
If you find this project useful, give us a star. It helps others discover the project.