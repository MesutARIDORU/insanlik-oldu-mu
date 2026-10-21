# Metin tanımları

Her metin türünün kendi doğru dili var. Şiirde dize kırılması yazarın kararıdır. Teknik şartnamede "-malıdır" gerekliliği bildirir, kurumsal e-postadaki selamlama da nezaket gereği orada durur. Bunları yapay zeka izi sanıp düzeltmek metni bozar. Bu dosya her tür için şunları söyler:
- Türü nereden tanırsın?
- Neye dokunmazsın?
- O türde yapay zeka nasıl iz bırakır?
- Hangi dille yazarsın?

`audit.py --profile` yüzeydeki ipuçlarından bir tahmin verir. Tahmin bir ipucudur. Metni okuyup son kararı sen verirsin. Bir metin iki türün arasındaysa (örneğin LinkedIn'de paylaşılan bir şirket duyurusu) asıl okura göre karar ver ve tanımda ikisini de söyle: "Sosyal medya dili · kurumsal duyuru".

**Alan** (sektör), metnin konusu olan iş kolu: yazılım, finans, sağlık, hukuk, eğitim, kamu, perakende, insan kaynakları. Alan, okuru, hassas bilgileri ve terimleri belirler. Her alanın rehberi `sectors.md`, terim tabloları `jargon.md` dosyasında. Edebi metinde alan "edebiyat"tır.

---

## Şiir dili

**Tanıma:** Kısa dizeler, satır sonunda noktalama yok ya da seyrek, kıtalar, ses tekrarı ve uyak.

**Dokunma:** Dize kırılmaları, kıta düzeni, uyak, ölçü, noktalama tercihleri, devrik söz dizimi. Bunlar şiirin kendisidir.

**Yapay zeka izi:**
- Soyut adlarla kurulmuş imgeler: "sessizliğin dansı", "zamanın nehri", "umudun ışığı".
- Her kıtanın bir teselliyle bitmesi ("yeniden doğdum her nefeste").
- Zorlama uyak için anlamı bükmek.
- "Fısıltı, yankı, eşik, sonsuzluk, derinlik" kelime kümesi.
- Her dizenin aynı uzunlukta olması.

**Yazım dili:** Varsayılan mod **teşhis**. Kullanıcı açıkça istemedikçe şiiri yeniden yazma. İzleri göster, dizeye dokunmadan nedenini söyle. Kullanıcı düzeltme isterse hafif dokunuşla yalnızca işaretli dizeyi değiştir. Soyut imgenin yerine somut bir nesne koymayı öner ama nesneyi uydurma, kullanıcıya sor. Akış kuralları (A1-A35) şiirde geçerli değildir.

## Edebi anlatı dili

**Tanıma:** Öykü, roman, anı. Diyalog, konuşma çizgisi, geçmiş zamanlı anlatı, karakter adları, sahne.

**Dokunma:** Karakterin sesi ve sicili, diyalog düzeni ve satır başı konuşma çizgisi, yazarın bilinçli devrikleri, anlatıcının kişisi ve zamanı.

**Yapay zeka izi:** Duyguyu adıyla söylemek ("içini bir huzursuzluk kapladı"), aynı anda iki zıt duygu, her sahnenin bir sonuç cümlesiyle bitmesi, "dedi" kalıbının tekdüzeliği (bkz. `patterns.md` G5).

**Yazım dili:** Anlatı kuralları (A5, A17-A19, A32-A35) burada işin çoğunu görür. Sahneye eklediğin her beden ayrıntısını tabloda "eklenen ayrıntı" diye belirt. Olay örgüsüne, karakterin kararlarına ve sona dokunma.

## Deneme ve köşe yazısı dili

**Tanıma:** Birinci kişiden görüş, tartışma, okura soru, gündelik örnekler.

**Dokunma:** Yazarın görüşü ve tezi, ironisi, kişisel örnekleri.

**Yapay zeka izi:** Her paragrafın vecizeyle bitmesi, "X değil, Y" iskeleti, "asıl mesele" anonsları, iki taraflı ve kimseyi kızdırmayan sonuç.

**Yazım dili:** Ses yazarda varsa güçlendir, yoksa uydurma. Okurla konuşma (A26), tavır sözcükleri (A27) ve devrik vurgu (A14) bu türde yerindedir.

## Kişisel yazı dili

**Tanıma:** Blog, gezi yazısı, kişisel paylaşım. Birinci tekil kişi ("gittim, düşündüm"), yaşanmış an.

**Dokunma:** Yazarın yaşadığı her ayrıntı, kendi kelimeleri, şakaları.

**Yapay zeka izi:** Broşür dili ("büyüleyici bir deneyim", "sizi bekliyor"), klişe giriş ve kapanış, yaşanmamış genellemeler.

**Yazım dili:** Somut olan yazarın deneyimidir. Deneyim metinde yoksa uydurma, yer tutucu bırak ya da sor. Sohbet tonu serbesttir ama argo serpiştirme (G6).

## Kurumsal yazışma dili

**Tanıma:** E-posta, duyuru, bilgilendirme yazısı. Selamlama ("Merhaba", "Sayın"), kapanış ("Saygılarımla", "İyi çalışmalar"), kurumun "biz" ağzından okura "siz" diye seslenmesi.

**Dokunma:** Selamlama ve kapanış biçimi (kurum kültürüdür), ad ve unvanlar, tarih, tutar, ekler, istenen eylem.

**Yapay zeka izi:**
- "Umarım bu e-posta sizi iyi bulur". İngilizceden birebir çeviri, Türkçe yazışmada kullanılmaz.
- "Konuyla ilgili olarak sizinle iletişime geçmek istedim" gibi amaca gelmeyen giriş.
- "Herhangi bir sorunuz olursa çekinmeden iletişime geçin" kalıbı.
- Duyuruda klişe giriş ("Günümüzün hızla değişen dünyasında") ve slogan kapanış.

**Yazım dili:** İlk cümle amacı söyler. İstenen eylem ve son tarih tek ve açık bir cümlede durur. Sicil kurumun sicilidir. Ekip içi yazışmada "Merhaba" ve "deadline" doğaldır, müşteriye giden yazıda "Sayın" ve "son tarih" tercih edilir (bkz. `jargon.md`). Deyim ve devrik cümle kullanma.

## Teknik şartname dili

**Tanıma:** Numaralı maddeler, "-malıdır, -melidir, -ecektir" gereklilik kipi, ölçü birimleri, "en az, en fazla", sistem ve modül adları.

**Dokunma:** Gereklilik kipi. "-malıdır" burada bir yükümlülüğü, "-ebilir" bir seçeneği bildirir ve ikisi birbirine çevrilemez. Ayrıca madde numaraları, sayılar, birimler, standart adları (AES-256, ISO 27001) ve tanımlı terimler.

**Yapay zeka izi:** Sınanamayan sıfatlar: "kullanıcı dostu", "sorunsuz", "kapsamlı", "uygun formatlarda", "yüksek performanslı". "Olanak tanıyacaktır" gibi süslü yüklemler. Bir maddeye iki gereklilik sıkıştırmak.

**Yazım dili:** Her madde tek ve sınanabilir bir gereklilik söyler. Belirsiz sıfatı kaldır ve yerine ölçüt koy. Ölçüt metinde yoksa uydurma, yer tutucu bırak: "Raporlama modülü [hangi biçimler: PDF, CSV?] biçiminde dışa aktarabilmelidir." Akış kuralları, ikileme, deyim ve devrik cümle kullanılmaz. Burada aynı ekle biten cümleler (Y1) iz sayılmaz, türün gereğidir.

## Teknik doküman dili

**Tanıma:** Kurulum rehberi, README, API belgesi, kullanım kılavuzu. Başlıklar, kod blokları, komutlar, okura emir kipiyle yol gösterme ("yükleyin, çalıştırın").

**Dokunma:** Kod, komut, dosya yolu, parametre, arayüz etiketi, sürüm numarası. Bunlar harfi harfine kalır.

**Yapay zeka izi:** "Bu kapsamlı rehberde...", "Hadi başlayalım!", başlıklarda emoji, aşırı çeviri terimler ("konuşlandırma", "çekme isteği", bkz. `jargon.md`), aynı kavrama üç ad.

**Yazım dili:** Adım adım, kısa emir ve tek gerekçe (A30). Her adım bir iş. Terimler belge boyunca aynı kalır. Hedef okur geliştiriciyse yerleşik İngilizce terimler kalır.

## Akademik dil

**Tanıma:** Kaynak gösterimi, "bu çalışmada", yöntem, bulgular, edilgen çatı, "-maktadır".

**Dokunma:** "-maktadır", edilgen çatı, terimler, kaynak gösterimi, istatistik ve tablo atıfları.

**Yapay zeka izi:** Önem şişirmesi ("kritik bir rol oynamaktadır"), yapay zeka kelime kümesi (S1), belirsiz otorite (G1), şablon "zorluklar ve gelecek" paragrafı (G4).

**Yazım dili:** Varsayılan mod **hafif dokunuş**. Sicili koru, yalnız şişirmeyi ve dolguyu al. Kaynağı belli olmayan iddiayı uydurma bir kaynakla destekleme, kullanıcıya sor.

## Hukuki dil

**Tanıma:** "İşbu", "taraflar", madde numaraları, "yükümlüdür", kanun ve yönetmelik adları.

**Dokunma:** Hukuki terimler, kalıplaşmış ifadeler, madde yapısı, tanımlı terimlerin büyük harfi. Anlamı değiştirebilecek her şey.

**Yapay zeka izi:** Hukuki metne karışmış pazarlama ve broşür dili, gereksiz tekrar, belirsiz atıflar.

**Yazım dili:** Varsayılan mod **teşhis ya da hafif dokunuş**. Önerilerini tabloya yaz, metni kendin değiştirmeden önce kullanıcıya sor. Hukuki sonucu olan bir değişikliği asla sessizce yapma.

## Haber dili

**Tanıma:** Yer ve kaynak girişi ("İSTANBUL (Haber Merkezi) –"), aktarım fiilleri ("açıkladı, bildirildi"), kurum adları, sayılar.

**Dokunma:** Alıntılar, kaynak adları, sayılar, tarih ve yer.

**Yapay zeka izi:** Yorum ve övgü sızması ("projenin kente büyük değer katacağı"), broşür dili, belirsiz otorite.

**Yazım dili:** Yansız ses. En önemli bilgi ilk cümlede. Birinci kişi ve okura seslenme yoktur.

## Pazarlama dili

**Tanıma:** Kampanya, indirim, satış çağrısı, ünlem, okura emir ("keşfedin, kaçırmayın").

**Dokunma:** Ürünün gerçek özellikleri, fiyat, tarih, koşullar, marka adları.

**Yapay zeka izi:** Broşür dili (S9: eşsiz, benzersiz, büyüleyici), içi boş sıfat yığını, her cümlede ünlem.

**Yazım dili:** Satış çağrısı bu türde meşrudur, çıkarma. Ama boş sıfatların yerine ürünün gerçek bir özelliğini koy. Özellik metinde yoksa uydurma, yer tutucu bırak.

## Sosyal medya dili

**Tanıma:** LinkedIn, X, Instagram gönderisi. Emoji, etiket, takipçiye soru ("Peki siz?"), kısa paragraflar.

**Dokunma:** Yazarın kendi emoji ve etiket alışkanlığı, marka adları.

**Yapay zeka izi:** "Heyecan verici bir duyurumuz var!", soru sorup kendi cevaplama (R3), "X değil, Y" (R1), slogan kapanış ve her gönderinin aynı soruyla bitmesi (T7).

**Yazım dili:** Kısa, kişisel, tek fikir. Kitle karmaşıksa ekip jargonunu Türkçeleştir (bkz. `jargon.md`).
