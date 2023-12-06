def shift_left(vector, amount):
    """Сдвиг вектора влево на указанное количество разрядов."""
    return vector[amount:] + [0] * amount

def add_vectors(vec1, vec2):
    """Покомпонентное сложение векторов по модулю 2."""
    return [(a + b) % 2 for a, b in zip(vec1, vec2)]

def encode(info_vector, generator_poly):
    """Кодирование информационного вектора."""
    r = len(generator_poly) - 1  # степень образующего полинома
    encoded_vector = info_vector + [0] * r  # добавляем r нулей для умножения на x^r

    while encoded_vector[0] != 0:
        # находим остаток от деления
        remainder = [a ^ b for a, b in zip(encoded_vector, generator_poly)]
        # обновляем вектор
        encoded_vector = shift_left(remainder, 1)

    # добавляем остаток в конец информационного вектора
    return add_vectors(info_vector, encoded_vector[1:])

def decode(received_vector, generator_poly):
    """Декодирование принятого вектора."""
    r = len(generator_poly) - 1
    decoded_vector = received_vector + [0] * r

    while decoded_vector[0] != 0:
        remainder = [a ^ b for a, b in zip(decoded_vector, generator_poly)]
        decoded_vector = shift_left(remainder, 1)

    return decoded_vector[1:]

def find_error_location(syndrome, generator_poly):
    """Нахождение места ошибки."""
    r = len(generator_poly) - 1
    error_location = syndrome

    while error_location[0] != 0:
        remainder = [a ^ b for a, b in zip(error_location, generator_poly)]
        error_location = shift_left(remainder, 1)

    return error_location[1:r+1]

def channel_model(input_vector, error_probability):
    """Модель канала связи с добавлением ошибок."""
    return [bit if random.random() > error_probability else 1 - bit for bit in input_vector]

def generate_all_possible_errors(n):
    """Генерация всех возможных ошибок заданной кратности."""
    errors = []
    for i in range(2**n):
        error = [int(bit) for bit in format(i, f'0{n}b')]
        errors.append(error)
    return errors

def generate_syndromes_for_errors(errors, generator_poly):
    """Генерация симптомов ошибок."""
    syndromes = {}
    for error in errors:
        received_vector = add_vectors(info_vector, error)
        syndrome = decode(received_vector, generator_poly)
        syndrome_key = tuple(syndrome)
        
        if syndrome_key in syndromes:
            syndromes[syndrome_key].append(error)
        else:
            syndromes[syndrome_key] = [error]

    return syndromes

def generate_error_correction_table(syndromes):
    """Генерация таблицы кратность - корректирующая способность."""
    table = {}
    for syndrome, errors in syndromes.items():
        error_multiplicity = errors[0].count(1)
        if error_multiplicity not in table:
            table[error_multiplicity] = {'syndromes': [], 'correction_capabilities': []}
        
        table[error_multiplicity]['syndromes'].append(syndrome)
        table[error_multiplicity]['correction_capabilities'].append(len(errors))

    return table

if __name__ == "__main__":
    import random

    # Заданные данные
    info_vector = [1, 0, 1, 0]
    generator_poly = [1, 0, 1, 1]

    # Шаг 1: Генерация всех возможных ошибок
    max_error_multiplicity = 3  # Выберите максимальную кратность ошибки
    all_possible_errors = generate_all_possible_errors(max_error_multiplicity)

    # Шаг 2: Генерация симптомов ошибок
    all_syndromes = generate_syndromes_for_errors(all_possible_errors, generator_poly)

    # Шаг 3: Генерация таблицы кратность - корректирующая способность
    correction_table = generate_error_correction_table(all_syndromes)

    # Вывод результатов
    print("Таблица ошибок, сортированных по кратности:")
    for multiplicity in sorted(correction_table.keys()):
        print(f"Кратность {multiplicity}: {correction_table[multiplicity]['syndromes']}")
    
    print("\nТаблица симптомов ошибок, сортированных по кратности с коллизиями:")
    for multiplicity in sorted(correction_table.keys()):
        print(f"Кратность {multiplicity}: {correction_table[multiplicity]['syndromes']} - {correction_table[multiplicity]['correction_capabilities']}")

    print("\nТаблица симптомов для всех ошибок:")
    for syndrome, errors in all_syndromes.items():
        print(f"Симптом: {syndrome}, Ошибки: {errors}")

    print("\nРезультирующая таблица кратность ошибки – корректирующая способность:")
    print("Кратность ошибки | Количество ошибок, которые можно скорректировать")
    for multiplicity in sorted(correction_table.keys()):
        print(f"{multiplicity}               | {sum(correction_table[multiplicity]['correction_capabilities'])}")
