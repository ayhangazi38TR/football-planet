import os
import re
import shutil
import markdown
import locale
from jinja2 import Environment, FileSystemLoader

# Tema klasörünün yolu (örneğin "templates" klasörünü kullanabilirsin)
TEMPLATE_FOLDER = ""

# İçerik ve çıktı dizinleri
CONTENT_DIR = "Icerik"
OUTPUT_DIR = "public"

# Jinja2 ortamını kuruyoruz
env = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER))
template = env.get_template("layout.html")

def get_base_url(output_path):
    """
    output_path: 'public/oyuncu/selin-gunes.html' gibi bir yol.
    OUTPUT_DIR'a göre göreli yol bazında kaç klasör yukarı çıkılacaksa
    base_url = "../" * o kadar
    """
    rel_path = os.path.relpath(os.path.dirname(output_path), OUTPUT_DIR)
    if rel_path == ".":
        return ""
    levels = rel_path.count(os.sep) + 1
    return "../" * levels

def fix_links(md_text, base_url):
    """
    Markdown içindeki linkleri .html'ye çevirir ve base_url prefix'i ekler.
    Örnek:
      [Elmas Evi](/stadyum/elmas-evi) → [Elmas Evi](../stadyum/elmas-evi.html)
    """
    pattern = r'\((/[^)]+)\)'

    def repl(match):
        url = match.group(1)
        if url.endswith(".md"):
            url = url[:-3] + ".html"
        elif not url.endswith(".html") and not url.startswith("http"):
            url += ".html"

        if url.startswith("/"):
            url = base_url + url[1:]
        return f"({url})"

    return re.sub(pattern, repl, md_text)

# Yeni fonksiyon: Renk kodlarını span'a çevirir
def convert_colors_to_circles(text):
    """
    Belirli renk kodlarını (HEX formatında) bulur ve onları
    .color-circle sınıfına sahip <span> etiketlerine dönüştürür.
    Örnek: #7D7D7D -> <span class="color-circle" style="background-color: #7D7D7D;"></span>
    """
    # Renk kodlarını bulan regex (örnekte verilenler ve genel HEX renk kodları)
    # Renk kodlarını doğrudan belirtilen liste üzerinden veya genel regex ile bulabiliriz.
    # Genel HEX renk kodu regex'i: #(?:[0-9a-fA-F]{3}){1,2}\b
    
    # Senin listende belirtilen renkler:
    # #7D7D7D, #8B4513, #6B8E23
    
    # regex pattern'ı daha spesifik yapabiliriz veya genel bir HEX regex'i kullanabiliriz
    # Genel bir HEX renk kodunu yakalamak için:
    color_pattern = r'#(?:[0-9a-fA-F]{3}){1,2}\b'

    def replacer(match):
        hex_code = match.group(0) # Yakalanan renk kodu, örn: #7D7D7D
        return f'<span class="color-circle" style="background-color: {hex_code};"></span>'

    return re.sub(color_pattern, replacer, text)

def generate_html_page(title, content, base_url=""):
    """
    Jinja2 şablonunu render edip tam HTML sayfası döndürür.
    """
    return template.render(title=title, content=content, base_url=base_url)

def process_markdown_file(input_path, output_path):
    """
    Markdown dosyasını okuyup HTML'ye çevirir, çıktı dosyasına yazar.
    Başlığı markdown dosyasının ilk satırındaki H1 etiketinden çeker.
    Renk kodlarını span'lara dönüştürür.
    """
    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Başlığı markdown dosyasının ilk H1 başlığından çekmeye çalış
    lines = md_content.splitlines()
    extracted_title = None
    if lines:
        first_line = lines[0].strip()
        if first_line.startswith('#'):
            extracted_title = first_line.lstrip('#').strip()
            md_content_without_title = "\n".join(lines[1:])
        else:
            md_content_without_title = md_content
    else:
        md_content_without_title = "" # Dosya boşsa

    if not extracted_title:
        extracted_title = slug_to_title(os.path.splitext(os.path.basename(input_path))[0])
        md_to_convert = md_content
    else:
        md_to_convert = md_content_without_title
    
    # Renk kodlarını HTML span'larına dönüştür
    md_with_circles = convert_colors_to_circles(md_to_convert)

    base_url = get_base_url(output_path)
    # Link düzeltmeleri de renk dönüşümünden sonra yapılmalı
    md_fixed_links = fix_links(md_with_circles, base_url) 

    html_content = markdown.markdown(md_fixed_links, extensions=["fenced_code", "tables"])
    
    full_html = generate_html_page(extracted_title, html_content, base_url=base_url)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)
def copy_assets():
    """
    style.css varsa doğrudan çıktı dizinine kopyala.
    """
    if os.path.exists("style.css"):
        shutil.copy("style.css", os.path.join(OUTPUT_DIR, "style.css"))
    else:
        print("UYARI: style.css dosyası bulunamadı!")

def slug_to_title(slug):
    """
    Tireleri boşluk yapar, kelimelerin ilk harflerini büyük yapar.
    Bu artık yedek olarak kullanılacak.
    """
    return " ".join(word.title() for word in slug.replace("_", "-").split("-"))

# --- build_static_site fonksiyonu ---
def build_static_site():
    print("Statik site oluşturuluyor...\n")
    PAGE_SIZE = 20  # Sayfa başına gösterilecek dosya sayısı

    # Türkçe locale ayarını burada yapıyoruz
    try:
        locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
        print("Yerel ayar 'tr_TR.UTF-8' olarak ayarlandı.")
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'tr_TR')
            print("Yerel ayar 'tr_TR' olarak ayarlandı.")
        except locale.Error:
            try:
                locale.setlocale(locale.LC_ALL, 'Turkish')
                print("Yerel ayar 'Turkish' olarak ayarlandı.")
            except locale.Error as e:
                print(f"UYARI: Türkçe yerel ayar ayarlanamadı: {e}. Sıralama doğru çalışmayabilir.")
                print("Linux'ta 'sudo locale-gen tr_TR.UTF-8' komutuyla locale'i oluşturmanız gerekebilir.")
                print("Windows'ta 'Denetim Masası > Bölge ve Dil Seçenekleri' üzerinden ayarlama yapmanız gerekebilir.")
                # Hiçbiri olmazsa, varsayılanı kullanmaya çalış
                try:
                    locale.setlocale(locale.LC_ALL, '')
                    print("Varsayılan sistem yerel ayarı kullanılıyor.")
                except locale.Error as e_default:
                    print(f"HATA: Varsayılan yerel ayar da ayarlanamadı: {e_default}. Çıkış yapılıyor.")
                    return # Locale ayarlanamazsa devam etmemek en iyisi

    # Çıktı dizinini temizle (isteğe bağlı ama önerilir)
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        print(f"'{OUTPUT_DIR}' dizini temizlendi.")
    os.makedirs(OUTPUT_DIR)
    print(f"'{OUTPUT_DIR}' dizini oluşturuldu.")

    for root, dirs, files in os.walk(CONTENT_DIR):
        html_files_in_dir = []

        for file in files:
            if file.endswith(".md"):
                full_input = os.path.join(root, file)
                rel_path = os.path.relpath(full_input, CONTENT_DIR).replace("\\", "/")
                
                html_file_name = "index.html" if file == "index.md" else file.replace(".md", ".html")
                output_path = os.path.join(OUTPUT_DIR, os.path.dirname(rel_path), html_file_name)

                print(f"İçerik: {rel_path} → Çıktı: {output_path}")
                
                # Markdown dosyasını oku ve başlığı çek
                with open(full_input, "r", encoding="utf-8") as f:
                    md_content_for_title_extract = f.read()
                
                # Başlığı çekmek için özel mantık
                lines_for_title = md_content_for_title_extract.splitlines()
                current_file_title = None
                if lines_for_title:
                    first_line_for_title = lines_for_title[0].strip()
                    if first_line_for_title.startswith('#'):
                        current_file_title = first_line_for_title.lstrip('#').strip()
                
                # Eğer markdown içinden başlık çekilemediyse, dosya adından türet
                if not current_file_title:
                    current_file_title = slug_to_title(os.path.splitext(file)[0])

                # process_markdown_file'a artık başlığı doğrudan göndermiyoruz,
                # çünkü o fonksiyon başlığı kendi içinde buluyor veya türetiyor.
                process_markdown_file(full_input, output_path) 

                html_files_in_dir.append({
                    "filename": html_file_name,
                    "title": current_file_title # Burada çekilen başlığı kullan
                })

        if html_files_in_dir:
            # Türkçe locale ayarı sonrası bu yöntemle sıralama yapılır:
            html_files_in_dir.sort(key=lambda x: locale.strxfrm(x["title"].lower()))

            total_items = len(html_files_in_dir)
            total_pages = (total_items + PAGE_SIZE - 1) // PAGE_SIZE

            current_output_subdir = os.path.relpath(root, CONTENT_DIR).replace("\\", "/")
            if current_output_subdir == ".":
                current_output_subdir = ""

            def build_pagination_html(current_page, total_pages, base_url_for_pagination):
                pagination_html = '<div class="pagination">\n'
                
                if current_page > 1:
                    prev_page_link = "index.html" if current_page == 2 else f"index_{current_page - 1}.html"
                    pagination_html += f'<a href="{base_url_for_pagination}{prev_page_link}">&larr; Önceki</a> '
                
                for p in range(1, total_pages + 1):
                    page_link = "index.html" if p == 1 else f"index_{p}.html"
                    if p == current_page:
                        pagination_html += f'<strong>{p}</strong> '
                    else:
                        pagination_html += f'<a href="{base_url_for_pagination}{page_link}">{p}</a> '
                
                if current_page < total_pages:
                    next_page_link = f"index_{current_page + 1}.html"
                    pagination_html += f'<a href="{base_url_for_pagination}{next_page_link}">Sonraki &rarr;</a>'
                
                pagination_html += '\n</div>\n'
                return pagination_html

            for page_num in range(1, total_pages + 1):
                start_idx = (page_num - 1) * PAGE_SIZE
                end_idx = start_idx + PAGE_SIZE
                page_items = html_files_in_dir[start_idx:end_idx]

                index_items_html = "<ul>\n"
                for f in page_items:
                    index_items_html += f'  <li><a href="{f["filename"]}">{f["title"]}</a></li>\n'
                index_items_html += "</ul>"

                index_filename = "index.html" if page_num == 1 else f"index_{page_num}.html"
                index_output_path = os.path.join(OUTPUT_DIR, current_output_subdir, index_filename)
                
                base_url_for_pagination = get_base_url(index_output_path)
                index_items_html += build_pagination_html(page_num, total_pages, base_url_for_pagination)

                page_title = f"{current_output_subdir if current_output_subdir else 'Ana'} Dizin"
                if total_pages > 1:
                    page_title += f" (Sayfa {page_num})"
                
                index_html = generate_html_page(page_title, index_items_html, base_url=base_url_for_pagination)

                os.makedirs(os.path.dirname(index_output_path), exist_ok=True)
                with open(index_output_path, "w", encoding="utf-8") as f:
                    f.write(index_html)

                print(f"Dizin sayfası oluşturuldu: {index_output_path}")

    copy_assets()
    print(f"\nTüm site başarıyla '{OUTPUT_DIR}' klasörüne yazıldı.")

if __name__ == "__main__":
    build_static_site()

