"""Validate output at the boundary between a model and application code."""

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class SearchDocuments(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    query: str = Field(min_length=1, max_length=500)
    limit: int = Field(ge=1, le=5)


if __name__ == "__main__":
    valid = SearchDocuments.model_validate_json('{"query":"headset","limit":2}')
    print(valid.model_dump_json())
    try:
        SearchDocuments.model_validate_json('{"query":"headset","limit":"2"}')
    except ValidationError as error:
        print("Rejected:", error.errors()[0]["loc"][0])
