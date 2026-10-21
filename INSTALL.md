# Kurulum

İnsanlık öldü mü? düz Markdown ve küçük Python betiklerinden oluşur. Dosya okuyabilen her ajan `SKILL.md` talimatını kullanabilir. Betikler (ölçüm, inceleme sayfası, canlı köprü) Python 3.8 ya da daha yenisini ister ve yalnız standart kütüphaneyi kullanır.

## En kolay yol: `npx skills`

```bash
npx skills add MesutARIDORU/insanlik-oldu-mu -g
```

Skill ortak `~/.agents/skills` klasörüne tek kopya olarak kurulur ve `~/.agents/.skill-lock.json` kilit dosyasına yazılır. Hangi ajanlara (Claude Code, Codex, Gemini CLI...) bağlanacağını `npx skills` sorar. Soru sormadan kurmak için ajanları komutta say: `npx skills add MesutARIDORU/insanlik-oldu-mu -g -y -a claude-code codex gemini-cli`. Güncellemek için `npx skills update insanlik-oldu-mu`.

## Ayarlar

`npx skills` skill'i kurar ama araçların ayarlarına dokunmaz. Onlar için kurulan kopyadaki betiği çalıştır:

```bash
python3 ~/.agents/skills/insanlik-oldu-mu/scripts/install.py
```

Betik skill'i yeniden kurmaz. Şunları yapar:

1. Bilgisayarındaki Claude Code, Codex ve Gemini CLI'ı bulur. Her biri için canlı köprünün hangi yollarını (oturum çatalı, bağlamsız çağrı) desteklediğine bakar.
2. Hangi araçlar için ayar yapılacağını sorar. Bulunanlar işaretli gelir. Numaraları virgülle yazarsın, Enter işaretlileri seçer, 0 hiçbirini seçmez. Terminal yoksa bulunanların hepsini seçer.
3. Claude Code'un skill klasöründe (`~/.claude/skills/insanlik-oldu-mu`) bağlantı olup olmadığına bakar. `npx skills` Claude'u bağlamadıysa bağlantıyı aynı kopyaya kurar. Codex ortak klasörü kendisi okuduğu için ona ayrıca bağlantı kurulmaz, yoksa skill iki kez görünür. Gemini CLI için `/insanlik-oldu-mu` komutunu yazar.
4. Köprü ayarını `~/.config/insanlik-oldu-mu/config.json` dosyasına yazar.
5. İstersen Claude Code'un skill'i ve betiklerini her seferinde sormadan çalıştırmasına izin verir: `Skill(insanlik-oldu-mu)` ve betik başına bir `Bash(python3 …)` kuralı. Bunu yalnızca sen onaylarsan yapar ve önce eski ayarın yedeğini alır. İzin yoksa Claude Code skill'i ilk kullanışında ve her betikte onay ister.
6. Codex seçildiyse Codex'in genel talimatlarına yönlendirme notu eklemek isteyip istemediğini sorar (bkz. Codex).
7. Kısa bir deneme yapar: ölçüm, sayfa üretimi, köprünün açılıp kapanması.

Seçenekler:

| Seçenek | Ne yapar |
|---|---|
| `--dry-run` | Hiçbir şeyi değiştirmeden ne yapacağını gösterir |
| `--yes` | Soru sormadan çalışır. İzin ayarlarına dokunmaz |
| `--permissions` | Claude Code'a skill ve betik izinlerini ekler, artık olmayan betiklere ait izinleri çıkarır |
| `--targets claude,codex` | Soru sormadan yalnız belirtilen araçlar için çalışır. `all` bulunanların hepsi demektir |
| `--codex-routing` | Codex'in genel talimatlarına (`~/.codex/AGENTS.override.md` varsa ona, yoksa `~/.codex/AGENTS.md`) yönlendirme notunu ekler. Codex bu skill'i kendiliğinden seçer |
| `--try-engine` | Bağlamsız öneri motorunu gerçek bir çağrıyla dener. Az miktarda kullanım harcar |
| `--no-check` | Sondaki denemeyi atlar |

Ajan tabanlı bir araçtaysan ajana "Şu skill'i kur: https://github.com/MesutARIDORU/insanlik-oldu-mu" demen de yeter. Ajan bu dosyayı okuyup `npx skills` ile kurar.

## Node.js olmadan

Depoyu istediğin bir klasöre klonla ve kurulum betiğini oradan çalıştır:

```bash
git clone https://github.com/MesutARIDORU/insanlik-oldu-mu.git ~/insanlik-oldu-mu
```

```bash
python3 ~/insanlik-oldu-mu/scripts/install.py
```

Depodan çalıştırılınca betik hangi araçlara kurulacağını sorar ve skill'i oraya kendisi bağlar: Claude Code'a `~/.claude/skills/insanlik-oldu-mu`, Codex'e `~/.codex/skills/insanlik-oldu-mu`. Bağlama, depoyu `git pull` ile güncellediğinde skill'in de güncellenmesini sağlar. Bağlamak yerine kopyalamak için `--copy` ekle. Ayar adımları yukarıdakiyle aynı.

## Claude Code

`npx skills` Claude Code'u seçtiğinde skill'i `~/.claude/skills/insanlik-oldu-mu` klasörüne bağlar. Elle kurmak istersen depoyu skill klasörüne klonla:

```bash
git clone https://github.com/MesutARIDORU/insanlik-oldu-mu.git ~/.claude/skills/insanlik-oldu-mu
```

Kullanım: Metni ver ve "doğallaştır" de ya da `/insanlik-oldu-mu` komutunu kullan.

## Codex

Codex skill'leri hem ortak `~/.agents/skills` klasöründen hem `~/.codex/skills` altından yükler. `npx skills` ile kurduysan başka bir şey yapmana gerek yok. Elle kurmak istersen:

```bash
git clone https://github.com/MesutARIDORU/insanlik-oldu-mu.git ~/.codex/skills/insanlik-oldu-mu
```

**Adı ve simgesi:** Codex skill'in adını ve simgesini `agents/openai.yaml` dosyasından okur. Skill listede "İnsanlık öldü mü?" adıyla ve kuru kafa simgesiyle görünür.

**Canlı köprü hakkında:** Köprü yalnız 127.0.0.1'de çalışan yerel bir sunucu açar. codex-cli 0.162.1 ile varsayılan sandbox'ta denendi: Ajan köprüyü dinleyebiliyor ve sayfadan gönderilen kararları alabiliyor. Sandbox ayarların daha sıkıysa ve Codex komut için onay isterse o oturum için izin vermen yeterli.

**Codex'te skill'in devreye girmesi:** Çok sayıda skill yüklüyse Codex bu skill'i kendiliğinden seçmeyebilir. Ayar betiği bunun için Codex'in genel talimatlarına üç satırlık bir yönlendirme notu eklemeyi önerir (`--codex-routing`). codex-cli 0.162.1 ile denendi: Not varken skill adı verilmeden devreye giriyor. Not istemezsen isteğinin başına `$insanlik-oldu-mu` yazman yeterli.

## Gemini CLI

Ayar betiği `~/.gemini/commands/insanlik-oldu-mu.toml` komutunu yazar. Elle kurmak için [adapters/gemini/insanlik-oldu-mu.toml](adapters/gemini/insanlik-oldu-mu.toml) dosyasını o klasöre kopyala ve `<SKILL-YOLU>` yazan yerleri deponun yoluyla değiştir.

Kullanım: `/insanlik-oldu-mu [metin]`.

Gemini'de "Başka öner" yalnızca bağlamsız çağrıyla çalışır, çünkü Gemini CLI oturum çatallamayı desteklemiyor. Bağlamsız çağrı için de hesabının Gemini CLI'ı kullanabilmesi gerekir: Google, bireysel ücretsiz Gemini Code Assist hesaplarında bu istemciyi kapattı.

## AGENTS.md okuyan diğer araçlar

OpenCode, Amp, Jules gibi araçlarda önce depoyu bilgisayarına klonla. Ardından [adapters/agents-md-snippet.md](adapters/agents-md-snippet.md) dosyasındaki bloğu projenin ya da aracın `AGENTS.md` dosyasına ekle ve `<KLON-YOLU>` yerine deponun klasörünü yaz.

## Web sohbet arayüzleri

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

Ardından ayar betiğinin yazdıklarını sil:
- `~/.gemini/commands/insanlik-oldu-mu.toml`
- `~/.config/insanlik-oldu-mu`

Elle kurduysan şunları da sil:
- `~/.claude/skills/insanlik-oldu-mu`
- `~/.codex/skills/insanlik-oldu-mu`
- Klonladığın depo klasörü

Claude Code'a izin eklediysen `~/.claude/settings.json` içindeki `Skill(insanlik-oldu-mu)` ve `insanlik-oldu-mu/scripts` satırlarını da çıkar. Codex'e yönlendirme notu eklediysen `~/.codex/AGENTS.override.md` (ya da `AGENTS.md`) içinde `insanlik-oldu-mu:start` ile `insanlik-oldu-mu:end` arasındaki bloğu sil. Ayar betiği eski ayarın yedeğini aynı klasörde bırakmıştır.
