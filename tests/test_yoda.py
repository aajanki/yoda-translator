from yoda.yoda import reorder_osv, reorder_xsv


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
    assert reorder_osv('') == ''


def test_reorder_one_word():
    assert reorder_osv('Tule') == 'Tule'


def test_reorder_osv():
    assert (reorder_osv('Vikkelä koira jahtasi raidallista kissaa.') ==
            'Raidallista kissaa vikkelä koira jahtasi.')

    assert (reorder_osv('Tyttö tuijotti roskia äkäisesti.') ==
            'Roskia tyttö tuijotti äkäisesti.')

    assert (reorder_osv('Pankki myönsi ison lainan pienyrittäjälle.') ==
            'Ison lainan pankki myönsi pienyrittäjälle.')

    assert (reorder_osv('Eikö kukaan ajattele lapsia?') ==
            'Lapsia eikö kukaan ajattele?')

    assert (reorder_osv('Ihmiset juhlivat voittoa.') ==
            'Voittoa ihmiset juhlivat.')


def test_reorder_osv_object_with_relative_clause():
    assert (reorder_osv('Vikkelä koira jahtasi raidallista kissaa, joka kiipesi puuhun.') ==
            'Raidallista kissaa, joka kiipesi puuhun, vikkelä koira jahtasi.')


def test_reorder_osv_object_in_independent_clause():
    s = 'Ihmiset kokoontuvat toreilla ja juhlivat voittoa.'
    assert reorder_osv(s) == s


def test_reorder_osv_simple_sentences():
    for s in simple_sentences:
        assert reorder_osv(s) == s


def test_reorder_osv_no_change_without_object():
    for s in sentences_without_object:
        assert reorder_osv(s) == s


def test_reorder_xsv_xcomp():
    assert (reorder_xsv('Pyysin sinua vastaamaan!') ==
            'Sinua vastaamaan pyysin!')

    assert (reorder_xsv('Hän yritti suorittaa tehtävää ilman suurempaa innostusta.') ==
            'Suorittaa tehtävää ilman suurempaa innostusta hän yritti.')


def test_reorder_xsv_advmod():
    assert reorder_xsv('Etene varovasti!') == 'Varovasti etene!'
    
    assert (reorder_xsv('Avaimet olivat kadoksissa eilen.') ==
            'Eilen avaimet olivat kadoksissa.')


def test_reorder_xsv_start_with_advmod():
    s = 'Huomenna hän tulee'
    assert reorder_xsv(s) == s


def test_reoder_xsv_simple_sentences():
    for s in simple_sentences:
        assert reorder_osv(s) == s
