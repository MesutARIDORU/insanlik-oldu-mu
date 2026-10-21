# İnsanlık öldü mü?

![İnsanlık öldü mü? Türkçe metindeki yapay zeka izlerini bulur, metni bilgisine dokunmadan doğal Türkçeyle yeniden kurar.](assets/cover.png)

Okuduğun duyurunun, gönderinin ya da e-postanın bir makineden çıktığını bazen ilk cümlede anlarsın:
- Söze "Hızla değişen dünyamızda" diye girer.
- Cümleler sırayla "-maktadır", "-mektedir" diye biter.
- Her özellik "yalnızca bir araç değil, bir deneyim" olur.
- Metin, kimsenin itiraz etmeyeceği parlak bir gelecek cümlesiyle kapanır.

**İnsanlık öldü mü?** bu izleri bulan ve metni, bilgisine dokunmadan, bir insanın yazacağı gibi yeniden kuran bir ajan skill'i. Claude Code, Codex ve Gemini CLI'da çalışıyor. Dosya okuyabilen her ajan da talimat dosyasını (`SKILL.md`) kullanabilir.

## Hızlı başlangıç

**1. Kur.** Terminale şunu yapıştır:

```bash
npx skills add MesutARIDORU/insanlik-oldu-mu -g
```

Komut hangi yapay zeka araçlarına kurulacağını sorar: Claude Code, Codex, Gemini CLI ve diğerleri. Skill, öbür skill'lerinle aynı ortak klasöre (`~/.agents/skills`) kurulur. Gerekenler Node.js ve Python 3.

**2. Kullan.** Ajana metni ver ve ne istediğini söyle:

```
Şu e-postayı doğallaştır:
[metin]
```

"Doğallaştır", "insanlaştır", "yapay zeka kokuyor", "bunu yapay zeka mı yazmış?" gibi istekler yeterli. Skill'i adıyla da çağırabilirsin:

| Araç | Komut |
|---|---|
| Claude Code | `/insanlik-oldu-mu [metin]` |
| Codex | `$insanlik-oldu-mu [metin]` |
| Gemini CLI | `/insanlik-oldu-mu [metin]` |

**3. Sonucu al.** Skill devreye girince sohbette önce şu satır belirir:

> 💀 **İnsanlık öldü mü❓** · Metin tanımı: kurumsal yazışma dili (e-posta) · Alan: finans · Yaklaşım: …

Ardından yeniden yazılmış metin ve "Neyi neden değiştirdim" tablosu gelir. En sonda skill, değişiklikleri önizleme sayfasında görmek isteyip istemediğini sorar. Sayfayı sonradan görmek için sohbete "önizle" yazman yeter.

Ayrıntılı kurulum seçenekleri aşağıdaki [Kurulum](#kurulum) bölümünde.

## Neyi farklı yapıyor

**Metnin ne olduğunu anlıyor.** Şiirde dize kırılması yazarın kararıdır. Teknik şartnamede "-malıdır" gerekliliği bildirir, kurumsal e-postanın sonundaki "Saygılarımla" da nezaket gereği orada durur. Bunları yapay zeka izi sanıp düzeltmek metni bozar. Skill önce metnin türünü ve alanını tanır, sonra o türün diliyle çalışır:
- şiir ve edebi anlatı,
- deneme ve kişisel yazı,
- kurumsal yazışma,
- teknik şartname ve teknik doküman,
- akademik, hukuki ve haber dili,
- pazarlama ve sosyal medya.

Şiire varsayılan olarak dokunmaz, yalnızca izleri gösterir. Şartnamede sınanamayan sıfatları ayıklar, gereklilik kipine elini sürmez. E-postada selamlama kalır, amaca gelmeyen giriş gider.

Alanın da kendi rehberi var. Yazılım, finans, sağlık, eğitim, hukuk, kamu, e-ticaret, insan kaynakları ve pazarlama için ayrı notlar tutuyor: okur kim, hangi terim kalır, o alanda model nasıl iz bırakır. Değişirse zarar doğuracak bilgiler de bu notlarda. Bankanın e-postasındaki oran ve tarih, hastanenin bilgilendirmesindeki doz ve süre, sözleşmedeki madde numarası harfi harfine kalır.

İş başlarken sohbete tek satırla neyle uğraştığını yazar:

> 💀 **İnsanlık öldü mü❓** · Metin tanımı: kurumsal yazışma dili (e-posta) · Alan: finans · Yaklaşım: tam yeniden yazım, selamlama ve kapanış korunur

Baştaki kuru kafa ve sondaki kırmızı soru işareti logodur: Skill'in devrede olduğunu buradan anlarsın. Aynı tanım inceleme sayfasında da başlığın altında yazar.

**Bilgi uydurmaz.** Yapay zeka metnini "insanlaştıran" araçların çoğu metni somutlaştırmak için rakam, kurum adı ya da anı uydurur. Okur bunu yayımlar, uydurma bilgi dünyaya çıkar. Bu skill kaynakta olmayan hiçbir bilgiyi eklemez. Somutluk gereken yerde ya metindeki bilgiyi öne çıkarır ya köşeli parantezli bir yer tutucu bırakır ya da sana sorar.

**Önce iskelete bakar.** Hangi kelimelerin "yapay zeka kokduğu" her yeni modelle değişiyor. Cümlenin kuruluşundaki izler ise kalıyor:
- aynı boydaki cümleler,
- aynı ekle biten yüklemler,
- "X değil, Y" iskeleti,
- her şeyi üçe bölmek.

Skill önce iskeleti değiştirir, sonra boşalan yere Türkçenin kendi ritmini koyar:
- virgülle akan eylem zinciri,
- ikileme,
- miş'li anlatım,
- cümle sonuna kayan bağlaç.

**Her değişikliğin gerekçesi var.** Teslimle birlikte bir değişiklik tablosu gelir: önce, sonra, neden. Gerekçeler kodlu kalıp kataloğundan geldiği için tutarlı.

**Son söz senin.** Metin ve değişiklik tablosu hemen gelir. Ardından skill sohbette sorar: "Değişiklikleri önizleme sayfasında görmek ister misin?" Seçenekler "Önizle" ve "Gerek yok". Claude Code bunu tıklanabilir seçenekler olarak gösterir. Codex ve Gemini CLI'da cevabı yazman yeterli.

Önizlemeyi seçersen değişiklikler defter görünümlü bir sayfada açılıyor:
- Metinde yalnızca değişen kelimeler işaretli: orta kalınlıkta, arkalarında çok hafif sarı bir fosforlu kalem. Silinen yerde küçük bir "[silindi]" notu duruyor.
- Tıklayınca önceki hal, gerekçe ve seçenekler çıkıyor: eski ya da yeni hali seçebilir, "Başka öner" diyebilir, not ekleyebilirsin.

![İnceleme sayfası: değişen kelimeler orta kalınlıkta ve hafif sarı fosforlu, tıklayınca önceki hal ve seçenekler çıkıyor](assets/review-page.png)

**Sayfa ajanla konuşuyor.** Canlı açıldığında:
- "Başka öner" kutusuna "daha resmî", "deyimle söyle" gibi bir istek yazarsan ajan iki üç seçenek getirir.
- "Ajana gönder" kararlarını kopyala-yapıştıra gerek kalmadan sohbete yollar.

Öneriler üç yoldan gelir, hangisinin kullanılacağını sayfanın ayarlarından seçersin:
- sohbetteki ajanın kendisi,
- sohbetin bağlamını bilen bir kopyası,
- bağlamsız hızlı bir çağrı.

**Sayıyla da bakıyor.** `scripts/audit.py` dedektörlerin ölçtüğü şeyleri sayar:
- cümle boyu çeşitliliği,
- açılış tekrarı,
- cümle sonu kafiyesi,
- uzun tire,
- "değil" ve "asıl" sıklığı,
- yapay zeka ve moda sözler,
- plaza jargonu,
- İngilizceden çevrilmiş e-posta kalıpları,
- Ateşman okunabilirliği.

Teslimde önce ve sonra değerleri yan yana durur.

## Kurulum

İnsanlık öldü mü? Claude Code, Codex ve Gemini CLI ile çalışır. Gerekenler: Node.js (`npx` için) ve Python 3.8 ya da daha yenisi. Betikler yalnız Python'un standart kütüphanesini kullanır, ek paket kurulmaz.

### 1. Kur

```bash
npx skills add MesutARIDORU/insanlik-oldu-mu -g
```

`npx skills` hangi ajanlara kurulacağını sorar. Claude Code, Codex ve Gemini CLI'ı orada işaretle. Skill ortak `~/.agents/skills` klasörüne tek kopya olarak kurulur, kilit dosyasına (`~/.agents/.skill-lock.json`) yazılır ve seçtiğin ajanlara bağlanır. Bilgisayarındaki öbür skill'ler de bu yolla kuruluysa hepsi aynı yerde durur.

### 2. Ayarları yap (isteğe bağlı)

```bash
python3 ~/.agents/skills/insanlik-oldu-mu/scripts/install.py
```

Bu betik skill'i yeniden kurmaz, yalnızca ayarları yapar. Önce hangi araçlar için ayar yapılacağını sorar:

```
Hangi araçlar için ayar yapılsın?
  1) [x] Claude Code  bulundu · 2.1.300 (Claude Code) · bağlantı ve betik izinleri
  2) [x] Codex        bulundu · codex-cli 0.162.1 · yönlendirme notu
  3) [x] Gemini CLI   bulundu · 0.60.0 · /insanlik-oldu-mu komutu
? Numaraları virgülle yaz (örnek: 1,2). Enter: işaretliler, 0: hiçbiri:
```

Sonra her adımdan önce ayrıca onay ister:
- **Claude Code:** Skill'e ve betiklerine izin ekler. Eklersen Claude onları her seferinde sormadan çalıştırır. Betik önce ayar dosyanın yedeğini alır.
- **Codex:** Codex'in genel talimatlarına üç satırlık bir yönlendirme notu ekler. Not, Codex'in bu skill'i kendiliğinden seçmesini sağlar.
- **Gemini CLI:** `/insanlik-oldu-mu` komutunu yazar.

En sonda kısa bir deneme yapar: ölçüm, inceleme sayfası ve canlı köprü. Soru sormadan çalıştırmak için seçenekleri komuta ekle:

```bash
python3 ~/.agents/skills/insanlik-oldu-mu/scripts/install.py --targets claude,codex --permissions --codex-routing
```

Node.js yoksa depoyu klonlayıp kurulum betiğini çalıştırabilirsin. Adımlar [INSTALL.md](INSTALL.md) dosyasında.

### Kurulduğunu nasıl anlarım?

Ajana Türkçe bir metin ver ve "doğallaştır" de. Skill devreye girdiyse sohbette ilk olarak şu satır belirir:

> 💀 **İnsanlık öldü mü❓** · Metin tanımı: kurumsal yazışma dili (e-posta) · Alan: finans · Yaklaşım: …

| Araç | Kendiliğinden devreye girer | Adıyla çağırmak için |
|---|---|---|
| Claude Code | Evet | `/insanlik-oldu-mu` |
| Codex | Ayar adımında yönlendirme notunu eklersen evet. Not yoksa ve çok sayıda skill yüklüyse seçmeyebilir | `$insanlik-oldu-mu` |
| Gemini CLI | Hayır | `/insanlik-oldu-mu` |

### Güncelleme ve kaldırma

Güncellemek için:

```bash
npx skills update insanlik-oldu-mu
```

Kaldırmak için:

```bash
npx skills remove insanlik-oldu-mu -g
```

Ayar adımında eklenen izinlerin ve notun nasıl silineceği ve AGENTS.md okuyan öbür araçlar için elle kurulum [INSTALL.md](INSTALL.md) dosyasında.

## Kullanım

Ajana metni ver ve ne istediğini söyle:

```
Şu LinkedIn gönderisini doğallaştır, okurlar genel kitle:
[metin]
```

| Ne istiyorsun | Şöyle de |
|---|---|
| Tam yeniden yazım | "doğallaştır", "insanlaştır", "akıcı yap" |
| Hafif dokunuş | "çok değiştirme, sadece düzelt" |
| Teşhis | "bunu yapay zeka mı yazmış?", "puanla ama değiştirme" |
| Sıfırdan yazım | "doğal bir Türkçeyle şu duyuruyu yaz" |
| Kendi sesinle | Kendi yazından iki üç paragraf ekle. Skill cümle boyunu, sicili, hitabı ve kelime seçimini ondan alır, örnekteki bilgileri metne taşımaz |

Skill'i adıyla da çağırabilirsin: Claude Code ve Gemini CLI'da `/insanlik-oldu-mu`, Codex'te `$insanlik-oldu-mu`.

## Bir örnek

**Önce** (şirket içi duyuru):

> Günümüzün hızla değişen dijital dünyasında müşteri memnuniyeti her zamankinden daha kritik bir öneme sahiptir. Bu doğrultuda yeni destek panelimizi geçtiğimiz cuma günü başarıyla konuşlandırdık — ve sonuçlar şimdiden umut verici!
>
> Yeni panel sadece bir araç değil, aynı zamanda ekiplerimiz arasındaki iş birliğini güçlendiren bir köprü. Talepler artık tek ekranda toplanıyor, öncelikler otomatik olarak belirleniyor ve yanıt süreleri önemli ölçüde kısalıyor.

**Sonra:**

> Yeni destek panelini cuma günü canlıya aldık. İlk izlenimler iyi.
>
> Talepler artık tek ekranda toplanıyor, öncelikleri panel kendisi belirliyor, yanıt süreleri de kısalıyor [ilk haftanın ortalama yanıt süresi?]. Ekipler aynı talebi aynı ekranda gördüğü için birlikte çalışmak da kolaylaştı.

Ne değişti:
- Klişe giriş ve önem şişirmesi çıktı.
- "Konuşlandırdık" yerine ekiplerin gerçekten kullandığı söz geldi.
- Uzun tire ve "sadece X değil" kalıbı gitti.
- Rakam olmayan "önemli ölçüde" iddiası küçüldü. Rakam uydurulmadı, köşeli parantezle soruldu.

## Teknoloji jargonu

Kelime seçiminde ölçü, okurun gerçekten kullandığı dil. Karar kitleye göre veriliyor:
- **Geliştirici ekibine giden metin:** "deploy", "PR", "deadline" kalır. "Konuşlandırma" ya da "çekme isteği" gibi kimsenin kullanmadığı çeviriler iz sayılır.
- **Genel okura giden metin:** "canlıya almak" ve "teslim tarihi" tercih edilir. "Süre sonu" gibi tutmamış karşılıklar önerilmez.
- **Her metinde:** Ürünün ne yaptığını söylemeden metni "teknolojik" gösteren sözler iz sayılır: dijital dönüşüm, uçtan uca, ölçeklenebilir, sorunsuz entegrasyon.

## Neyi bozmaz

- **Sağlam metin:** Akademik metindeki "-maktadır" orada doğru üsluptur. Editörden geçmiş temiz bir yazı da yapay zeka sayılmaz. İz, tek tek kelimelerden çok kümelenmede aranır.
- **Dokunulmayanlar:** Alıntılar, özel adlar, kod, ürün adları ve arayüz etiketleri.
- **Diyalog çizgileri:** Romandaki satır başı konuşma çizgisi TDK'nin tanımladığı bir işarettir, silinmez.
- **İnsan izleri:** Tuhaf ama özgül detaylar, karışık duygular, devrik cümleler ve noktalamaya sızmış duygu görülünce skill metne daha az dokunur.

## Nereden besleniyor

- **TDK'nin yazım kuralları:** Noktalama, düzeltme işareti, uzun çizgi, büyük harf, sayılar, kısaltmalar ve pekiştirmeli sözler sayfaları tek tek okundu.
- **TDK Güncel Türkçe Sözlük:** Deyimlerin sözlükte ayrı madde olarak bulunup bulunmadığı tek tek işaretli. Akış kurallarındaki bazı örnekler sözlükte geçen, telif süresi dolmuş yazarlara ait gerçek cümleler.
- **Ateşman okunabilirlik formülü:** `audit.py` içindeki okunabilirlik puanı.
- **Kullanım:** Jargon kararlarında ölçü, okurun gerçekte kullandığı dil. Örneğin "süre sonu" kulağa yapay geldiği için "deadline" yerine önerilmiyor.
- **Alan notları:** Dokuz alanın okuru, terimleri ve hassas bilgileri `references/sectors.md` ve `references/jargon.md` dosyalarında.
- **Kendi deneme setimiz:** `evals/` altında altı örnek metin ve her biri için beklenen davranış.

Ayrıntılı kaynak listesi [references/sources.md](references/sources.md) dosyasında.

## English summary

*İnsanlık öldü mü?* ("Is humanity dead?") is an agent skill for Turkish text. It finds the marks that make a text read as machine-written and rewrites it without adding facts that were not in the source.
- **Patterns:** It detects 50 coded patterns, from "-maktadır" rhyme and "not X but Y" scaffolding to buzzwords, over-translated tech terms and fabricated sources.
- **Flow:** 35 rules built on Turkish grammar (word order, mood and certainty, reduplication, address) guide the rewrite.
- **Sectors:** Guides for nine fields (software, finance, health, education, law, public sector, e-commerce, HR, marketing) say who reads the text, which terms stay and which facts must never change.
- **Delivery:** Every rewrite comes with a change table and a numeric audit.
- **Review page:** An optional notebook-style page marks only the changed words, in medium weight with a faint yellow highlighter. For each change the user can keep it, revert it or ask the agent for alternatives.
- **Live bridge:** A local bridge connects the page to Claude Code, Codex or Gemini CLI, either through the listening agent, a forked session or a stateless call.

Install with `npx skills add MesutARIDORU/insanlik-oldu-mu -g`; it asks which agents (Claude Code, Codex, Gemini CLI…) to install into. Optional settings (Claude Code permissions, Codex routing note, Gemini command): `python3 ~/.agents/skills/insanlik-oldu-mu/scripts/install.py`.

## Lisans

MIT. Telif © 2026 MesutARIDORU. Ayrıntı [LICENSE](LICENSE) dosyasında.
