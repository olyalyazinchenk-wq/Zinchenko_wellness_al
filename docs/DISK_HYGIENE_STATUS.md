# Disk Hygiene Status

## 2026-04-25 23:35:58 +03:00

- Before C:: `210.32 GB used / 12.69 GB free`
- After C:: `209.93 GB used / 13.09 GB free`
- Delta free space: `+0.40 GB` (`+425.03 MB`)
- Safe cleanup performed:
  - `C:\Users\HP\AppData\Local\Temp`: removed `8` stale files, freed `198.49 MB`, `14` locked/in-use deletions skipped
  - `C:\Windows\Temp`: no stale items removed
  - Recycle Bin: confirmed empty
  - Project-local pip cache: not present
- Desktop hygiene:
  - ensured category folders exist
  - moved `Antigravity.lnk` into `C:\Users\HP\Desktop\00_Ярлыки`
  - left project/work folders in place
- Risk flags:
  - some temp items were locked or in use and were skipped safely
  - free space is above the `10 GB` escalation threshold, so no large-folder triage was required

## 2026-04-26 11:37:24 +03:00

- Before C:: `210.18 GB used / 12.72 GB free`
- After C:: `210.04 GB used / 12.86 GB free`
- Delta free space: `+0.14 GB` (`+139.86 MB`)
- Safe cleanup performed:
  - `C:\Users\HP\AppData\Local\Temp`: removed `41` stale items, freed `143.57 MB`, `44` locked/in-use deletions skipped
  - `C:\Windows\Temp`: no stale items removed
  - Recycle Bin: confirmed empty
  - Project-local pip cache: not present
- Desktop hygiene:
  - ensured category folders exist
  - no loose user files needed moving
  - left existing project/work folders in place
- Risk flags:
  - some temp items were locked or in use and were skipped safely
  - `Clear-RecycleBin` returned a path error, but COM verification showed `0` items before and after
  - free space is above the `10 GB` escalation threshold, so no large-folder triage was required

## 2026-04-26 23:39:04 +03:00

- Before C:: `210.23 GB used / 12.78 GB free`
- After C:: `210.00 GB used / 13.02 GB free`
- Delta free space: `+0.24 GB` (`+241.45 MB`)
- Safe cleanup performed:
  - `C:\Users\HP\AppData\Local\Temp`: removed `39` stale items, freed `241.45 MB`, `15` locked/in-use deletions skipped
  - `C:\Windows\Temp`: no stale items removed
  - Recycle Bin: confirmed empty before and after cleanup
  - Project-local pip cache: not present
- Desktop hygiene:
  - confirmed category folders already exist
  - no loose user files needed moving
  - left existing project/work folders in place
- Risk flags:
  - some temp items were locked or in use and were skipped safely
  - free space is above the `10 GB` escalation threshold, so no large-folder triage was required

## 2026-04-27 11:39:48 +03:00

- Before C:: `210.26 GB used / 12.76 GB free`
- After C:: `210.25 GB used / 12.76 GB free`
- Delta free space: `+0.00 GB` (`+1.02 MB`)
- Safe cleanup performed:
  - `C:\Users\HP\AppData\Local\Temp`: removed `4` stale items, freed `1.58 MB`, `45` locked/in-use deletions skipped
  - `C:\Windows\Temp`: no stale items removed
  - Recycle Bin: confirmed empty before and after cleanup
  - Project-local pip cache: not present
- Desktop hygiene:
  - confirmed category folders already exist
  - no loose user files needed moving
  - left existing project/work folders in place
- Risk flags:
  - some temp items were locked or in use and were skipped safely
  - free space is above the `10 GB` escalation threshold, so no large-folder triage was required

## 2026-04-28 11:42:13 +03:00

- Before C:: `214.44 GB used / 8.58 GB free`
- After C:: `214.44 GB used / 8.57 GB free`
- Delta free space: `-0.01 GB` (`-10.24 MB` after background disk activity; cleanup itself removed stale temp files)
- Safe cleanup performed:
  - `C:\Users\HP\AppData\Local\Temp`: removed `44` stale items (`5` files, `39` directories), approx `0.56 MB`
  - `C:\Windows\Temp`: no stale items removed
  - Recycle Bin: confirmed empty before and after cleanup
  - Project-local pip cache: not present in `C:\Users\HP\Desktop\Новая папка`
- Desktop hygiene:
  - confirmed category folders already exist
  - moved `Antigravity.lnk`, `Google Flow Music.lnk`, and `Mixboard.lnk` into `C:\Users\HP\Desktop\00_Ярлыки`
  - moved loose file `Новая` into `C:\Users\HP\Desktop\06_Разное`
  - left existing project/work folders in place
- Large-folder triage because free space is below `10 GB`:
  - Downloads top folders:
    - `C:\Users\HP\Downloads\Зинченко_Ольга_Викторовна_1521` — `0.52 GB`
    - `C:\Users\HP\Downloads\wps_download` — `0.24 GB`
    - `C:\Users\HP\Downloads\Telegram Desktop` — `0.02 GB`
    - `C:\Users\HP\Downloads\соп админ` — `0.01 GB`
    - `C:\Users\HP\Downloads\Antigravity_Unlocker-1.23.2` — `0.01 GB`
  - Desktop top folders:
    - `C:\Users\HP\Desktop\Новая папка` — `0.20 GB`
    - `C:\Users\HP\Desktop\папины фото с тел` — `0.07 GB`
    - `C:\Users\HP\Desktop\справка ндфл` — `0.04 GB`
    - `C:\Users\HP\Desktop\Codex` — `0.03 GB`
    - `C:\Users\HP\Desktop\дипломная работа` — `0.02 GB`
- Recommended delete-review candidates:
  - `C:\Users\HP\Downloads\Зинченко_Ольга_Викторовна_1521`
  - `C:\Users\HP\Downloads\wps_download`
  - `C:\Users\HP\Downloads\Telegram Desktop`
- Risk flags:
  - drive `C:` remains below the `10 GB` free-space threshold after safe cleanup
  - the safe cleanup target sizes are now too small to materially improve space without manual deletion of larger user folders

## 2026-04-28 23:44:08 +03:00

- Before C:: `214.91 GB used / 8.10 GB free`
- After C:: `214.91 GB used / 8.10 GB free`
- Delta free space: `+0.00 GB` (`0.00 MB` net change after cleanup)
- Safe cleanup performed:
  - `C:\Users\HP\AppData\Local\Temp`: removed `11` stale items (`10` files, `1` directory); `22` locked/in-use deletions skipped; folder size still grew during the run because background apps wrote new temp data
  - `C:\Windows\Temp`: no stale items removed
  - Recycle Bin: confirmed empty before and after cleanup
  - Project-local pip cache: not present in `C:\Users\HP\Desktop\Новая папка`
- Desktop hygiene:
  - confirmed category folders already exist
  - no loose user files needed moving
  - left existing project/work folders in place
- Large-folder triage because free space is below `10 GB`:
  - Downloads top folders:
    - `C:\Users\HP\Downloads\Зинченко_Ольга_Викторовна_1521` — `0.52 GB`
    - `C:\Users\HP\Downloads\wps_download` — `0.24 GB`
    - `C:\Users\HP\Downloads\Telegram Desktop` — `0.02 GB`
    - `C:\Users\HP\Downloads\соп админ` — `0.01 GB`
    - `C:\Users\HP\Downloads\Antigravity_Unlocker-1.23.2` — `0.01 GB`
    - `C:\Users\HP\Downloads\The Elder Scrolls V Skyrim Special Edition by xatab` — `0.00 GB`
    - `C:\Users\HP\Downloads\Metro 2033 Redux` — `0.00 GB`
  - Desktop top folders:
    - `C:\Users\HP\Desktop\Новая папка` — `0.20 GB`
    - `C:\Users\HP\Desktop\папины фото с тел` — `0.07 GB`
    - `C:\Users\HP\Desktop\справка ндфл` — `0.04 GB`
    - `C:\Users\HP\Desktop\Codex` — `0.03 GB`
    - `C:\Users\HP\Desktop\03_Изображения` — `0.02 GB`
    - `C:\Users\HP\Desktop\дипломная работа` — `0.02 GB`
    - `C:\Users\HP\Desktop\01_Документы` — `0.01 GB`
    - `C:\Users\HP\Desktop\Денис документы для военкомата` — `0.00 GB`
    - `C:\Users\HP\Desktop\04_Веб_Прототипы` — `0.00 GB`
    - `C:\Users\HP\Desktop\00_Ярлыки` — `0.00 GB`
- Recommended delete-review candidates:
  - `C:\Users\HP\Downloads\Зинченко_Ольга_Викторовна_1521`
  - `C:\Users\HP\Downloads\wps_download`
  - `C:\Users\HP\Downloads\Telegram Desktop`
- Risk flags:
  - drive `C:` remains below the `10 GB` free-space threshold after safe cleanup
  - temp cleanup removed stale items, but active applications refilled `%TEMP%` during the run
  - meaningful recovery now requires manual review of user-owned folders, especially in `Downloads`

## 2026-04-29 21:13:16 +03:00

- Before C:: `214.49 GB used / 8.53 GB free`
- After C:: `214.49 GB used / 8.53 GB free`
- Delta free space: `+0.00 GB` (`0.00 MB` net change after safe cleanup)
- Safe cleanup performed:
  - `C:\Users\HP\AppData\Local\Temp`: removed `1` stale item; `14` locked/in-use deletions skipped
  - `C:\Windows\Temp`: no stale items removed
  - Recycle Bin: `Clear-RecycleBin` did not complete cleanly
  - Project-local pip cache: not present in `C:\Users\HP\Desktop\Новая папка`
- Desktop hygiene:
  - confirmed category folders exist: `00_Ярлыки`, `01_Документы`, `02_Таблицы`, `03_Изображения`, `04_Веб_Прототипы`, `05_Текст_Заметки`, `06_Разное`
  - no loose user files needed moving
  - left existing project/work folders in place
- Large-folder triage because free space is below `10 GB`:
  - Downloads top folders:
    - `C:\Users\HP\Downloads\Зинченко_Ольга_Викторовна_1521` — `0.52 GB`
    - `C:\Users\HP\Downloads\wps_download` — `0.24 GB`
    - `C:\Users\HP\Downloads\Telegram Desktop` — `0.02 GB`
    - `C:\Users\HP\Downloads\соп админ` — `0.01 GB`
    - `C:\Users\HP\Downloads\Antigravity_Unlocker-1.23.2` — `0.01 GB`
    - `C:\Users\HP\Downloads\The Elder Scrolls V Skyrim Special Edition by xatab` — `0.00 GB`
    - `C:\Users\HP\Downloads\Metro 2033 Redux` — `0.00 GB`
  - Desktop top folders:
    - `C:\Users\HP\Desktop\Новая папка` — `0.20 GB`
    - `C:\Users\HP\Desktop\папины фото с тел` — `0.07 GB`
    - `C:\Users\HP\Desktop\справка ндфл` — `0.04 GB`
    - `C:\Users\HP\Desktop\Codex` — `0.03 GB`
    - `C:\Users\HP\Desktop\дипломная работа` — `0.02 GB`
    - `C:\Users\HP\Desktop\03_Изображения` — `0.02 GB`
    - `C:\Users\HP\Desktop\01_Документы` — `0.01 GB`
    - `C:\Users\HP\Desktop\скан дядя Женя` — `0.00 GB`
    - `C:\Users\HP\Desktop\00_Ярлыки` — `0.00 GB`
    - `C:\Users\HP\Desktop\Денис документы для военкомата` — `0.00 GB`
- Recommended delete-review candidates:
  - `C:\Users\HP\Downloads\Академия Эксперт BIO_часть 2.7z.crdownload` — `13.00 GB` incomplete download file
  - `C:\Users\HP\Downloads\Академия Эксперт BIO_часть 1.7z.crdownload` — `11.47 GB` incomplete download file
  - `C:\Users\HP\Downloads\Зинченко_Ольга_Викторовна_1521`
  - `C:\Users\HP\Downloads\wps_download`
  - `C:\Users\HP\Downloads\Telegram Desktop`
- Risk flags:
  - drive `C:` remains below the `10 GB` free-space threshold after safe cleanup
  - `%TEMP%` still contains locked items that were skipped safely
  - Recycle Bin may still contain locked or protected items
  - the biggest immediate recovery opportunity is manual review of the two `.crdownload` files in `Downloads`

## 2026-05-01 09:17:53 +03:00

- Before C:: `220.38 GB used / 2.68 GB free`
- After C:: `220.38 GB used / 2.68 GB free`
- Delta free space: `+0.00 GB` (`0.00 MB` net change after safe cleanup)
- Safe cleanup performed:
  - `C:\Users\HP\AppData\Local\Temp`: no stale items removed; `26` locked/in-use deletions skipped
  - `C:\Windows\Temp`: no stale items removed
  - Recycle Bin: confirmed empty before and after cleanup, although `Clear-RecycleBin` returned a path error
  - Project-local pip cache: not present in `C:\Users\HP\Desktop\Новая папка`
- Desktop hygiene:
  - confirmed category folders exist: `00_Ярлыки`, `01_Документы`, `02_Таблицы`, `03_Изображения`, `04_Веб_Прототипы`, `05_Текст_Заметки`, `06_Разное`
  - no loose user files needed moving
  - left existing project/work folders in place
- Large-folder triage because free space is below `10 GB`:
  - Downloads top folders:
    - `C:\Users\HP\Downloads\Зинченко_Ольга_Викторовна_1521` — `0.52 GB`
    - `C:\Users\HP\Downloads\wps_download` — `0.24 GB`
    - `C:\Users\HP\Downloads\Telegram Desktop` — `0.02 GB`
    - `C:\Users\HP\Downloads\соп админ` — `0.01 GB`
    - `C:\Users\HP\Downloads\Antigravity_Unlocker-1.23.2` — `0.01 GB`
    - `C:\Users\HP\Downloads\The Elder Scrolls V Skyrim Special Edition by xatab` — `0.00 GB`
    - `C:\Users\HP\Downloads\Metro 2033 Redux` — `0.00 GB`
  - Desktop top folders:
    - `C:\Users\HP\Desktop\Новая папка` — `0.20 GB`
    - `C:\Users\HP\Desktop\папины фото с тел` — `0.07 GB`
    - `C:\Users\HP\Desktop\справка ндфл` — `0.04 GB`
    - `C:\Users\HP\Desktop\Codex` — `0.04 GB`
    - `C:\Users\HP\Desktop\03_Изображения` — `0.02 GB`
    - `C:\Users\HP\Desktop\дипломная работа` — `0.02 GB`
    - `C:\Users\HP\Desktop\01_Документы` — `0.01 GB`
    - `C:\Users\HP\Desktop\Денис документы для военкомата` — `0.00 GB`
    - `C:\Users\HP\Desktop\04_Веб_Прототипы` — `0.00 GB`
    - `C:\Users\HP\Desktop\00_Ярлыки` — `0.00 GB`
- Recommended delete-review candidates:
  - `C:\Users\HP\Downloads\Академия Эксперт BIO_часть 2.7z.crdownload` — `13.00 GB` incomplete download file
  - `C:\Users\HP\Downloads\Академия Эксперт BIO_часть 1.7z.crdownload` — `11.47 GB` incomplete download file
  - `C:\Users\HP\Downloads\Зинченко_Ольга_Викторовна_1521`
  - `C:\Users\HP\Downloads\wps_download`
  - `C:\Users\HP\Downloads\Telegram Desktop`
- Risk flags:
  - drive `C:` remains below the `10 GB` free-space threshold after safe cleanup
  - `%TEMP%` still contains locked items that were skipped safely
  - `Clear-RecycleBin` returned a path error even though the Recycle Bin was empty before and after verification
  - the biggest immediate recovery opportunity is manual review of the two `.crdownload` files in `Downloads`

## 2026-05-01 10:20:00 +03:00

- Before C:: 220.51 GB used / 2.51 GB free
- After C:: $usedGb GB used / 26.98 GB free
- Delta free space: approximately +24.47 GB
- Safe cleanup performed:
  - Deleted two old incomplete Chrome download files from C:\Users\HP\Downloads:
    - Академия Эксперт BIO_часть 2.7z.crdownload — 13.00 GB, last modified 2026-04-25 00:51
    - Академия Эксперт BIO_часть 1.7z.crdownload — 11.47 GB, last modified 2026-04-25 00:51
- Safety notes:
  - No project code, .env, tokens, client analyses, WellnessBot/data, PDF/photo uploads, or runtime data were deleted.
  - Paths were resolved and verified inside C:\Users\HP\Downloads before deletion.
- Result:
  - Disk C: is back above the 10 GB safety floor.

## 2026-05-01 21:18:59 +03:00

- Before C:: `198.44 GB used / 24.58 GB free`
- After C:: `198.44 GB used / 24.58 GB free`
- Delta free space: `-0.00 GB` (`-0.06 MB`, background disk activity outweighed cleanup)
- Safe cleanup performed:
  - `C:\Users\HP\AppData\Local\Temp`: no stale items removed; `26` locked/in-use deletions skipped
  - `C:\Windows\Temp`: no stale items removed
  - Recycle Bin: confirmed empty before and after cleanup, although `Clear-RecycleBin` returned a path error
  - Project-local pip cache: not present in `C:\Users\HP\Desktop\Новая папка`
- Desktop hygiene:
  - confirmed category folders exist: `00_Ярлыки`, `01_Документы`, `02_Таблицы`, `03_Изображения`, `04_Веб_Прототипы`, `05_Текст_Заметки`, `06_Разное`
  - moved loose file `Новая` into `C:\Users\HP\Desktop\06_Разное\Новая (1)` because `Новая` already existed there
  - left existing project/work folders in place
- Risk flags:
  - `%TEMP%` still contains locked items that were skipped safely
  - `Clear-RecycleBin` returned a path error even though the Recycle Bin was empty before and after verification
  - free space is above the `10 GB` escalation threshold, so no large-folder triage was required

## 2026-05-02 09:20:29 +03:00

- Before C:: `200.01 GB used / 23.01 GB free`
- After C:: `200.01 GB used / 23.00 GB free`
- Delta free space: `0.00 GB` (`-1.48 MB`, background disk activity outweighed cleanup)
- Safe cleanup performed:
  - `C:\Users\HP\AppData\Local\Temp`: no stale items removed; `14` locked/in-use deletions skipped
  - `C:\Windows\Temp`: no stale items removed
  - Recycle Bin: confirmed empty before and after cleanup, although `Clear-RecycleBin` returned a path error
  - Project-local pip cache: not present in `C:\Users\HP\Desktop\Новая папка`
- Desktop hygiene:
  - confirmed category folders exist: `00_Ярлыки`, `01_Документы`, `02_Таблицы`, `03_Изображения`, `04_Веб_Прототипы`, `05_Текст_Заметки`, `06_Разное`
  - no loose user files needed moving
  - left existing project/work folders in place
- Risk flags:
  - `%TEMP%` still contains locked items that were skipped safely
  - `Clear-RecycleBin` returned a path error even though the Recycle Bin was empty before and after verification
  - free space is above the `10 GB` escalation threshold, so no large-folder triage was required

## 2026-05-02 21:22:34 +03:00

- Before C:: `199.57 GB used / 23.44 GB free`
- After C:: `199.57 GB used / 23.44 GB free`
- Delta free space: `0.00 GB` (`0.00 MB` net change after safe cleanup)
- Safe cleanup performed:
  - `C:\Users\HP\AppData\Local\Temp`: no stale items removed; `16` locked/in-use deletions skipped
  - `C:\Windows\Temp`: no stale items removed
  - Recycle Bin: confirmed empty before and after cleanup, although `Clear-RecycleBin` returned a path error
  - Project-local pip cache: not present in `C:\Users\HP\Desktop\Новая папка`
- Desktop hygiene:
  - confirmed category folders exist: `00_Ярлыки`, `01_Документы`, `02_Таблицы`, `03_Изображения`, `04_Веб_Прототипы`, `05_Текст_Заметки`, `06_Разное`
  - no loose user files needed moving
  - left existing project/work folders in place
- Risk flags:
  - `%TEMP%` still contains locked items that were skipped safely
  - `Clear-RecycleBin` returned a path error even though the Recycle Bin was empty before and after verification
  - free space is above the `10 GB` escalation threshold, so no large-folder triage was required
