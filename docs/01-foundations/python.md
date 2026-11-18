# Build a Python CLI

Build a command-line interface for Document Assistant. You will give it a question, check the input, and test its behavior before adding a model.

**Core · 45 minutes** · **Prerequisites** Python 3.11 or later and a terminal.

## The problem

An application needs a clear boundary between what a user enters and what the program does with it. Start with the smallest version of that boundary. A function receives a string, checks it, and returns a value or raises an error.

## Your first working example

Save the following as `examples/cli.py` or use the copy in the handbook source.


```python
--8<-- "examples/cli.py"
```


Run the module from the project root. Python's `-m` flag locates and runs the module by its dotted name.


```console
python -m examples.cli "How many days do I have to return an unopened headset?"
```

Expect `You asked: How many days do I have to return an unopened headset?`.


## How it works

`argparse` converts shell arguments into Python values. The annotation `question: str` describes what the function expects. The function still checks that the string contains something after trimming whitespace. The `__main__` guard lets a test import the function without reading terminal arguments.

## Extend and debug

Try a whitespace-only question. Expect `Enter a question.` and a nonzero exit code. Read `$LASTEXITCODE` in PowerShell or `$?` in Bash immediately afterward. The shell can use that status to decide whether the next step should run.

Add a direct check for normalization. This exercise imports only the application function.


```console
python -c "from examples.cli import answer; assert answer('  headset  ') == 'You asked: headset'"
```


A successful assertion prints nothing. Temporarily remove `strip()` and rerun it. The resulting `AssertionError` tells you the function's output changed even though the CLI still starts.

## In production

Keep validation close to application entry points. Give users actionable messages for invalid input. Treat unexpected exceptions as failures and log them with enough context to diagnose the operation. A small pure function remains easy to test after the terminal entry point becomes HTTP.

## Recap and next step

You built and tested the input boundary. [Next: From your shell to an HTTP request](developer-tools.md)

[Python argparse](https://docs.python.org/3.11/library/argparse.html)
