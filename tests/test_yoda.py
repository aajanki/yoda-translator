from yoda import Yoda


yoda = Yoda()

simple_sentences = [
    'Talo on punainen.',
    'Asiat olivat paremmin.',
]

sentences_without_object = [
    'Eduskunnan rooli tässä työssä on tärkeä.',
    'Ainakin neljä uhkatekijää nousee heti esiin.',
    'Miksi et ymmärrä?',
    'Tule nopeasti!',
]


def test_reorder_empty():
    assert yoda('') == ''


def test_reorder_whitespace():
    assert yoda('\n\n ') == '\n\n '


def test_reorder_one_word():
    assert yoda('Tule') == 'Tule'


def test_reorder_osv():
    assert (yoda.reorder_osv('Vikkelä koira jahtasi raidallista kissaa.') ==
            'Raidallista kissaa vikkelä koira jahtasi.')

    assert (yoda.reorder_osv('Tyttö tuijotti roskia äkäisesti.') ==
            'Roskia tyttö tuijotti äkäisesti.')

    assert (yoda.reorder_osv('Pankki myönsi ison lainan pienyrittäjälle.') ==
            'Ison lainan pankki myönsi pienyrittäjälle.')

    assert (yoda.reorder_osv('Eikö kukaan ajattele lapsia?') ==
            'Lapsia eikö kukaan ajattele?')

    assert (yoda.reorder_osv('Ihmiset juhlivat voittoa.') ==
            'Voittoa ihmiset juhlivat.')


def test_reorder_osv_object_with_relative_clause():
    assert (yoda.reorder_osv('Vikkelä koira jahtasi raidallista kissaa, joka kiipesi puuhun.') ==
            'Raidallista kissaa, joka kiipesi puuhun, vikkelä koira jahtasi.')


def test_reorder_osv_object_in_independent_clause():
    s = 'Ihmiset kokoontuvat toreilla ja juhlivat voittoa.'
    assert yoda.reorder_osv(s) == s


def test_reorder_osv_simple_sentences():
    for s in simple_sentences:
        assert yoda.reorder_osv(s) == s


def test_reorder_osv_no_change_without_object():
    for s in sentences_without_object:
        assert yoda.reorder_osv(s) == s


def test_reorder_osv_proper_name():
    assert yoda.reorder_osv('Niinistö piti puheen.') == 'Puheen Niinistö piti.'


def test_reorder_xsv_xcomp():
    assert (yoda.reorder_xsv('Pyysin sinua vastaamaan!') ==
            'Sinua vastaamaan pyysin!')

    assert (yoda.reorder_xsv('Hän yritti suorittaa tehtävää ilman suurempaa innostusta.') ==
            'Suorittaa tehtävää ilman suurempaa innostusta hän yritti.')


def test_reorder_xsv_advmod():
    assert yoda.reorder_xsv('Etene varovasti!') == 'Varovasti etene!'
    
    assert (yoda.reorder_xsv('Avaimet olivat kadoksissa eilen.') ==
            'Eilen avaimet olivat kadoksissa.')


def test_reorder_xsv_start_with_advmod():
    s = 'Huomenna hän tulee'
    assert yoda.reorder_xsv(s) == s


def test_reorder_xsv_simple_sentences():
    for s in simple_sentences:
        assert yoda.reorder_osv(s) == s


def test_reorder_multiple_sentences():
    assert (yoda('Kalle kiipesi puuhun. Omenat kasvoivat puussa.') ==
            'Puuhun Kalle kiipesi. Puussa omenat kasvoivat.')


def test_reorder_multiple_sentences_whitespace():
    assert (yoda('Kalle kiipesi puuhun.\n\nOmenat kasvoivat puussa.') ==
            'Puuhun Kalle kiipesi.\n\nPuussa omenat kasvoivat.')
