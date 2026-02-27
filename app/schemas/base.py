from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

#chat input model
class Input(BaseModel):
    text: str|None
    file: str|None

#student model
class Student(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50, description="Name of student")]
    sch_class: Annotated[int, Field(gt=0, lt=13, description="Class that student belongs to")]
    roll_no: Annotated[int, Field(description="Roll_no of student")]
    blood_group: Annotated[Literal["A+", "A-", "B+", "B-", "AB+","AB-", "O+", "O-"], Field(description="Blood group of student")]
    age: Annotated[int, Field(gt=3, lt=25, description="Age of student")]
    address: Annotated[str, Field(min_length=5, description="Student's home address")]
    parent_contact: int
    #embed= name, address, parent contact
    #metadata= class, roll no, blood grp, age

#subject model
class Subject(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50, description="Name of the subject being taught")]
    class_taught: Annotated[int, Field(gt=0, lt=13, description="The class to which the subject is taught")]
    textbook: Annotated[str, Field(min_length=2, max_length=50, description="Name of the textbook for this subject+class combo")]

#teacher model
class Teacher(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50, description="Name of student")]
    subject: Optional[list[dict]]= Field(description="Contains mongo id of subject, name of subject, class to which the teacher teaches this subject")
    class_teacher: Optional[int]= Field(description="The class to which the teacher is a homeroom teacher")

#marksheet model
class MarkSheet(BaseModel):
    student_id: Annotated[str, Field(description="The id of the student to which the marksheet belongs")]
    score: list[dict[str,float]]

    @computed_field
    @property
    def percentage(self)->Optional[float]:
        sum=0
        if not self.score: 
            return None
        for marks in self.score:
            for key,value in marks.items():
                sum+=value
        percentage=sum/len(self.score)
        return percentage

    @computed_field
    @property
    def status(self)->Optional[str]:
        if not self.percentage:
            return None
        if self.percentage>= 33:
            return 'pass'
        return 'fail'

#MONGO QUERY MODELS
#find query input model
class FindQueryInput(BaseModel):
    idx_name:  Annotated[str, Field("Name of the table/collection to which the data has to be fetched.")]
    filters:  Annotated[dict, Field(description="The filter criteria to identify which records to fetch.")]
    sort: Optional[list]=None
    limit: Optional[int]=None
    skip: Optional[int]=None

#update query input model
class UpdateQueryInput(BaseModel):
    idx_name: Annotated[str, Field("Name of the table/collection to which the data has to be updated.")]
    filters: Annotated[dict, Field(description="The filter criteria to identify which records to update.")]
    update: Annotated[dict, Field(description="The update operations to apply to matching records.")]

class CreateQueryInput(BaseModel):
    idx_name: Annotated[str, Field("Name of the table/collection to which the data has to be added.")]
    data: Annotated[dict, Field("The input fields needed for the record creation as per the table")]

#VECTOR QUERY MODELS
#vector memory input model
class VectorMemoryInput(BaseModel):
    idx_name: Annotated[str, Field(description="Name of the vector index to store the data in.")]
    id: Annotated[str, Field(description="The id of the vector record to be updated.")]
    metadata: Optional[dict]=Field(default_factory=dict, description="The metadata fields to be updated in the vector db record.")
    text: Optional[str]=Field(default=None, description="The text content to be updated in the vector db record.")

class SchemaSearchInput(BaseModel):
    idx_name: Annotated[str, Field(description="Name of the vector index to perform the schema search on.")]
    input: Annotated[str, Field(description="The input text query for which relevant information is to be retrieved from the vector db inorder to create a mongo query.")]
    top_k: Annotated[int, Field(description="The number of top results to return from the schema search.")]
    filters: Optional[dict]=Field(default_factory=dict, description="The filters criteria to apply during the schema search.")