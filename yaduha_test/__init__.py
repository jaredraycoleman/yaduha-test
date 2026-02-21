from yaduha import Language, Sentence
from pydantic import Field
from enum import Enum


class Tense(str, Enum):
    PRESENT = "present"
    PAST = "past"
    FUTURE = "future"


class NounCase(str, Enum):
    NOMINATIVE = "nom"
    ACCUSATIVE = "acc"


# Testak vocabulary
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
        root = NOUNS.get(self.english, self.english)
        if self.case == NounCase.ACCUSATIVE:
            root += "an"
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
    """A sentence with just a subject and verb."""
    
    subject: str = Field(description="The subject (pronoun)")
    verb: str = Field(description="The verb root")
    tense: Tense = Field(default=Tense.PRESENT, description="The tense")
    
    def __str__(self) -> str:
        subj = PRONOUNS.get(self.subject, self.subject)
        verb_root = VERBS.get(self.verb, self.verb)
        if self.tense == Tense.PAST:
            verb_root += "is"
        elif self.tense == Tense.FUTURE:
            verb_root += "os"
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
    """A sentence with subject, object, and verb."""
    
    subject: str = Field(description="The subject (pronoun)")
    object_noun: str = Field(description="The object noun")
    object_plural: bool = Field(default=False, description="Whether the object is plural")
    verb: str = Field(description="The verb root")
    tense: Tense = Field(default=Tense.PRESENT, description="The tense")
    
    def __str__(self) -> str:
        subj = PRONOUNS.get(self.subject, self.subject)
        obj_root = NOUNS.get(self.object_noun, self.object_noun)
        verb_root = VERBS.get(self.verb, self.verb)
        obj = obj_root + "an"
        if self.object_plural:
            obj += "es"
        if self.tense == Tense.PAST:
            verb_root += "is"
        elif self.tense == Tense.FUTURE:
            verb_root += "os"
        return f"{subj} {obj} {verb_root}"
    
    @classmethod
    def get_examples(cls):
        return [
            ("I see a cat.", cls(subject="I", object_noun="cat", verb="see")),
            ("You eat food.", cls(subject="you", object_noun="food", verb="eat")),
            ("She loved the dog.", cls(subject="she", object_noun="dog", verb="love", tense=Tense.PAST)),
            ("We will see birds.", cls(subject="we", object_noun="bird", object_plural=True, verb="see", tense=Tense.FUTURE)),
        ]


class CopulaSentence(Sentence):
    """A sentence with 'to be' copula."""
    
    subject: str = Field(description="The subject")
    predicate: str = Field(description="What the subject is")
    predicate_plural: bool = Field(default=False, description="Whether predicate is plural")
    tense: Tense = Field(default=Tense.PRESENT, description="The tense")
    
    def __str__(self) -> str:
        subj = PRONOUNS.get(self.subject, NOUNS.get(self.subject, self.subject))
        pred_root = NOUNS.get(self.predicate, self.predicate)
        if self.predicate_plural:
            pred_root += "es"
        copula = "est"
        if self.tense == Tense.PAST:
            copula = "estis"
        elif self.tense == Tense.FUTURE:
            copula = "estos"
        return f"{subj} {copula} {pred_root}"
    
    @classmethod
    def get_examples(cls):
        return [
            ("I am a cat.", cls(subject="I", predicate="cat")),
            ("You were a bird.", cls(subject="you", predicate="bird", tense=Tense.PAST)),
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
