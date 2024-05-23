from fastapi import APIRouter, FastAPI, HTTPException, status
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic.fields import Field
from mrz.generator.td1 import TD1CodeGenerator
from mrz.generator.td2 import TD2CodeGenerator
from mrz.generator.td3 import TD3CodeGenerator
from mrz.generator.mrva import MRVACodeGenerator
from mrz.generator.mrvb import MRVBCodeGenerator
from mrz.checker.td1 import TD1CodeChecker
from mrz.checker.td2 import TD2CodeChecker
from mrz.checker.td3 import TD3CodeChecker
from mrz.checker.mrva import MRVACodeChecker
from mrz.checker.mrvb import MRVBCodeChecker


fast = FastAPI()

fast.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app = APIRouter(prefix="/api/v1")


class CheckDocument(BaseModel):
    format_type: str = Field(
        title="format of the document",
        description="can be TD1, TD2, P, MRVA, MRVB",
        min_length=0,
        max_length=4,
    )

    mrz: str = Field(
        title="mrz string",
        description="mrz string of the document",
    )


class Document(BaseModel):
    format_type: str = Field(
        title="format of the document",
        description="can be TD1, TD2, P, MRVA, MRVB",
        min_length=0,
        max_length=4,
    )

    document_type: str = Field(
        title="type of the document",
        description="""
        for TD1 and TD2 the first letter can be (I, A, C),
        for P the first letter can be (P),
        for MRVA, MRVB first letter can be (V, A)
        """,
        min_length=0,
        max_length=2,
    )

    contry_code: str = Field(
        title="country code",
        description="country code of the document",
        min_length=3,
        max_length=3,
    )

    document_number: str = Field(
        title="document number",
        description="document number",
        min_length=0,
        max_length=9,
    )

    birth_date: str = Field(
        title="birth date",
        description="birth date in the format DD/MM/YYYY",
        min_length=10,
        max_length=10,
    )

    sex: str = Field(
        title="sex",
        description="for Male: M, for Female F, fow not specified X | <",
        min_length=1,
        max_length=1,
    )

    expiration_date: str = Field(
        title="expiration date",
        description="expiration date in the format DD/MM/YYYY",
        min_length=10,
        max_length=10,
    )

    nationality: str = Field(
        title="national",
        description="nationality in format of country code",
        min_length=3,
        max_length=3,
    )

    surname: str = Field(
        title="surname",
        description="surname of the person",
        min_length=0,
        max_length=30,
    )

    given_names: str = Field(
        title="given name",
        description="given name of the person",
        min_length=0,
        max_length=30,
    )

    optional_data_1: str = Field(
        title="optional data",
        default="",
        description="optional data",
        min_length=0,
        max_length=15,
    )

    optional_data_2: str = Field(
        title="optional data",
        default="",
        description="optional data valid only for TD1",
        min_length=0,
        max_length=15,
    )


def compute_mrz(document: Document):
    match document.format_type:
        case "TD1":
            code = TD1CodeGenerator(
                document_type=document.document_type,
                country_code=document.contry_code,
                document_number=document.document_number,
                birth_date=convert_date(document.birth_date),
                expiry_date=convert_date(document.expiration_date),
                sex=document.sex,
                nationality=document.nationality,
                surname=document.surname,
                given_names=document.given_names,
                optional_data1=document.optional_data_1,
                optional_data2=document.optional_data_2,
            )
            return f"{code._line1()}\n{code._line2()}\n{code._line3()}"
        case "TD2":
            code = TD2CodeGenerator(
                document_type=document.document_type,
                country_code=document.contry_code,
                document_number=document.document_number,
                birth_date=convert_date(document.birth_date),
                expiry_date=convert_date(document.expiration_date),
                sex=document.sex,
                nationality=document.nationality,
                surname=document.surname,
                given_names=document.given_names,
                optional_data=document.optional_data_1,
            )
            return f"{code._line1()}\n{code._line2()}"
        case "P":
            code = TD3CodeGenerator(
                document_type=document.document_type,
                country_code=document.contry_code,
                document_number=document.document_number,
                birth_date=convert_date(document.birth_date),
                expiry_date=convert_date(document.expiration_date),
                sex=document.sex,
                nationality=document.nationality,
                surname=document.surname,
                given_names=document.given_names,
                optional_data=document.optional_data_1,
            )
            return f"{code._line1()}\n{code._line2()}"
        case "MRVA":
            code = MRVACodeGenerator(
                document_type=document.document_type,
                country_code=document.contry_code,
                document_number=document.document_number,
                birth_date=convert_date(document.birth_date),
                expiry_date=convert_date(document.expiration_date),
                sex=document.sex,
                nationality=document.nationality,
                surname=document.surname,
                given_names=document.given_names,
                optional_data=document.optional_data_1,
            )
            return f"{code._line1()}\n{code._line2()}"
        case "MRVB":
            code = MRVBCodeGenerator(
                document_type=document.document_type,
                country_code=document.contry_code,
                document_number=document.document_number,
                birth_date=convert_date(document.birth_date),
                expiry_date=convert_date(document.expiration_date),
                sex=document.sex,
                nationality=document.nationality,
                surname=document.surname,
                given_names=document.given_names,
                optional_data=document.optional_data_1,
            )
            return f"{code._line1()}\n{code._line2()}"
        case _:
            return "error"


def compute_check_mrz(document: CheckDocument):
    match document.format_type:
        case "TD1":
            return TD1CodeChecker(document.mrz, compute_warnings=True)
        case "TD2":
            return TD2CodeChecker(document.mrz, compute_warnings=True)
        case "P":
            return TD3CodeChecker(document.mrz, compute_warnings=True)
        case "MRVA":
            return MRVACodeChecker(document.mrz, compute_warnings=True)
        case "MRVB":
            return MRVBCodeChecker(document.mrz, compute_warnings=True)
        case _:
            return "error"


def convert_date(date: str):
    day, month, year = date.split('/')
    return year[2:] + month + day


@app.get("/")
def healthcheck():
    return {"status": "ok"}


@app.post("/generate")
def generate(document: Document):
    cmp = compute_mrz(document)
    if cmp == "error":
        raise HTTPException(
            status_code=status.HTTP_400,
            detail="invalid format type"
        )
    return {"mrz": cmp}


@app.post("/check")
def check(document: CheckDocument):
    cmp = compute_check_mrz(document)
    if cmp == "error":
        raise HTTPException(
            status_code=status.HTTP_400,
            detail="invalid format type"
        )
    return cmp


fast.include_router(app)
