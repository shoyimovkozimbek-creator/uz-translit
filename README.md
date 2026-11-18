# uz-translit

Uzbek Cyrillic ↔ Latin transliteration and **passport-style romanisation** of Uzbek names, addresses and places.

```python
from uz_translit import cyr_to_lat, to_passport

cyr_to_lat("Қўштепа тумани")   # 'Qoʻshtepa tumani'
to_passport("Qodirova")         # 'KODIROVA'
to_passport("Хўжаев")           # 'KHOJAYEV'
to_passport("Qo'shtepa")        # 'KOSHTEPA'
```

## Why

Uzbek is written in two scripts, and Latin Uzbek is typed with at least six different apostrophes
(`o'`, `` o` ``, `o’`, `o‘`, `oʼ`, `oʻ`). On top of that, passports and international forms do not use
Uzbek Latin as is: `q` becomes `K`, `x` becomes `KH`, and the `ʻ` marks disappear.

Visa agencies, HR systems, banks and booking forms in Uzbekistan each re-implement these rules by hand,
and small mismatches (`QODIROVA` vs `KODIROVA`) cause rejected or delayed applications.
`uz-translit` puts the rules in one small, tested, dependency-free library.

## Install

```bash
pip install uz-translit          # once published on PyPI
# or, from source:
pip install git+https://github.com/shoyimovkozimbek-creator/uz-translit
```

Python 3.8+, no dependencies.

## API

| Function | What it does |
|---|---|
| `cyr_to_lat(text)` | Uzbek Cyrillic → official Uzbek Latin (1995 alphabet). Handles `е` → `ye` at word start and after vowels, `ц` → `s`/`ts`, `ъ` → `ʼ`, and keeps the case of words (`ШОИМОВ` → `SHOIMOV`, `Шоимов` → `Shoimov`). |
| `normalize_latin(text)` | Turns every apostrophe variant into the official `ʻ` (after `o`/`g`) or `ʼ` (tutuq). |
| `to_passport(text)` | Cyrillic or Latin → upper-case passport form: `oʻ`→`O`, `gʻ`→`G`, `q`→`K`, `x`→`KH`, tutuq dropped. |

## Passport rules used

| Uzbek | Passport | Example |
|---|---|---|
| `q` / `қ` | `K` | Qodirova → KODIROVA |
| `x` / `х` | `KH` | Xudoyberdiyev → KHUDOYBERDIYEV |
| `h` / `ҳ` | `H` | Hamidov → HAMIDOV |
| `oʻ` / `ў` | `O` | Yoʻldosheva → YOLDOSHEVA |
| `gʻ` / `ғ` | `G` | Gʻulomov → GULOMOV |
| `ʼ` / `ъ` | — | Maʼrufjon → MARUFJON |

**Always prefer the spelling already printed in the person's passport.** Older passports sometimes use
Russian-era spellings (`DJURAEV`, `ZHURAEV`). Use `to_passport` for relatives, addresses, districts and
organisation names that have no official romanisation yet, so that every document in an application
spells them the same way.

## Roadmap

- npm package with the same API
- Latin → Cyrillic
- optional Russian-era passport variants (`DJ`, `ZH`, `-EV` without `Y`)
- a larger test set of real-world names and all district names of Uzbekistan

Contributions and edge cases are welcome — open an issue with the input, the expected output and where
that spelling comes from.

---

## Oʻzbekcha qisqacha

Kutubxona oʻzbekcha matnni kirilldan lotinga oʻgiradi va ism, familiya, manzillarni pasport/viza
anketasidagi shaklga keltiradi: `Qodirova` → `KODIROVA`, `Xoʻjayev` → `KHOJAYEV`.
Pasportda yozilgan shakl boʻlsa — doim oʻshanisi ishlatiladi.

## License

MIT
