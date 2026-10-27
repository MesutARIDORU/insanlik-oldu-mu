# Değişiklik günlüğü

## 1.7.2 · Daha kolay okunan README

- **README baştan yazıldı:** Örnek artık girişin hemen altında, okur skill'in ne yaptığını önce görüyor. Her ilkenin kendi başlığı var: "Metne bilgi eklemez", "Metnin türüne göre yazar", "Önce cümlenin kuruluşunu düzeltir", "Her değişikliği gerekçesiyle gösterir" ve "Sağlam metni bozmaz".
- **"Bilgi uydurmaz" paragrafı:** "Okur bunu yayımlar" cümlesi kimin neyi yayımladığını söylemiyordu. Paragraf artık araçların neyi uydurduğunu, metni kimin fark etmeden yayımladığını ve skill'in eksik bilgi karşısında yaptığı üç şeyi ayrı ayrı anlatıyor.
- **İnceleme sayfası:** Sayfanın ne zaman açıldığı bir tabloda, sayfada ne yapılacağı kısa bir listede. Kart konumu ve seçenek balonu gibi ince ayrıntılar açılır-kapanır bir bölümde.
- **Kullanım tablosu:** İstekler okurun kendi diliyle yazıldı ("Metni baştan kurması"), teslimde göreceği mod adı parantezde.

Skill'in davranışı değişmedi, yalnızca README yenilendi.

## 1.7.1 · Daha çok araçta

- **Açıklama:** Skill'in açıklaması artık tetikleyici kelimelerle başlıyor ("Türkçe metni doğallaştırır ve insanlaştırır"), adı sonda. Codex çok sayıda skill yüklüyken açıklamaları kısaltıyor ve tetikleyici kelimeler kesilen kısımda kalıyordu. 230 skill yüklü bir bilgisayarda Codex skill'i artık adı verilmeden seçiyor.
- **Claude sohbeti:** Her sürüme `insanlik-oldu-mu.zip` ekleniyor. Claude'un masaüstü ve web sohbetine Customize > Skills'ten yüklenebiliyor. Tarayıcının ulaşamadığı böyle bir ortamda inceleme sayfası canlı açılmıyor, indirilebilir bir dosya olarak geliyor ve kararlar kopyala-yapıştırla dönüyor.
- **Hangi araçlarda çalışır:** README'deki tabloda her araçta neyin denendiği yazıyor: Claude Code, Codex CLI, ChatGPT masaüstü uygulamasındaki Codex, Antigravity, Gemini CLI ve Claude sohbeti. Gemini CLI'ın, Google ücretsiz bireysel hesaplarda kapattığı için o hesaplarla çalışmadığı da yazıyor.
- **Güncelleme komutu:** `npx skills update -g insanlik-oldu-mu`. `-g` olmadan komut kapsam soruyor, Enter "Project"i seçiyor ve global kurulan skill güncellenmiyor.

## 1.7.0 · İlk seferde önizleme, Antigravity

- **İlk kullanımda önizleme:** Skill ilk kez kullanıldığında önizleme sayfası sormadan açılıyor. Sayfadaki bantlı not bundan sonrasını soruyor: "Her seferinde aç", "Önce bana sor" ya da "Ben isteyince aç". "Ben isteyince aç" seçilince not, sohbet kutusuna "önizle", "sayfada göster", "değişiklikleri sayfada aç" yazan bir animasyonla sayfanın nasıl açılacağını gösteriyor. Claude Code ve Codex'te "bu sohbette hep aç" ve "bu sohbette açma" seçenekleri de var.
- **Tercih dosyada:** Seçim `~/.config/insanlik-oldu-mu/preferences.json` dosyasında duruyor. 5. adım sormadan önce `bridge.py preview` ile ona bakıyor. "Önce bana sor" seçiliyken metin uzunsa ya da değişiklik çoksa sayfa sormadan açılıyor. Tercih sayfanın ayarlarındaki Önizleme satırından ya da sohbette "önizleme hep açılsın" gibi bir cümleyle değişiyor.
- **Antigravity:** Kurulum betiği Antigravity'yi buluyor ve skill'i onun okuduğu `~/.gemini/config/skills` klasörüne bağlıyor. `npx skills` Antigravity'ye bağlantı kurmadığı için skill orada görünmüyordu. `npx skills` ile kurduktan sonra: `python3 ~/.agents/skills/insanlik-oldu-mu/scripts/install.py --targets antigravity`. Ayrıntısı INSTALL.md'de.
- **Başlık:** "İnsanlık öldü mü?" yine Marker Felt ile, sayfada, kapakta ve görüntülerde.

## 1.6.1 · Yeni kapak

- **README kapağı:** Kapak resmi inceleme sayfasının yeni görünümüyle yeniden çizildi: ahşap masada defter yaprağı, el yazısı, yeşil fosforlu kalem, seçenek balonu ve bantlı kart. Örnek aynı: "Yeni sürüm sadece bir güncelleme değil, sayfaları iki kat hızlandıran bir dönüşüm yolculuğu." cümlesi "Yeni sürüm sayfaları iki kat hızlandırıyor." oluyor. Yazılar çizgilerin hemen üstüne oturuyor.

## 1.6.0 · Masadaki defter

- **Yeni görünüm:** İnceleme sayfası ahşap bir masada duran, delikli, çizgili bir defter yaprağı. Metin, başlık ve kart Patrick Hand el yazısıyla yazılıyor. Font ve dokular (kâğıt, bant, fosforlu kalem, ahşap) sayfanın içine gömülü, sayfa dışarıya istek atmıyor.
- **Metin:** Değişen kelimelerin arkasında yeşil bir fosforlu kalem var. Onaylanan değişikliğin eski hali üstü çizili olarak yeni halin hemen üstünde ya da önünde kalıyor.
- **Kenar boşluğu:** Her değişikliğin ortasında numaralı bir yuvarlak var, birden çok satıra yayılan değişikliği turuncu bir küme parantezi sarıyor. Gerekçenin ilk cümlesi sağ kenara küçük bir okla not düşülüyor. Yan yana duran değişikliklerin yuvarlakları üst üste binmiyor, alt alta diziliyor.
- **Kart:** Bantlı bir not kâğıdı. "Öneriyi uygula" (`1`) değişikliği onaylayıp sıradakini açıyor, altında "Kalsın" (`2`) ve "Kendim düzenleyeyim" (`3`) var. Başka seçenekler yanlarındaki okla seçiliyor. Uzun bir kartın içeriği bandın altında kayıyor.
- **Seçenek balonu:** Değişen bir kısmın üstüne gelince el çizimi bir konuşma balonu açılıyor, yazısı başlığın altındaki çizginin kırmızısı. Balon metindeki seçeneğin adını ve sırasını gösteriyor. ‹ › seçenekler arasında geziyor, ▾ hepsini listeliyor. Canlı köprüyle açılan sayfada seçenek yoksa listeden ajana istek gönderilebiliyor. Balon son hal önizlemesinde de çıkıyor.
- **İlerleme:** Son satır onaylanan değişiklikleri sayıyor: "3 / 5 onaylandı".
- **Ayarlar:** Yazı tipi ayarı yeni bir adla saklanıyor ve varsayılanı el yazısı. Eski ayar yok sayıldığı için herkes yeni sayfayı bir kez varsayılan haliyle görüyor.
- **Gerekçeler:** Gerekçenin ilk cümlesi kenar notu olduğu için SKILL.md onu kısa tutmayı ve ayrıntıyı ikinci cümleye bırakmayı istiyor.

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
