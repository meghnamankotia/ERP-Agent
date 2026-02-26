from pydantic import BaseModel, Field
from typing import Annotated, Literal, Optional

#chat input model
class Input(BaseModel):
    text: str|None
    file: str|None

#student model
class Student(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50, description="Name of student")]
    sch_class: Annotated[int, Field(gt=1, lt=13, description="Class that student belongs to")]
    roll_no: Annotated[int, Field(description="Roll_no of student")]
    blood_group: Annotated[Literal["A+", "A-", "B+", "B-", "AB+","AB-", "O+", "O-"], Field(description="Blood group of student")]
    age: Annotated[int, Field(gt=3, lt=25, description="Age of student")]
    address: Annotated[str, Field(min_length=5, description="Student's home address")]
    parent_contact: int
    #embed= name, address, parent contact
    #metadata= class, roll no, blood grp, age

#find query input model
class FindQueryInput(BaseModel):
    filters: dict
    sort: Optional[list]=None
    limit: Optional[int]=None
    skip: Optional[int]=None

#update query input model
class UpdateQueryInput(BaseModel):
    filters: Annotated[dict, Field(description="The filter criteria to identify which records to update.")]
    update: Annotated[dict, Field(description="The update operations to apply to matching records.")]

#vector memory input model
class VectorMemoryInput(BaseModel):
    idx_name: Annotated[str, Field(description="Name of the vector index to store the data in.")]
    data: Annotated[dict, Field(description="Text field to be embedded and each metadata field set sepearatley in the vector db record.")]

class SchemaSearchInput(BaseModel):
    idx_name: Annotated[str, Field(description="Name of the vector index to perform the schema search on.")]
    input: Annotated[str, Field(description="The input text query for which relevant information is to be retrieved from the vector db inorder to create a mongo query.")]
    top_k: Annotated[int, Field(description="The number of top results to return from the schema search.")]
    filter: Optional[dict]=Field(default_factory=dict, description="The filter criteria to apply during the schema search.")

class VectorUpdateInput(BaseModel):
    idx_name: Annotated[str, Field(description="Name of the vector index to store the data in.")]
    id: Annotated[str, Field(description="The id of the vector record to be updated.")]
    metadata: Optional[dict]=Field(default_factory=dict, description="The metadata fields to be updated in the vector db record.")
    text: Optional[str]=Field(default=None, description="The text content to be updated in the vector db record.")