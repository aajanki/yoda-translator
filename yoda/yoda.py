import spacy
from spacy.tokens.doc import Doc
from spacy.tokens.token import Token
from spacy.tokens.span import Span


class Yoda():
    def __init__(self):
        self.nlp = spacy.load('fi_experimental_web_md')
        self.nlp.add_pipe(self.nlp.create_pipe('sentencizer'))

    def __call__(self, text: str) -> str:
        """Reorder words in each sentence of text in XSV order.

        X is the object or other verb modifier.

        Object (obj):
        Lapset lukivat kirjaa. -> Kirjaa lapset lukivat.

        Oblique nominal (obl):
        Etsimme taskulampun kanssa. -> Taskulampun kanssa etsimme.

        Open clausal complement (xcomp):
        Oletin sinun muuttavan mieltäsi. -> Sinun mieltäsi muuttavan oletin.

        Adverbial modifier (advmod):
        Katsoin eilen. -> Eilen katsoin.

        """
        transformed = [self.reorder(self.nlp(sent.text))
                       for sent in self.nlp(text).sents]
        return self._join_with_spaces(transformed)

    def reorder(self, doc: Doc) -> str:
        subtree = self._find_child_dep(doc, ['obj', 'xcomp', 'obl', 'advmod'])
        return self._reorder_subtree(doc, subtree)

    def _reorder_subtree(self, doc: Doc, subtree: Token) -> str:
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

        if subtree.left_edge.i > 0 and doc[0].pos_ != 'PROPN':
            rest_text = rest_text[0].lower() + rest_text[1:]

        sep2 = ', ' if any(t.text[:-1] == ',' for t in span) else ' '
        return subtree_text + sep2 + rest_text

    def _find_child_dep(self, doc, deps):
        for t in doc:
            if t.dep_ == 'ROOT' and t.pos_ in ['VERB', 'AUX']:
                for child in t.children:
                    if child.dep_.split(':', 1)[0] in deps:
                        return child

                return None

        return None

    def _join_with_spaces(self, sentences):
        res = []
        needs_whitespace = False
        for s in sentences:
            if needs_whitespace and s and not s[0].isspace():
                res.append(' ')

            res.append(s)

            if s:
                needs_whitespace = not s[-1].isspace()

        return ''.join(res)


if __name__ == '__main__':
    import sys

    if len(sys.argv) >= 2:
        process = Yoda()
        print(process(open(sys.argv[1]).read()))
