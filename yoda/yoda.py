import spacy


nlp = spacy.load('fi_experimental_web_md')


def reorder_osv(sentence: str) -> str:
    """Reorder the words in a sentence in the object-subject-verb order."""

    doc = nlp(sentence)
    obj = find_obj(doc)
    if obj is None:
        return sentence

    obj_span = doc[obj.left_edge.i : obj.right_edge.i + 1]
    obj_text = obj_span.text
    obj_text = obj_text[0].upper() + obj_text[1:]

    right_start_token = doc[obj.right_edge.i+1]
    sep = '' if right_start_token.is_punct or right_start_token.is_quote else ' '
    rest_text = doc[:obj.left_edge.i].text + sep + doc[obj.right_edge.i+1:].text
    rest_text = rest_text[0].lower() + rest_text[1:]

    sep = ', ' if any(t.text == ',' for t in obj_span) else ' '
    return obj_text + sep + rest_text


def find_obj(doc):
    root = [t for t in doc if t.dep_ == 'ROOT']
    if not root:
        return None

    root = root[0]
    for t in root.children:
        if t.dep_ == 'obj':
            return t

    return None
