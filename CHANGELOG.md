# Değişiklik günlüğü

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
