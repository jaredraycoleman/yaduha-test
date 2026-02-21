from yaduha import Language, Sentence
from pydantic import Field


class SimpleSentence(Sentence):
    """A basic sentence with a subject and verb."""

    subject: str = Field(description="The subject of the sentence")
    verb: str = Field(description="The verb/action")

    def __str__(self) -> str:
        return f"{self.subject} {self.verb}"

    @classmethod
    def get_examples(cls):
        return [
            ("I sleep.", cls(subject="I", verb="sleep")),
            ("You run.", cls(subject="you", verb="run")),
        ]


language = Language(
    code="test",
    name="test-project",
    sentence_types=(SimpleSentence,),
)
