import requests
from bs4 import BeautifulSoup
import csv
import json
import logging
import argparse
import time
import sys
from datetime import datetime
from urllib.parse import urljoin
from pathlib import Path

# =====================================================
# НАСТРОЙКА ЛОГИРОВАНИЯ
# =====================================================
def setup_logging(log_file=None):
    """
    Настраивает логирование: вывод в консоль и (опционально) в файл.
    """
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    # Обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format))
    
    # Настраиваем корневой логгер
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    
    # Обработчик для файла (если указан)
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)
        logging.info(f"Логирование также сохраняется в файл: {log_file}")
    
    return logger

# Получаем логгер
logger = logging.getLogger(__name__)

# Настройки User-Agent для имитации браузера (чтобы сайты не блокировали запрос)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# URL для парсинга по умолчанию (Hacker News - надёжный источник новостей о технологиях)
DEFAULT_NEWS_URL = "https://news.ycombinator.com/"

# Имена файлов для сохранения результатов по умолчанию
DEFAULT_CSV_FILE = "news.csv"
DEFAULT_JSON_FILE = "news.json"

# Задержка между запросами (в секундах) для предотвращения перегрузки сервера
REQUEST_DELAY = 2  # 2 секунды между запросами


def fetch_page(url, request_delay=REQUEST_DELAY):
    """
    Отправляет GET-запрос к странице с User-Agent.
    Возвращает объект BeautifulSoup или None при ошибке.
    """
    try:
        logging.info(f"Загружаю страницу: {url}")
        # Пауза перед запросом (чтобы не нагружать сервер)
        time.sleep(request_delay)
        
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Проверяет статус ответа (4xx, 5xx вызовут исключение)
        
        logging.debug(f"Статус код: {response.status_code}")
        return BeautifulSoup(response.content, 'html.parser')
    
    except requests.exceptions.Timeout:
        logging.error(f"❌ Ошибка: Превышено время ожидания (10 сек) для {url}")
        return None
    except requests.exceptions.ConnectionError:
        logging.error(f"❌ Ошибка: Не удалось подключиться к {url}")
        return None
    except requests.exceptions.HTTPError as e:
        logging.error(f"❌ Ошибка HTTP {e.response.status_code} для {url}")
        return None
    except Exception as e:
        logging.error(f"❌ Неизвестная ошибка при загрузке {url}: {e}")
        return None


def extract_news(soup, base_url=DEFAULT_NEWS_URL):
    """
    Извлекает новости из HTML-разметки.
    Возвращает список словарей с информацией о новостях.
    """
    news_list = []
    
    try:
        # Ищем все строки таблицы со новостями на Hacker News
        # Селектор: каждая новость находится в <tr> с классом "athing"
        news_rows = soup.find_all('tr', class_='athing')
        
        if not news_rows:
            logging.warning("⚠ Новости не найдены (возможно, изменилась структура сайта)")
            return news_list
        
        logging.info(f"Найдено элементов для обработки: {len(news_rows)}")
        
        # Проходим по каждой найденной новости
        for idx, row in enumerate(news_rows, 1):
            try:
                # Селектор для заголовка и ссылки: <span class="titleline"> -> <a>
                title_span = row.find('span', class_='titleline')
                if not title_span:
                    continue
                
                title_elem = title_span.find('a')
                if not title_elem:
                    continue
                
                # Извлекаем заголовок и ссылку
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')
                
                # Преобразуем relative URL в absolute (если необходимо)
                if link and not link.startswith('http'):
                    link = urljoin(base_url, link)
                
                # На Hacker News дата не всегда легко доступна в основном блоке
                # Пока оставим её пустой (в реальных новостных сайтах она есть)
                date = ""
                
                # Проверяем, что нашли хотя бы заголовок и ссылку
                if title and link:
                    news_list.append({
                        'title': title,
                        'link': link,
                        'date': date
                    })
                    logging.debug(f"[{idx}] Извлечена новость: {title[:50]}...")
            
            except Exception as e:
                logging.warning(f"Ошибка при обработке новости #{idx}: {e}")
                continue
        
        return news_list
    
    except Exception as e:
        logging.error(f"❌ Ошибка при извлечении новостей: {e}")
        return []


def save_to_csv(news_list, filename):
    """
    Сохраняет новости в CSV файл.
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'link', 'date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(news_list)
        
        logging.info(f"✅ Данные сохранены в {filename} ({len(news_list)} новостей)")
    
    except Exception as e:
        logging.error(f"❌ Ошибка при сохранении CSV: {e}")


def save_to_json(news_list, filename):
    """
    Сохраняет новости в JSON файл.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(news_list, jsonfile, ensure_ascii=False, indent=4)
        
        logging.info(f"✅ Данные сохранены в {filename} ({len(news_list)} новостей)")
    
    except Exception as e:
        logging.error(f"❌ Ошибка при сохранении JSON: {e}")


def read_urls_from_file(filename):
    """
    Читает список URL из файла (по одному URL на строку).
    Возвращает список URL, пропуская пустые строки и комментарии (#).
    """
    urls = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                # Убираем пробелы и переводы строк
                url = line.strip()
                
                # Пропускаем пустые строки и комментарии
                if url and not url.startswith('#'):
                    urls.append(url)
        
        logging.info(f"Прочитано {len(urls)} URL из файла {filename}")
        return urls
    
    except FileNotFoundError:
        logging.error(f"❌ Файл не найден: {filename}")
        return []
    except Exception as e:
        logging.error(f"❌ Ошибка при чтении файла URL: {e}")
        return []


def parse_single_url(url, csv_file, json_file, request_delay=REQUEST_DELAY, append_mode=False):
    """
    Парсит одну страницу и сохраняет результаты.
    
    Args:
        url: URL страницы для парсинга
        csv_file: Название CSV файла для сохранения
        json_file: Название JSON файла для сохранения
        request_delay: Задержка между запросами в секундах
        append_mode: Добавлять ли результаты к существующим файлам
    """
    logging.info(f"\n{'='*60}")
    logging.info(f"Парсинг: {url}")
    logging.info(f"{'='*60}")
    
    # Загружаем страницу
    soup = fetch_page(url, request_delay=request_delay)
    if not soup:
        logging.error(f"Не удалось загрузить {url}. Пропускаю...")
        return 0
    
    # Извлекаем новости
    news_list = extract_news(soup, base_url=url)
    
    if not news_list:
        logging.warning(f"Новости не найдены для {url}")
        return 0
    
    # Если это не первый URL (append_mode = True), читаем существующие данные
    if append_mode and Path(csv_file).exists():
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                existing_news = list(reader)
                news_list = existing_news + news_list
            logging.debug(f"Добавлено к существующим данным (всего {len(news_list)} новостей)")
        except Exception as e:
            logging.warning(f"Не удалось прочитать существующие данные: {e}")
    
    # Сохраняем в файлы
    save_to_csv(news_list, csv_file)
    save_to_json(news_list, json_file)
    
    return len(news_list)

def main():
    """
    Основная функция программы с поддержкой аргументов командной строки.
    """
    # =====================================================
    # ПАРСИНГ АРГУМЕНТОВ КОМАНДНОЙ СТРОКИ
    # =====================================================
    parser = argparse.ArgumentParser(
        description='Парсер новостей: собирает новости с веб-сайтов и сохраняет в CSV/JSON',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python parser.py
  python parser.py --url https://example.com
  python parser.py --url-file urls.txt --csv custom.csv --json custom.json
  python parser.py --url https://news.ycombinator.com/ --delay 3 --log app.log
        """
    )
    
    # Аргументы для одного URL
    parser.add_argument(
        '--url',
        type=str,
        default=DEFAULT_NEWS_URL,
        help=f'URL страницы для парсинга (по умолчанию: {DEFAULT_NEWS_URL})'
    )
    
    # Аргумент для файла со списком URL
    parser.add_argument(
        '--url-file',
        type=str,
        default=None,
        help='Файл со списком URL (по одному на строку). Если указан, игнорирует --url'
    )
    
    # Названия выходных файлов
    parser.add_argument(
        '--csv',
        type=str,
        default=DEFAULT_CSV_FILE,
        help=f'Имя CSV файла для сохранения (по умолчинию: {DEFAULT_CSV_FILE})'
    )
    
    parser.add_argument(
        '--json',
        type=str,
        default=DEFAULT_JSON_FILE,
        help=f'Имя JSON файла для сохранения (по умолчанию: {DEFAULT_JSON_FILE})'
    )
    
    # Задержка между запросами
    parser.add_argument(
        '--delay',
        type=float,
        default=REQUEST_DELAY,
        help=f'Задержка между запросами в секундах (по умолчанию: {REQUEST_DELAY})'
    )
    
    # Логирование в файл
    parser.add_argument(
        '--log',
        type=str,
        default=None,
        help='Файл для сохранения логов (опционально)'
    )
    
    # Уровень логирования
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Уровень детализации логов (по умолчанию: INFO)'
    )
    
    args = parser.parse_args()
    
    # =====================================================
    # ИНИЦИАЛИЗАЦИЯ ЛОГИРОВАНИЯ
    # =====================================================
    setup_logging(log_file=args.log)
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, args.log_level))
    
    logging.info(f"⏰ Время начала: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"🔧 Настройки: CSV={args.csv}, JSON={args.json}, Задержка={args.delay}с")
    
    # =====================================================
    # ОПРЕДЕЛЕНИЕ СПИСКА URL ДЛЯ ПАРСИНГА
    # =====================================================
    urls = []
    
    if args.url_file:
        # Читаем URL из файла
        urls = read_urls_from_file(args.url_file)
        if not urls:
            logging.error("❌ Не удалось загрузить URL из файла. Выход.")
            return
    else:
        # Используем URL из аргумента
        urls = [args.url]
    
    # =====================================================
    # ПАРСИНГ
    # =====================================================
    logging.info(f"🔍 Начинаем парсинг {len(urls)} URL(ов)\n")
    
    total_news = 0
    append_mode = False  # Для первого URL не меджим существующие данные
    
    for idx, url in enumerate(urls, 1):
        news_count = parse_single_url(
            url,
            args.csv,
            args.json,
            request_delay=args.delay,
            append_mode=append_mode
        )
        total_news += news_count
        append_mode = True  # После первого URL включаем режим добавления
    
    # =====================================================
    # ИТОГИ
    # =====================================================
    logging.info(f"\n{'='*60}")
    logging.info(f"📊 ИТОГИ ПАРСИНГА")
    logging.info(f"{'='*60}")
    logging.info(f"✅ Всего собрано новостей: {total_news}")
    logging.info(f"📁 Результаты сохранены в:")
    logging.info(f"   - CSV: {args.csv}")
    logging.info(f"   - JSON: {args.json}")
    logging.info(f"⏰ Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if args.log:
        logging.info(f"📝 Логи сохранены в: {args.log}")
    
    return total_news


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.warning("\n⚠️  Программа прервана пользователем (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        logging.error(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
