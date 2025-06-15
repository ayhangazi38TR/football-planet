import os
import re
import shutil
import markdown
import locale
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from bs4 import BeautifulSoup

# Tema klasörünün yolu (örneğin "templates" klasörünü kullanabilirsin)
TEMPLATE_FOLDER = ""

# İçerik ve çıktı dizinleri
CONTENT_DIR = "Icerik"
OUTPUT_DIR = "public"
ASSETS_DIR = os.path.join(CONTENT_DIR, "resimler")  # İçerik klasörü içindeki resimler
ASSETS_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "resimler")  # Public klasörü içindeki resimler

# ***********************************************************************************
# DİKKAT: Sitenizin dağıtıldığı kök dizin altındaki yolu buraya yazın.
# Eğer siteniz doğrudan "public_html" gibi ana dizinde ise "" (boş string) bırakın.
# Eğer siteniz "public_html/football-planet/" gibi bir alt dizinde ise "/football-planet" yazın.
# Burayı değiştirmeniz, canonical URL'lerin ve og:url'lerin doğru olmasını sağlar.
# Sitenizin dağıtım yolu değiştiğinde burayı güncellemeyi unutmayın!
SITE_BASE_PATH = "/football-planet"
# ***********************************************************************************

# Jinja2 ortamını kuruyoruz
env = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER))
template = env.get_template("layout.html")


# --- Yardımcı Fonksiyonlar ---
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
    Ayrıca resim linklerini de (örn: /resimler/image.jpg) düzeltir.
    """
    # [link metni](/yol/dosya.md) veya ![alt text](/resimler/gorsel.jpg)
    pattern = r'(!?\[[^\]]*\])\((?!https?://)(/[^)]+)\)' # Sadece / ile başlayan ve http olmayan linkleri yakala

    def repl(match):
        full_match_prefix = match.group(1)
        url = match.group(2) # /oyuncu/alp-pati.md veya /resimler/gorsel.jpg

        if url.endswith(".md"):
            # .md uzantısını .html'ye çevir
            url = url[:-3] + ".html"
        elif not url.endswith(".html") and not url.startswith("http") and not url.startswith("/resimler/") and not url.startswith("/assets/"):
            # Eğer .html değilse ve resim de değilse sonuna .html ekle (örneğin /oyuncu/alp-pati -> /oyuncu/alp-pati.html)
            url += ".html"
        
        # URL'nin başında '/' varsa, base_url ile birleştirerek göreceli yolu elde et
        if url.startswith("/"):
            return f'{full_match_prefix}({base_url}{url[1:]})'
        
        return f'{full_match_prefix}({url})'

    return re.sub(pattern, repl, md_text)


def generate_recent_posts_page(all_pages, output_dir):
    """
    Son yazılar listesini oluşturur ve 'neler-yeni.html' olarak yazar.
    all_pages: [{'title': ..., 'url': ..., 'mod_time': datetime}]
    """
    sorted_pages = sorted(all_pages, key=lambda x: x["mod_time"], reverse=True)[:20]

    html = "<h1>Son Yazılar</h1>\n<ul>\n"
    for page in sorted_pages:
        date_str = page["mod_time"].strftime("%d %B %Y, %H:%M")
        html += f'  <li><a href="{page["url"]}">{page["title"]}</a> <small>({date_str})</small></li>\n'
    html += "</ul>\n"

    # Canonical URL için SITE_BASE_PATH'i ekle
    final_canonical_url = f"{SITE_BASE_PATH}/neler-yeni.html"

    full_html = generate_html_page(
        title="Neler Yeni?",
        content=html,
        base_url="",
        description="Futbol Gezegeni'ndeki en son güncellemeler ve eklenen sayfalar.",
        keywords="neler yeni, son güncellemeler, futbol haberleri",
        og_title="Futbol Gezegeni - Neler Yeni?",
        og_description="Futbol Gezegeni'ndeki en son güncellemeler ve eklenen sayfalar.",
        og_type="website",
        canonical_url=final_canonical_url # Kökten başlayan ve base path içeren URL
    )

    output_path = os.path.join(output_dir, "neler-yeni.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"✔ Son yazılar sayfası oluşturuldu: {output_path}")


def convert_colors_to_circles(text):
    """
    Belirli renk kodlarını (HEX formatında) bulur ve onları
    .color-circle sınıfına sahip <span> etiketlerine dönüştürür.
    """
    color_pattern = r'#(?:[0-9a-fA-F]{3}){1,2}\b'

    def replacer(match):
        hex_code = match.group(0)
        return f'<span class="color-circle" style="background-color: {hex_code};"></span>'

    return re.sub(color_pattern, replacer, text)


def generate_html_page(title, content, base_url="", description="", keywords="", og_title="", og_description="", og_image="", og_type="website", canonical_url=""):
    """
    Jinja2 şablonunu render edip tam HTML sayfası döndürür.
    SEO ve Open Graph için ek parametreler alır.
    Tüm URL'ler artık göreli veya base_url ile türetilmiş olacak.
    """
    # og_image için varsayılanı belirle.
    default_og_image = f"{base_url}resimler/default-og-image.jpg" 

    if not og_title:
        og_title = title
    
    if not og_description:
        og_description = description if description else title
    
    if not og_image: # Eğer içerikten bir görsel gelmediyse varsayılanı kullan
        og_image = default_og_image
    
    # Canonical URL'in her zaman dolu gelmesi beklenir.
    # Burada sadece bir güvenlik fallback'i var, normalde buraya hiç düşmemeli.
    if not canonical_url:
        page_slug = title.lower().replace(' ', '-').replace('ı', 'i').replace('ş', 's').replace('ç', 'c').replace('ö', 'o').replace('ü', 'u').replace('ğ', 'g')
        canonical_url = f"{SITE_BASE_PATH}/{page_slug}.html" # SITE_BASE_PATH'i de dahil et

    return template.render(
        title=title,
        content=content,
        base_url=base_url,
        description=description,
        keywords=keywords,
        og_title=og_title,
        og_description=og_description,
        og_image=og_image,
        og_type=og_type,
        canonical_url=canonical_url
    )


def extract_info_from_content(md_content):
    """
    Markdown içeriğinden başlık, açıklama ve ilk görsel URL'sini türetir.
    """
    lines = md_content.splitlines()
    
    # 1. Başlık (H1) çıkarma
    extracted_title = None
    for line in lines:
        if line.strip().startswith('# '): # Sadece H1 başlığını al
            extracted_title = line.strip().lstrip('# ').strip()
            break
    
    if not extracted_title:
        extracted_title = ""

    # 2. Açıklama türetme (ilk paragraf veya ilk birkaç cümle)
    description = ""
    temp_html = markdown.markdown(md_content)
    soup = BeautifulSoup(temp_html, 'html.parser')
    
    first_text = ""
    # Sadece <p> etiketlerindeki metni ara
    for tag in soup.find_all('p'):
        text_content = tag.get_text(separator=' ', strip=True)
        if text_content:
            first_text = text_content
            break

    if first_text:
        description = first_text[:160] # Açıklama için uygun uzunluk
        if len(first_text) > 160:
            description += "..."
    else:
        description = extracted_title + " hakkında bilgiler." if extracted_title else "Bu sayfa hakkında daha fazla bilgi."

    # 3. İlk görseli bulma
    first_image_src = ""
    img_tag = soup.find('img')
    if img_tag and img_tag.get('src'):
        first_image_src = img_tag['src']

    return {
        "title": extracted_title,
        "description": description,
        "og_image": first_image_src
    }


def process_markdown_file(input_path, output_path):
    """
    Markdown dosyasını okuyup HTML'ye çevirir, çıktı dosyasına yazar.
    Başlık, açıklama ve görseli içerikten türetir.
    """
    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # İçerikten otomatik olarak bilgileri türet
    info = extract_info_from_content(md_content)
    extracted_title = info["title"]
    description = info["description"]
    og_image_from_content = info["og_image"]

    if not extracted_title:
        extracted_title = slug_to_title(os.path.splitext(os.path.basename(input_path))[0])

    keywords = extracted_title.lower().replace(' ', ', ') + ", futbol, futbol gezegeni"

    og_type = "article" if "blog" in input_path or "haber" in input_path else "website"

    # Canonical URL'yi KÖKTEN BAŞLAYAN VE SITE_BASE_PATH'İ İÇEREN göreli olarak oluştur
    # Örneğin: /football-planet/oyuncu/alp-pati.html
    canonical_relative_path_segment = os.path.relpath(output_path, OUTPUT_DIR).replace("\\", "/")

    if os.path.basename(canonical_relative_path_segment) == "index.html":
        canonical_relative_path_segment = os.path.dirname(canonical_relative_path_segment)
        if canonical_relative_path_segment == ".": # Ana dizindeki index.html
            canonical_relative_path_segment = ""
        if canonical_relative_path_segment and not canonical_relative_path_segment.endswith('/'):
            canonical_relative_path_segment += '/'
    
    # SITE_BASE_PATH'i başa ekle ve başında '/' olduğundan emin ol
    if canonical_relative_path_segment == "": # Anasayfa için
        final_canonical_url = SITE_BASE_PATH + "/"
    else:
        final_canonical_url = f"{SITE_BASE_PATH}/{canonical_relative_path_segment}"

    # '/' fazlalığını düzelt, örn: //blog/index.html -> /blog/index.html
    final_canonical_url = final_canonical_url.replace("//", "/")


    # Renk kodlarını HTML span'larına dönüştür
    md_with_circles = convert_colors_to_circles(md_content)

    base_url = get_base_url(output_path)
    md_fixed_links = fix_links(md_with_circles, base_url)

    # Markdown'ı HTML'e çevir
    html_content = markdown.markdown(md_fixed_links, extensions=["fenced_code", "tables"])

    # OG_image yolunu düzenle
    final_og_image = ""
    if og_image_from_content:
        if og_image_from_content.startswith('/'): # Kökten başlayan göreli yol ise
            final_og_image = base_url + og_image_from_content[1:]
        elif not og_image_from_content.startswith('http'): # Sayfa göreli yol ise
            final_og_image = base_url + og_image_from_content
        else: # Mutlak URL ise
            final_og_image = og_image_from_content
    # Eğer içerikte görsel yoksa, generate_html_page varsayılanı ayarlayacak.


    # Jinja2 şablonunu render ederken türetilen bilgileri kullan
    full_html = generate_html_page(
        title=extracted_title,
        content=html_content,
        base_url=base_url,
        description=description,
        keywords=keywords,
        og_title=extracted_title,
        og_description=description,
        og_image=final_og_image,
        og_type=og_type,
        canonical_url=final_canonical_url # Buraya SITE_BASE_PATH'li URL'yi gönderiyoruz
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)


def copy_assets():
    """
    style.css, ASSETS_DIR içindeki tüm dosyaları ve .htaccess dosyasını çıktı dizinine kopyalar.
    """
    print("\nStatik dosyalar kopyalanıyor...")

    if os.path.exists("style.css"):
        shutil.copy("style.css", os.path.join(OUTPUT_DIR, "style.css"))
        print("✔ 'style.css' kopyalandı.")
    else:
        print("UYARI: 'style.css' dosyası bulunamadı!")

    if os.path.exists(ASSETS_DIR):
        if os.path.exists(ASSETS_OUTPUT_DIR):
            shutil.rmtree(ASSETS_OUTPUT_DIR)
        shutil.copytree(ASSETS_DIR, ASSETS_OUTPUT_DIR)
        print(f"✔ '{ASSETS_DIR}' klasörü '{ASSETS_OUTPUT_DIR}' olarak kopyalandı.")
    else:
        print(f"UYARI: '{ASSETS_DIR}' klasörü bulunamadı, resimler kopyalanamadı.")

    htaccess_source = os.path.join(CONTENT_DIR, ".htaccess")
    htaccess_destination = os.path.join(OUTPUT_DIR, ".htaccess")
    if os.path.exists(htaccess_source):
        shutil.copy(htaccess_source, htaccess_destination)
        print(f"✔ '{htaccess_source}' dosyası '{htaccess_destination}' olarak kopyalandı.")
    else:
        print(f"UYARI: '{htaccess_source}' dosyası bulunamadı, kopyalanamadı.")


def slug_to_title(slug):
    """
    Tireleri boşluk yapar, kelimelerin ilk harflerini büyük yapar.
    """
    return " ".join(word.title() for word in slug.replace("_", "-").split("-"))


def build_static_site():
    print("Statik site oluşturuluyor...\n")
    PAGE_SIZE = 20
    all_pages = []

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
                try:
                    locale.setlocale(locale.LC_ALL, '')
                    print("Varsayılan sistem yerel ayarı kullanılıyor.")
                except locale.Error as e_default:
                    print(f"HATA: Varsayılan yerel ayar da ayarlanamadı: {e_default}. Çıkış yapılıyor.")
                    return

    if os.path.exists(OUTPUT_DIR):
        for item in os.listdir(OUTPUT_DIR):
            item_path = os.path.join(OUTPUT_DIR, item)
            if os.path.isdir(item_path) and item != os.path.basename(ASSETS_OUTPUT_DIR):
                shutil.rmtree(item_path)
            elif os.path.isfile(item_path) and item not in ["style.css", ".htaccess", "404.html"]:
                os.remove(item_path)
        print(f"'{OUTPUT_DIR}' dizini içeriği temizlendi.")
    else:
        os.makedirs(OUTPUT_DIR)
        print(f"'{OUTPUT_DIR}' dizini oluşturuldu.")

    error_404_md_path = os.path.join(CONTENT_DIR, "404.md")
    error_404_output_path = os.path.join(OUTPUT_DIR, "404.html")
    if os.path.exists(error_404_md_path):
        process_markdown_file(error_404_md_path, error_404_output_path)
        print(f"✔ 404 sayfası oluşturuldu: {error_404_output_path}")
    else:
        print(f"UYARI: '404.md' dosyası bulunamadı: {error_404_md_path}. 404 sayfası oluşturulamadı.")


    for root, dirs, files in os.walk(CONTENT_DIR):
        if os.path.basename(root) == os.path.basename(ASSETS_DIR):
            continue
        if root == CONTENT_DIR:
            if ".htaccess" in files:
                files.remove(".htaccess")
            if "404.md" in files:
                files.remove("404.md")

        html_files_in_dir = []

        for file in files:
            if file.endswith(".md"):
                full_input = os.path.join(root, file)
                rel_path = os.path.relpath(full_input, CONTENT_DIR).replace("\\", "/")

                html_file_name = "index.html" if file == "index.md" else file.replace(".md", ".html")
                output_path = os.path.join(OUTPUT_DIR, os.path.dirname(rel_path), html_file_name)

                print(f"İçerik: {rel_path} → Çıktı: {output_path}")

                with open(full_input, "r", encoding="utf-8") as f:
                    md_content_for_info_extract = f.read()

                info_for_list = extract_info_from_content(md_content_for_info_extract)
                current_file_title = info_for_list["title"]

                if not current_file_title:
                    current_file_title = slug_to_title(os.path.splitext(file)[0])

                process_markdown_file(full_input, output_path)

                mod_time = datetime.fromtimestamp(os.path.getmtime(full_input))
                rel_output_url = os.path.relpath(output_path, OUTPUT_DIR).replace("\\", "/")
                all_pages.append({
                    "title": current_file_title,
                    "url": rel_output_url,
                    "mod_time": mod_time
                })

                html_files_in_dir.append({
                    "filename": html_file_name,
                    "title": current_file_title
                })

        if html_files_in_dir:
            html_files_in_dir.sort(key=lambda x: locale.strxfrm(x["title"].lower()))

            total_items = len(html_files_in_dir)
            total_pages = (total_items + PAGE_SIZE - 1) // PAGE_SIZE

            current_output_subdir = os.path.relpath(root, CONTENT_DIR).replace("\\", "/")
            if current_output_subdir == ".":
                dir_display_name = 'Ana Dizin'
            else:
                dir_display_name = slug_to_title(os.path.basename(current_output_subdir))

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

                index_items_html = f"<h2>{dir_display_name}</h2>\n<ul>\n"
                for f in page_items:
                    index_items_html += f'  <li><a href="{f["filename"]}">{f["title"]}</a></li>\n'
                index_items_html += "</ul>"

                index_filename = "index.html" if page_num == 1 else f"index_{page_num}.html"
                index_output_path = os.path.join(OUTPUT_DIR, current_output_subdir, index_filename)

                base_url_for_pagination = get_base_url(index_output_path)
                page_content_description = f"Futbol Gezegeni'ndeki {dir_display_name} kategorisindeki sayfa {page_num}."
                index_items_html += build_pagination_html(page_num, total_pages, base_url_for_pagination)

                page_title_for_html_tag = f"{dir_display_name} (Sayfa {page_num})"

                # Dizin sayfaları için canonical URL'yi kökten başlayan ve SITE_BASE_PATH'i içeren olarak ayarla
                rel_url_for_canonical_index_segment = os.path.relpath(index_output_path, OUTPUT_DIR).replace("\\", "/")
                if os.path.basename(rel_url_for_canonical_index_segment) == "index.html":
                    rel_url_for_canonical_index_segment = os.path.dirname(rel_url_for_canonical_index_segment)
                    if rel_url_for_canonical_index_segment == ".":
                        rel_url_for_canonical_index_segment = ""
                    if rel_url_for_canonical_index_segment and not rel_url_for_canonical_index_segment.endswith('/'):
                        rel_url_for_canonical_index_segment += '/'
                
                if rel_url_for_canonical_index_segment == "":
                    final_canonical_url_for_index = SITE_BASE_PATH + "/"
                else:
                    final_canonical_url_for_index = f"{SITE_BASE_PATH}/{rel_url_for_canonical_index_segment}"
                final_canonical_url_for_index = final_canonical_url_for_index.replace("//", "/")


                index_html = generate_html_page(
                    title=page_title_for_html_tag,
                    content=index_items_html,
                    base_url=base_url_for_pagination,
                    description=page_content_description,
                    keywords=f"{dir_display_name.lower()}, sayfa {page_num}, futbol, futbol gezegeni",
                    og_title=page_title_for_html_tag,
                    og_description=page_content_description,
                    og_type="website",
                    canonical_url=final_canonical_url_for_index # SITE_BASE_PATH'li Canonical URL
                )

                os.makedirs(os.path.dirname(index_output_path), exist_ok=True)
                with open(index_output_path, "w", encoding="utf-8") as f:
                    f.write(index_html)

                print(f"Dizin sayfası oluşturuldu: {index_output_path}")

    generate_recent_posts_page(all_pages, OUTPUT_DIR)

    copy_assets()
    print(f"\nTüm site başarıyla '{OUTPUT_DIR}' klasörüne yazıldı.")


if __name__ == "__main__":
    build_static_site()
