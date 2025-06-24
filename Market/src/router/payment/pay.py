# import hashlib
#
# def generate_token(data: dict):
#     params = dict(data)
#     params['Password'] = 'TinkoffBankTest'  # Тестовый пароль
#     token_str = ''.join(str(params[k]) for k in sorted(params.keys()))
#     return hashlib.sha256(token_str.encode('utf-8')).hexdigest()
#
# # Тестовый набор обязательных параметров (Token не включаем, DATA и Receipt не включаем!)
# base_data = {
#     "TerminalKey": "TinkoffBankTest",
#     "Amount": 14900,  # 149 рублей в копейках
#     "OrderId": "TEST-001",
#     "Description": "Булочка тестовая"
# }
#
# token = generate_token(base_data)
# print('Тестовый токен:', token)