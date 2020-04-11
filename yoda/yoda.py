import spacy
from spacy.tokens.doc import Doc
from spacy.tokens.token import Token


nlp = spacy.load('fi_experimental_web_md')


def reorder_osv(sentence: str) -> str:
    """Reorder the words in a sentence in the object-subject-verb order."""
    doc = nlp(sentence)
    obj = find_child_dep(doc, ['obj'])
    return reorder_subtree(doc, obj)


def reorder_xsv(sentence: str) -> str:
    """Reorder non-object complement to the verb as the first term.

    This is the "XSV order" where X is something else that the object.

    (obl)
    Etsimme taskulampun kanssa. -> Taskulampun kanssa etsimme.

    (xcomp)
    Oletin sinun muuttavan mieltäsi. -> Sinun mieltäsi muuttavan oletin.
    
    (advmod)
    Katsoin eilen. -> Eilen katsoin.
    """
    doc = nlp(sentence)
    subtree = find_child_dep(doc, ['xcomp', 'obl', 'advmod'])
    return reorder_subtree(doc, subtree)


def reorder_subtree(doc: Doc, subtree: Token) -> str:
    if subtree is None:
        return doc.text

    span = doc[subtree.left_edge.i : subtree.right_edge.i + 1]
    subtree_text = span.text
    subtree_text = subtree_text[0].upper() + subtree_text[1:]

    right_start_token = doc[subtree.right_edge.i+1]
    sep = '' if right_start_token.is_punct or right_start_token.is_quote else ' '
    rest_texts = [
        doc[:subtree.left_edge.i].text,
        doc[subtree.right_edge.i+1:].text
    ]
    rest_texts = [x for x in rest_texts if x]
    rest_text = sep.join(rest_texts)
    rest_text = rest_text[0].lower() + rest_text[1:]

    sep2 = ', ' if any(t.text == ',' for t in span) else ' '
    return subtree_text + sep2 + rest_text


def find_child_dep(doc, deps):
    for t in doc:
        if t.dep_ == 'ROOT':
            for child in t.children:
                if child.dep_.split(':', 1)[0] in deps:
                    return child

    return None
