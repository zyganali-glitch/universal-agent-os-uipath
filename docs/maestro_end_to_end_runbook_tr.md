# UiPath Maestro Uçtan Uca Tamamlama Kılavuzu

Son güncelleme: 22 Haziran 2026

## Hedef

Jürinin görmek istediği kanıt yalnızca BPMN çizimi veya ayrı API çağrıları
değildir. Hedef, UiPath Maestro tarafından yürütülen tek bir process instance
içinde insan, otomasyon ve karar adımlarının birbirine bağlanması ve instance'ın
`Completed` durumuna ulaşmasıdır.

Mevcut Python akışı Data Fabric ve Action Center entegrasyonunu canlı olarak
kanıtladı. Ancak `backend/labs_smoke_test.py register` içindeki
`start_maestro_process` çağrısı gerçekte Orchestrator Jobs API üzerinden bir RPA
release'i başlatır. Bu nedenle adı yanıltıcı olsa da tek başına Maestro runtime
kanıtı değildir.

## Önerilen uygulama sırası

En düşük riskli yol iki aşamalıdır:

1. Önce gerçek Maestro + Action App + gateway akışını `Completed` yap.
2. Sonra Data Fabric ve mevcut RPA/Python bileşenlerini aynı process içine
   bağlayarak entegrasyon derinliğini artır.

Bu sıra, bir child automation yetki veya runtime problemi yaşadığında bütün
Maestro kanıtının bloke olmasını önler.

## 1. Secret'i döndür

Önceki secret sohbette açığa çıktığı için artık güvenli kabul edilmemelidir.

1. Automation Cloud Admin'i aç.
2. External Applications > OAuth apps yoluna git.
3. `UniversalAgentOS` uygulamasını aç.
4. Eski secret'i sil.
5. Yeni secret üret.
6. Yeni değeri yalnızca ev bilgisayarındaki `.env` dosyasına yaz.
7. Secret'i ajana, sohbete veya ekran görüntüsüne koyma.

## 2. Tenant ve roller

Aynı tenant ve folder kullanılmalı:

- Organization: `zyganaligroup`
- Tenant: `DefaultTenant`
- Folder / OU ID: `7950291`

Kullanıcıda veya ilgili automation publisher hesabında şunlar bulunmalı:

- Maestro ve Studio Web erişimi;
- Orchestrator folder erişimi;
- package yayınlamak için `Packages - Create` veya uygun
  `Automation Publisher` rolü;
- Apps yayınlama/deploy yetkisi;
- Actions görüntüleme ve tamamlama yetkisi;
- Data Fabric read/write erişimi;
- child RPA kullanılırsa robot account, machine ve uygun runtime lisansı.

## 3. Action App oluştur ve deploy et

Maestro User Task, mevcut Python Generic Task formunu doğrudan seçmez. Maestro
için deploy edilmiş bir Action App gerekir.

Studio Web'de bir Action App oluştur:

**Ad:** `Phase0.Alignment.Review`

**Input alanları:**

| Alan | Tip | Zorunlu |
|---|---|---|
| `AgentProposedPlan` | String / multiline text | Evet |
| `TaskDescription` | String | Evet |
| `SessionId` | String | Evet |

**Output alanları:**

| Alan | Tip | Varsayılan |
|---|---|---|
| `Approved` | Boolean | `false` |
| `ReviewerNotes` | String | boş |
| `Decision` | String | `Rejected` |

Form üzerinde:

1. Planı salt okunur multiline text olarak göster.
2. `I approve this plan and grant execution permission` checkbox'ını
   `Approved` alanına bağla.
3. Reviewer Notes alanını `ReviewerNotes` değerine bağla.
4. İki net action kullan: `Approve` ve `Reject`.
5. Approve action'ı `Approved=true`, `Decision="Approved"` çıktısı vermeli.
6. Reject action'ı `Approved=false`, `Decision="Rejected"` çıktısı vermeli.
7. App'i publish et.
8. Orchestrator > ilgili folder > Automations > Apps > Deploy app yolundan
   deploy et.
9. Deploy edilen uygulamanın Action App olarak seçilebilir olduğunu doğrula.

## 4. Maestro Agentic Process'i oluştur

Automation Cloud > Maestro > Start modeling yolundan veya Studio Web'de yeni
`Agentic Process` projesi oluşturarak başla.

**Project/process adı:** `UniversalAgentOS_Phase0_Flow`

Repository'deki
[`../uipath_project/workflows/phase0_alignment.bpmn`](../uipath_project/workflows/phase0_alignment.bpmn)
dosyasını referans al. Tenant import sorun çıkarırsa canvas üzerinde elle kur.

İlk çalışır sürümde şu akış yeterlidir:

```text
Start
  -> Prepare Review
  -> Human Review
  -> Approved?
       -> Yes -> Grant Execution -> Save Approved State -> Approved End
       -> No  -> Record Rejection -> Rejected End
```

## 5. Process değişkenlerini tanımla

| Değişken | Tip | Örnek |
|---|---|---|
| `taskDescription` | String | `Start governed Phase-0` |
| `sessionId` | String | benzersiz çalışma kimliği |
| `agentProposedPlan` | String | kullanıcıya gösterilecek plan |
| `approved` | Boolean | `false` |
| `reviewerNotes` | String | boş |
| `decision` | String | boş |
| `stateRecordId` | String | boş |

## 6. Her BPMN düğümüne gerçek implementation bağla

Hiçbir task `None` olarak kalmamalı.

### 6.1 Prepare Review

En hızlı ilk sürüm:

- Element type: `Script task` veya `Service task`
- Action: `Execute script`
- Çıktı:
  `agentProposedPlan` değişkenine incelenecek planı yaz.

Daha güçlü sürüm:

- Action: `Execute connector activity`
- Connector: Data Fabric
- `CodeSoul`, `MinefieldHistory`, `Persona`, `StateMemory` kayıtlarını oku.
- Okunan kurallardan kısa bir review metni üret.

Connector aktivitesi tenant'ta uygun read işlemini sunmuyorsa ilk completed
instance için script kullan; Data Fabric entegrasyonunu ikinci sürümde ekle.

### 6.2 Human Review

- Element type: `User task`
- Action: `Create action app task`
- Action App: deploy edilen `Phase0.Alignment.Review`
- Task title: `Phase-0 Alignment Review`
- Input mapping:
  - `AgentProposedPlan <- agentProposedPlan`
  - `TaskDescription <- taskDescription`
  - `SessionId <- sessionId`
- Output mapping:
  - `approved <- Approved`
  - `reviewerNotes <- ReviewerNotes`
  - `decision <- Decision`

Maestro ayrıca `Action` ve `hitlTask` çıktıları sunabilir. Gateway'i mümkünse
Action App'in açık `Approved` Boolean çıktısına bağla; UI sürümü buna izin
vermiyorsa `Action == "Approve"` veya `hitlTask` içindeki karşılık gelen alanı
kullan.

### 6.3 Approved? gateway

Exclusive Gateway üzerinde iki koşul tanımla:

```text
Approved path: vars.approved == true
Rejected path: vars.approved == false
```

Canvas'ın kullandığı ifade sözdizimine göre Variable Picker ile
`approved` değişkenini seç. Elle yazılan ifadenin validation hatası vermediğini
kontrol et.

### 6.4 Grant Execution

İlk completed sürüm:

- Action: `Execute script`
- `decision = "APPROVED"` yap.

Derin entegrasyon sürümü:

- Action: `Start and wait for RPA workflow`, `Start and wait for API workflow`
  veya `Execute connector activity`.
- Mevcut Phase-0/gate mantığını child implementation olarak çağır.
- Input/output mapping'i açıkça yap.

### 6.5 Save Approved State

Tercih edilen:

- Action: `Execute connector activity`
- Connector: Data Fabric
- `StateMemory` içinde session, task, decision, reviewer notes ve Maestro
  instance correlation bilgisini kaydet.
- Dönen record ID'yi `stateRecordId` içine bağla.

İlk completed sürümde Data Fabric mapping engel çıkarırsa script ile sonucu
process değişkeninde tut; daha sonra Data Fabric write ekle.

### 6.6 Record Rejection

Tercih edilen:

- Action: `Execute connector activity`
- `MinefieldHistory` içine rejection lesson ve reviewer notes yaz.

Gateway'in rejected yolunu en az bir kez debug ederek doğrula.

## 7. Debug configuration

Canvas'ta `Debug configuration` aç:

1. Solution Resources altında Action App'i gerçek deploy edilmiş kaynağa bağla.
2. Data Fabric connector kullanılıyorsa doğru workspace/connection'ı seç.
3. Child RPA veya agent varsa gerçek process/agent kaynağını seç.
4. Project Arguments altında test değerlerini gir.
5. Önce `Debug step-by-step` çalıştır.
6. User Task oluştuğunda Actions ekranına git, görevi tamamla.
7. Execution Trail'de gateway'in doğru dala gittiğini izle.

Debug çalışması 30 dakika ile sınırlı olabilir; Action Center görevini bekletme.

## 8. Child RPA `Pending` sorununu kapat

Mevcut Orchestrator job'larının `Pending` kalması genellikle execution identity
veya runtime bulunmadığını gösterir.

Child RPA kullanacaksan:

1. Orchestrator > ilgili folder > Manage Access bölümünde bir robot account veya
   kullanıcı hesabı ata.
2. Unattended execution yetkisi ve lisansını doğrula.
3. Machine template ve runtime slot'un folder'a bağlı olduğunu doğrula.
4. Process'i aç > Package Requirements.
5. Child process yanında Execution settings'i aç.
6. Runtime type seç.
7. Account seç veya uygun olduğunda `Run as myself` kullan.
8. Child process'i Orchestrator'dan tek başına çalıştır ve `Successful` gör.
9. Bundan sonra Maestro içinden `Start and wait for RPA workflow` ile çağır.

Child process tek başına tamamlanmıyorsa Maestro'ya bağlama; aksi halde ana
instance da bekler veya fault olur.

## 9. Validation, publish ve deploy

1. Canvas'taki bütün validation error'ları kapat.
2. Approved ve rejected debug senaryolarını çalıştır.
3. Üst menüden `Publish` seç.
4. Solution adı, semantik version ve açıklayıcı changelog gir.
5. Publish işlemini tamamla.
6. Shared/tenant feed kullanıldıysa Orchestrator'da solution/process'i aynı
   folder'a deploy et.
7. Personal Workspace feed kullanıldıysa otomatik deploy durumunu doğrula.
8. Birden fazla start event varsa Orchestrator > Automations >
   Processes (Agentic processes) > Edit > Runtime arguments üzerinden default
   entry point seç.
9. Package Requirements altında bütün bağımlılıkların çözüldüğünü doğrula.

## 10. Gerçek process instance çalıştır

1. Orchestrator veya Maestro üzerinden deploy edilen agentic process'i aç.
2. Run/Start seç.
3. Gerekli input argument'larını ver.
4. Maestro > Process Instances ekranında yeni instance'ı aç.
5. Human Review adımında instance'ın beklediğini doğrula.
6. Actions ekranında bu instance'ın oluşturduğu görevi aç.
7. Approve seçeneğini kullan ve gönder.
8. Process Instances ekranına dön.
9. Execution Trail'de Approved gateway yolunu izle.
10. Final durumun `Completed` olmasını bekle.

API ile ayrı oluşturulan task değil, Maestro User Task'ın oluşturduğu task
kullanılmalıdır.

## 11. Zorunlu kanıt paketi

Repository'ye secret içermeden şunları ekle:

1. Maestro canvas: tüm task implementation'ları görünür.
2. Debug configuration: kaynak binding'leri görünür, credential görünmez.
3. Published solution version.
4. Orchestrator Agentic Process deployment ekranı.
5. Process Instance ID ve başlangıç zamanı.
6. Instance'ın Human Review üzerinde beklediği ekran.
7. Aynı instance'a bağlı Action Center task ID.
8. Approved gateway path execution trail.
9. Final `Completed` instance ekranı.
10. StateMemory write veya rejection MinefieldHistory kaydı.
11. Child jobs varsa `Successful` durumları.

Kanıt dosyalarını `docs/demo_screenshots/maestro_runtime/` altına koy ve
`docs/evidence_manifest.md` ile README'yi güncelle.

## 12. Başarı kriteri

Şunların tamamı olmadan "Maestro uçtan uca tamamlandı" deme:

- Published ve deployed bir Agentic Process var.
- Process Instances ekranında gerçek instance var.
- User Task, deploy edilmiş Action App ile Action Center görevi oluşturuyor.
- İnsan kararı gateway'i doğru dala yönlendiriyor.
- Instance terminal durumda `Completed`.
- Gerekli child process'ler `Pending` değil.
- Instance ID, task ID, version ve execution trail kanıtları repoda.

## Resmi UiPath kaynakları

- [Understanding Process implementation](https://docs.uipath.com/maestro/automation-cloud/latest/user-guide/understanding-process-implementation)
- [User task and Action App task](https://docs.uipath.com/maestro/automation-cloud/latest/user-guide/user-task)
- [Implementing a complex process](https://docs.uipath.com/maestro/automation-cloud/latest/user-guide/how-to-complex-process)
- [Debugging](https://docs.uipath.com/maestro/automation-cloud/latest/user-guide/debugging)
- [Publishing and upgrading agentic processes](https://docs.uipath.com/maestro/automation-cloud/latest/user-guide/publishing-deploying-and-upgrading-agentic-processes)
- [Process instances](https://docs.uipath.com/maestro/automation-cloud/latest/user-guide/all-instances-view)
