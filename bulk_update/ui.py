from __future__ import print_function, unicode_literals

from examples import custom_style_2
from PyInquirer import prompt


class UI:
    def _user_input(self, name, message):
        questions = [
            {
                "type": "input",
                "name": name,
                "message": message,
            }
        ]

        answers = prompt(questions)
        return answers[name]

    def _show_list_of_options(self, name, choices, message, append_options=[]):
        if append_options:
            choices.extend(append_options)
        questions = [
            {
                "type": "list",
                "name": name,
                "message": message,
                "choices": choices,
            }
        ]
        answers = prompt(questions, style=custom_style_2)
        return answers[name]

    def _show_multi_select(
        self,
        name,
        choices,
        message,
    ):
        def _check_choices(choices):
            checked_choices = []

            for choice in choices:
                if isinstance(choice, str):
                    checked_choices.append({"name": choice})
                if isinstance(choice, dict):
                    checked_choices.append(
                        {
                            "name": choice["name"],
                            "checked": choice.get("checked", False),
                        }
                    )
            return checked_choices

        questions = {
            "type": "checkbox",
            "message": message,
            "name": name,
            "choices": _check_choices(choices),
        }
        answers = prompt(questions, style=custom_style_2)
        return answers[name]
