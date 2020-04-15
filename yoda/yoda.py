import sys
import plac
import spacy
from spacy.tokens.doc import Doc
from spacy.tokens.token import Token
from spacy.tokens.span import Span
from spacy.language import Language


class YodaTranslator():
    def __init__(self, spacy_model: Language):
        self.nlp = spacy_model
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
        subtree = self._find_child_dep(doc, ['obj', 'xcomp', 'obl', 'advmod',
                                             'acomp', 'dobj', 'attr'])
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

        if (subtree.left_edge.i > 0 and
            doc[0].pos_ != 'PROPN' and
            doc[0].text != 'I'):
            rest_text = rest_text[0].lower() + rest_text[1:]

        sep2 = ', ' if any(t.text == ',' for t in span[:-1]) else ' '
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


class YodaFi(YodaTranslator):
    def __init__(self):
        super().__init__(spacy.load('fi_experimental_web_md'))


class YodaEn(YodaTranslator):
    def __init__(self):
        super().__init__(spacy.load('en_core_web_sm'))


def main(lang: ('Language', 'option', 'g', str, ['en', 'fi']) = 'fi',
         filename: 'Input file, use - for stdin'='-'):

    if lang == 'fi':
        translate = YodaFi()
    elif lang == 'en':
        translate = YodaEn()
    else:
        print(f'Unknown language {lang}')
        sys.exit(1)

    inp = sys.stdin if filename == '-' else open(filename)
    print(translate(inp.read()))


if __name__ == '__main__':
    plac.call(main)
