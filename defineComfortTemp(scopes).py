COMFORTABLE_TEMPERATURE1 = 25

def get_diff_from_comfortable_temperature(*, temperature = int) -> int:
    return COMFORTABLE_TEMPERATURE1 - temperature

print(get_diff_from_comfortable_temperature(temperature=20))