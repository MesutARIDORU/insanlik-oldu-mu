# Kuralların dayanağı

Bu dosya, skill'in kurallarının nereye dayandığını gösterir. Yalnızca bu projede gerçekten açılıp okunan, sorgulanan ya da denenen kaynaklar burada.

## TDK yazım kuralları

Aşağıdaki sayfalar Ekim 2026'da tek tek okundu, son dördü 21 Ekim 2026'da. `spelling.md` dosyasındaki kurallar bunlara dayanıyor.

| Sayfa | Skill'deki karşılığı |
|---|---|
| [Noktalama işaretleri](https://tdk.gov.tr/icerik/yazim-kurallari/noktalama-isaretleri-aciklamalar/) | Noktalı virgül ve iki noktanın meşru kullanımı, ara söz için bitişik kısa çizgi |
| [Uzun çizgi](https://tdk.gov.tr/icerik/yazim-kurallari/uzun-cizgi/) | Satır başı konuşma çizgisinin korunması (B1 istisnası) |
| [Düzeltme işareti](https://tdk.gov.tr/icerik/yazim-kurallari/duzeltme-isareti/) | Şapkanın sicile göre kullanımı ve tutarlılık (B8) |
| [Büyük harflerin kullanıldığı yerler](https://tdk.gov.tr/icerik/yazim-kurallari/buyuk-harflerin-kullanildigi-yerler/) | Alt başlıklarda küçük kalan bağlaçlar (B6), kurum adları, belirli tarihteki ay ve gün adları, para birimlerinin küçük harfi |
| [Sayıların yazılışı](https://tdk.gov.tr/icerik/yazim-kurallari/sayilarin-yazilisi/) | Rakam ve yazı seçimi, basamak noktası, kesir virgülü, yüzde işareti, sıra ve üleştirme sayıları |
| [Kısaltmalar](https://tdk.gov.tr/icerik/yazim-kurallari/kisaltmalar/) | Kısaltmalara gelen ekler, ölçü birimleri, noktalı kısaltmalar |
| [Pekiştirmeli sözlerin yazılışı](https://tdk.gov.tr/icerik/yazim-kurallari/pekistirmeli-sozlerin-yazilisi/) | Pekiştirmenin bitişik yazımı (A22) |

## TDK Güncel Türkçe Sözlük

[sozluk.gov.tr](https://sozluk.gov.tr) üzerinden Ekim 2026'da sorgulandı.

- **Deyimler:** `idioms.md` dosyasındaki kalıpların çoğu tek tek arandı. Ayrı madde olarak bulunanlar ✓ ile işaretli, bulunmayanlar işaretsiz. 21 Ekim 2026'da eklenen kalıplar ◦ ile işaretli: Sözlüğün sorgu servisi o gün 502 hatası veriyordu, bu kalıplar henüz aranamadı. Servis açılınca aranıp işaretleri güncellenecek.
- **Akış kuralı örnekleri:** `flow.md` dosyasındaki bazı örnekler sözlüğün madde örneklerinden alındı. Hepsi telif süresi dolmuş yazarların cümleleri: Ahmet Haşim, Orhan Veli Kanık, Sermet Muhtar Alus. Her örneğin yanında hangi maddeden alındığı yazıyor.

## Ölçümler

- **Ateşman okunabilirlik formülü:** `audit.py` okunabilirlik puanını bu formülle hesaplıyor: 198,825 − 40,175 × (hece / kelime) − 2,610 × (kelime / cümle). Hece sayısı ünlü sayısından bulunuyor.
- **Metin tanımı tahmini:** Tür ve alan tahmini bu proje için yazıldı. Yüzeydeki ipuçlarına bakar: dize yapısı, diyalog, kişi ekleri, gereklilik kipi, selamlama ve kapanış, kod blokları, kaynak gösterimi, alan sözcükleri. Farklı türlerden örnek metinlerle denendi. Bir ipucudur, son kararı ajan verir.
- **Öbür ölçümler:** Cümle boyu çeşitliliği, eş boy cümle dizileri, açılış tekrarı, cümle sonu kafiyesi, kalıp sözlerin sayımı ve ilk-son paragraf örtüşmesi bu proje için yazıldı. Eşikler alarm zili olarak seçildi, bilimsel bir sınır iddiası taşımıyor.

## Alan rehberleri

`sectors.md` ve `jargon.md` dosyalarındaki alan notları ve terim tabloları bu proje için yazıldı. Her alanın okurunu, yerleşik terimlerini ve o alanda değişirse zarar doğuracak bilgileri gözleme dayanarak sayıyor. Hukuki ya da tıbbi tavsiye değil, yazım rehberi. Alanlardaki sayı, tarih, kısaltma ve kurum adı yazımı TDK'nin yukarıdaki sayfalarına dayanıyor.

## Kullanım ve kullanıcı geri bildirimi

- **Jargon:** Kelime seçiminde ölçü sözlük değil, kitlenin gerçek kullanımı. Kullanıcı testinde TDK'nin "deadline" için önerdiği "süre sonu" yapay bulundu. `jargon.md` bu ilkeyle yazıldı.
- **İnceleme sayfası:** Sayfanın görünümü kullanıcıyla birlikte, tek tek denenerek kuruldu. Değişen kelimelerin yalnızca orta kalınlık ve hafif bir sarı fosforla işaretlenmesi bu denemelerin sonucu.

## Kendi deneme setimiz

`evals/` klasöründe altı örnek metin ve her biri için beklenen davranış var: genel kitleye LinkedIn gönderisi, bilgi uydurmadan blog yazısı, akademik metne hafif dokunuş, konuşma çizgili öykü, insan yazısının teşhisi ve geliştirici jargonu.

## Genel bilgi

Kalıp kataloğundaki izler (karşıtlıkla parlatma, önem şişirmesi, klişe giriş ve kapanış, uzun tire gibi), yapay zeka yazısı üzerine kamuya açık tartışmalarda yaygın olarak bilinen gözlemler. Akış kuralları Türkçe dil bilgisinin bilinen araçlarını (söz dizimi, kip, ikileme, pekiştirme) yazım kuralı olarak düzenliyor. Örneklerin TDK'den alınanlar dışındaki hepsi bu proje için yazıldı.
