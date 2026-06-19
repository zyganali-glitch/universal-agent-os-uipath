# UiPath Labs Gerçek Kurulum ve Çalıştırma Kılavuzu (Runbook)

## Hedef
Universal Agent OS'i sadece yerel (offline) simülasyon olarak değil, UiPath Labs / Automation Cloud üzerinde gerçek ve çalışan bir entegrasyon olarak çalıştırmak.

## Ön Koşullar
- UiPath Labs / Automation Cloud erişimi (zyganali@gmail.com hesabı ile giriş yapabilirsiniz)
- Tenant (Kiracı) ve Organizasyon (Organization Unit - OU) bilgileri
- Data Service modülünün etkin olması
- Maestro BPMN modülünün etkin olması
- Action Center (İşlem Merkezi) modülünün etkin olması
- API erişim anahtarı veya kimlik doğrulama tokenı (Access Token)
- Python 3.11+ sürümü

---

## Adım 1 — Data Service Varlıklarını (Entities) Oluşturma
UiPath Automation Cloud -> Data Service ekranına gidin ve aşağıdaki şemaları kullanarak tabloları oluşturun:
- `uipath_project/entities/code_soul.json`
- `uipath_project/entities/minefield_history.json`
- `uipath_project/entities/persona.json`
- `uipath_project/entities/state_memory.json`

Alan isimlerini ve tiplerini şema dosyalarındaki isimlerle birebir aynı yapmaya dikkat edin.

## Adım 2 — Bellek Kayıtlarını Başlatma (Seed Data)
Oluşturduğunuz varlıklara örnek kayıtlar ekleyin:
- **CodeSoul:** `"No eval() code injection allowed"` (eval enjeksiyonuna izin verilmez) gibi kurallar girin.
- **MinefieldHistory:** `"Idempotency guard required on payments"` (ödemelerde mükerrerlik koruması şarttır) gibi geçmiş hata dersleri ekleyin.
- **Persona:** Geliştirici tercihlerini belirten bir kayıt girin: `"strictness: high"`.
- **StateMemory:** Boş veya varsayılan bir oturum kaydı oluşturun.

## Adım 3 — Maestro BPMN Sürecini Tasarlama
UiPath Studio veya Maestro üzerinde şu isimde bir süreç (Process) oluşturun:
`UniversalAgentOS_Phase0_Flow`

Sürece şu düğümleri (nodes) ekleyin ve bağlayın:
1. **StartEvent_TaskSubmitted** (Geliştirici görev gönderir)
2. **ServiceTask_FetchMasterMemory** (Data Service'ten bellek kayıtlarını çeker)
3. **ServiceTask_RunPhase0Alignment** (Kodlama ajanı ile hizalama arayüzünü çalıştırır)
4. **UserTask_ActionCenterReview** (Action Center üzerinde insan onay bekletmesi)
5. **ExclusiveGateway_ApprovalDecision** (Onaylandı mı? kararı)
6. **ServiceTask_GrantExecution** (Onaylandıysa ajana çalıştırma izni verir)
7. **ServiceTask_SaveStateMemory** (Durum verisini Data Service'e kaydeder)
8. **ServiceTask_UpdateMinefieldHistory** (Reddedildiyse dersi hata geçmişine ekler)
9. **EndEvent_Approved** (Onaylı bitiş)
10. **EndEvent_Rejected** (Reddedilmiş bitiş)

## Adım 4 — Action Center Bağlantısı
Action Center'da insan onayını yönetecek şu isimde bir form görevi (Form Task) oluşturun:
`Phase-0 Alignment Review`

Form alanları:
- Agent (Ajan ismi)
- Requested task (İstenen görev)
- Minefield matches (Hata eşleşmeleri)
- Proposed plan (Önerilen plan)
- Approval decision (Onay kararı)
- Reviewer notes (İnceleyen notları)

## Adım 5 — Sıkı Gerçek Modu (Strict Real Mode) Yapılandırma
`.env.example` dosyasını kopyalayarak `.env` dosyası oluşturun.

Aşağıdaki çevre değişkenlerini doldurun:
- `UIPATH_MOCK_MODE=false` (Sahte mod kapalı, gerçek API çağrıları aktif)
- `UIPATH_TENANT_NAME` (Tenant adınız)
- `UIPATH_OU_ID` (Klasör/Organizasyon ID'niz)
- `UIPATH_ACCESS_TOKEN` (API'den alacağınız token)
- `UIPATH_TIMEOUT_SECONDS=30`

Eğer Labs sunucu adresleriniz varsayılan cloud URL'lerinden farklıysa şu geçersiz kılma (override) adreslerini girin:
- `UIPATH_ORCHESTRATOR_ODATA_URL`
- `UIPATH_DATA_SERVICE_API_URL`
- `UIPATH_ACTION_CENTER_ODATA_URL`

## Adım 6 — Smoke Testini Çalıştırma
Aşağıdaki komutları çalıştırarak gerçek entegrasyonu doğrulayın:
```bash
python -m py_compile backend/sync_markdown_to_uipath.py backend/uipath_api_connector.py
python backend/labs_smoke_test.py
```
*(Bu test token veya hassas bilgileri sızdırmadan sonuçları `run_artifacts/labs_smoke_result.sanitized.json` dosyasına yazacaktır).*

## Adım 7 — Kanıtları Toplama
`docs/labs_evidence_checklist.md` dosyasındaki listeyi takip ederek ekran görüntülerini alıp ilgili klasöre yerleştirin.

---

## 🎥 Jüri Demo Videosu Nasıl Çekilir? (Adım Adım Video Rehberi)

Jürinin projenin sadece yerel bir mock değil, gerçek bir UiPath çözümü olduğunu anlaması için videoda şu adımları izleyin:

1. **Giriş ve Bulut Arayüzü (0:00 - 1:00):**
   - zyganali@gmail.com hesabınız ile **UiPath Automation Cloud**'a giriş yapın.
   - Kiracı (Tenant) ana sayfanızı göstererek gerçek bir bulut ortamında olduğunuzu kanıtlayın.
2. **Data Service Kayıtları (1:00 - 2:00):**
   - **Data Service** sekmesine gidin.
   - Oluşturduğunuz `CodeSoulRule` ve `MinefieldHistory` tablolarını gösterin. İçindeki kayıtları (örneğin Stripe ödeme kurallarını) göstererek belleğin veritabanında saklandığını gösterin.
3. **BPMN Süreç Tasarımı (2:00 - 3:00):**
   - **UiPath Studio**'yu veya Maestro süreç ekranını açın.
   - `UniversalAgentOS_Phase0_Flow` iş akışını (BPMN şemasını) gösterin. Sürecin insan onay kutusuna (Action Center) nasıl yönlendiğini şema üzerinden anlatın.
4. **Çalıştırma ve Tetikleme (3:00 - 4:00):**
   - Yerel kontrol panelinde görevi başlatın veya terminalde `python backend/labs_smoke_test.py` çalıştırın.
   - Konsolda gerçek API çağrılarının başarıyla gittiğini gösterin.
5. **Action Center İnsan Onayı (4:00 - 4:45):**
   - Automation Cloud'da **Action Center** sayfasına girin.
   - Düşen onay görevini açın. Ajanın önerdiği kodlama planını jüriye gösterip ardından **Approve** (Onayla) butonuna basın.
   - İnsan onayı verilene kadar ajanın kod yazmasının Maestro tarafından bloke edildiğini vurgulayın.
6. **Kapanış (4:45 - 5:00):**
   - Tekrar Data Service sayfasına girip onay durumunun ve logların veritabanına işlendiğini gösterin.
   - GitHub/GitLab deposunu göstererek videoyu bitirin.
