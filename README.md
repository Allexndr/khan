# API для получения данных о машине с che168.com

## Быстрый старт

### 1. URL запроса

```
https://apipcmusc.che168.com/v1/car/getcarinfo?_appid=2sc.pc&infoid={ID_МАШИНЫ}
```

### 2. Как получить ID машины

Из URL страницы: `https://www.che168.com/dealer/466343/56635701.html`
- ID машины = `56635701` (последнее число в URL)

### 3. Пример использования

**Через браузер или curl:**
```bash
curl "https://apipcmusc.che168.com/v1/car/getcarinfo?_appid=2sc.pc&infoid=56635701"
```

**Через Python (см. файл `get_car_info.py`):**
```python
python3 get_car_info.py 56635701
```

## Что возвращает API

JSON с данными о машине:
- Название, марка, модель
- Цена, пробег, год выпуска
- ID дилера, название дилера
- И многое другое

## Файлы в этой папке

- `get_car_info.py` - готовый скрипт для получения данных
- `README.md` - эта инструкция


