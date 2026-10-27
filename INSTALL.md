# Kurulum

İnsanlık öldü mü? düz Markdown ve küçük Python betiklerinden oluşur. Dosya okuyabilen her ajan `SKILL.md` talimatını kullanabilir. Betikler (ölçüm, inceleme sayfası, canlı köprü) Python 3.8 ya da daha yenisini ister ve yalnız standart kütüphaneyi kullanır.

## npx skills ile

Skill ortak `~/.agents/skills` klasörüne tek kopya olarak iner ve `~/.agents/.skill-lock.json` kilit dosyasına yazılır. Codex ve Gemini CLI skill'i bu klasörden okur. Claude Code kendi klasörüne bakar, `npx skills` oraya ortak kopyaya giden bir bağlantı kurar. Antigravity de kendi klasöründen okur ama `npx skills` oraya bağlantı kurmaz. Antigravity kullanıyorsan kurulumdan sonra ayar betiğini çalıştır (bkz. Antigravity).

### Tek komutla

```bash
npx skills add MesutARIDORU/insanlik-oldu-mu -g -y -a claude-code codex gemini-cli
```

Soru sormadan Claude Code, Codex ve Gemini CLI'a kurar. Sonunda şu özeti görürsün:

```
◇  Installed 1 skill
│  ✓ ~/.agents/skills/insanlik-oldu-mu
│    universal: Codex, Gemini CLI
│    symlinked: Claude Code
```

`-a` ile yalnızca saydığın ajanlara kurulur. Örneğin yalnız `-a claude-code` yazarsan skill ortak klasöre inmez, Claude Code'un klasörüne kopyalanır. Codex ve Gemini CLI'ı da istiyorsan üçünü birlikte say.

### Listeden seçerek

```bash
npx skills add MesutARIDORU/insanlik-oldu-mu -g
```

Komut önce skill'i bulur ve açıklamasını gösterir, sonra sırayla şunları sorar:

1. **Which agents do you want to install to?**
   - Üstteki "Universal (.agents/skills)" bölümünde Codex, Gemini CLI ve ortak klasörü okuyan öbür ajanlar var. Bunlar her zaman dahildir.
   - Claude Code alttaki "Additional agents" bölümünde ve seçili gelmez. "Search" alanına `claude` yaz, Claude Code'u boşluk tuşuyla işaretle, Enter'a bas.
   - Yalnızca Enter'a basarsan skill Codex ve Gemini CLI'a kurulur, Claude Code'a kurulmaz.
2. **Installation method:** Ek bir ajan seçtiysen sorulur. "Symlink (Recommended)" seçili gelir: Ajanın klasörüne ortak kopyaya giden bir bağlantı kurulur, güncelleme hepsine birden yansır. Enter'a bas.
3. **Proceed with installation?** Kurulumun özetini ve skill'in güvenlik taramasını gösterir. "Yes" seçili gelir, Enter'a bas.

### Güncelleme

Skill günde bir kez, o gün ilk çalıştığında `api.github.com` üzerinden son sürüme bakar. Yeni sürüm varsa ve teslim ettiği metin 250 karakterden uzunsa önce kendini şu komutla günceller, sonra "Tamam" ya da "Eski sürüme dön" diye sorar. Metin kısaysa önce sorar: "Güncelle" denirse günceller, "şimdi değil" denirse ertesi gün yeniden sorar. Eski sürüme dönüş, `npx skills add` ile o sürümün etiketini yeniden kurar. Geri çevrilen sürüm bir daha sorulmadan kurulmaz. Baktığı gün `~/.config/insanlik-oldu-mu/update.json` dosyasında durur. Skill bir git klonundan çalışıyorsa güncellemeyi `git pull --ff-only` ile yapar. ZIP olarak yüklendiyse yeni ZIP'in indirileceği sürüm sayfasını verir.

Elle güncellemek için:

```bash
npx skills update -g insanlik-oldu-mu
```

`-g` önemli: Onsuz komut kapsam sorar, Enter'a basınca "Project" seçilir ve global kurulan skill güncellenmez.

Ajan tabanlı bir araçtaysan ajana "Şu skill'i kur: https://github.com/MesutARIDORU/insanlik-oldu-mu" demen de yeter. Ajan bu dosyayı okuyup tek komutu çalıştırır.

## İsteğe bağlı ayarlar

`npx skills` skill'i kurar ama araçların ayarlarına dokunmaz. Skill ayarsız da çalışır. Şunları istersen kurulan kopyadaki ayar betiğini çalıştır:

```bash
python3 ~/.agents/skills/insanlik-oldu-mu/scripts/install.py
```

Betik skill'i yeniden kurmaz. Sırayla şunları yapar:

1. Bilgisayarındaki Claude Code, Codex, Gemini CLI ve Antigravity'yi bulur. Her biri için canlı köprünün hangi yollarını (oturum çatalı, bağlamsız çağrı) desteklediğine bakar.
2. Hangi araçlar için ayar yapılacağını sorar. Bulunanlar işaretli gelir. Numaraları virgülle yazarsın, Enter işaretlileri seçer, 0 hiçbirini seçmez:
   ```
   Hangi araçlar için ayar yapılsın?
     1) [x] Claude Code  bulundu · 2.1.300 (Claude Code) · bağlantı ve betik izinleri
     2) [x] Codex        bulundu · codex-cli 0.162.1 · yönlendirme notu
     3) [x] Gemini CLI   bulundu · 0.60.0 · /insanlik-oldu-mu komutu
     4) [x] Antigravity  bulundu · ~/.gemini/config/skills · skill bağlantısı
   ```
3. Claude Code'un skill klasöründe (`~/.claude/skills/insanlik-oldu-mu`) bağlantı olup olmadığına bakar. Kurulumda Claude Code seçilmediyse bağlantıyı aynı kopyaya kurar. Codex ortak klasörü kendisi okuduğu için ona ayrıca bağlantı kurmaz, yoksa skill iki kez görünür. Antigravity'ye ise `~/.gemini/config/skills/insanlik-oldu-mu` yolunda aynı kopyaya bir bağlantı kurar, çünkü `npx skills` onu atlar.
4. Gemini CLI için `~/.gemini/commands/insanlik-oldu-mu.toml` komutunu yazar.
5. Köprü ayarını `~/.config/insanlik-oldu-mu/config.json` dosyasına yazar.
6. Claude Code'un skill'i ve betiklerini her seferinde sormadan çalıştırmasına izin vermek isteyip istemediğini sorar: `Skill(insanlik-oldu-mu)` ve betik başına bir `Bash(python3 …)` kuralı. Onaylarsan önce `~/.claude/settings.json` dosyasının yedeğini alır. İzin yoksa Claude Code skill'i ilk kullanışında ve her betikte onay ister.
7. Codex'in genel talimatlarına yönlendirme notu eklemek isteyip istemediğini sorar (bkz. Codex).
8. Kısa bir deneme yapar: ölçüm, sayfa üretimi, köprünün açılıp kapanması.

Seçenekler:

| Seçenek | Ne yapar |
|---|---|
| `--dry-run` | Hiçbir şeyi değiştirmeden ne yapacağını gösterir |
| `--yes` | Soru sormadan çalışır. İzin ayarlarına ve Codex notuna dokunmaz |
| `--targets claude,codex` | Soru sormadan yalnız belirtilen araçlar için çalışır: `claude`, `codex`, `gemini`, `antigravity`. `all` bulunanların hepsi demektir |
| `--permissions` | Claude Code'a skill ve betik izinlerini ekler, artık olmayan betiklere ait izinleri çıkarır |
| `--codex-routing` | Codex'in genel talimatlarına (`~/.codex/AGENTS.override.md` varsa ona, yoksa `~/.codex/AGENTS.md`) yönlendirme notunu ekler |
| `--try-engine` | Bağlamsız öneri motorunu gerçek bir çağrıyla dener. Az miktarda kullanım harcar |
| `--no-check` | Sondaki denemeyi atlar |

Soru sormadan bütün ayarlar için:

```bash
python3 ~/.agents/skills/insanlik-oldu-mu/scripts/install.py --targets claude,codex,gemini,antigravity --permissions --codex-routing
```

## Node.js olmadan

Depoyu istediğin bir klasöre klonla ve kurulum betiğini oradan çalıştır:

```bash
git clone https://github.com/MesutARIDORU/insanlik-oldu-mu.git ~/insanlik-oldu-mu
```

```bash
python3 ~/insanlik-oldu-mu/scripts/install.py
```

Depodan çalıştırılınca betik hangi araçlara kurulacağını sorar ve skill'i oraya kendisi bağlar: Claude Code'a `~/.claude/skills/insanlik-oldu-mu`, Codex'e `~/.codex/skills/insanlik-oldu-mu`, Antigravity'ye `~/.gemini/config/skills/insanlik-oldu-mu`. Bağlama, depoyu `git pull` ile güncellediğinde skill'in de güncellenmesini sağlar. Bağlamak yerine kopyalamak için `--copy` ekle. Öbür adımlar yukarıdaki ayarlarla aynı.

## Araçlara göre notlar

### Claude Code

Skill `~/.claude/skills/insanlik-oldu-mu` klasöründen yüklenir. `npx skills` bu klasöre ortak kopyaya giden bir bağlantı kurar. Tek komutu kullandıysan ya da listede Claude Code'u işaretlediysen bağlantı vardır, yoksa ayar betiği kurar.

Kullanım: Metni ver ve "doğallaştır" de ya da `/insanlik-oldu-mu` komutunu kullan.

### Codex

Codex skill'leri ortak `~/.agents/skills` klasöründen okur, `npx skills` ile kurduysan başka bir şey gerekmez. Skill'i ayrıca `~/.codex/skills` altına koyma, Codex onu iki kez görür.

**Adı ve simgesi:** Codex skill'in adını ve simgesini `agents/openai.yaml` dosyasından okur. Skill listede "İnsanlık öldü mü?" adıyla ve kuru kafa simgesiyle görünür.

**Skill'in devreye girmesi:** Codex başlangıçta skill listesine bağlamın küçük bir payını ayırır, skill çoksa açıklamaları kısaltır. Skill'in açıklaması bu yüzden tetikleyici kelimelerle ("doğallaştırır ve insanlaştırır") başlar. 230 skill yüklü bir bilgisayarda codex-cli 0.162.1 skill'i adı verilmeden seçti. Yine de çok sayıda skill yüklüyse Codex bu skill'i kendiliğinden seçmeyebilir. Ayar betiği bunun için Codex'in genel talimatlarına üç satırlık bir yönlendirme notu eklemeyi önerir (`--codex-routing`). codex-cli 0.162.1 ile denendi: Not varken skill adı verilmeden devreye giriyor. Not istemezsen isteğinin başına `$insanlik-oldu-mu` yazman yeterli.

**Canlı köprü:** Köprü yalnız 127.0.0.1'de çalışan yerel bir sunucu açar. codex-cli 0.162.1 ile varsayılan sandbox'ta denendi: Ajan köprüyü dinleyebiliyor ve sayfadan gönderilen kararları alabiliyor. Sandbox ayarların daha sıkıysa ve Codex komut için onay isterse o oturum için izin vermen yeterli.

### ChatGPT masaüstü uygulaması

ChatGPT'nin masaüstü uygulamasının içinde kendi Codex'i var ve Codex CLI ile aynı skill klasörünü (`~/.agents/skills`) okur. `npx skills` ile kurduysan skill orada da hazırdır, ayrıca bir şey gerekmez. ChatGPT 26.1016 içindeki Codex 0.163.0-alpha ile denendi: Skill'i bu klasörden buluyor. Codex için yazılan notlar (yönlendirme notu, `$insanlik-oldu-mu`) burada da geçerli.

### Claude masaüstü ve web sohbeti

Claude'un masaüstü uygulamasında iki ayrı yer var. **Code** sekmesi Claude Code'dur, skill'i `~/.claude/skills` klasöründen okur ve `npx skills` ile kurulan skill orada hazırdır. **Sohbet** ise skill'leri bilgisayarındaki klasörlerden değil Claude hesabından alır ve Claude'un bulut ortamında çalıştırır. Sohbete eklemek için:

1. Settings > Capabilities altında "Code execution and file creation" açık olsun.
2. [Sürümler sayfasından](https://github.com/MesutARIDORU/insanlik-oldu-mu/releases/latest) `insanlik-oldu-mu.zip` dosyasını indir. Her sürümde otomatik eklenir.
3. Customize > Skills altında "+" > "Create skill" > "Upload a skill" ile ZIP'i yükle.

Bu ortamda ölçüm, yeniden yazım ve değişiklik tablosu çalışır. İnceleme sayfası canlı açılmaz: Claude onu indirilebilir bir HTML dosyası olarak verir, kararlarını sayfadaki "Geri bildirimi kopyala" ile sohbete yapıştırırsın. Önizleme tercihi orada saklanmaz. Bu yol henüz denenmedi. Claude'un yardım sayfası ZIP'teki klasör adının skill adıyla aynı olmasını istiyor, ZIP buna göre hazırlanır.

### Gemini CLI

**Hesap:** Google, Gemini CLI'ı Gemini Code Assist'in ücretsiz bireysel hesaplarında kapattı. Böyle bir hesapla CLI her istekte "This client is no longer supported for Gemini Code Assist for individuals" der ve Antigravity'ye yönlendirir. Gemini CLI 0.60.0 ile böyle bir hesapta denendi: Skill'i `~/.agents/skills` klasöründen buluyor (`gemini skills list`) ama hiçbir istek çalışmıyor. Gemini API anahtarıyla ya da ücretli bir planla çalışır. Ücretsiz hesapla Antigravity'yi kullan.

`npx skills` skill'i Gemini CLI'ın okuduğu ortak klasöre kurar. Ayar betiği ayrıca `~/.gemini/commands/insanlik-oldu-mu.toml` komutunu yazar, skill'i adıyla çağırmak için: `/insanlik-oldu-mu [metin]`. Komutu elle eklemek istersen [adapters/gemini/insanlik-oldu-mu.toml](adapters/gemini/insanlik-oldu-mu.toml) dosyasını o klasöre kopyala ve `<SKILL-YOLU>` yazan yerlere `~/.agents/skills/insanlik-oldu-mu` yolunu yaz.

Gemini'de "Başka öner" yalnızca bağlamsız çağrıyla çalışır, çünkü Gemini CLI oturum çatallamayı desteklemiyor. Bağlamsız çağrı için de hesabının Gemini CLI'ı kullanabilmesi gerekir: Google, bireysel ücretsiz Gemini Code Assist hesaplarında bu istemciyi kapattı.

### Antigravity

Antigravity genel skill'leri `~/.gemini/config/skills` klasöründen okur. Eski sürümleri `~/.gemini/antigravity/skills` klasörüne bakardı, ayar betiği hangisi varsa onu kullanır. `npx skills` Antigravity'yi ortak klasörü okuyan ajanlardan saydığı için oraya bağlantı kurmaz ve skill Antigravity'de görünmez. `npx skills` ile kurduktan sonra şunu çalıştır:

```bash
python3 ~/.agents/skills/insanlik-oldu-mu/scripts/install.py --targets antigravity
```

Betik `~/.gemini/config/skills/insanlik-oldu-mu` yolunda ortak kopyaya bir bağlantı kurar. Böylece `npx skills update` Antigravity'deki skill'i de günceller. Antigravity'de yeni bir sohbet aç ve `/insanlik` yaz, skill listede çıkar. Çıkmazsa Antigravity'yi yeniden başlat. Bağlantıyı görmeyen bir sürümde betiği `--copy` ile çalıştır, ama o zaman her güncellemeden sonra yeniden çalıştırman gerekir.

Canlı köprüde dinleyen ajan Antigravity'de de çalışır. Oturum çatalı çalışmaz, bağlamsız çağrı da bilgisayarda kurulu Claude Code, Codex ya da Gemini CLI üzerinden yapılır. "Yalnız bu sohbet için" önizleme seçimini köprü kaydedemez, çünkü Antigravity sohbetini tanıyamaz. O seçimi ajan sohbet boyunca kendisi hatırlar.

### AGENTS.md okuyan öbür araçlar

Ortak klasörü okumayan araçlarda önce depoyu bilgisayarına klonla. Ardından [adapters/agents-md-snippet.md](adapters/agents-md-snippet.md) dosyasındaki bloğu projenin ya da aracın `AGENTS.md` dosyasına ekle ve `<KLON-YOLU>` yerine deponun klasörünü yaz.

### Web sohbet arayüzleri

Claude'un sohbeti için yukarıdaki ZIP yolu var. ChatGPT, Claude.ai ya da Gemini'nin web arayüzünde dosya okuma ve betik çalıştırma yoksa `SKILL.md` içeriğini özel talimat, Project ya da Gem alanına yapıştırabilirsin. Bu durumda iki şey eksik kalır:
- Ölçümler elle yapılır.
- İnceleme sayfası olmaz.

Değişiklik tablosu yine gelir.

## Kurulumu doğrulama

Ajana şunu yaz:

```
Şunu doğallaştır: Dijital dönüşümün hız kazandığı bu dönemde, ekibimiz müşteri deneyimini uçtan uca iyileştiren yenilikçi bir çözüm geliştirmiştir.
```

Doğru kurulduysa cevap şöyle görünür:
- Sohbette önce `💀 İnsanlık öldü mü❓ · Metin tanımı: …` satırı belirir, ajan sonra işe devam eder.
- Teslim de aynı logoyla başlar.
- Klişe girişi, moda sözleri ("dijital dönüşüm", "uçtan uca", "yenilikçi") ve -miştir kipini fark eder.
- Çözümün ne olduğunu uydurmaz. Metinde yazmadığı için yer tutucu bırakır ya da sorar.
- Bir değişiklik tablosu verir.

Ajan cümleyi yalnızca eşanlamlılarla değiştirip geçiyorsa ya da kendinden bir özellik ekliyorsa talimatı okumamıştır.

## Kaldırma

`npx skills` ile kurduysan:

```bash
npx skills remove insanlik-oldu-mu -g
```

Ayar betiğini çalıştırdıysan onun yazdıklarını da sil:
- `~/.gemini/commands/insanlik-oldu-mu.toml`
- Antigravity bağlantısı: `~/.gemini/config/skills/insanlik-oldu-mu`
- `~/.config/insanlik-oldu-mu`
- Claude Code'a izin eklediysen `~/.claude/settings.json` içindeki `Skill(insanlik-oldu-mu)` ve `insanlik-oldu-mu/scripts` satırları.
- Codex'e yönlendirme notu eklediysen `~/.codex/AGENTS.override.md` (ya da `AGENTS.md`) içinde `insanlik-oldu-mu:start` ile `insanlik-oldu-mu:end` arasındaki blok.

Ayar betiği `settings.json` dosyasının ve Codex talimat dosyasının eski hallerini değiştirmeden önce aynı klasöre yedeklemiştir.

Depodan elle kurduysan `~/.claude/skills/insanlik-oldu-mu` ve `~/.codex/skills/insanlik-oldu-mu` bağlantılarını ve klonladığın klasörü sil.
