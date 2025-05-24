import re
import unicodedata

meaningless_words = [
    "woo", "skrt", "yeah", "ayy", "ooh", "huh", "ugh", "hey", "whoa",
    "brr", "pow", "bang", "vroom", "beep", "bop",
    "grr", "pew", "doot", "boom", "la", "hey", "wo", "o", "oh"
]

regex_patterns = [rf'\b{re.escape(word[:-1])}{word[-1]}+\b' for word in meaningless_words]

def clean_lyrics(lyrics):
    lyrics = unicodedata.normalize('NFC', str(lyrics))

    # Thay thế tất cả ký tự xuống dòng và Unicode escape CR/LF
    lyrics = re.sub(r'[\r\n]+|\\u000D\\u000A|\\u000D|\\u000A|\\u002D|\\u002C', ' ', lyrics)
    
    # thay thế ký tự \u0027 và \u0022 là các ký tự Unicode cho dấu nháy đơn và nháy kép
    lyrics = re.sub(r'\\u0027|\\u0022', "'", lyrics)
    #\u002D là ký tự Unicode cho dấu gạch ngang
    lyrics = re.sub(r'\\u002D', '-', lyrics)

    # Loại bỏ các chuỗi lặp lại như "La la la la la"
    lyrics = re.sub(r'\b(?:(la|lá|là|La|Lá|Là)\s*)+(la|lá|là|La|Lá|Là)\b', '', lyrics, flags=re.IGNORECASE)
    lyrics = re.sub(r'\b(?:(ay|Ay)\s*)+(ay|Ay)\b', '', lyrics, flags=re.IGNORECASE)

    # Loại bỏ số
    lyrics = re.sub(r'\d+', '', lyrics)

    # Loại bỏ các từ vô nghĩa
    for pattern in regex_patterns:
        lyrics = re.sub(pattern, '', lyrics, flags=re.IGNORECASE)

    # Chuẩn hóa các từ bị kéo dài (sky-y-y-y -> sky)
    lyrics = re.sub(r'\b(\w+?)(-\w+)*\b', r'\1', lyrics)

    # Xử lý các từ kéo dài kiểu "Ơiiiiiiii" -> "Ơi" (chỉ áp dụng cho nguyên âm)
    lyrics = re.sub(r'([aăâeêioôơuưy])\1+', r'\1', lyrics, flags=re.UNICODE)

    # Loại bỏ các đoạn trong ngoặc vuông và ngoặc tròn
    lyrics = re.sub(r'\[.*?\]|\(.*?\)', '', lyrics)

    # Loại bỏ ký tự không phải chữ cái, số hoặc khoảng trắng
    lyrics = re.sub(r'[^\w\s-]', '', lyrics, flags=re.UNICODE)

    # Chuyển thành chữ thường
    lyrics = lyrics.lower()

    # Chuẩn hóa khoảng trắng
    lyrics = re.sub(r'\s+', ' ', lyrics).strip()

    # Chuẩn hóa các biến thể "baby"
    pattern = r'\b(bae|babi|bei|babe|babey|babie|babby|bby|bb|bebi|bebé|beb|bayb|baybe|baybee|babiie|babii|babbey)\b'
    lyrics = re.sub(pattern, 'baby', lyrics, flags=re.IGNORECASE)

    return lyrics

