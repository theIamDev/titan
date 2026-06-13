from phonenumbers import parse, is_valid_number, NumberParseException
from phonenumbers.phonenumberutil import PhoneNumberFormat, format_number

def validate_and_format_phone_number(raw_phone: str, region: str = "IN") -> str:
    """
    Parses raw string and returns E.164 formatted string.
    Raises ValidationError if the number is mathematically invalid.
    """
    try:
        parsed_num = parse(raw_phone, region)
        if not is_valid_number(parsed_num):
            raise ValueError("Number is not a valid phone number for region ")
        return format_number(parsed_num, PhoneNumberFormat.E164)
    except NumberParseException as e:
        raise ValueError("Format error") from e