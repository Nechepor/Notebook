import re


class Custom:

    def is_phone_number(self, input_string):
        phone_pattern = re.compile(r'7(\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2})\b')
        return bool(phone_pattern.match(input_string))
