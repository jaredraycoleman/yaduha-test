from yaduha import Language, Sentence
from pydantic import Field
from enum import Enum
from typing import Optional


class Person(str, Enum):
    """Grammatical person"""
    FIRST = "first"
    SECOND = "second"
    THIRD = "third"


class Number(str, Enum):
    """Grammatical number"""
    SINGULAR = "singular"
    PLURAL = "plural"


class Tense(str, Enum):
    """Verb tense"""
    PRESENT = "present"
    PAST = "past"
    FUTURE = "future"


# Pronoun lookup table
PRONOUNS = {
    (Person.FIRST, Number.SINGULAR): "zo",
    (Person.SECOND, Number.SINGULAR): "te",
    (Person.THIRD, Number.SINGULAR): "ka",
    (Person.FIRST, Number.PLURAL): "pa",
    (Person.SECOND, Number.PLURAL): "tena",
    (Person.THIRD, Number.PLURAL): "ma",
}

# Tense suffixes
TENSE_SUFFIXES = {
    Tense.PRESENT: "is",
    Tense.PAST: "at",
    Tense.FUTURE: "um",
}


class IntransitiveSentence(Sentence):
    """A sentence with just a subject and verb (e.g., 'I sleep')"""
    
    person: Person = Field(description="Grammatical person of the subject")
    number: Number = Field(description="Singular or plural")
    verb_root: str = Field(description="The verb root (e.g., 'dorm' for sleep)")
    tense: Tense = Field(description="When the action occurs")

    def __str__(self) -> str:
        subject = PRONOUNS[(self.person, self.number)]
        verb = self.verb_root + TENSE_SUFFIXES[self.tense]
        return f"{subject} {verb}"

    @classmethod
    def get_examples(cls):
        return [
            ("I sleep.", cls(person=Person.FIRST, number=Number.SINGULAR, 
                           verb_root="dorm", tense=Tense.PRESENT)),
            ("You ran.", cls(person=Person.SECOND, number=Number.SINGULAR,
                           verb_root="kur", tense=Tense.PAST)),
            ("They will dance.", cls(person=Person.THIRD, number=Number.PLURAL,
                                    verb_root="dans", tense=Tense.FUTURE)),
        ]


class TransitiveSentence(Sentence):
    """A sentence with subject, object, and verb (SOV word order)"""
    
    subject_person: Person = Field(description="Grammatical person of the subject")
    subject_number: Number = Field(description="Subject number")
    object_noun: str = Field(description="The object being acted upon")
    verb_root: str = Field(description="The verb root")
    tense: Tense = Field(description="When the action occurs")

    def __str__(self) -> str:
        subject = PRONOUNS[(self.subject_person, self.subject_number)]
        obj = f"en {self.object_noun}"  # Object marker 'en'
        verb = self.verb_root + TENSE_SUFFIXES[self.tense]
        return f"{subject} {obj} {verb}"

    @classmethod
    def get_examples(cls):
        return [
            ("I see the dog.", cls(subject_person=Person.FIRST, subject_number=Number.SINGULAR,
                                  object_noun="hund", verb_root="vid", tense=Tense.PRESENT)),
            ("You ate food.", cls(subject_person=Person.SECOND, subject_number=Number.SINGULAR,
                                 object_noun="nurt", verb_root="et", tense=Tense.PAST)),
            ("We will build a house.", cls(subject_person=Person.FIRST, subject_number=Number.PLURAL,
                                          object_noun="dom", verb_root="bild", tense=Tense.FUTURE)),
        ]


class AdjectiveSentence(Sentence):
    """A copula sentence with an adjective (e.g., 'The cat is big')"""
    
    noun: str = Field(description="The noun being described")
    adjective: str = Field(description="The adjective")
    tense: Tense = Field(description="When the state exists")

    def __str__(self) -> str:
        # Copula 'es' (to be) + tense suffix, adjective comes after with 'si'
        copula = "es" + TENSE_SUFFIXES[self.tense]
        return f"{self.noun} si {self.adjective} {copula}"

    @classmethod
    def get_examples(cls):
        return [
            ("The cat is big.", cls(noun="kat", adjective="grond", tense=Tense.PRESENT)),
            ("The water was cold.", cls(noun="akva", adjective="frij", tense=Tense.PAST)),
            ("The sky will be beautiful.", cls(noun="siel", adjective="bel", tense=Tense.FUTURE)),
        ]


language = Language(
    code="test",
    name="Testlang",
    sentence_types=(IntransitiveSentence, TransitiveSentence, AdjectiveSentence),
)
