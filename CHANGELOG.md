# Değişiklik günlüğü

## 1.5.0 · Defterde yeni dokunuşlar

- **Yerinde seçenekler:** Değişen bir kısmın üstüne gelince başında küçük oklar çıkıyor. Oklar önerilen hal, daha kısa, daha resmî, daha sıcak ve eski hal arasında metnin içinde geziyor, seçeneğin adı yanda kısa süre görünüyor. Oklar kısmın başında durduğu için metin kısalıp uzasa da yerinden oynamıyor.
- **Son hal:** Başlığın yanındaki göz düğmesi ya da `p` tuşu kararların uygulanmış halini işaretsiz, kartsız gösteriyor. Burada da değişen kısmın üstüne gelince oklar çıkıyor.
- **Kart üstte:** Geniş ekranda kart defterin sağında üst hizada açılıyor, sayfa kaydırılırken yerinde kalıyor. Kesik çizgi cümleden çıkıp kartın yanında kıvrılarak ona bağlanıyor.
- **Son satır:** İlerleme, açık sorular, "Kalanları kabul et" ve "Ajana gönder" köşede yüzen banttan kâğıdın son satırına indi. "1 soru açık" yazısına tıklayınca sıradaki soruya gidiliyor.
- **Ayırıcı:** Skill'in notlarıyla metin arasında ince bir fosforlu kalem çizgisi var.
- **Kart okunurluğu:** Bölüm başlıkları daha belirgin. "Neydi" kırmızı kalemle yazılıyor, çıkarılan kelimeler harflerin arkasından geçen silik bir kalem iziyle karalanıyor.
- Düzenle menüsündeki "önizle" düğmesinin adı, son hal önizlemesiyle karışmasın diye "geri bildirimi göster" oldu.

## 1.4.0 · Ortak defter

- **Ortak çekirdek:** İnceleme sayfası ve canlı köprü, İngilizce kardeşi Still Human? ile ortak kullanılan [notebook-review](https://github.com/MesutARIDORU/notebook-review) deposuna taşındı. Skill'de `notebook/` klasöründe bir kopyası durur, kimliği (ad, dil, kalıp adları) `notebook.json` dosyasında. `scripts/review.py` ve `scripts/bridge.py` artık bu çekirdeği çağıran kısa betikler. Komutlar ve seçenekler aynı kaldı. `assets/review.html` kaldırıldı.
- **Eşitleme:** Her gün çalışan bir GitHub iş akışı (`.github/workflows/sync-notebook.yml`) `notebook/` klasörünü ortak depodaki son haliyle karşılaştırır, değiştiyse sayfanın hâlâ üretildiğini deneyip günceller.
- **Cümle bölme:** "Dr. Ayşe", "vb. meyveler" gibi kısaltmalarda ve küçük harfle devam eden yerlerde cümle artık bölünmüyor. Böylece karşılaştırmada cümleler daha doğru eşleşiyor.
- **Güvenlik:** Kullanıcının metninde ya da başlıkta geçen bir yazı sayfanın şablon yuvalarından biri gibi okunamıyor.

## 1.3.0 · Yeni not kartı

- **Not kartı:** Sade, düz yazılı bir kart. Üç bölümü var: "Neydi" (çıkarılan kısımların üstü çizili), "Önerilen" (eklenen kelimeler kalın) ve "Başka seçenekler" (aynı cümlenin daha kısa, daha resmî ve daha sıcak hali). Karar "Kalsın", "Eskisine dön", bir seçeneğin yanındaki "Kullan" ya da "Kendim yazayım" ile verilir. Kartın üstünde değişiklikler arasında gezinme okları ve kalıbın adı var.
- **Duyarlı yerleşim:** Geniş ekranda kart defterin sağında, cümlenin hizasında açılır ve kesik bir çizgiyle cümleye bağlanır. Ajanın içindeki tarayıcı gibi dar bir pencerede cümlenin altında, telefonda ekranın altından açılır. Dar pencerede küçük bir not, kartı yanda görmek için sayfayı tarayıcıda açmayı önerir.
- **Kenar işaretleri ve ilerleme bandı:** Kenar boşluğunda her değişen satırın durumu görünür: bakılmadı, kalsın, eskisine döndü, senin yazdığın. Alttaki bant ilerlemeyi ve açık soruları gösterir, "Kalanları kabul et" düğmesi bakılmayanları bu haliyle onaylar.
- **Sorular:** Köşeli parantezli yer tutucular metinde ve kartta turuncu görünür.
- **Seçenekler notlarda:** Ajan inceleme notlarına her değişiklik için `alternatives` alanını yazar. Köprü açıksa ve seçenek yoksa kart üç hali ajandan ister, kullanıcı başka bir istek de yazabilir.
- **Yazı tipleri:** Arayüzde el yazısı yazı tipi kalmadı, yalnızca başlıktaki logo el yazısı.
- **Düzeltme (`scripts/review.py`):** Tamamen silinen ya da tamamen eklenen bir cümlenin karşı metindeki yeri yanlış hesaplanıyordu. Bu yüzden "[silindi]" işareti yanlış yere düşüyor, önündeki değişmemiş metin (örneğin selamlama) değişmiş gibi görünüyordu. Böyle bir cümle artık yanındaki boşluğu da götürüyor, değişiklik geri alınınca çift boşluk kalmıyor.

## 1.2.2 · Kurulum anlatımı

- **Kurulum belgeleri:** README ve INSTALL.md artık `npx skills`'in gerçekte gösterdiği ekranları anlatıyor. Etkileşimli kurulumda Codex ve Gemini CLI her zaman dahil, Claude Code ise seçili gelmiyor. Belgeler onu nasıl işaretleyeceğini söylüyor. Hızlı başlangıç, üç ajana da soru sormadan kuran tek komutla açılıyor: `npx skills add MesutARIDORU/insanlik-oldu-mu -g -y -a claude-code codex gemini-cli`.
- **Ayar betiği (`scripts/install.py`):** README'de kurulumun parçası gibi duran menüsü kalktı, betik isteğe bağlı bir adım olarak ayrı anlatılıyor. Depodan çalışırken `npx skills`'e geçtiği yerde Claude Code'un nasıl seçileceğini söylüyor.

## 1.2.1 · İlk yayın

Türkçe metindeki yapay zeka izlerini bulan ve metni, bilgisine dokunmadan, doğal Türkçeyle yeniden kuran ajan skill'i. Claude Code, Codex ve Gemini CLI'da çalışır, `npx skills` ile kurulur. Kod, dosya ve klasör adları, betik komutları ve seçenekleri İngilizce. Kullanıcının gördüğü her şey Türkçe.

**Yazım**
- **Bilgi sadakati:** Kaynakta olmayan rakam, kurum, kaynak, anı ya da görüş metne girmez. Eksik bilgi yer tutucuyla işaretlenir ya da kullanıcıya sorulur. İddianın gücü korunur. Kurguda sahneye eklenen ayrıntılar tabloda "eklenen ayrıntı" diye ayrıca gösterilir.
- **Beş mod:** teşhis, hafif dokunuş, tam yeniden yazım, sıfırdan yazım ve geri bildirim turu.
- **Metin tanımı ve alan:** Skill metnin türünü (12 tür, `references/genres.md`) ve alanını (9 alan, `references/sectors.md`) tanır, o türün ve alanın diliyle çalışır. Alan rehberleri okuru, o alandaki tipik izleri ve değişirse zarar doğuracak bilgileri (doz, oran, süre, yasal uyarı) sayar.
- **Kalıp kataloğu:** Altı ailede 50 kodlu kalıp (Y, R, S, T, B, G). Her kalıbın önce/sonra örneği, çoğunun alanlardan bir örneği ve iz sayılmayan kullanımları ("Yanlış alarm") `references/patterns.md` dosyasında.
- **Akış kuralları:** Türkçe dil bilgisine dayanan 35 kural (A1-A35): söz dizimi, bağlama, ritim, vurgu, kip ve kesinlik, kelime dokusu, hitap, iş metni ve anlatı. Örneklerin bir kısmı TDK Güncel Türkçe Sözlük'te geçen, telif süresi dolmuş yazarlara ait cümleler.
- **Deyimler:** İş durumlarına göre gruplanmış deyimler, her birinin yerine geçtiği yapay zeka kalıbı ve alanından bir örnek. Türlere göre doz, çeviri kokan deyimler, karıştırılan çiftler ve atasözleri. TDK sözlüğünde ayrı madde olarak bulunanlar ✓, henüz aranmamış olanlar ◦ ile işaretli.
- **Terimler:** Yazılım, finans, sağlık, hukuk, kamu, e-ticaret, insan kaynakları, eğitim ve pazarlama için terim tabloları. Ölçü sözlük değil, okurun gerçek kullanımı.
- **Yazım ve noktalama:** TDK'nin yazım kuralları sayfalarından: konuşma çizgisi, ara söz için kısa çizgi, düzeltme işareti, başlık düzeni, sayı, para, yüzde, tarih, saat, kısaltma, kurum adı ve unvan yazımı.

**Teslim**
- **Sohbette duyuru:** Skill iş başlarken sohbete `💀 İnsanlık öldü mü❓ · Metin tanımı: … · Alan: … · Yaklaşım: …` satırını yazar ve beklemeden devam eder.
- **Teslim biçimi:** Logolu başlık satırı, nihai metin, "Neyi neden değiştirdim" tablosu, ölçüm satırı ve gerekiyorsa en fazla üç soru.
- **Önizleme sorusu:** Teslimden sonra skill, değişiklikleri önizleme sayfasında görmek isteyip istemediğini sohbette seçenekli olarak sorar. Metin soru yüzünden beklemez.
- **Örnek yazıdan ses:** Kullanıcı kendi yazısından örnek verirse cümle boyu, sicil, hitap ve kelime seçimi oradan alınır, örnekteki bilgiler metne taşınmaz.

**Betikler**
- **Sayısal denetim (`scripts/audit.py`):** Cümle boyu çeşitliliği, eş boy cümle dizileri, açılış tekrarı, cümle sonu kafiyesi, tire ve noktalı virgül, karşıtlık ve üçleme, yapay zeka ve moda sözleri, plaza jargonu, aşırı terim çevirisi, çeviri e-posta kalıpları, klişe giriş ve kapanış, şapka tutarlılığı, başlık düzeni ve Ateşman okunabilirliği. Önce ve sonra değerleri yan yana verir. Tür ve alan tahmini yapar, `--guide` ile ilgili rehberleri yazdırır.
- **İnceleme sayfası (`scripts/review.py`):** Defter görünümlü, tek dosyalık bir sayfa. Yalnızca değişen kelimeler işaretli: orta kalınlık ve arkasında çok hafif sarı bir fosforlu kalem. Tıklayınca önceki hal, gerekçe ve seçenekler çıkar: eski ya da yeni hali seçmek, "Başka öner", not eklemek.
- **Canlı köprü (`scripts/bridge.py`):** Sayfa ajandan öneri ister ve kararları doğrudan ajana gönderir. Üç yol: dinleyen ajan, oturum çatalı (Claude Code ve Codex) ve bağlamsız çağrı (Claude Code, Codex, Gemini CLI). Sunucu yalnız 127.0.0.1'de ve oturuma özel bir anahtarla çalışır.
- **Ayar betiği (`scripts/install.py`):** `npx skills` ile kurulan kopyadan çalışınca yalnızca ayarları yapar: Claude Code izinleri, Codex yönlendirme notu, Gemini CLI komutu ve köprü ayarı. Node.js olmayan bilgisayarda depodan çalıştırılınca skill'i seçilen araçlara kendisi bağlar.

**Görünüm**
- **Logo:** Kuru kafa ve kırmızı soru işareti. Sohbette `💀 İnsanlık öldü mü❓` imzası, inceleme sayfasında el çizimi bir kuru kafa.
- **Codex:** `agents/openai.yaml` ile Türkçe adı ("İnsanlık öldü mü?"), kuru kafa simgesi ve kısa açıklaması.
