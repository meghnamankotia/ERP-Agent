#TABLE DEFINITIONS
studentdatas="""class Student(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50, description="Name of student")]
    sch_class: Annotated[int, Field(gt=0, lt=13, description="Class that student belongs to")]
    roll_no: Annotated[int, Field(description="Roll_no of student")]
    blood_group: Annotated[Literal["A+", "A-", "B+", "B-", "AB+","AB-", "O+", "O-"], Field(description="Blood group of student")]
    age: Annotated[int, Field(gt=3, lt=25, description="Age of student")]
    address: Annotated[str, Field(min_length=5, description="Student's home address")]
    parent_contact: int

    #metadata= class, roll no, blood grp, age
    """

subjects=  """class Subject(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50, description="Name of the subject being taught")]
    class_taught: Annotated[int, Field(gt=0, lt=13, description="The class to which the subject is taught")]
    textbook: Annotated[str, Field(min_length=2, max_length=50, description="Name of the textbook for this subject+class combo")]
    
    #metadata= class_taught

    eg- "name": "Maths"
        "class_taught": 4
        "textbook": "Primary mathematics- 4th grade, 1st edition by RD Sharma."
    """

teachers="""class Teacher(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50, description="Name of student")]
    subject: Optional[list[dict]]= Field(description="Contains mongo id of subject, name of subject, class to which the teacher teaches this subject")
    class_teacher: Optional[int]= Field(description="The class to which the teacher is a homeroom teacher")

    #metadata=class_teacher

    eg- "name": "Smita Mishra"
        "subject": [
            {"subject_id": "1222434577", #to be retrieve from subject table only if it exists ,str
             "name": "Maths" #str,
             "class": 4 #int},
            {"subject_id": "1222434678", #to be retrieved from subject table only if it exists
             "name": "Maths",
             "class": 6} 
        ]
        "class_teacher": 6
    """

marksheets="""class MarkSheet(BaseModel):
    student_id: Annotated[str, Field(description="The id of the student to which the marksheet belongs")]
    score: list[dict[str,float]]

    @computed_field
    @property
    def percentage(self)->Optional[float]:
        if not self.score:
            return None
        sum=0
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

    #metadata: percentage, status

    eg- "student_id": "1223425e345" # to be retrieved from student table i.e records is to be created only if the student exists.
        "score": [
            {"maths": 88.5},
            {"english": 95}
        ]
        "percentage": 91.75
        "status":"pass"    
    """


#SCHEMA DICTIONARY
table_schemas={
    "studentdatas": studentdatas ,

    "subjects": subjects,

    "teachers": teachers,

    "marksheets": marksheets
}
