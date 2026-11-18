import pytest

from uz_translit import cyr_to_lat, normalize_latin, to_passport


@pytest.mark.parametrize(
    "cyr, lat",
    [
        ("Тошкент", "Toshkent"),
        ("ТОШКЕНТ", "TOSHKENT"),
        ("Ўзбекистон", "Oʻzbekiston"),
        ("Ғулом", "Gʻulom"),
        ("Қодирова", "Qodirova"),
        ("Ҳамидов", "Hamidov"),
        ("Хўжаев", "Xoʻjayev"),
        ("Шоимов", "Shoimov"),
        ("ШОИМОВ", "SHOIMOV"),
        ("Чиноз", "Chinoz"),
        ("Ёқубов", "Yoqubov"),
        ("Юсупова", "Yusupova"),
        ("Яккасарой", "Yakkasaroy"),
        ("Евгений", "Yevgeniy"),
        ("Алиев", "Aliyev"),
        ("эшик", "eshik"),
        ("маъно", "maʼno"),
        ("цирк", "sirk"),
        ("милиция", "militsiya"),
        ("Қўштепа тумани", "Qoʻshtepa tumani"),
        ("2026-йил 18-ноябрь", "2026-yil 18-noyabr"),
    ],
)
def test_cyr_to_lat(cyr, lat):
    assert cyr_to_lat(cyr) == lat


@pytest.mark.parametrize(
    "raw",
    ["O'zbekiston", "O`zbekiston", "O’zbekiston", "O‘zbekiston", "Oʼzbekiston", "Oʻzbekiston"],
)
def test_normalize_apostrophe_variants(raw):
    assert normalize_latin(raw) == "Oʻzbekiston"


def test_normalize_tutuq():
    assert normalize_latin("ma'no") == "maʼno"


@pytest.mark.parametrize(
    "src, passport",
    [
        ("Qodirova", "KODIROVA"),
        ("Qo'shtepa", "KOSHTEPA"),
        ("Қўштепа", "KOSHTEPA"),
        ("Xo'jayev", "KHOJAYEV"),
        ("Хўжаев", "KHOJAYEV"),
        ("G'ulomov", "GULOMOV"),
        ("Shoimov", "SHOIMOV"),
        ("Hamidov", "HAMIDOV"),
        ("Yo'ldosheva", "YOLDOSHEVA"),
        ("Ёқубов", "YOKUBOV"),
        ("Ma'rufjon", "MARUFJON"),
        ("Toshkent shahri", "TOSHKENT SHAHRI"),
        ("Qashqadaryo viloyati", "KASHKADARYO VILOYATI"),
    ],
)
def test_to_passport(src, passport):
    assert to_passport(src) == passport


def test_latin_and_cyrillic_give_same_passport_form():
    assert to_passport("Xudoyberdiyev") == to_passport("Худойбердиев") == "KHUDOYBERDIYEV"
