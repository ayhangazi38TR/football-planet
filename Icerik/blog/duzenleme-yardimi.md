## İçerik Ekleme ve Düzenleme

Football Planet projesine yeni içerik eklemek veya mevcut bilgileri düzenlemek, projenin statik yapısı sayesinde oldukça basittir. Temel olarak, **Markdown (`.md`) dosyalarını düzenlemeniz** ve ardından **statik HTML çıktılarını yeniden oluşturmanız** gerekir.

Markdown dosyalarını düzenlemek için, özellikle Markdown odaklı metin düzenleyicileri kullanmanız iş akışınızı kolaylaştıracaktır. Bu konuda **GhostWriter** uygulamasını şiddetle tavsiye ederiz. GhostWriter hakkında daha fazla bilgi için resmi sitesini ziyaret edebilirsiniz: [https://ghostwriter.kde.org/tr/](https://ghostwriter.kde.org/tr/)

---

### Mevcut İçeriği Düzenleme

Mevcut bir içeriği düzenlemek için, ilgili Markdown dosyasını projenizin dosya yapısı içinde bulmanız yeterlidir. Örneğin, bir takımın bilgilerini güncellemek istiyorsanız:

1.  **İlgili Klasöre Gidin:** Proje dizininde `takim` klasörüne gidin.
2.  **Takım Dosyasını Bulun:** Düzenlemek istediğiniz takımın Markdown dosyasını (örneğin, `ornek-takim-fc.md`) bulun ve açın.
3.  **İçeriği Düzenleyin:** Dosyayı tercih ettiğiniz bir metin düzenleyici ile açın ve istediğiniz değişiklikleri yapın. Markdown söz dizimine uygun şekilde başlıkları, listeleri, bağlantıları ve metinleri düzenleyebilirsiniz.
4.  **Değişiklikleri Kaydedin:** Yaptığınız değişiklikleri `.md` dosyasına kaydedin.

---

### Yeni İçerik Ekleme

Yeni bir takım veya herhangi başka bir kategoriye (oyuncu, stadyum, yetenek vb.) yeni bir girdi eklemek için aşağıdaki adımları izleyin:

1.  **Doğru Klasörü Seçin:** Eklemek istediğiniz içeriğin türüne göre ilgili klasöre gidin. Örneğin, yeni bir takım eklemek için `takim` klasörüne gidin.
2.  **Yeni `.md` Dosyası Oluşturun:** Klasör içinde yeni bir Markdown dosyası oluşturun. Dosya adının, içeriğin başlığına uygun ve URL dostu (küçük harf, boşluk yerine tire ile) olmasına dikkat edin. Örneğin, `yeni-takim-adi.md`.
3.  **İçeriği Oluşturun:** Yeni oluşturduğunuz `.md` dosyasının içine, projenin diğer örnek dosyalarındaki yapıya uygun şekilde Markdown söz dizimi ile içeriği yazın.
    * **Örnek Takım Yapısı:** Aşağıdaki gibi bir şablon kullanabilirsiniz:
        ```markdown
        # Yeni Takım Adı
        ## New Team Name

        ### Künye
        * Diziliş: 1-4-4-2 (Futbol Diziliş Kuralları)
        * Koç: Yeni Koç Adı
        * Menajer: Yeni Menajer Adı
        * Kaptan: Yeni Kaptan Adı
        * Renkler: #RRGGBB, #AABBCC
        * Stadyum: [Yeni Stadyum Adı](/stadyum/yeni-stadyum)

        ## Oyuncular
        * GK: [Kaleci Adı](/oyuncu/kaleci-adi)
        * DF: [Defans Adı](/oyuncu/defans-adi)
        * MF: [Orta Saha Adı](/oyuncu/ortasaha-adi)
        * FW: [Forvet Adı](/oyuncu/forvet-adi)
        ```
4.  **Kaydedin:** Dosyayı kaydedin.

---

### Statik Çıktıları Yeniden Oluşturma

Herhangi bir `.md` dosyasında değişiklik yaptığınızda veya yeni bir `.md` dosyası eklediğinizde, bu değişikliklerin web sitesinde görünür olması için **statik HTML çıktılarını yeniden oluşturmanız** gerekir.

1.  **Dönüştürücüyü Çalıştırın:** Projenizin ana dizininde bulunan **`statik.py`** dosyasını çalıştırın:
    ```bash
    python statik.py
    ```
    Bu komut, tüm `.md` dosyalarını tarayacak ve güncel HTML çıktılarını oluşturacaktır.

2.  **Kontrol Edin:** Statik çıktıları oluşturduktan sonra, web sunucunuzda veya doğrudan tarayıcınızdan ilgili sayfayı kontrol ederek değişikliklerin yansıdığından emin olun.

Bu basit adımlarla, Football Planet projenizin içeriğini kolayca yönetebilir ve güncel tutabilirsiniz.