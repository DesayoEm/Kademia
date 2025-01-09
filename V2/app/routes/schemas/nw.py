# def validate_year(year: int) -> int:
#     current_year = date.today().year
#     if year < 1900:
#         raise Exception()
#     if year > current_year:
#         raise Exception()
#     return year
#
#
# def validate_phone(phone: str) -> bool:
#     if not len(phone) == 11 or not phone.isdigit():
#         raise ValueError("Phone must be 11 digits")
#     return phone
#
# def validate_name(name: str, max_length: int = 30) -> bool:
#     if not name or len(name) > max_length:
#         raise ValueError(f"Name must be between 1 and {max_length} characters")
#     return name