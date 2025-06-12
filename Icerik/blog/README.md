# Football Planet Projesi

Football Planet, futbol temalı statik bir veri tabanı projesidir. Temel amacı; oyuncular, takımlar, stadyumlar, yetenekler ve blog içerikleri gibi futbolla ilgili verileri düzenli ve erişilebilir bir formatta sunmaktır.

---

## Proje Tanımı

Bu proje, başlangıçta PHP ve Markdown (.md) ile geliştirilmeye çalışılmış, ancak Apache2 entegrasyonuyla yaşanan zorluklar nedeniyle tamamen **Python (.py)** tabanlı bir yapıya geçiş yapmıştır. Tüm özellikler, projenin sahibi tarafından belirlenmiş ve büyük ölçüde yapay zeka (ChatGPT) desteğiyle kodlanmıştır.

Sistem, anahtar olarak **Markdown (.md)** formatındaki verileri işleyerek web tabanlı çıktılara dönüştürür. **Projenin tüm içerikleri hala .md dosyaları olarak muhafaza edilmektedir.** Ayrıca, dahili bir dizinleme mekanizması projenin ayrılmaz bir parçasıdır.

Kod tabanı, **Python (.py)** ile birlikte gömülü **CSS** ve **HTML5** kodlarını içermektedir. Geleneksel web sunucularının doğrudan Python kodunu yorumlayamaması sebebiyle, yapay zeka tarafından **`statik.py`** adında bir dönüştürücü geliştirilmiştir. Bu dönüştürücü, projenin statik HTML çıktılarını üreterek PHP destekli sunucular da dahil olmak üzere çeşitli ortamlarda sorunsuz bir şekilde barındırılmasını mümkün kılar. Proje ayrıca, sunucu yapılandırmalarını optimize etmek için **`.htaccess`** dosyasını da içermektedir.

Sistem, yüksek taşınabilirlik gözetilerek kodlanmıştır. Mevcut yedekleme altyapısı sayesinde, projenin farklı ortamlara taşınması veya dağıtımı sorunsuz bir şekilde gerçekleştirilebilir.

---

## Projenin Amacı

Football Planet Projesi, değişken veri içermeyen, tamamen statik bir yapıya sahiptir. Tüm güncellemeler kişisel bir bilgisayar üzerinden manuel olarak yönetilmekte olup, bu yaklaşım projenin basitliğini ve bakım kolaylığını sağlamaktadır.

Projenin temel amacı, kapsamlı bir **veri tabanı** işlevi görmektir. Sosyal etkileşim özelliklerinin, OpenGraph entegrasyonlarının veya temel yorum sistemlerinin dahi bulunmadığı bu projede, odak noktası yalnızca veri sunumu ve erişilebilirliğidir.

---

## İçerik Yapısı

Proje kapsamındaki veriler aşağıdaki ana kategorilere ayrılmıştır:

* **Blog:** Romanlar için içerik kuralları veya bilinmesi gerekenler gibi bilgilendirici metinler.
* **Oyuncular:** Detaylı oyuncu profilleri ve istatistikleri.
* **Takımlar:** Futbol takımlarına özel veriler.
* **Stadyumlar:** Futbol stadyumlarına dair bilgiler.
* **Yetenekler:** Oyuncuların spesifik yeteneklerine ilişkin açıklamalar.

**Blog** kategorisi dışındaki tüm içerikler (Oyuncular, Takımlar, Stadyumlar, Yetenekler) birbiriyle ilişkili ve bağlantılıdır. Her bir içerik veya kategoriye erişimde, ilgili verilere göre dizinleme özelliği sunan bir `index.html` sayfası bulunmaktadır. Bu özelliğiyle proje, bir **Wiki** ve **veri tabanı** arasında hibrit bir yapı sergilemektedir.

---

## Kamuya Açıklık Nedenleri

Projenin başlangıçta halka açık olması planlanmamıştı. Ancak, projenin sahibi olarak verilere her yerden erişim ihtiyacının doğması, bu projenin dışarıya açılmasına yol açmıştır. Aksi takdirde, verilerin yönetimi yalnızca yerel bir ortamda Python ile sürdürülebilirdi.

---

## Kaynak Kodlarına Erişim

Projenin kaynak kodları bugün itibari ile açıldı.

## Kurulum

Bu projeyi yerel sisteminize kurmak ve çalıştırmak için aşağıdaki adımları takip edebilirsiniz:

1.  **Gereksinimler:**
    * **Python 3.x** yüklü olmalıdır. ***Python 3.10'un üzerindeki sürümlerde kapsamlı testler yapılmamıştır.***
    * Projenin **dağıtımı** veya **yayınlanması** için bir **web sunucusu** (Apache, Nginx vb.) gerekebilir. Ancak, **yerel testler için doğrudan bir web sunucusu kurulumu zorunlu değildir.**

2.  **Proje Dosyalarını Kopyalama:**
    Proje kaynak kodlarına erişiminiz olduğunda, tüm dosyaları hedef dizine kopyalayın. 

3.  **Python Bağımlılıklarını Kurma:**
    Projenin çalışması için belirli Python kütüphaneleri gerekebilir. Proje dizininde (genellikle `requirements.txt` dosyasında listelenmiştir) gerekli bağımlılıkları yüklemek için aşağıdaki komutu çalıştırın:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Statik Çıktıları Oluşturma:**
    Football Planet, içeriklerini Markdown (.md) dosyalarından okuyarak statik HTML çıktıları üretir. Bu statik çıktıları oluşturmak için **`statik.py`** dönüştürücüsünü çalıştırmanız gerekmektedir:
    ```bash
    python statik.py
    ```
    Bu komut, `.md` dosyalarını işleyecek ve web tarayıcıları tarafından doğrudan görüntülenebilen HTML dosyalarını belirlenen çıktı dizinine yerleştirecektir.

5.  **Web Sunucusu Yapılandırması (Dağıtım İçin Önerilir):**
    Proje, `.htaccess` dosyası gibi sunucu yapılandırma örneklerini içerebilir. Bu dosyalar, Apache gibi sunucularda URL yeniden yazma (URL Rewriting) ve diğer sunucu davranışlarını yönetmek için kullanılır. Eğer bir Apache sunucusu üzerinde yayın yapmayı planlıyorsanız, sunucunuzda **`mod_rewrite`** modülünün etkin olduğundan ve `.htaccess` dosyalarının kullanımına izin verildiğinden emin olun.
    **Önemli Not:** `.htaccess` dosyası proje tarafından otomatik olarak oluşturulmaz veya güncellenmez. Sunucunuzun özel gereksinimlerine ve projenin hedef URL yapısına uygun olarak **elle yapılandırılması** gerekmektedir.

6.  **Erişim:**
    Statik çıktıları oluşturduktan sonra, bu HTML dosyalarını bir web sunucusu aracılığıyla veya doğrudan web tarayıcınızda açarak Football Planet'e erişebilirsiniz. Örneğin, yerel kurulumunuz için `file:///path/to/your/project/index.html` (doğrudan dosya erişimi) veya bir web sunucusu üzerinden yayınlanıyorsa `http://sitenizinadresi/` ya da ilgili alan adı üzerinden erişim sağlayabilirsiniz.