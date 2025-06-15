# Siteyi Yayınlama ve Temel URL Ayarları

Statik web siteni farklı sunucu ortamlarında sorunsuz bir şekilde yayınlamak için bazı temel URL ayarlarını anlaman önemli. Özellikle siten, alan adının ana dizini (`https://example.com/`) yerine bir alt dizine (`https://example.com/football-planet/` gibi) kurulduğunda bu ayarlar daha da kritik hale geliyor.

- - -

## Neden "Temel URL" Ayarı Gerekli?

Web sitendeki görseller, CSS dosyaları, JavaScript dosyaları ve diğer sayfalar arası bağlantılar genellikle **göreli yollarla** tanımlanır (örneğin, `../style.css` veya `/resimler/varsayilan-gorsel.jpg`). Bu göreli yolların tarayıcılar ve arama motorları tarafından doğru şekilde yorumlanabilmesi için sitenin internetteki **gerçek konumunu** bilmesi gerekir.

Özellikle SEO (Arama Motoru Optimizasyonu) ve sosyal medya paylaşımları için kullanılan **Canonical URL** (`<link rel="canonical">`) ve **Open Graph URL** (`<meta property="og:url">`) etiketleri, bir sayfanın internetteki tekil ve tercih edilen adresini tam olarak belirtmeli. Eğer siten bir alt dizinde kuruluysa ve bu etiketler alt dizin bilgisini içermezse, arama motorları sitenin konumunu yanlış anlayabilir veya içerik tekrarı gibi sorunlar yaşayabilir.

- - -

## `SITE_BASE_PATH` Değişkeni Nedir ve Nasıl Kullanılır?

'statik.py' Python dosyanın en başında bulunan `SITE_BASE_PATH` değişkeni, sitenin kök dizini altındaki gerçek yolunu belirtmeni sağlar. Bu sayede, statik site oluşturucu, tüm Canonical URL'leri ve Open Graph URL'lerini bu yolu da içerecek şekilde doğru olarak üretir.

Eğer normal dizinde olacaksa o `SITE_BASE_PATH` kısmın başına # olacak, ona dokunmayın.


### Nasıl Ayarlanır?
```
# ***********************************************************************************
# DİKKAT: Sitenizin dağıtıldığı kök dizin altındaki yolu buraya yazın.
# Eğer siteniz doğrudan "public_html" gibi ana dizinde ise "" (boş string) bırakın.
# Eğer siteniz "public_html/football-planet/" gibi bir alt dizinde ise "/football-planet" yazın.
# Burayı değiştirmeniz, canonical URL'lerin ve og:url'lerin doğru olmasını sağlar.
# Sitenizin dağıtım yolu değiştiğinde burayı güncellemeyi unutmayın!
SITE_BASE_PATH = "/football-planet" # <-- Bu satırı kendi durumunuza göre ayarlayın
# ***********************************************************************************
```

*   **Eğer siten alan adının ana dizininde yayınlanacaksa (örneğin `https://example.com/`):**  
    `SITE_BASE_PATH = ""` (Boş bırakın)
*   **Eğer siten alan adının bir alt dizininde yayınlanacaksa (örneğin `https://example.com/football-planet/`):**  
    `SITE_BASE_PATH = "/football-planet"` (Başına `/` koymayı unutma)

### Örnek Etkileri

`SITE_BASE_PATH = "/football-planet"` olarak ayarladığında:

*   **Canonical URL:** `/oyuncu/alp-pati.html` yerine `<link rel="canonical" href="/football-planet/oyuncu/alp-pati.html">` olarak üretilir.
*   **Open Graph URL:** Aynı şekilde, `<meta property="og:url" content="/football-planet/oyuncu/alp-pati.html">` olarak doğru şekilde ayarlanır.

Bu ayar, sitenin farklı dağıtım ortamlarına uyum sağlaması ve arama motorları ile sosyal medya platformları tarafından doğru şekilde anlaşılması için kritik öneme sahip.

- - -

## Önemli Not: Her Değişiklikte Tekrar Çalıştırma

`SITE_BASE_PATH` değerini değiştirdiğinde veya siteni farklı bir alt dizine taşıdığında, statik site oluşturucu betiği **tekrar çalıştırmalı** ve oluşan tüm `public` klasörü içeriğini **yeniden sunucuna yüklemelisin.** Aksi takdirde, siten eski URL yapılandırmasıyla çalışmaya devam eder.

Sunucunda aktif bir **önbellekleme (caching)** sistemi varsa (CDN, LiteSpeed Cache vb.), yeni içeriklerin düzgün servis edilebilmesi için önbelleği de temizlemeyi unutma.