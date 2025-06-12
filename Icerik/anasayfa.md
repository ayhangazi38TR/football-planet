# Anasayfa
## Home Page

Football Planet, futbol dünyasına dair kapsamlı bilgileri düzenli ve erişilebilir bir formatta sunmayı amaçlayan, tamamen **statik bir veri tabanı projesidir**. Amacımız, sürekli güncel kalabilen, hafif ve hızlı bir bilgi kaynağı oluşturmaktır.

---

## Projenin Temel Mantığı

Football Planet'in mimarisi, başlangıçtaki PHP tabanlı yaklaşımdan, Apache2 sunucusunun getirdiği karmaşıklıkları aşmak adına tamamen **Python (.py)** diline geçilerek tasarlanmıştır. Bu dönüşüm, projenin hem geliştirme sürecini hem de yönetimini önemli ölçüde basitleştirmiştir.

Projenin kalbinde, tüm içeriğin **Markdown (.md)** formatında barındırılması yatar. Bu sayede içerik oluşturma ve düzenleme süreci son derece kolay ve metin tabanlı hale gelmiştir. Python tabanlı sistemimiz, bu `.md` dosyalarını alarak otomatik olarak okunabilir **HTML çıktılarına** dönüştürür. Bu dönüştürücü sayesinde, ortaya çıkan statik HTML dosyaları herhangi bir standart web sunucusunda (Apache, Nginx vb.) sorunsuzca yayınlanabilir.

---

## Neden Statik?

Football Planet'in statik yapısı, beraberinde birçok avantajı getirir:

* **Performans:** Sunucu tarafında dinamik bir işlem olmadığı için sayfalar çok daha hızlı yüklenir.
* **Güvenlik:** Dinamik kod çalıştırmadığı için potansiyel güvenlik açıkları minimuma iner.
* **Basitlik:** Karmaşık veritabanı veya sunucu konfigürasyonlarına ihtiyaç duymaz. Tüm güncellemeler yerel makinede yapılır ve ardından statik çıktıların sunucuya yüklenmesiyle yayınlanır.
* **Taşınabilirlik:** Üretilen statik dosyalar, herhangi bir hosting ortamına kolayca taşınabilir.

Projenin temel amacı, bir etkileşim platformu olmaktan ziyade, saf bir bilgi kaynağı olarak hizmet etmektir. Bu nedenle yorum sistemleri, kullanıcı etkileşimleri veya sosyal medya entegrasyonları gibi özellikler bilinçli olarak dahil edilmemiştir.

---

## İçerik Yapısı ve Kapsamı

Football Planet, futbolun farklı yönlerine odaklanan kapsamlı bir bilgi havuzu sunar. Mevcut içerik kategorileri şunlardır:

* **Oyuncular:** Futbolculara dair detaylı bilgiler.
* **Takımlar:** Kulüpler ve milli takımlar hakkında veriler.
* **Stadyumlar:** Futbol sahalarının özellikleri ve bilgileri.
* **Yetenekler:** Oyuncuların sahip olduğu özel yeteneklerin açıklamaları.
* **Blog:** Projeyle ilgili duyurular, geliştirme notları veya genel futbol yazıları için bir alan sunar.

Oyuncular, takımlar, stadyumlar ve yetenekler arasındaki ilişkiler, projenin dizinleme sistemi sayesinde birbirine bağlıdır. Bu sayede kullanıcılar, veriler arasında kolayca gezinebilir ve ilgili bilgilere hızla ulaşabilir. Projenin bu yapısı, onu bir **Wiki** ve **veri tabanı** arasında hibrit bir konuma getirir.

---

### Blog ve Daha Fazlası

Projemizdeki blog içeriklerine ulaşmak ve güncellemeler hakkında bilgi edinmek için [Blog Ana Sayfası](/blog/README.md) bağlantısını ziyaret edebilirsiniz.