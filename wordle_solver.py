import sys
import random
from collections import defaultdict

FIRST_WORD = 'orate'

class Rule:
    def __init__(self, letter, i=None):
        self.letter, self.i = letter, i


class RuleMatch(Rule):
    code = '='
    def apply(self, words, matched_counts):
        words = [word for word in words if word[self.i] == self.letter]
        return words


class RuleContainsElsewhere(Rule):
    code = '+'
    def apply(self, words, matched_counts):
        # Only keep words which contain letter (not in position i, or else
        # it would be an exact match (= not +) and which don't contain the
        # letter more often than the number of counted matches.
        words = [word for word in words if self.letter in word
                    and word[self.i] != self.letter
                    and matched_counts[self.letter] <= word.count(self.letter)]
        return words


class RuleExcludedLetter(Rule):
    code = '-'
    def apply(self, words, matched_counts):
        _words = []
        for word in words:
            if not matched_counts[self.letter] and self.letter in word:
                # letter has not been matched anywhere in the word:
                # don't include any words which have this letter.
                continue
            if matched_counts[self.letter] > word.count(self.letter):
                # letter has been matched n times: we can't include
                # words that don't include it at least as many times.
                continue
            _words.append(word)
        words = _words[:]
        return words

RuleCls = {'=': RuleMatch, '+': RuleContainsElsewhere, '-': RuleExcludedLetter}


class Wordle:
    def __init__(self, target_word=None, word_length=5):
        self.target_word = target_word
        self.word_length = word_length
        if target_word:
            self.word_length = len(target_word)

        #self.wordlist_name = 'sowpods.txt'
        # Uncomment the line below to use only the most common 5-letter words.
        #self.wordlist_name = 'common-5-words.txt'
        self.wordlist_name = '5-words.txt'
        self.read_words()

    def read_words(self):
        """Read in words of length word_length from our word list."""

        with open(self.wordlist_name) as fi:
            # NB the inclusion of the end-of-line character (which we
            # subsequently strip) increases the target word length by one.
            self.words = [word.strip() for word in fi
                                    if len(word) == self.word_length + 1]


    def assess_word(self, test_word):

        target = list(self.target_word)
        matched_counts = defaultdict(int)
        rules = [None] * self.word_length
        # Test test_word for the "exact match" and "excluded letter" rules.
        for i, letter in enumerate(test_word):
            if letter == target[i]:
                rules[i] = RuleMatch(letter, i)
                target[i] = '*'
                matched_counts[letter] += 1
            elif letter not in target:
                rules[i] = RuleExcludedLetter(letter, i)

        for i, letter in enumerate(test_word):
            if rules[i]:
                continue
            if letter in target:
                # NB exact matches have already been filtered out.
                rules[i] = RuleContainsElsewhere(letter, i)
                target[target.index(letter)] = '*'
                matched_counts[letter] += 1
            else:
                rules[i] = RuleExcludedLetter(letter, i)

        rule_str = ''.join(rule.code for rule in rules)
        return rules, matched_counts, rule_str


    def parse_rule_codes(self, rule_codes, test_word):
        rules = []
        matched_counts = defaultdict(int)
        for i, letter in enumerate(test_word):
            rules.append(RuleCls[rule_codes[i]](letter, i))
            if rule_codes[i] in '+=':
                matched_counts[letter] += 1
        return rules, matched_counts

    def apply_rules(self, rules, matched_counts):
        for rule in rules:
            self.words = rule.apply(self.words, matched_counts)
            
    def symbol_generation(self,test_word):
        target=list(self.target_word)
        test=list(test_word)
        symbols=[None]*5
        flag=[0]*5
      
        
        for i in range(0,5):
            if test[i] in target:
                if test[i]==target[i]:
                    symbols[i]='='
                    target[i]=None
                    flag[i]=1
        
        for i in range(0,5):
            if test[i] not in target and flag[i]==0:
                symbols[i]='-'       
                flag[i] = 1

        
        for i in range(0,5):             
            if test[i] in target and flag[i]==0:
                symbols[i]='+'
                
                target[target.index(test[i])]=None
                flag[i] = 1
        
        for i in range(0,5):
            if test[i] not in target and flag[i]==0:
                symbols[i]='-'        

        return ''.join(symbols)


    def get_test_word(self):
        k = random.choice(range(len(self.words)))
        return self.words[k], k
    
    def get_rules_input(self, test_word):
        
        print('Try the word ',test_word)
        print(self.symbol_generation(test_word))
        return self.symbol_generation(test_word)
#         return input(f'Try the word "{test_word}": ')
    
    def interactive(self):
        j = 0
        init = FIRST_WORD, self.words.index(FIRST_WORD)
        while len(self.words) > 1:
            test_word, k = self.get_test_word() if j else init
            j += 1
            rule_codes = self.get_rules_input(test_word)
            rules, matched_counts = self.parse_rule_codes(rule_codes,test_word)
            self.apply_rules(rules, matched_counts)

            if len(self.words) == 0:
                sys.exit('I think you made a mistake: no words match this set'
                         ' of rules.')
            elif len(self.words) == 1:
                break
            if test_word in self.words:
                del self.words[self.words.index(test_word)]
        print(f'The word is {self.words[0]}, found in {j+1} attempts.')
        
    
        


    