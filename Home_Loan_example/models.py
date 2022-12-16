from sqlalchemy.sql.expression import null
from database import Base
from sqlalchemy import String,Boolean,Integer,Column,Text, Float


class Features(Base):
    __tablename__ = 'home_loan_predictions3'


    Id = Column(Integer, primary_key=True)
    Gender = Column(Integer)
    Married = Column(Integer)
    Education = Column(Integer)
    Self_Employed = Column(Integer)
    ApplicantIncome=Column(Integer)
    CoApplicantIncome=Column(Float)
    LoanAmount=Column(Integer)
    Loan_Amount_Term=Column(Integer)
    Credit_History=Column(Integer)
    Property_Area = Column(Integer)
    Loan_status = Column(Integer)



    def __repr__(self):
        return f"<Item name={self.Property_Area} price={self.CoApplicantIncome}>"
