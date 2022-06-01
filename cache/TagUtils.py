
def overlap(span, example):
    for opinion in example['opinions']:
        if opinion['from']==opinion['to']:
            continue

        if (span[0]<=int(opinion['from']) and int(opinion['from'])<span[1]) or (span[0]<int(opinion['to']) and int(opinion['to'])<=span[1]) or (int(opinion['from'])<=span[0] and span[1]<=int(opinion['to'])):
            return True
    
    return False


def idhead(span, example):
    for opinion in example['opinions']:
        if span[0]==int(opinion['from']):
            return True
            
    return False

from nltk.tokenize.util import string_span_tokenize
import nltk

def tag_example(example):
    text = example['text']
    tokens = []
    
    spans = list(string_span_tokenize(text, " "))
    ate_tags = []
    
    
    for span in spans:
#        print(f"overlap({span}, example) is {overlap(span, example)}")
        if overlap(span, example):
            aspectTerms = ""
            subtokens = nltk.wordpunct_tokenize(text[span[0]:span[1]])
            # tokens.extend(subtokens)
            
            subtokensLength = [len(subtoken) for subtoken in subtokens]
            
            subSpans = [(span[0]+sum(subtokensLength[:i]), span[0]+sum(subtokensLength[:i+1])) for i, subtoken in enumerate(subtokens)]
            
            for subSpan, subToken in zip(subSpans, subtokens):
                # print('subSpan', subSpan)
                if overlap(subSpan, example):
                    if idhead(subSpan, example):
                        ate_tags.append('B-ASP')
                        tokens.append(subToken)
                        aspectTerms+=subToken
                    else:
                        ate_tags.append('I-ASP')
                        tokens.append(subToken)
                        aspectTerms+=subToken
                else:
                    ate_tags.append('O')
                    tokens.append(subToken)

        else:
            subtokens = nltk.word_tokenize(text[span[0]:span[1]])
            tokens.extend(subtokens)
            ate_tags.extend(['O'] * len(subtokens))
            # print('O ', subtokens)
    
    # check aspect Integrity
    
    return {
        'tokens': tokens,
        'ate_tags': ate_tags
    }