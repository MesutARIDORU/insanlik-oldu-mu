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

```bash
npx skills update insanlik-oldu-mu
```

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

**Skill'in devreye girmesi:** Çok sayıda skill yüklüyse Codex bu skill'i kendiliğinden seçmeyebilir. Ayar betiği bunun için Codex'in genel talimatlarına üç satırlık bir yönlendirme notu eklemeyi önerir (`--codex-routing`). codex-cli 0.162.1 ile denendi: Not varken skill adı verilmeden devreye giriyor. Not istemezsen isteğinin başına `$insanlik-oldu-mu` yazman yeterli.

**Canlı köprü:** Köprü yalnız 127.0.0.1'de çalışan yerel bir sunucu açar. codex-cli 0.162.1 ile varsayılan sandbox'ta denendi: Ajan köprüyü dinleyebiliyor ve sayfadan gönderilen kararları alabiliyor. Sandbox ayarların daha sıkıysa ve Codex komut için onay isterse o oturum için izin vermen yeterli.

### Gemini CLI

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

ChatGPT, Claude.ai ya da Gemini'nin web arayüzünde dosya okuma ve betik çalıştırma yoksa `SKILL.md` içeriğini özel talimat, Project ya da Gem alanına yapıştırabilirsin. Bu durumda iki şey eksik kalır:
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
