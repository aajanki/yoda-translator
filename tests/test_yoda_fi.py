from yoda import YodaFi


y = YodaFi()


def test_reorder_empty():
    assert y('') == ''


def test_reorder_whitespace():
    assert y('\n\n ') == '\n\n '


def test_reorder_one_word():
    assert y('Tule') == 'Tule'


def test_reorder_object():
    assert (y('Laiha koira jahtasi raidallista kissaa.') ==
            'Raidallista kissaa laiha koira jahtasi.')

    assert (y('Tyttö tuijotti roskia äkäisesti.') ==
            'Roskia tyttö tuijotti äkäisesti.')

    assert (y('Pankki myönsi ison lainan pienyrittäjälle.') ==
            'Ison lainan pankki myönsi pienyrittäjälle.')

    assert (y('Eikö kukaan ajattele lapsia?') ==
            'Lapsia eikö kukaan ajattele?')

    assert (y('Ihmiset juhlivat voittoa.') ==
            'Voittoa ihmiset juhlivat.')


def test_reorder_object_with_relative_clause():
    assert (y('Laiha koira jahtasi raidallista kissaa, joka kiipesi puuhun.') ==
            'Raidallista kissaa, joka kiipesi puuhun, laiha koira jahtasi.')


def test_reorder_object_in_independent_clause():
    assert (y('Ihmiset kokoontuvat toreilla ja juhlivat voittoa.') ==
            'Toreilla ihmiset kokoontuvat ja juhlivat voittoa.')


def test_reorder_simple_sentences():
    simple_sentences = [
        'Talo on punainen.',
        'Asiat olivat paremmin.',
        'Miksi et ymmärrä?',
    ]

    for s in simple_sentences:
        assert y(s) == s


def test_reorder_proper_name():
    assert y('Niinistö piti puheen.') == 'Puheen Niinistö piti.'


def test_reorder_xcomp():
    assert (y('Pyysin sinua vastaamaan!') ==
            'Sinua vastaamaan pyysin!')

    assert (y('Hän yritti suorittaa tehtävää ilman suurempaa innostusta.') ==
            'Suorittaa tehtävää ilman suurempaa innostusta hän yritti.')


def test_reorder_advmod():
    assert y('Kävele varovasti!') == 'Varovasti kävele!'

    assert y('Avaimet katosivat eilen.') == 'Eilen avaimet katosivat.'


def test_reorder_start_with_advmod():
    s = 'Huomenna hän tulee'
    assert y(s) == s


def test_reorder_multiple_sentences():
    assert (y('Kalle kiipesi puuhun. Omenat kasvoivat puussa.') ==
            'Puuhun Kalle kiipesi. Puussa omenat kasvoivat.')


def test_reorder_multiple_sentences_whitespace():
    assert (y('Kalle kiipesi puuhun.\n\nOmenat kasvoivat puussa.') ==
            'Puuhun Kalle kiipesi.\n\nPuussa omenat kasvoivat.')
