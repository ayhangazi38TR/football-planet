## Tema Düzenleme

Football Planet’in görünümünü özelleştirmek mümkündür. Ancak bazı temel yapı taşlarına dikkat edilmelidir.

### 1. `layout.html`

Tüm tema yapısı `layout.html` dosyasında tanımlıdır.  
Bu dosya, statik olarak oluşturulan tüm sayfaların temel şablonudur ve HTML5 yapısı bu dosya üzerinden yönetilir.

#### Dikkat Edilmesi Gerekenler:

- `{{ }}` ve `{% %}` şeklindeki yapılar **Jinja2 şablon motoruna** aittir.  
  Bunlar içerik yerleştirme ve kontrol akışlarını temsil eder.  
  Bu bloklara yanlış müdahale edilmesi sayfaların doğru çalışmamasına neden olabilir.
- Görsel düzenlemeler için doğrudan HTML yapılarına müdahale edebilirsiniz.  
  Ancak, değişkenlerin geçtiği kısımları mümkünse değiştirmemeniz tavsiye edilir.

### 2. `style.css`

Görsel stil ayarları `style.css` dosyasında tanımlanmıştır.  
Bu dosya, sitenin renklerini, yazı tiplerini, kenar boşluklarını ve düzen öğelerini kontrol eder.

#### Düzenleyebileceğiniz Başlıca Alanlar:

- Arka plan ve yazı renkleri
- Başlık boyutları ve yazı tipi stilleri
- Navigasyon çubuğu ve alt bilgi (footer) tasarımı
- Kart görünümleri, liste düzenleri, tablo stili vb.

#### Tavsiyeler:

- Mevcut CSS sınıflarını değiştirirken, temanın bütünlüğünü korumaya dikkat edin.
- Yedek alarak çalışmanız önerilir.
- Modern tarayıcılarda test ederek görsel uyumluluğu kontrol edin.

---

### Genel Uyarı

Temayı özelleştirirken, sitenin işlevselliğini sağlayan yapılarla (şablon değişkenleri ve içerik döngüleri gibi) oynamamaya özen gösterin.  
Görsel düzenlemeler için `style.css` dosyasını, yapısal düzenlemeler için ise `layout.html` dosyasını kullanın.

---

> Bu yapı, işlevsel bir çekirdeğin üzerine inşa edilmiş sade bir görünüm sunar.  
> Renkleri, boşlukları ve çizgileri değiştirebilirsiniz; ama motoru yerinden sökmeyin. Yoksa site bozulur.
