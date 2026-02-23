from pydantic import BaseModel, Field
from typing import Annotated, Literal

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
    #metadata= id, class, roll no, blood grp, age