#!/usr/bin/env python3
"""
Получение ключевых характеристик автомобиля: тип двигателя, коробка передач, мощность
Использование: python3 get_engine_specs.py <ID_МАШИНЫ>
"""
import requests
import json
import sys

def get_engine_specs(car_id):
    """Получить ключевые характеристики автомобиля"""

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }

    print("=" * 70)
    print("ПОЛУЧЕНИЕ КЛЮЧЕВЫХ ХАРАКТЕРИСТИК АВТОМОБИЛЯ")
    print("=" * 70)

    try:
        # 1. Получаем базовую информацию
        print(f"\nПолучаю информацию о машине ID: {car_id}...")
        base_url = f"https://apipcmusc.che168.com/v1/car/getcarinfo?_appid=2sc.pc&infoid={car_id}"

        response = requests.get(base_url, headers=headers, timeout=10)
        base_data = response.json()

        if base_data.get('returncode') != 0:
            print(f"❌ Ошибка: {base_data.get('message')}")
            return None

        car = base_data.get('result', {})
        spec_id = car.get('specid')

        if not spec_id:
            print("❌ Не найден ID спецификации")
            return None

        # 2. Получаем детальные параметры
        param_url = f"https://cacheapigo.che168.com/CarProduct/GetParam.ashx?specid={spec_id}"
        param_response = requests.get(param_url, headers=headers, timeout=10)
        param_data = param_response.json()

        if param_data.get('returncode') != 0:
            print("❌ Ошибка получения параметров")
            return None

        # 3. Извлекаем ключевые характеристики
        specs = extract_key_specs(param_data, car)

        if specs:
            print_specs(specs)

            # Сохраняем в файл
            filename = f'engine_specs_{car_id}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(specs, f, ensure_ascii=False, indent=2)
            print(f"\n💾 Данные сохранены в: {filename}")

            return specs

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def extract_key_specs(param_data, car_info):
    """Извлечь только ключевые характеристики"""
    params = param_data.get('result', {}).get('paramtypeitems', [])

    specs = {
        'car_id': car_info.get('infoid'),
        'car_name': car_info.get('carname'),
        'brand': car_info.get('brandname'),
        'engine_type': None,
        'transmission': None,
        'horsepower': None,
        'engine_model': None,
        'engine_displacement': None,
        'engine_power_kw': None
    }

    for param_type in params:
        param_name = param_type.get('name')

        # Основные параметры
        if param_name == '基本参数':
            for param in param_type.get('paramitems', []):
                name = param.get('name')
                value = param.get('value')

                if name == '发动机':
                    specs['engine_type'] = value
                elif name == '变速箱':
                    specs['transmission'] = value
                elif name == '最大功率(kW)':
                    specs['engine_power_kw'] = value

        # Детали двигателя
        elif param_name == '发动机':
            for param in param_type.get('paramitems', []):
                name = param.get('name')
                value = param.get('value')

                if name == '发动机型号':
                    specs['engine_model'] = value
                elif name == '排量(L)':
                    specs['engine_displacement'] = value
                elif name == '最大马力(Ps)':
                    specs['horsepower'] = value

    return specs

def print_specs(specs):
    """Красиво вывести спецификации"""
    print(f"\n🚗 МАШИНА: {specs['car_name']}")
    print(f"🏷️  БРЕНД: {specs['brand']}")
    print(f"🆔 ID: {specs['car_id']}")
    print()

    print("🔧 ДВИГАТЕЛЬ:")
    if specs['engine_type']:
        print(f"  • Тип: {specs['engine_type']}")
    if specs['engine_model']:
        print(f"  • Модель: {specs['engine_model']}")
    if specs['engine_displacement']:
        print(f"  • Объем: {specs['engine_displacement']} L")
    if specs['horsepower']:
        print(f"  • Мощность: {specs['horsepower']} л.с.")
    if specs['engine_power_kw']:
        print(f"  • Мощность: {specs['engine_power_kw']} кВт")

    print()
    print("⚙️ КОРОБКА ПЕРЕДАЧ:")
    if specs['transmission']:
        print(f"  • Тип: {specs['transmission']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 get_engine_specs.py <ID_МАШИНЫ>")
        print("Пример: python3 get_engine_specs.py 57369943")
        sys.exit(1)

    car_id = sys.argv[1]
    get_engine_specs(car_id)
