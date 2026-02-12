from pydantic import BaseModel, Field
from typing import Annotated, Literal

#student model
class Student(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=50, description="Name of student")]
    sch_class: Annotated[int, Field(gt=1, lt=13, description="Class that student belongs to")]
    roll_no: Annotated[int, Field(description="Roll_no of student")]
    blood_group: Annotated[Literal["a+", "a-", "b+", "b-", "ab+","ab-", "o+", "o-"], Field(description="Blood group of student")]
    age: Annotated[int, Field(gt=0, description="Age of student")]
    address: Annotated[str, Field(min_length=0, description="Student's home address")]
    parent_contact: Annotated[int, Field(max_digits=10, gt=1000000000, description="")]