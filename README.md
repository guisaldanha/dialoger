# Dialoger

[![PyPI version](https://img.shields.io/pypi/v/dialoger)](https://pypi.org/project/dialoger/) [![License](https://img.shields.io/github/license/guisaldanha/dialoger)](LICENSE) [![Downloads](https://img.shields.io/pypi/dm/dialoger)](https://img.shields.io/pypi/dm/dialoger)

Dialoger is a Python package that provides a set of functions to create interactive dialog windows for your applications.

## Installation

You can install Dialoger using pip:

```shell
pip install dialoger
```

## Usage

Dialoger provides a set of functions to create interactive dialog windows with ease. The functions are: `ask`, `askwithanswers`, `confirm`, `alert`, `info`, `error` and `success`.

### ask

The `ask` function creates a dialog window with a question and a text input. It returns the text inputted by the user.

#### Parameters

- `title`: The title of the dialog window.
- `question`: The question to be asked to the user.
- `answer_type`: The type of the answer. Can be `str`, `int`, `float`, `alphanumeric` or `password`.
- `answer_default` (optional): The default answer. If `None`, the text input will be empty.
- `pattern` (optional): A pattern to validate the answer. # will be replaced by the number. For example, `##/##/####` can be used to ask for a date or `###.###.###-##` to ask for a CPF. If `None`, no pattern will be used.
- `allow_empty` (optional): If `True`, the user can leave the text input empty. If `False`, the user must input something.
- `allow_cancel` (optional): If `True`, the user can cancel the dialog window. If `False`, the user must answer the question.
- `entrance_width` (optional): The width of the text input. If omitted, the width will be 35.

```python
import dialoger

date = dialoger.ask('Birth date''', 'What is your birth date?', 'str', pattern='##/##/####', allow_empty=False, allow_cancel=False)

print(f"You were born in {date}")
```

### askwithanswers

The `askwithanswers` function creates a dialog window with a question and a list of choices. It returns the choice selected by the user.

#### Parameters

- `title`: The title of the dialog window.
- `question`: The question to be asked to the user.
- `choices`: A list of choices.

```python
import dialoger

answer = dialoger.askwithanswers('Favorite color', 'What is your favorite color?', ['Red', 'Green', 'Blue'])

print(f"Your favorite color is {answer}")
```

### confirm

The `confirm` function creates a dialog window with a message and two buttons. It returns `True` if the user clicks the first button, or `False` if the user clicks the second button. The default buttons are "Yes" and "No", but you can change them by passing a list of strings as the `choices` parameter.

#### Parameters

- `title`: The title of the dialog window.
- `message`: The message to be displayed to the user.
- `choices` (optional): A list of strings to be used as the buttons. The first string will be used as the first button, and the second string will be used as the second button. If `None`, the default buttons will be used.

```python
import dialoger

answer = dialoger.confirm('Confirm', 'Are you sure you want to delete this file?')

if answer:
    print('File deleted')
else:
    print('File not deleted')
```

### alert, info, error and success

The `alert`, `info`, `error` and `success` functions create a dialog window with a message and a button. They don't return anything.

#### Parameters

- `title`: The title of the dialog window.
- `message`: The message to be displayed to the user.

```python
import dialoger

dialoger.alert('Alert', 'This is an alert')
dialoger.info('Info', 'This is an info')
dialoger.error('Error', 'This is an error')
dialoger.success('Success', 'This is a success')
```

## Minimum dependencies

Dialoger has no dependencies. It uses only the standard Python Tkinter library.

## Appropriate icons

For each interaction, an icon corresponding to the type of interaction is displayed in the window. The icons are:

![Alert](https://raw.githubusercontent.com/guisaldanha/dialoger/main/dialoger/images/alert.png) ![Info](https://raw.githubusercontent.com/guisaldanha/dialoger/main/dialoger/images/info.png) ![Error](https://raw.githubusercontent.com/guisaldanha/dialoger/main/dialoger/images/error.png) ![Success](https://raw.githubusercontent.com/guisaldanha/dialoger/main/dialoger/images/success.png) ![Question](https://raw.githubusercontent.com/guisaldanha/dialoger/main/dialoger/images/question.png)

## License

Dialoger is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

## Contributing

Contributions are welcome! You can contribute by opening an issue or submitting a pull request.

## Credits

Dialoger was created by [Guilherme Saldanha](https://guisaldanha.com).
