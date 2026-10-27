---
name: insanlik-oldu-mu
description: >
  Türkçe metni doğallaştırır ve insanlaştırır: yapay zeka ya da ChatGPT yazmış gibi duran izleri bulur,
  metni bilgisine ve anlamına dokunmadan doğal Türkçeyle yeniden kurar. Türkçe bir metin için kullanıcı
  "doğallaştır", "insanlaştır", "insan yazmış gibi olsun", "yapay zeka kokuyor", "ChatGPT yazmış gibi
  duruyor", "robotik", "akıcı yap", "elden geçir", "redakte et" dediğinde; LinkedIn gönderisi, blog,
  e-posta, duyuru, ürün metni, rapor, makale özeti ya da hikaye gibi bir Türkçe metni daha insani yapmak
  istediğinde; "bunu yapay zeka mı yazmış?" diye sorduğunda; doğal bir Türkçeyle sıfırdan metin
  istediğinde ya da "[İnsanlık öldü mü? · geri bildirim]" ile başlayan bir mesaj yapıştırdığında kullan.
  Neyi neden değiştirdiğini bir tabloyla açıklar, istenirse değişiklikleri tek tek onaylatan bir
  inceleme sayfası açar. Adı: İnsanlık öldü mü? Metin İngilizceyse ya da yalnızca çeviri isteniyorsa
  kullanma.
license: MIT
metadata:
  version: "1.8.0"
  gorunen-ad: "İnsanlık öldü mü?"
compatibility: Dosya okuyabilen her ajan. Betikler için Python 3 gerekir, Python yoksa ölçümler elle yapılır.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
  - Bash(python3:*)
---

# İnsanlık öldü mü?

Bu skill, Türkçe bir metne bakıp onu yapay zeka yazmış gibi gösteren izleri bulur ve metni gerçek bir insanın elinden çıkmış gibi yeniden kurar. Kelime değiştirmekle yetinmez. Ritmi, cümle iskeletini ve akıl yürütmenin akışını onarır. Yaptığı her değişikliği gerekçesiyle gösterir, son sözü yazara bırakır.

Adı her yerde tam olarak **İnsanlık öldü mü?** diye yazılır. Baştaki İ noktalı ve büyük, "mü" ayrı ve küçük olur, sonda soru işareti bulunur. "Insanlik oldu mu" ya da "İnsanlık Öldü Mü?" yanlış.

**Logo:** Sohbette skill'in imzası `💀 **İnsanlık öldü mü❓**` biçimindedir: başta kuru kafa, sonda kırmızı soru işareti. İnceleme sayfasının başlığında da aynı ikili durur. Skill her çalıştığında kullanıcının sohbette gördüğü ilk satır ve teslimin başlık satırı bu logoyla başlar. Kullanıcı skill'in devrede olduğunu buradan anlar. Logoyu yalnız bu iki satırda kullan, metnin içine koyma.


## Üç ilke

**1. Bilgi sadakati.** Kaynakta olmayan hiçbir olgu eklenmez. Bunlar sayı, yüzde, tarih, kişi ya da kurum adı, alıntı, kaynak, anı ve yazarın sahip olmadığı bir görüş olabilir. Yapay zeka metinlerini insanlaştırırken en sık yapılan hata, metni "somutlaştırmak" için rakam ve hikaye uydurmaktır. Okur bunu yayımlar, uydurma bilgi dünyaya çıkar. Somutluk gerektiğinde dört yol vardır:
- Metnin içinde zaten olan bilgiyi öne çıkar.
- İddiayı küçült ve sadeleştir: "önemli ölçüde kısaldı" yerine "kısaldı".
- Yer tutucu bırak: `[ilk haftanın ortalama yanıt süresi?]`.
- Kullanıcıya en fazla üç hedefli soru sor.

Anlamı tersine çevirme, iddianın gücünü değiştirme ("kesin" olanı "belki"ye, "belki"yi "kesin"e çevirme), bilgi kalemlerinden hiçbirini sessizce düşürme. Tek istisna kurgudur: Duyguyu göstermek için eklenen küçük beden ve sahne ayrıntıları (titreyen el, düşen anahtar) anlatının gereğidir. Bunları değişiklik tablosunda "eklenen ayrıntı" diye ayrıca belirt ki yazar istemezse geri alsın.

**2. İskelet kelimeden önemli.** Kelime izleri bir iki yılda eskir, modeller damgalanan kelimeyi bırakır. Yapısal izler kalır: aynı boydaki cümleler, aynı ekle biten yüklemler, "X değil, Y" iskeleti, her şeyi üçe bölmek. Bir kalıbı eşanlamlılarla boyayıp iskeletini korursan kalıp yerinde durur. Yeniden yazarken önce iskeleti değiştir.

**3. Ölçü.** Doğallaştırmanın da bir izi var: zorlama kesik cümleler, sahte pürüzler, her paragrafa serpilmiş argo. Sağlam insan yazısını bozma. Akademik metindeki "-maktadır" orada doğru sicildir. Editörden geçmiş temiz bir metin de yapay zeka yazmış sayılmaz. İz, tek tek kelimelerden çok kümelenmede aranır.


## Hangi iş, hangi mod

| Kullanıcı ne diyor | Mod | Ne yapılır |
|---|---|---|
| "Yapay zeka mı yazmış?", "kontrol et", "puanla", "değiştirme, sadece söyle" | **Teşhis** | Metne dokunulmaz. İzler, ağırlıkları ve insan izleri raporlanır. |
| "Çok değiştirme", "sadece düzelt", "redakte et". Ayrıca akademik, hukuki ya da resmî metinler ve insan izleri güçlü metinler | **Hafif dokunuş** | Yalnız işaretli cümleler düzelir. Paragraf düzeni, sıra ve sicil korunur. |
| "Doğallaştır", "insanlaştır", "yeniden yaz", "akıcı yap" | **Tam yeniden yazım** (varsayılan) | İskelet yeniden kurulur, bilgi ve sıra mantığı korunur. |
| "Doğal bir Türkçeyle şunu yaz", "LinkedIn için bir duyuru yaz" | **Sıfırdan yazım** | Kalıplara düşmeden yazılır. İnceleme sayfası yoktur, kısa bir not eklenir. |
| Mesaj "[İnsanlık öldü mü? · geri bildirim]" ile başlıyor | **Geri bildirim turu** | Kullanıcının kararları uygulanır (bkz. Geri bildirim turu). |

Mod belirsizse metin tanımının varsayılan modunu kullan (bkz. Metin tanımları). O da belirsizse tam yeniden yazım yap. Modu çıktının başında söyle. Kullanıcı farklısını isterse ikinci turda değiştirirsin.


## İş akışı

**Komut kuralları.** Betikleri her seferinde tek başına çalıştır, `;`, `&&` ya da `|` ile başka bir komuta bağlama. Skill klasöründeki dosyaları okuman gerekirse Read aracını kullan, `cat`, `grep`, `sed` kullanma. Metni dosyaya yazmak yerine betiğe standart girdiden ver, betik onu kısa bir adla saklar. Claude Code bu kurallara uyan komutları onay sormadan çalıştırır, uymayanlarda her seferinde kullanıcıya sorar.

**1. Tanımla ve duyur.** Metni oku ve şunlara karar ver:
- **Metin tanımı:** Şiir dili, edebi anlatı dili, deneme ve köşe yazısı dili, kişisel yazı dili, kurumsal yazışma dili, teknik şartname dili, teknik doküman dili, akademik dil, hukuki dil, haber dili, pazarlama dili ya da sosyal medya dili. Gerekirse alt türünü ekle: "kurumsal yazışma dili · şirket içi duyuru".
- **Alan:** Metnin konusu olan iş kolu: yazılım, finans, sağlık, hukuk, eğitim, kamu, perakende...
- **Kitle ve sicil:** Geliştirici ekip mi, genel okur mu, müşteri mi? Resmî mi, samimi mi?
- **Yazarın sesi ve insan izleri:** Birinci tekil kişi, mizah, tuhaf ama özgül ayrıntılar, devrik cümleler. İnsan izleri güçlüyse hafif dokunuşa yönel.
- **Örnek yazı:** Kullanıcı kendi yazısından örnek verdiyse sesi oradan al: cümle boyu, sicil, hitap, sık kullandığı kelimeler ve noktalama alışkanlığı. Örnekteki bilgileri ve cümleleri metne taşıma, yalnızca sesini al. Örnekte yapay zeka izi varsa onu ses sayma.

Kullanıcı türü kendisi söylediyse onun dediği geçerlidir. Mod belirsizse türün varsayılan modunu kullan (bkz. Metin tanımları).

Hiçbir araç çağırmadan önce sohbete tek satır yaz, ardından beklemeden işe devam et:
```
💀 **İnsanlık öldü mü❓** · Metin tanımı: edebi anlatı dili (öykü) · Alan: edebiyat · Yaklaşım: hafif dokunuş, diyaloglar ve konuşma çizgileri korunur
```
Yaklaşım kısmına modu ve o türde neyi koruyacağını ya da neye odaklanacağını yaz. Satır kısa olsun, açıklamayı teslimde yaparsın. Kullanıcı skill'in devrede olduğunu bu satırdan anlar, o yüzden atlama.

**Ölç.** Metni betiğe standart girdiden ver:
```bash
python3 <skill-dizini>/scripts/audit.py - --save before --guide <<'METIN'
[metnin kendisi, olduğu gibi]
METIN
```
Betik metni "before" adıyla saklar, sayısal denetimi yazar ve sonuna tahmin ettiği türün ve alanın rehberini ekler. Raporun ilk satırı betiğin metin tanımı tahminidir. Tahmin yüzeydeki ipuçlarından çıkar. Senin kararından farklıysa metne bir daha bak. Kararın değişirse doğru türün ya da alanın rehberini al ve teslimde yeni tanımı kullan:
```bash
python3 <skill-dizini>/scripts/audit.py --guide "Teknik şartname dili"
```
```bash
python3 <skill-dizini>/scripts/audit.py --guide "Finans"
```
Tür rehberi neye dokunmayacağını, o türde yapay zekanın nasıl iz bıraktığını ve hangi dille yazacağını söyler. Alan rehberi (`references/sectors.md`) okuru, o alanda değişirse zarar doğuracak bilgileri (doz, oran, süre, yasal uyarı) ve alanın tipik izlerini söyler.

Python yoksa ölçümleri ve türü kabaca elle belirle. "Modeller saymakta kötüdür" bilgisini akılda tut, emin olmadığın sayıyı rapora yazma.

**2. Teşhis et.** Aşağıdaki kalıp kataloğundan metindeki izleri işaretle ve ağırlıklarını ayır:
- **Kesin iz:** Tek başına yeter. Örneğin sohbet artıkları (T1).
- **Güçlü iz:** Yapısal kalıplar. Örneğin R1, Y1, Y2.
- **Zayıf iz:** Tek başına bir şey kanıtlamaz, kümelenince anlam kazanır. Örneğin tek bir "kapsamlı".

**3. Yaz.** Moda ve metin tanımına göre yeniden kur. Her cümle için önce şunu sor: Bu cümle ne bilgi taşıyor? Bilgi yoksa (boş doğru, klişe giriş, kalıp kapanış) cümleyi çıkar. Bilgi varsa onu en yalın iskeletle ver, sonra türün yazım diliyle kur. Akış kuralları (A1-A35) her türde geçerli değildir. Şiirde, teknik şartnamede ve hukuki metinde ritim kuralları uygulanmaz (bkz. `references/genres.md`). Jargon ve yazım kararlarını alana ve kitleye göre ver.

**4. Denetle.** Yeni metni önceki haliyle karşılaştırarak ölç:
```bash
python3 <skill-dizini>/scripts/audit.py - --save after --before before <<'METIN'
[yeni metin]
METIN
```
Sonra kendine iki soru sor:
- "Bu metni hâlâ makine yazmış gibi gösteren ne?"
- "Kalıbı kaldırdım mı, yoksa kıyafetini mi değiştirdim?" (R9)

Kendi tiklerine de bak:
- Her paragraf vecizeyle mi bitiyor?
- "Asıl" ve iki noktalı anonslar sızdı mı?
- Bütün kapanışlar soruyla mı bağlanıyor?
- Bilgi sadakatini bozan bir ekleme yaptın mı?

**5. Teslim et, sonra önizlemeye karar ver.** Önce metni çıktı biçimiyle teslim et (bkz. aşağıda). Kullanıcıyı hiçbir şey için bekletme: Metin ve tablo her durumda hemen gelir.

Hafif dokunuş ya da tam yeniden yazım yaptıysan teslimin ardından kullanıcının önizleme tercihine bak:
```bash
python3 <skill-dizini>/scripts/bridge.py preview
```
Betik tek kelime yazar:

| Çıktı | Ne yaparsın |
|---|---|
| `first` | Skill ilk kez kullanılıyor. Sormadan sayfayı canlı aç (bkz. İnceleme sayfası) ve sohbete yaz: "İlk kez kullandığın için önizleme sayfasını kendiliğinden açtım. Bundan sonra ne olacağını sayfadaki notta seçebilirsin." Sayfa bu seçimi kendisi sorar. |
| `always` | Sormadan sayfayı canlı aç, adresini sohbete yaz. |
| `ask` | Aşağıdaki seçenekli soruyu sor. Ama metin 300 kelimeyi geçiyorsa, 8'den çok değişiklik varsa ya da kullanıcının karar vermesi gereken yer çoksa (köşeli parantezli sorular, birbirine yakın seçenekler) sormadan aç ve nedenini tek satırla söyle: "Metin uzun, değişikliklere sayfada bakmak daha kolay olur diye açtım." |
| `request` | Açma, sorma. Sayfa yalnız kullanıcı isteyince açılır. |

Betik çalışmazsa (Python yoksa) `ask` gibi davran. Bulutta, kullanıcının tarayıcısının ulaşamadığı bir ortamda çalışıyorsan (bkz. İnceleme sayfası) tercih orada saklanmaz: `first` çıktısını da `ask` say.

Seçenekli soru:
- **Seçenekli soru aracın varsa** onu kullan: Claude Code'da AskUserQuestion, Gemini CLI'da ask_user, Codex'te Plan modundaysan request_user_input. Soru: "Değişiklikleri önizleme sayfasında görmek ister misin?" Seçenekler sırasıyla:
  - "Önizle (Önerilen)": İnceleme sayfası tarayıcıda açılır, kararlarını orada verirsin.
  - "Gerek yok": Metin bu haliyle kalır.
- **Böyle bir araç yoksa** (örneğin Codex'in normal modunda) teslimin son satırına şunu yaz: "Önizleme sayfasını açayım mı? **Önizle** ya da **gerek yok** yazman yeterli."

"Önizle" seçilirse ya da kullanıcı sonradan "önizle" yazarsa sayfayı canlı aç (bkz. İnceleme sayfası) ve adresini sohbete yaz, sonra dinlemeye geç. "Gerek yok" seçilirse ya da kullanıcı başka bir şeyle devam ederse soruyu tekrarlama.

Kullanıcı tercihini sohbette de değiştirebilir. Bunu duyunca aynı betiği çalıştır, sonra tek satırla onayla:
- "önizleme hep açılsın": `bridge.py preview --set always`
- "önizlemeyi önce bana sor": `bridge.py preview --set ask`
- "önizlemeyi ben isteyince aç", "önizleme açılmasın": `bridge.py preview --set request`
- "bu sohbette hep aç": `bridge.py preview --chat on`. "Bu sohbette önizleme açma": `bridge.py preview --chat off`. Bunlar yalnız bu sohbeti etkiler. Betik sohbeti tanıyamazsa (Gemini CLI, Antigravity) hata verir, o zaman seçimi bu sohbet boyunca kendin hatırla.

Tercih ne olursa olsun kullanıcı "önizle", "sayfada göster" ya da "değişiklikleri sayfada aç" derse sayfayı aç. Sayfayı zaten istediyse tercihe bakmadan doğrudan sayfayla teslim et.

Şu durumlarda sayfayı açma, soru da sorma:
- Kullanıcı sayfa istemediğini söyledi ya da yalnızca metni istiyor.
- Mod teşhis, sıfırdan yazım ya da geri bildirim turu.

**6. Günde bir kez güncellemeye bak.** Her modda, teslimden sonra şunu çalıştır:
```bash
python3 <skill-dizini>/scripts/bridge.py update
```
Betik GitHub'daki son sürüme günde en çok bir kez bakar ve baktığı günü saklar. İlk satır tek kelimedir:

| Çıktı | Ne yaparsın |
|---|---|
| `available` | Yeni bir sürüm çıkmış. Aşağıdaki gibi davran. |
| `current` | Sürüm güncel. Bir şey söyleme. |
| `checked` | Bugün zaten bakıldı. Bir şey söyleme. |
| `unknown` | GitHub'a ulaşılamadı ya da sürüm okunamadı. Bir şey söyleme. |

Sonraki satırlar: `installed` kullanıcıdaki sürüm, `latest` yeni sürüm, `url` sürüm notlarının adresi. `reverted_from` satırı varsa ve `latest` ile aynıysa kullanıcı bu sürümden daha önce eski sürüme dönmüştür.

`available` çıktığında ne yapacağın, teslim ettiğin metnin uzunluğuna bağlı. Teşhis modunda kullanıcının metnine bak.
- **250 karakterden uzunsa önce güncelle, sonra sor.** Kullanıcı uzun bir metni okurken soruyu kaçırabilir, bu yüzden önerilen seçenek beklemeden uygulanır. Sormadan `bridge.py update --apply` çalıştır. Çıktı `updated` ise seçenekli soru sor: "İnsanlık öldü mü?'yü güncelledim: [before] → [installed]. Yeni sürüm bir sonraki kullanımda devreye girer. Sürüm notları: [url]" Seçenekler sırasıyla:
  - "Tamam (Önerilen)": Yeni sürüm kalır.
  - "Eski sürüme dön": [before] sürümüne geri dönerim.

  Kullanıcı cevap vermezse ya da başka bir şeyle devam ederse yeni sürüm kalır. Çıktı `updated` değilse aşağıdaki "Güncelle" seçeneğindeki gibi davran. `reverted_from` satırı `latest` ile aynıysa önce güncelleme: kullanıcı bu sürümü bir kez geri çevirdi, metin uzun olsa da önce sor.
- **250 karakter ya da daha kısaysa önce sor.** Seçenekli soru: "İnsanlık öldü mü?'nün yeni sürümü çıktı: [latest] (sende [installed]). Şimdi güncelleyeyim mi? Sürüm notları: [url]" Seçenekler sırasıyla:
  - "Güncelle (Önerilen)": Yeni sürüm kurulur, bir sonraki kullanımda devreye girer.
  - "Şimdi değil": Yarın yeniden sorarım.

Soruyu önizleme sorusuyla aynı araçla sor. Önizleme sorusu da sorulacaksa ikisini aynı çağrıda iki ayrı soru olarak sor. Seçenekli soru aracın yoksa soruyu teslimin son satırına yaz ve cevabın nasıl yazılacağını kalın göster: "**Tamam** ya da **eski sürüme dön** yazman yeterli." ya da "**Güncelle** ya da **şimdi değil** yazman yeterli."

"Güncelle" seçilirse:
```bash
python3 <skill-dizini>/scripts/bridge.py update --apply
```
- `updated`: "Güncelledim: [before] → [installed]. Yeni sürüm bir sonraki kullanımda devreye girer." de.
- `current`: Skill'in zaten güncel olduğunu söyle.
- `failed`: Hatayı tek satırla söyle ve elle güncelleme komutunu ver: `npx skills update -g insanlik-oldu-mu`.
- `manual`: Skill `npx skills` ya da git ile kurulmamış, örneğin Claude sohbetine ZIP olarak yüklenmiş. `download` satırındaki sürüm sayfasını ver: Yeni ZIP'i oradan indirip yeniden yüklemesi gerekir.

"Eski sürüme dön" seçilirse:
```bash
python3 <skill-dizini>/scripts/bridge.py update --revert
```
- `reverted`: "[installed] sürümüne döndüm. [before] sürümünü yarın yeniden sorarım, kendiliğinden kurmam." de.
- `failed`: Hatayı tek satırla söyle.
- `manual`: Skill bir git klonundan çalışıyor ya da elle kurulmuş. Klonda yerel değişiklikler olabileceği için betik geri dönmez. `git` satırındaki komutu ya da `npx` ve `download` satırlarını ver.

"Şimdi değil" seçilirse ya da kullanıcı başka bir şeyle devam ederse bir şey yapma. Betik o gün baktığını sakladığı için aynı gün yeniden sorulmaz, ertesi gün skill ilk çalıştığında yeniden sorulur. Kullanıcı "güncelleme var mı?" diye sorarsa `bridge.py update --now` çalıştır, günü beklemeden bakar.


## Metin tanımları

Her türün kendi doğru dili var. Ayrıntı, tanıma ipuçları ve her türdeki yapay zeka izleri `references/genres.md` dosyasında. 1. adımdaki `audit.py --guide` komutu ilgili bölümü yazdırır, yazmaya başlamadan önce mutlaka oku.

| Metin tanımı | Varsayılan mod | Dokunma | Odak |
|---|---|---|---|
| Şiir dili | Teşhis | Dize kırılması, kıta, uyak, ölçü, noktalama | Soyut imge kümesi, teselli kapanışı. Yeniden yazım yalnız istenirse |
| Edebi anlatı dili | Hafif dokunuş | Karakter sesi, diyalog, konuşma çizgisi (—), olay örgüsü | Adıyla söylenen duygu, kurgu klişesi (G5), anlatı kuralları (A32-A35) |
| Deneme ve köşe yazısı dili | Tam yeniden yazım | Yazarın görüşü, tezi, ironisi | Vecize kapanış, "X değil, Y", "asıl" anonsları |
| Kişisel yazı dili | Tam yeniden yazım | Yazarın yaşadıkları ve kendi kelimeleri | Broşür dili, klişe giriş ve kapanış, uydurma deneyim |
| Kurumsal yazışma dili | Tam yeniden yazım | Selamlama ve kapanış, ad, unvan, tarih, tutar, istenen eylem | Amaca gelmeyen giriş, "Umarım bu e-posta sizi iyi bulur", çekinmeyin kalıbı |
| Teknik şartname dili | Hafif dokunuş | "-malıdır / -ecektir" gereklilik kipi, madde numarası, sayı, birim, standart | Sınanamayan sıfat ("kullanıcı dostu", "sorunsuz"), madde başına tek gereklilik |
| Teknik doküman dili | Tam yeniden yazım | Kod, komut, yol, parametre, arayüz etiketi | Tanıtım girişi, aşırı çeviri terim (S3), adım adım emir kipi |
| Akademik dil | Hafif dokunuş | "-maktadır", edilgen çatı, terim, kaynak gösterimi | Önem şişirmesi (R6), kelime kümesi (S1), belirsiz otorite (G1) |
| Hukuki dil | Teşhis ya da hafif dokunuş | Hukuki terim, madde yapısı, anlamı değiştirebilecek her şey | Karışmış broşür dili. Değişikliği uygulamadan önce sor |
| Haber dili | Tam yeniden yazım | Alıntı, kaynak, sayı, tarih, yer | Yorum ve övgü sızması, belirsiz otorite |
| Pazarlama dili | Tam yeniden yazım | Ürünün gerçek özellikleri, fiyat, tarih, koşul | Boş sıfat yığını (S9). Satış çağrısı meşrudur |
| Sosyal medya dili | Tam yeniden yazım | Yazarın emoji ve etiket alışkanlığı | Anons (T5), kendi sorup cevaplama (R3), slogan kapanış (T7) |


## Kalıp kataloğu

Her kalıbın kodu, işareti ve çaresi aşağıda. Uzun önce/sonra örnekleri `references/patterns.md` dosyasında. Bir kalıptan emin olamadığında ya da iyi bir çare aradığında oku.

### Y · Yapı ve ritim (en kalıcı izler)
- **Y1 Kafiyeli yüklem.** Cümleler aynı ekle biter ("-maktadır", "-mıştır", hep "-yor"). Çare: Kipleri karıştır, isim cümlesi kur, bilineni yüklemin arkasına at (A1, A13).
- **Y2 Eş boy cümleler.** Cümleler ve paragraflar aynı boyda. Çare: Uzun bir zincir cümlenin yanına kısa bir cümle koy (A11).
- **Y3 Kesik vuruş zinciri.** "Kurallar yıkıldı. Ezberler bozuldu." gibi art arda kısa cümleler. Çare: Virgülle bağla, tek tük kısa cümleyi vurgu için sakla.
- **Y4 Açılış tekrarı.** Art arda aynı özneyle ya da "Ayrıca / Öte yandan / Dolayısıyla" ile açılan cümleler. Çare: Geçişi fikrin kendisiyle yap.
- **Y5 Ad tekrarı ve eşanlamlı döngüsü.** Ya aynı ad her cümlede yeniden kurulur ya da "şirket, firma, kuruluş, marka" diye dolaşılır. Çare: Özneyi bir kez tanıt (A9).
- **Y6 Mühürlü paragraf.** Her paragraf "Kısacası..." ile kendini özetler. Çare: Paragrafı geçişle bırak.
- **Y7 Başa dönen kapanış.** Giriş ne anlatılacağını sayar, kapanış girişi tekrar eder. Çare: Son paragrafa yeni bir bilgi ya da bir sonraki adımı koy, yoksa son fikirde bitir.
- **Y8 Üçleme alışkanlığı.** Sıfatlar, örnekler ve faydalar hep üçlü gelir. Çare: Kaç tane varsa o kadar say, listeyi kapatma (A28).
- **Y9 Kopuk mantık.** Cümleler tek tek düzgün ama aralarındaki köprü yok. Çare: Ara adımı yaz.

### R · Retorik kalıplar
- **R1 Karşıtlıkla parlatma.** "Mesele X değil, Y", "sadece X değil aynı zamanda Y", "X yerine Y", "Ne X. Ne Y. Sadece Z." Metinde "değil" sayısı üçü geçiyorsa iskelet olmuştur. Çare: Olumlu kur, önemli olanı söyle.
- **R2 Etiketli anons ve "asıl" enflasyonu.** "Asıl mesele şu:", "Sorun şu:", "Cevap basit:". Çare: Önce söyle, gerekirse sonra adlandır (A15).
- **R3 Kendi sorup kendi cevaplama.** "Peki neden? Çünkü..." Çare: Doğrudan anlat ya da soruyu açık bırak (A16).
- **R4 Sahte aralık.** "Küçük alışkanlıklardan büyük hedeflere kadar". Çare: Kapsadığı şeyleri düz say.
- **R5 Vecize ve sahte şiir.** "Tasarım, güvenin dilidir.", "Belki de asıl soru hiç sorulmamıştı." Çare: Vecizenin işaret ettiği somut iddiayı yaz.
- **R6 Önem şişirmesi.** "Sektör için bir dönüm noktası", "kilit rol oynamaktadır". Çare: Ne olduğunu söyle, önemini okura bırak.
- **R7 Boş doğru.** Tersini kimsenin savunmadığı genelleme ("Güven zamanla inşa edilir"). Çare: Sil ya da tartışılabilir bir iddiaya çevir.
- **R8 Zarf-fiil kuyruğu.** Cümle sonuna eklenen "-arak" öbeği ("...ni gözler önüne sererek"). Çare: Kuyruğu kes.
- **R9 Kılık değiştiren kalıp.** Kalıp kelimesi değişmiş halde duruyor ("X'le kalmıyor, Y oluyor"). Çare: Kanatlardan birini seç, iskeleti yık.

### S · Söz ve sicil
- **S1 Yapay zeka kelime kümesi.** Kapsamlı, kilit, yenilikçi, dönüştürücü, değer katmak, olanak tanımak, ışık tutmak, yolculuk (mecazi). Tek tük geçerse normaldir, iz olan kümelenmedir.
- **S2 Moda teknoloji sözleri.** Dijital dönüşüm, uçtan uca, ölçeklenebilir, sorunsuz entegrasyon, yapay zeka destekli, ekosistem, sinerji, inovasyon. Çare: Ürünün gerçekte ne yaptığını söyle (bkz. Jargon).
- **S3 Terim karmaşası.** Kimsenin kullanmadığı aşırı çeviri ("konuşlandırma", "çekme isteği") ya da aynı kavrama üç ad. Plaza fiilleri ("aksiyon almak", "challenge etmek") yanlış kitlede de bu gruba girer. Çare: Kitlenin kullandığı terim, tek terim.
- **S4 Bürokratik ek yığını.** "Kapsamında, doğrultusunda, çerçevesinde, noktasında" üst üste. Çare: Somut fiil.
- **S5 Süslü koşaç.** "Sergi alanı işlevi görmektedir", "özelliğine sahiptir". Çare: "Galeri, derneğin sergi alanı."
- **S6 Dolgu ve aşırı ihtiyat.** "Önemle belirtmek gerekir ki", "etkili olabileceği düşünülebilir". Çare: Sil, doğrudan söyle.
- **S7 Edilgen kaçış.** Fail gizli: "ayrılması gerekmektedir". Çare: Kimin yaptığını yaz, bilinmiyorsa uydurma.
- **S8 Sicil savrulması.** Aynı metinde "kanka" ile "olanak tanımaktadır". Çare: Tek sicil.
- **S9 Broşür dili.** Eşsiz, büyüleyici, unutulmaz deneyim, sizi bekliyor. Çare: Bilgi ver.
- **S10 Hep en olası kelime.** Her kelime akla ilk gelen seçim, hiçbir yer şaşırtmıyor. Çare: Yerinde birkaç beklenmedik ama doğru seçim yap. Egzotik kelimeye kaçma, özgül ayrıntı kullan.
- **S11 Çeviri Türkçesi.** Her cümlede "siz/ben", "bir" bolluğu, birebir metafor ("karmaşık bir goblen", "günün sonunda", "...in dinamik dünyasında"), İngilizce e-posta kalıbının çevirisi ("Umarım bu e-posta sizi iyi bulur", "ekte ... bulabilirsiniz", "iletişime geçmekten çekinmeyin"). Çare: Türkçe kur, zamiri düşür.

### T · Ton ve sohbet
- **T1 Sohbet artığı.** "Umarım yardımcı olur", "Elbette!", "Bir yapay zeka modeli olarak", "Regenerate response". Kesin iz. Çare: Tamamen sil.
- **T2 Yağcılık.** "Harika bir soru!" Çare: Doğrudan konuya gir.
- **T3 Terapist sesi.** Duygusal olmayan metinde "Bu konuda yalnız değilsiniz". Çare: Sil.
- **T4 Sahte samimiyet kancası.** "Dürüst olmak gerekirse...", "Açık konuşalım:". Çare: Lafı dolandırmadan söyle.
- **T5 Anons ve rehber sesi.** "Gelin birlikte inceleyelim", "konunun derinlerine inelim", "bilmeniz gereken her şey burada". Çare: İçerikle başla.
- **T6 Klişe giriş.** "Günümüzde...", "Teknolojinin hızla geliştiği çağımızda". Çare: İlk cümle bilgi taşısın.
- **T7 Kalıp kapanış.** "Sonuç olarak" ile açılan iyimser son cümle, slogan, "Peki siz ne düşünüyorsunuz?" Çare: Yeni bir bilgi, plan ya da sahneyle bitir. Kapanış hamlelerini metinden metne değiştir.

### B · Biçim ve noktalama
- **B1 Uzun tire.** Düzyazıda ara söz ya da vurgu için kullanılan "—" ve "–". Çare: Nokta, virgül, parantez ya da iki nokta. Satır başı konuşma çizgisi bunun dışında (bkz. Yazım).
- **B2 Noktalı virgül göçü.** Kaldırılan tirenin yerine geçen noktalı virgül. Çare: İki vuruşlu iskeleti de boz.
- **B3 Kalın vurgu enflasyonu.** Her terimin kalın yazılması. Çare: Vurguyu bir iki yere sakla.
- **B4 Etiketli madde listesi.** "**Performans:** Performans arttı." gibi listeler ya da sıralanabilir olmayan fikrin maddelenmesi. Çare: Düz yazı.
- **B5 Emoji süsü.** Başlık ve madde başına emoji. Çare: Kaldır. Yazarın kendi alışkanlığıysa ölçülü bırak.
- **B6 Başlık düzeni.** Başlıkta büyütülmüş bağlaç ("Yükselişi Ve Geleceği") ya da metin içinde tutarsız başlık düzeni. Çare: Tek düzen, bağlaçlar küçük.
- **B7 Parantez açıklama takıntısı.** Her terimin yanında açıklama: "temettü (kâr payı)". Çare: Okurun bildiğini açıklama.
- **B8 Yazım tutarsızlığı.** Aynı metinde "hâlâ" ile "hala" birlikte, "de/da" ve "ki" hataları. Çare: Tutarlı yazım.

### G · Güven ve kurgu
- **G1 Belirsiz otorite.** "Uzmanlara göre", "araştırmalar gösteriyor". Çare: Kaynak metinde varsa adını yaz, yoksa iddiayı sahiplen ya da yer tutucu bırak. Kaynak uydurma.
- **G2 Uydurma vaka ve rakam.** "Bir müşterimiz satışlarını iki haftada yüzde 60 artırdı." Çare: Gerçek değilse çıkar ya da varsayımsal olduğunu açıkça söyle.
- **G3 Boşluk doldurma.** "Kaynaklarda sınırlı bilgi var, muhtemelen..." diye başlayıp tahmin yürütmek. Çare: Bilinmeyeni söyle ya da cümleyi çıkar.
- **G4 Şablon zorluklar paragrafı.** "Tüm bu zorluklara rağmen..." ile açılan formül. Çare: Gerçek sorunu metindeki bilgiyle anlat.
- **G5 Kurgu klişesi.** "İçini bir huzursuzluk dalgası kapladı", gözlerde aynı anda iki zıt duygu. Çare: Duyguyu bedenle ve sahneyle göster (A32).
- **G6 Aşırı düzeltme izi.** Zorlama kesik cümle, yapmacık argo, her yere serpilmiş pürüz. Doğallaştırıcıların kendi imzası budur. Çare: Ölçü.


## Teknoloji ve iş jargonu

Ölçü, kitlenin gerçekten kullandığı dildir. Sözlükte olup kullanımda tutmamış karşılıklar metni yapaylaştırır. "Deadline" için "süre sonu" demek buna örnek. Ayrıntılı tablolar `references/jargon.md` dosyasında: yazılım, finans, sağlık, hukuk, kamu, e-ticaret, insan kaynakları, eğitim ve pazarlama terimleri. Teknik ya da iş metni düzeltirken mutlaka oku.

- **Geliştirici ve ekip içi metin:** Yerleşik terimler kalır: deploy, PR, commit, sprint, backlog, deadline, release. Bunları "konuşlandırma", "çekme isteği", "taahhüt" diye çevirmek yapay zeka izidir.
- **Genel okur:** İnsanların kullandığı Türkçe tercih edilir: canlıya almak ya da yayına almak, teslim tarihi, geri bildirim, güncelleme.
- **Resmî ve kamu metni:** Türkçe karşılık tercih edilir, ama yerleşmiş olanı. Uydurma karşılık kullanılmaz.
- **Her metinde iz sayılanlar:** Moda sözler (S2), aynı kavrama birden fazla ad (S3), kitleye uymayan plaza fiilleri. "Aksiyon aldık" iç yazışmada doğal durur, müşteriye giden metinde sırıtır.
- **Asla değişmeyenler:** Kod, komut, dosya ve ürün adları, arayüz etiketleri, alıntılar.


## Akış kuralları

Kalıbı silmek işin yarısı. Boşalan yere Türkçenin kendi araçlarını koymak gerekiyor. Her kuralın açıklaması, hangi türde işe yaradığı ve alanlardan örnekler `references/flow.md` dosyasında. Örneklerin bir kısmı TDK sözlüğünde telif süresi dolmuş yazarlardan geçen gerçek cümleler. Anlatı ya da diyalog içeren metinde bu dosyayı mutlaka oku.

- **Söz dizimi:**
  - A1 Yeni bilgiyi yüklemin önüne koy, bilineni yüklemin arkasına sarkıtabilirsin.
  - A2 Özneyle yüklemi uzaklaştırma: araya giren uzun öbeği ayrı cümleye al.
  - A3 Ad tamlaması zincirini fiille çöz.
  - A4 Adlaşmış fiili ("yapılmasının sağlanması") kendi fiiline çevir.
  - A5 Devriği konuşmaya ve duygunun doruğuna bırak.
- **Cümleleri bağlamak:**
  - A6 Ardışık eylemleri virgülle tek cümlede akıt.
  - A7 Bağlacı sona da al ("çünkü", "ama" cümle sonunda da durur).
  - A8 Zıtlıkta "ama" yeter.
  - A9 Özneyi bir kez tanıt: tam ad, kısa ad, adıl, sonra yazılmayan özne.
  - A10 Geçişi bağlaçla değil fikirle kur.
- **Ritim:**
  - A11 Uzunla kısayı yan yana koy.
  - A12 Cümle boyu duyguyu izlesin.
  - A13 Cümle sonlarını çeşitle: isim cümlesi, kip değişimi, sarkıtma.
- **Vurgu:**
  - A14 Vurguyu anons değil yapı taşısın: tekrar ve devrik.
  - A15 Önce söyle, sonra adlandır.
  - A16 Soruyu sorup hemen cevaplama.
- **Kip ve kesinlik:**
  - A17 Duyduğunu -miş'le anlat.
  - A18 Geçmişi katmanla: -mişti, -iyordu, -di.
  - A19 Tezlik ve sürerlik: -ıvermek, -akalmak, -ıp durmak.
  - A20 Kesinliği kaynağa göre ayarla: -dır, -abilir, -mış olmalı. Kesini olasıya, olasıyı kesine çevirme.
- **Kelime dokusu:**
  - A21 İkileme.
  - A22 Pekiştirme: apaçık, yepyeni, sapasağlam.
  - A23 Somut fiil: "gerçekleştirmek, sağlamak" yerine eylemin kendi fiili.
  - A24 Duruluk: Çıkınca anlamı eksiltmeyen kelime fazladır.
- **Okurla ilişki:**
  - A25 Hitabı sabitle: sen ya da siz, biz ya da kurumun adı.
  - A26 Okura dön ("bakın", "değil mi").
  - A27 Tavır sözcükleri (bari, hele, ki, de, herhalde).
  - A28 Listeyi taşır ya da kes: "beş altı kişi" de.
- **Öğretici ve iş metni:**
  - A29 Kuralın yanına örnek koy.
  - A30 Kısa emir, tek gerekçe.
  - A31 Okurun aradığını (ne, ne zaman, nerede, ne kadar) öne al.
- **Anlatı ve diyalog:**
  - A32 Duyguyu adlandırma, göster.
  - A33 Düşünceyi anlatıya karıştır.
  - A34 Kişiyi nitelemeyle an.
  - A35 Konuşma etiketini çeşitle.

Deyim de metne doku katar, ama ölçüsü ayrı: Bir paragrafta en çok bir deyim, yalnızca `references/idioms.md` dosyasındakilerden ya da kesin bildiklerinden. Dosya deyimleri iş durumlarına ve türlere göre veriyor, çeviri kokan kalıpları da ayrıca sayıyor.


## Yazım ve noktalama

TDK'nin yazım kuralları resmî ve yayımlanacak metinlerde iyi bir başvurudur. Gündelik metinde yazarın tercihine uyulur. Her durumda esas olan tutarlılıktır. Ayrıntı ve TDK'den alınmış örnekler `references/spelling.md` dosyasında.

- **Uzun çizgi (—):** Düzyazıda ara söz ya da vurgu için kullanılırsa yapay zeka izidir (B1). Ancak satır başına alınmış konuşmayı gösteren konuşma çizgisi TDK'nin tanımladığı bir işarettir. Kurgudaki diyalogda ona dokunma. Ara sözü virgül, parantez ya da TDK'nin bitişik kısa çizgisiyle ver.
- **Düzeltme işareti (şapka):** Resmî metinde TDK'ye uy: kâr/kar, hâlâ/hala, dükkân, resmî. Gündelik metinde yazar şapkasız yazıyorsa ona uy. İz olan, aynı metinde iki biçimin karışmasıdır.
- **Başlık:** TDK kitap ve makale alt başlıklarında kelimelerin büyük harfle başlamasına izin verir, ama "ve, ile, ya, veya, ki, de, da" ile "mı/mi" küçük kalır. Web'de yalnızca ilk kelimenin büyük olduğu düzen de yaygındır. İz olan büyütülmüş bağlaç ve tutarsızlıktır.
- **Noktalı virgül ve iki nokta:** İkisinin de meşru kullanımı var. Noktalı virgül virgüllü öbekleri ayırır, iki nokta örnek ya da açıklama getirir. İz olan yoğunluk ve "Sorun şu:" tipi anonstur (R2, B2).


## Dokunma listesi

Bunları görünce metne daha az dokun:
- **Yapay zeka sayılmayan şeyler:**
  - Kusursuz dil bilgisi.
  - Akademik ve resmî kipler.
  - Tek tük "ayrıca" ya da "kapsamlı".
  - Tek bir kısa vurucu cümle.
  - Gündelik "belki de".
  - Kaynaksız ama sıradan iddialar.
  - Alıntı, başlık ve özel adların içindeki kalıplar.
- **İnsan işi hatalar:** Özneyle yüklemin uyuşmaması, mantık kayması ya da eksik öge gibi anlatım bozukluklarını çoğunlukla insanlar yapar, modeller pek yapmaz. Onları iz sayma, dil bilgisi düzeltmesi olarak ayrıca ve nazikçe belirt.
- **İnsan izleri:**
  - Uydurulması zor özgül detaylar.
  - Karışık duygular.
  - Döneme ve alt kültüre özgü göndermeler.
  - Yazarın kendi sözünü kestiği ara sözler.
  - Noktalamaya sızmış duygu (üç nokta, ünlem).
  - Devrik cümleler.

Dedektörler temiz ve sade yazılmış insan metnini de sık sık yapay zeka sanır. Bu skillin işi iyi Türkçe yazmak, dedektörü kandırmaya çalışmaz.


## Çıktı biçimi

Varsayılan teslim biçimi aşağıda. Kullanıcı yalnız metni isterse yalnız metni ver.

```
💀 **İnsanlık öldü mü❓** · Tam yeniden yazım · Sosyal medya dili · 152 → 118 kelime

[nihai metin]

**Neyi neden değiştirdim**

| # | Önce | Sonra | Neden |
|---|------|-------|-------|
| 1 | "Günümüzde yapay zeka... haline geldi." | (çıkarıldı) | Klişe giriş, bilgi taşımıyor (T6) |
| 2 | "-maktadır" ile biten yedi cümle | geçmiş zaman ve isim cümleleri | Kafiyeli yüklem (Y1) |

**Ölçüm:** cümle boyu çeşitliliği 0,24 → 0,57 · uzun tire 3 → 0 · alarm 6 → 0
**Sana sorum var:** [yer tutucu bıraktığın yerler ve hedefli sorular, en fazla üç]
**İnceleme sayfası:** [adres] (yalnızca kullanıcı sayfayı istediyse)
```

- **Başlık satırı:** Logo, mod, metin tanımı ve kelime sayısı. 1. adımda sohbete yazdığın duyuru satırı ayrıca durur, teslimde tekrar etme.
- **Tablo:** En fazla sekiz satır olsun ve en önemli değişiklikleri göstersin. Tekrar eden değişiklikleri tek satırda topla ("-maktadır → -dı, 9 yerde"). Neden sütununu düz Türkçeyle yaz, kodu paranteze koy.
- **Ölçüm satırı:** Yalnızca betik çalıştıysa ekle. Sayıları betikten al, kendin uydurma.
- **Soru satırı:** Yalnızca yer tutucu bıraktıysan ekle.
- **Teşhis modu:** Nihai metin yerine "Kanı" satırı gelir: güçlü iz / karışık / zayıf iz. Ardından iz tablosu (iz, metinden kısa alıntı, ağırlık), insan izleri ve ölçüm. Sonunda "İstersen hafif ya da tam yeniden yazayım" de.
- **Sıfırdan yazım:** Metin ve iki üç cümlelik bir not gelir. Not, hangi kalıplardan bilerek kaçındığını ve hangi bilgileri yer tutucu bıraktığını söyler.


## İnceleme sayfası

5. adımdaki tercih sayfayı açtırıyorsa, kullanıcı teslimden sonraki soruda "Önizle"yi seçtiyse, sayfayı kendisi istediyse ya da sonradan "önizle" yazdıysa etkileşimli bir inceleme sayfası üret. Bunun için Python çalıştırabilmen ve dosya yazabilmen gerekir.

Sayfa tek bir HTML dosyası ve görünüşü ahşap masada duran bir defter yaprağı:
- Metinde değişen kelimelerin arkasında yeşil bir fosforlu kalem var. Kullanıcının onayladığı değişikliğin eski hali üstü çizili olarak yeni halin üstünde kalıyor. Silinen yerde küçük bir "[silindi]" notu duruyor. Köşeli parantezli sorular turuncu.
- Kenarda her değişikliğin numaralı bir yuvarlağı var. Gerekçenin ilk cümlesi sağ kenarda kısa bir not olarak duruyor.
- Cümleye tıklayınca bantlı bir not kartı açılıyor. Kart üç şeyi gösteriyor: "Neydi" (eski hal, üstü çizili), "Önerilen" (yeni hal ve gerekçe) ve "Başka seçenekler" (aynı cümlenin daha kısa, daha resmî ve daha sıcak hali). Kullanıcı "Öneriyi uygula", "Kalsın", "Kendim düzenleyeyim" ya da bir seçeneğin yanındaki okla karar veriyor, not ekleyebiliyor.
- Kart geniş ekranda defterin sağında üst hizada, dar ekranda cümlenin altında, telefonda ekranın altından açılıyor. Kâğıdın son satırı kaç değişikliğin onaylandığını gösteriyor.
- Değişen bir kısmın üstüne gelince açılan balonla seçenekler metnin içinde değiştirilebiliyor. Göz düğmesi (ya da `p` tuşu) kararların uygulanmış son halini işaretsiz gösteriyor.
- Kullanıcı kararlarını verip "Ajana gönder"e basıyor. Sayfa köprüsüz açıldıysa düğmenin adı "Geri bildirimi kopyala" olur ve kullanıcı metni sohbete yapıştırır.

Sayfayı üretmek için iki adım var. Orijinal metin 1. adımda "before", nihai metin 4. adımda "after" adıyla saklandı. Ayrıca dosya yazman gerekmez.
1. Gerekçeleri JSON olarak hazırla. Sayfa değişiklikleri cümle cümle böldüğü için **her değişen cümleye bir kayıt** aç. "before" ve "after" alanlarına cümleleri metinde geçtiği gibi, harfi harfine yaz. Kayıtları metindeki sırayla diz. Sayfa bu kayıtları çapa olarak kullanır, böylece ağır yeniden yazımda da her eski cümle kendi yenisiyle eşleşir. Silinen cümlede "after" boş kalır. Gerekçenin ilk cümlesi sayfanın kenarına not olarak yazıldığı için onu kısa tut, ayrıntıyı ikinci cümleye bırak: "Karşıtlıkla parlatma. Bilgi aynen korundu, kalıp gitti."

   Silinmeyen her cümleye "alternatives" alanında aynı cümlenin üç halini daha yaz: daha kısa, daha resmî ve daha sıcak. Kart bunları "Başka seçenekler" olarak gösterir, kullanıcı tek tıkla seçer. Seçenekler de aynı kurallara uyar: kaynakta olmayan bilgi girmez, iddianın gücü değişmez, yer tutucular yerinde kalır. Bir hal metnin türüne uymuyorsa (şartnamede "daha sıcak" gibi) onu yazma.
   ```json
   {
     "title": "LinkedIn duyurusu",
     "mode": "Tam yeniden yazım",
     "profile": {
       "label": "Sosyal medya dili",
       "subtype": "şirket duyurusu",
       "sector": "yazılım",
       "audience": "genel kitle",
       "approach": "Ekip jargonu Türkçeleşti, anons ve slogan kapanış çıktı."
     },
     "changes": [
       {"before": "orijinaldeki cümle", "after": "yerine gelen cümle", "reason": "kısa gerekçe", "pattern": "R1",
        "alternatives": [
          {"kind": "Daha kısa", "text": "cümlenin kısa hali"},
          {"kind": "Daha resmî", "text": "cümlenin resmî hali"},
          {"kind": "Daha sıcak", "text": "cümlenin sıcak hali"}
        ]}
     ]
   }
   ```
2. Betiği çalıştır, JSON'u standart girdiden ver:
   ```bash
   python3 <skill-dizini>/scripts/review.py --before before --after after --notes - --live --open <<'JSON'
   {...yukarıdaki biçimde notlar...}
   JSON
   ```
   "profile" alanına 1. adımda verdiğin kararı yaz. Sayfa bunu defterin üst kısmında "Metin tanımı" olarak gösterir. Alanı boş bırakırsan sayfa betiğin tahminini kullanır.

   `--live` sayfayı yerel bir köprü üzerinden açar, sayfa böylece seninle konuşur (bkz. Canlı inceleme). `--open` sayfayı tarayıcıda açar. Köprü açılamazsa betik bunu söyler ve sayfa dosya olarak açılır. Betiğin yazdığı adresi çıktının sonundaki "İnceleme sayfası" satırına koy.

   **Tarayıcı açamayan ortamlar:** Claude'un masaüstü ya da web sohbeti gibi bulutta çalışan bir ortamdaysan kullanıcının tarayıcısı senin makinene ulaşamaz. O zaman `--live` ve `--open` kullanma. Sayfayı `--output` ile kullanıcının indirebileceği bir yere yaz (Claude'da `/mnt/user-data/outputs/inceleme.html`) ve dosya olarak ver. Bu sayfada düğmenin adı "Geri bildirimi kopyala" olur, kullanıcı kararlarını kopyalayıp sohbete yapıştırır.


## Canlı inceleme

`--live` ile açılan sayfada iki ek özellik var:
- **Başka seçenek iste:** Kullanıcı kartta "daha samimi", "deyimle" gibi bir istek yazıp ajandan 2-3 seçenek ister. Notlarda "alternatives" yoksa kart daha kısa, daha resmî ve daha sıcak halleri de bu yolla ister.
- **Ajana gönder:** Kullanıcı kararlarını kopyala-yapıştır yerine doğrudan sana yollar.

Köprü bir öneri isteğini üç yoldan biriyle cevaplatır. Kullanıcı yolu Ayarlar'dan seçer. "Otomatik" seçiliyse sıra şöyledir:
1. **Dinleyen ajan:** Sen `bridge.py wait` ile bekliyorsan istek sana gelir. En bağlamlı yol budur.
2. **Oturum çatalı:** Sohbetin araç kullanamayan bir kopyası açılır. Bütün bağlamı bilir, ama uzun sohbetlerde yavaş ve maliyetlidir.
3. **Bağlamsız çağrı:** `claude -p`, `codex exec` ya da `gemini -p` sohbet geçmişi olmadan çağrılır.

Sayfayı açtıktan ve teslimini yaptıktan sonra dinlemeye geç:
```bash
python3 <skill-dizini>/scripts/bridge.py wait
```
Komut bir olay gelene kadar (en çok 9 dakika) bekler ve olayı yazdırır:
- **Öneri isteği:** Kurallara (bilgi sadakati, kalıplardan kaçınma, bağlama oturma) uyan 2-3 seçenek yaz ve yolla. İstek "Üç seçenek yaz, bu sırayla: daha kısa, daha resmî, daha sıcak." ise tam üç seçenek, o sırayla yaz: Kart onları bu sıraya göre adlandırır. Ardından yeniden `wait`.
  ```bash
  python3 <skill-dizini>/scripts/bridge.py reply --request 4 --suggestion "..." --suggestion "..." --suggestion "..."
  ```
- **Kullanıcı kararlarını gönderdi:** Metni "Geri bildirim turu" adımlarıyla işle. Sonra köprüyü kapat: `bridge.py close`.
- **Zaman aşımı:** Dinlemeyi bırak ve kullanıcıya söyle. Bundan sonraki öneriler oturum çatalıyla ya da bağlamsız gelecek. Kararlarını gönderdikten sonra sohbette "devam" yazması yeter. "Devam" gelince kararları oku:
  ```bash
  python3 <skill-dizini>/scripts/bridge.py status
  ```

Kabuk komutlarının süre sınırı kısa olan ortamlarda (örneğin Codex) dinlemeyi `wait --timeout 50` ile kısa aralıklarla döngüye al. Toplamda yine yaklaşık 9 dakika dinle.

Kullanıcı sayfadaki öneri seçeneklerinden birini seçerse o metin "BAŞKA ÖNERİ" olarak geri bildirime düşer. Onu da kullanıcının kendi önerisi gibi değiştirmeden kullan.


## Geri bildirim turu

Kullanıcı "[İnsanlık öldü mü? · geri bildirim]" ile başlayan bir mesaj yapıştırırsa kararları şöyle işle:

- `#n ESKİSİNE DÖN`: O parçada orijinal hali geri getir.
- `#n BAŞKA ÖNERİ`: "kullanıcının önerisi" satırındaki metni olduğu gibi kullan. İçinde bir kalıp görürsen notta nazikçe söyle, ama kullanıcının tercihini değiştirme.
- `#n BÖYLE KALSIN, NOTLU`: Değişikliği koru. Nota bak, gerekiyorsa o cümleyi notun yönünde ince ayarla.
- `Genel not`: Bütün metne uygula. Örneğin ton, uzunluk ya da sicil.
- `[Kararlar uygulanmış metin] ... [/metin]`: Bu blok varsa ikinci turun temeli odur. Kararlar ondan okunur, üstüne yalnız notları uygula.

Sonra yeniden ölç ve aynı çıktı biçimiyle teslim et. Bu sefer tablo yalnızca bu turdaki değişiklikleri gösterir. Kullanıcı inceleme sayfasıyla çalışıyorsa ve bu turda üçten fazla değişiklik varsa sayfayı yeniden üret. Önizleme sorusunu bu turda yeniden sorma.


## Örnek

**Önce** (şirket içi duyuru, karma kitle):

> Değerli ekip arkadaşlarım,
>
> Günümüzün hızla değişen dijital dünyasında müşteri memnuniyeti her zamankinden daha kritik bir öneme sahiptir. Bu doğrultuda yeni destek panelimizi geçtiğimiz cuma günü başarıyla konuşlandırdık — ve sonuçlar şimdiden umut verici!
>
> Yeni panel sadece bir araç değil, aynı zamanda ekiplerimiz arasındaki iş birliğini güçlendiren bir köprü. Talepler artık tek ekranda toplanıyor, öncelikler otomatik olarak belirleniyor ve yanıt süreleri önemli ölçüde kısalıyor.
>
> Sonuç olarak, bu yolculukta emeği geçen herkese teşekkür ederim. Birlikte daha da güçlüyüz! 🚀

**Sohbette ilk satır** (1. adım, ardından iş sürer):

💀 **İnsanlık öldü mü❓** · Metin tanımı: kurumsal yazışma dili (şirket içi duyuru) · Alan: yazılım · Yaklaşım: tam yeniden yazım, hitap korunur, ekip içi terimler sadeleşir

**Teslim:**

💀 **İnsanlık öldü mü❓** · Tam yeniden yazım · Kurumsal yazışma dili · 68 → 52 kelime

> Değerli ekip arkadaşlarım,
>
> Yeni destek panelini cuma günü canlıya aldık. İlk izlenimler iyi.
>
> Talepler artık tek ekranda toplanıyor, öncelikleri panel kendisi belirliyor, yanıt süreleri de kısalıyor [ilk haftanın ortalama yanıt süresi?]. Ekipler aynı talebi aynı ekranda gördüğü için birlikte çalışmak da kolaylaştı.
>
> Emeği geçen herkese teşekkürler.

**Neyi neden değiştirdim**

| # | Önce | Sonra | Neden |
|---|------|-------|-------|
| 1 | "Günümüzün hızla değişen dijital dünyasında... kritik bir öneme sahiptir." | (çıkarıldı) | Klişe giriş ve önem şişirmesi, duyuruya bilgi katmıyor (T6, R6) |
| 2 | "konuşlandırdık" | "canlıya aldık" | Ekiplerin kullandığı söz. "Konuşlandırmak" aşırı çeviri (S3) |
| 3 | "— ve sonuçlar şimdiden umut verici!" | "İlk izlenimler iyi." | Uzun tire ve abartı. Yazarın görüşü korundu, sesi indirildi (B1) |
| 4 | "sadece bir araç değil, aynı zamanda... bir köprü" | "Ekipler aynı talebi aynı ekranda gördüğü için..." | Karşıtlıkla parlatma. İddia metindeki bilgiyle somutlaştı (R1) |
| 5 | "önemli ölçüde kısalıyor" | "kısalıyor [ilk haftanın ortalama yanıt süresi?]" | Rakamsız büyütme. Rakam uydurulmadı, soruldu (G2) |
| 6 | "Sonuç olarak... Birlikte daha da güçlüyüz! 🚀" | "Emeği geçen herkese teşekkürler." | Kalıp kapanış, slogan ve emoji (T7, B5) |

**Sana sorum var:** İlk haftanın ortalama yanıt süresini biliyorsan köşeli parantezli yere yazalım. Bilmiyorsan o kısmı çıkarırım.

Bu örnekte hitap ("Değerli ekip arkadaşlarım") olduğu gibi kaldı. Yazarın kendi tercihi, iz sayılmaz.


## Dosyalar

| Dosya | Ne zaman okunur ya da çalıştırılır |
|---|---|
| `references/genres.md` | Tür rehberleri. `audit.py --guide` ilgili bölümü yazdırır, dosyayı ayrıca okuman gerekmez |
| `references/sectors.md` | Alan rehberleri: okur, dokunulmayacak bilgiler, alanın tipik izleri, önce/sonra örneği. `audit.py --guide` tahmin edilen alanın bölümünü de yazdırır |
| `references/patterns.md` | Bir kalıptan emin değilsen, örnek bir çare arıyorsan ya da bir kullanımın o türde iz sayılıp sayılmadığını bilmek istiyorsan ("Yanlış alarm" notları) |
| `references/flow.md` | Akış kurallarının ayrıntısı ve hangi türde hangi kuralların geçtiği için. Anlatı ve diyalogda mutlaka |
| `references/jargon.md` | Teknik, yazılım ya da bir alana özgü iş metninde mutlaka |
| `references/spelling.md` | Noktalama, şapka, başlık, konuşma çizgisi, sayı, para, tarih, kısaltma ve kurum adı yazımı için |
| `references/idioms.md` | Deyim ya da atasözü kullanmadan önce, çeviri kokan bir deyim gördüğünde |
| `references/sources.md` | Kuralların nereden geldiğini merak eden kullanıcıya göstermek için |
| `scripts/audit.py` | Ölçüm, metin tanımı tahmini, tür ve alan rehberi (1. adım), önce/sonra karşılaştırması (4. adım). `--save` metni saklar, `--guide` rehberi verir, `--profile` yalnız tahmini verir |
| `scripts/review.py` | Etkileşimli inceleme sayfası (5. adımdaki tercih ya da kullanıcının isteğiyle), `--live` ile köprülü |
| `scripts/bridge.py` | Canlı köprü: `wait`, `reply`, `status`, `close`. `preview` önizleme tercihini söyler ve değiştirir (5. adım). `update` günde bir kez yeni sürüme bakar, `--apply` günceller (6. adım) |
| `scripts/install.py` | Kurulum: skill'i ajanlara bağlar, köprüyü ayarlar, dener |
| `notebook/`, `notebook.json` | İnceleme sayfasının ve köprünün ortak çekirdeği, skill'in kimliği. notebook-review deposundan kopyalanır, okuman ya da değiştirmen gerekmez. `review.py` ve `bridge.py` bunları kullanır |
