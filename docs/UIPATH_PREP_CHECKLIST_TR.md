# UiPath Demo Hazırlık Kontrol Listesi

Video başlamadan önce bu hazırlıkların tamamı yeşil olmalıdır.

## 1. Action Center

- `Actions` servisi tenant üzerinde açık.
- Kullanıcı Action görüntüleme, atama ve tamamlama yetkisine sahip.
- Unassigned görevler düzenlenemiyorsa görevi kendine atama/claim etme yetkisi var.

UiPath'e göre Unassigned görevler salt okunur olabilir; düzenlemek için görev
kullanıcıya atanmalı ve `Pending` durumuna geçmelidir.

## 2. Data Fabric / Data Service

- `CodeSoul`, `MinefieldHistory` ve `StateMemory` entity'leri mevcut.
- External application için en az Data Read ve Data Write yetkileri açık.
- `CodeSoul` içinde en az bir kural bulunuyor.
- `MinefieldHistory` içinde en az bir geçmiş ders bulunuyor.

Hizmet görünmüyorsa: Automation Cloud `Admin` → tenant → `Services` →
`Add Services` yolundan Data Fabric / Data Service'i etkinleştir.

## 3. Orchestrator

- `UniversalAgentOS_Phase0_Flow` process'i doğru folder'da yayınlanmış.
- `.env` içindeki OU/folder ID aynı folder'a ait.
- Release read izni yoksa `UIPATH_RELEASE_KEY` doldurulmuş.
- Folder içinden `Automations` → `Jobs` ekranı açılabiliyor.

## 4. Maestro

- Maestro servisi tenant üzerinde erişilebilir.
- Canlı iddia kullanılacaksa modeling canvas üzerinde süreç oluşturulmuş ve
  yayınlanmış.
- İzleme kanıtı için `Process instances` veya process `Monitoring` ekranı
  erişilebilir.

Sadece portable BPMN varsa bunu canlı Maestro run olarak adlandırma.

## 5. Yerel repo

```powershell
python -m pytest -q
python -m py_compile backend/uipath_api_connector.py backend/labs_smoke_test.py backend/phase0_interview.py
```

İki komut da başarılı olmalı.

## 6. Video sekmeleri

Şu sekmeleri kayıt öncesinde aç:

1. IDE
2. Action Center → Actions
3. Data Fabric / Data Service → Entities
4. Orchestrator → doğru folder → Automations → Jobs
5. Maestro → ilgili project/canvas

Sekmeler hazır değilken kaydı durdur; arama ve yükleme sürelerini final videoya
alma.
