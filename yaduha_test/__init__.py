from yaduha import Language, Sentence, VocabEntry
from pydantic import Field
from enum import Enum
from typing import Optional


class Tense(str, Enum):
    PRESENT = "present"
    PAST = "past"
    FUTURE = "future"


class NounCase(str, Enum):
    NOMINATIVE = "nom"  # subject
    ACCUSATIVE = "acc"  # object


# Core vocabulary
PRONOUNS = {
    "I": "ko",
    "you": "tu",
    "he": "li",
    "she": "li",
    "we": "kom",
    "they": "lim",
}

VERBS = {
    "sleep": "dorm",
    "run": "kur",
    "eat": "manj",
    "see": "vid",
    "speak": "parl",
    "love": "am",
    "want": "vol",
    "go": "ir",
}

NOUNS = {
    "cat": "kat",
    "dog": "hun",
    "bird": "av",
    "book": "libr",
    "water": "akv",
    "house": "dom",
    "food": "sib",
    "tree": "arb",
}


class Noun(Sentence):
    """A noun with case and number."""
    
    english: str = Field(description="The English word")
    plural: bool = Field(default=False, description="Whether the noun is plural")
    case: NounCase = Field(default=NounCase.NOMINATIVE, description="Grammatical case")
    
    def __str__(self) -> str:
        # Get the Testak root
        root = NOUNS.get(self.english, self.english)
        
        # Add case suffix
        if self.case == NounCase.ACCUSATIVE:
            root += "an"
        
        # Add plural suffix
        if self.plural:
            root += "es"
        
        return root
    
    @classmethod
    def get_examples(cls):
        return [
            ("cat", cls(english="cat")),
            ("cats", cls(english="cat", plural=True)),
            ("the dog (object)", cls(english="dog", case=NounCase.ACCUSATIVE)),
        ]


class IntransitiveSentence(Sentence):
    """A sentence with just a subject and verb (no object)."""
    
    subject: str = Field(description="The subject (pronoun)")
    verb: str = Field(description="The verb root")
    tense: Tense = Field(default=Tense.PRESENT, description="The tense")
    
    def __str__(self) -> str:
        # Get Testak words
        subj = PRONOUNS.get(self.subject, self.subject)
        verb_root = VERBS.get(self.verb, self.verb)
        
        # Add tense suffix to verb
        if self.tense == Tense.PAST:
            verb_root += "is"
        elif self.tense == Tense.FUTURE:
            verb_root += "os"
        # Present tense has no suffix
        
        # SOV word order: subject verb
        return f"{subj} {verb_root}"
    
    @classmethod
    def get_examples(cls):
        return [
            ("I sleep.", cls(subject="I", verb="sleep")),
            ("You run.", cls(subject="you", verb="run")),
            ("They slept.", cls(subject="they", verb="sleep", tense=Tense.PAST)),
            ("We will go.", cls(subject="we", verb="go", tense=Tense.FUTURE)),
        ]


class TransitiveSentence(Sentence):
    """A sentence with a subject, object, and verb."""
    
    subject: str = Field(description="The subject (pronoun)")
    object_noun: str = Field(description="The object noun")
    object_plural: bool = Field(default=False, description="Whether the object is plural")
    verb: str = Field(description="The verb root")
    tense: Tense = Field(default=Tense.PRESENT, description="The tense")
    
    def __str__(self) -> str:
        # Get Testak words
        subj = PRONOUNS.get(self.subject, self.subject)
        obj_root = NOUNS.get(self.object_noun, self.object_noun)
        verb_root = VERBS.get(self.verb, self.verb)
        
        # Object takes accusative case
        obj = obj_root + "an"
        if self.object_plural:
            obj += "es"
        
        # Add tense suffix to verb
        if self.tense == Tense.PAST:
            verb_root += "is"
        elif self.tense == Tense.FUTURE:
            verb_root += "os"
        
        # SOV word order: subject object verb
        return f"{subj} {obj} {verb_root}"
    
    @classmethod
    def get_examples(cls):
        return [
            ("I see a cat.", cls(subject="I", object_noun="cat", verb="see")),
            ("You eat food.", cls(subject="you", object_noun="food", verb="eat")),
            ("She loved the dog.", cls(subject="she", object_noun="dog", verb="love", tense=Tense.PAST)),
            ("We will see birds.", cls(subject="we", object_noun="bird", object_plural=True, verb="see", tense=Tense.FUTURE)),
            ("They ate books.", cls(subject="they", object_noun="book", object_plural=True, verb="eat", tense=Tense.PAST)),
        ]


class CopulaSentence(Sentence):
    """A sentence with 'to be' (copula): X is Y."""
    
    subject: str = Field(description="The subject")
    predicate: str = Field(description="What the subject is")
    predicate_plural: bool = Field(default=False, description="Whether predicate is plural")
    tense: Tense = Field(default=Tense.PRESENT, description="The tense")
    
    def __str__(self) -> str:
        # Get subject
        subj = PRONOUNS.get(self.subject, NOUNS.get(self.subject, self.subject))
        
        # Get predicate noun
        pred_root = NOUNS.get(self.predicate, self.predicate)
        if self.predicate_plural:
            pred_root += "es"
        
        # Copula "est" with tense
        copula = "est"
        if self.tense == Tense.PAST:
            copula = "estis"
        elif self.tense == Tense.FUTURE:
            copula = "estos"
        
        # Order: subject copula predicate
        return f"{subj} {copula} {pred_root}"
    
    @classmethod
    def get_examples(cls):
        return [
            ("I am a cat.", cls(subject="I", predicate="cat")),
            ("You were a bird.", cls(subject="you", predicate="bird", tense=Tense.PAST)),
            ("They will be dogs.", cls(subject="they", predicate="dog", predicate_plural=True, tense=Tense.FUTURE)),
        ]


language = Language(
    code="test",
    name="Testak",
    sentence_types=(
        Noun,
        IntransitiveSentence,
        TransitiveSentence,
        CopulaSentence,
    ),
)
