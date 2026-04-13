import re
import string

def clean_text(text):
    """Metni küçük harfe çevirir, noktalama işaretlerini ve sayıları temizler."""
    text = text.lower()
    # Noktalama işaretlerini kaldır
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    # Sayıları kaldır
    text = re.sub(r"\d+", "", text)
    # Gereksiz boşlukları temizle
    text = text.strip()
    return text
