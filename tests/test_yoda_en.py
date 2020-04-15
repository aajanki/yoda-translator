from yoda import YodaEn


y = YodaEn()


def test_en():
    assert y('You have become powerful.') == 'Powerful you have become.'
    assert y('I sense the dark side in you.') == 'The dark side in you I sense.'
