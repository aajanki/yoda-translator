from yoda import Yoda


yoda = Yoda()


def test_reorder_empty():
    assert yoda('') == ''


def test_reorder_whitespace():
    assert yoda('\n\n ') == '\n\n '


def test_reorder_one_word():
    assert yoda('Tule') == 'Tule'


def test_reorder_object():
    assert (yoda('Laiha koira jahtasi raidallista kissaa.') ==
            'Raidallista kissaa laiha koira jahtasi.')

    assert (yoda('Tyttö tuijotti roskia äkäisesti.') ==
            'Roskia tyttö tuijotti äkäisesti.')

    assert (yoda('Pankki myönsi ison lainan pienyrittäjälle.') ==
            'Ison lainan pankki myönsi pienyrittäjälle.')

    assert (yoda('Eikö kukaan ajattele lapsia?') ==
            'Lapsia eikö kukaan ajattele?')

    assert (yoda('Ihmiset juhlivat voittoa.') ==
            'Voittoa ihmiset juhlivat.')


def test_reorder_object_with_relative_clause():
    assert (yoda('Laiha koira jahtasi raidallista kissaa, joka kiipesi puuhun.') ==
            'Raidallista kissaa, joka kiipesi puuhun, laiha koira jahtasi.')


def test_reorder_object_in_independent_clause():
    assert (yoda('Ihmiset kokoontuvat toreilla ja juhlivat voittoa.') ==
            'Toreilla ihmiset kokoontuvat ja juhlivat voittoa.')


def test_reorder_simple_sentences():
    simple_sentences = [
        'Talo on punainen.',
        'Asiat olivat paremmin.',
        'Miksi et ymmärrä?',
    ]

    for s in simple_sentences:
        assert yoda(s) == s


def test_reorder_proper_name():
    assert yoda('Niinistö piti puheen.') == 'Puheen Niinistö piti.'


def test_reorder_xcomp():
    assert (yoda('Pyysin sinua vastaamaan!') ==
            'Sinua vastaamaan pyysin!')

    assert (yoda('Hän yritti suorittaa tehtävää ilman suurempaa innostusta.') ==
            'Suorittaa tehtävää ilman suurempaa innostusta hän yritti.')


def test_reorder_advmod():
    assert yoda('Kävele varovasti!') == 'Varovasti kävele!'

    assert yoda('Avaimet katosivat eilen.') == 'Eilen avaimet katosivat.'


def test_reorder_start_with_advmod():
    s = 'Huomenna hän tulee'
    assert yoda(s) == s


def test_reorder_multiple_sentences():
    assert (yoda('Kalle kiipesi puuhun. Omenat kasvoivat puussa.') ==
            'Puuhun Kalle kiipesi. Puussa omenat kasvoivat.')


def test_reorder_multiple_sentences_whitespace():
    assert (yoda('Kalle kiipesi puuhun.\n\nOmenat kasvoivat puussa.') ==
            'Puuhun Kalle kiipesi.\n\nPuussa omenat kasvoivat.')
