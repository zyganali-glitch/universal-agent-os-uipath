# Universal Agent OS — Yeni Demo Video Yönetmeni

Bu belge, UiPath ekranlarını iyi bilmeyen bir kullanıcının videoyu kesintisiz
çekebilmesi için hazırlanmıştır. Hedef süre 3–4 dakikadır.

## Kullanılacak tek başlangıç promptu

IDE ajanına yalnızca şunu yaz:

> Bir fikrim var, birlikte yapalım.

Prompt içinde teknik kelime, ürün türü, framework veya UiPath talimatı verme.
Videonun iddiası, ajanın repo kurallarını kendisinin keşfetmesidir.

## Kayıttan önce yapılacak hazırlık

1. UiPath Automation Cloud hesabına giriş yap.
2. Tarayıcıda şu sayfaları ayrı sekmelerde hazırla:
   - Action Center
   - Orchestrator Jobs
   - Data Fabric / Data Service
   - Maestro
3. IDE'de repo kökünü aç.
4. Terminali kapalı tut; ajan komutları kendi çalıştırmalıdır.
5. Tarayıcı yakınlaştırmasını `%125` veya `%150` yap.
6. Bildirimleri kapat; token, `.env` veya hesap ayarları ekranını videoda açma.

## Sahne 1 — Teknik olmayan başlangıç

**Kaydı başlat.**

1. IDE ajanına `Bir fikrim var, birlikte yapalım.` yaz.
2. Ajanın teknik soru sormadan repo kurallarını okumasını bekle.
3. Ajan önce salt-okunur `doctor` kontrolünü kendi çalıştırmalı; `ready: true`
   görünmeli.
4. Ajan ardından `register` komutunu kendi çalıştırmalı.
5. Çıktıda `gate_status: AWAITING_HUMAN` ve Task ID görünmeli.

**Bu noktada videoyu durdurma.** Task ID ekranda okunacak kadar kısa bekle.

## Sahne 2 — Onay olmadan ilerleyemediğini kanıtla

1. Ajan senden Action Center onayı istemeli.
2. Ajan Phase-0 sorusu sormamalı ve kod yazmamalı.
3. IDE ekranında bu bekleme mesajını göster.

**Burada kaydı geçici durdur.**

Tarayıcıya geçiş, sekme bulma veya giriş bekleme süresini videoya alma.

## Sahne 3 — Action Center görevi

**Action Center sekmesi hazır olduğunda kaydı yeniden başlat.**

1. Sol menüden `Actions` bölümünü aç.
2. Önce `Unassigned` sekmesine bak.
3. Görev düzenlenemiyorsa görevi kendine ata/claim et; sonra `Pending` sekmesine geç.
4. Başlığı `Phase-0 Alignment Review` olan ve IDE'deki Task ID ile eşleşen görevi aç.
5. Plan metnini göster.
6. `I approve this plan and grant execution permission` kutusunu işaretle.
7. İstersen Reviewer Notes alanına `Approved for Phase-0 interview` yaz.
8. `Submit Decision` düğmesine bas.

Görev `Completed` durumuna geçince 1–2 saniye bekle.

**Kaydı yeniden durdur.**

## Sahne 4 — Sunucu tarafında doğrulama

IDE sekmesine dön ve hazır olunca **kaydı yeniden başlat**.

1. Ajana yalnızca `Tamamladım.` yaz.
2. Ajan `verify` komutunu kendi çalıştırmalı.
3. Şunları yakınlaştırarak göster:
   - `completed: true`
   - `approved: true`
   - `gate_status: APPROVED`
4. Ajan bundan sonra `phase0_interview.py start` komutunu çalıştırmalı.
5. İlk Phase-0 sorusunu günlük dille ve tek başına sormalı.

Bu sahne, chat onayının değil UiPath verisinin esas alındığını kanıtlar.

## Sahne 5 — Collective Memory kanıtı

**Kaydı geçici durdur**, Data Fabric sekmesine geç, sonra yeniden başlat.

1. UiPath ana menüsünden `Data Fabric` veya hesabında hâlâ eski ad görünüyorsa
   `Data Service` bölümünü aç.
2. `Entities` listesini göster.
3. `StateMemory` entity'sini aç.
4. `Data` sekmesinde en yeni kaydı göster.
5. Kayıtta son görevin, `approved` sonucunun ve Action Center bağlantılı
   geçmişin bulunduğunu belirt.
6. Kısaca `CodeSoul` ve `MinefieldHistory` entity adlarını da göster.

**Kaydı durdur.**

## Sahne 6 — Orchestrator Job kanıtı

Orchestrator sekmesine geçip doğru folder'ı seç. Hazır olunca kaydı başlat.

1. Folder içinden `Automations` → `Jobs` yolunu aç.
2. En yeni `UniversalAgentOS_Phase0_Flow` job'ını bul.
3. IDE çıktısındaki Job ID ile eşleşmesini göster.
4. State, creation time ve process adını görünür tut.

5–8 saniye yeterlidir. **Kaydı durdur.**

## Sahne 7 — Maestro kanıtı

Maestro sekmesine geç. Hazır olunca kaydı başlat.

1. Maestro Home'dan ilgili projeyi aç.
2. Modeling canvas üzerinde şunları göster:
   - memory fetch;
   - Phase-0 alignment;
   - human review;
   - approval gateway;
   - approved/rejected yolları.
3. Varsa `Process instances` veya ilgili process'in `Monitoring` sekmesini aç.
4. Canlı instance/run kimliğini göster.

Canlı Maestro deployment henüz yoksa bunu saklama: portable BPMN modelini
göster ve canlı canvas deployment'ın hazırlık adımı olduğunu açıkça söyle.

**Kaydı durdur.**

## Sahne 8 — Phase-0 mülakatına giriş ve kapanış

IDE'ye dönüp kaydı başlat.

1. Ajanın ilk sorusuna günlük dille cevap ver.
2. Ajan cevabı kaydedip yalnızca ikinci soruyu sormalı.
3. Kapanış cümlesi:

> Teknik bilgisi olmayan kullanıcı tek cümleyle başladı. UiPath insan onayı
> doğrulanmadan ajan ilerlemedi; doğrulamadan sonra mülakatı kendi yönetti.

Bu noktada videoyu bitir. Sekiz sorunun tamamını videoda cevaplamak gerekmez;
birinci cevabın kaydedilip ikinci sorunun otomatik gelmesi Phase-0 motorunu
kanıtlamak için yeterlidir.

## Videoda kesinlikle gösterme

- `.env` dosyasının içeriği
- access token, client secret veya authorization header
- kişisel e-posta adresi
- uzun yükleme ve giriş bekleme ekranları
- eski Task ID veya önceki demo kayıtları
