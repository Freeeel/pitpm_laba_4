from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

# Создание объекта FastAPI
app = FastAPI()

# Настройка базы данных MySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://isp_p_Samylov:12345@192.168.25.23/isp_p_Samylov"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Определение модели SQLAlchemy для пользователя
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    surname = Column(String(50))
    patronymic = Column(String(50))
    numberPasport = Column(String(100), unique=True)

class Cashier(Base):
    __tablename__ = "cashiers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    surname = Column(String(50))
    patronymic = Column(String(50))


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    codeSoldCurrency = Column(Integer)
    codeBoughtCurrency = Column(Integer)
    cashierId = Column(Integer)
    clientId = Column(Integer)
    dateDeal = Column(String(8))
    timeDeal = Column(String(4))
    sumSoldCurrency = Column(Integer)
    sumBoughtCurrency = Column(Integer)

class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, index=True)
    codeSoldCurrency = Column(Integer)
    codeBoughtCurrency = Column(Integer)
    nameCurrency = Column(String(50))
    cashierId = Column(Integer)
    clientId = Column(Integer)
    courseSale = Column(Integer)
    coursePurchase = Column(Integer)

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)


class ClientCreate(BaseModel):
    name: str
    surname: str
    patronymic: str
    numberPasport: str


class ClientResponce(BaseModel):
    name: str
    surname: str
    patronymic: str
    numberPasport: str

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/clients/{client_id}", response_model=ClientResponce)
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(client_id == Client.id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="User ")
    return client

@app.post("/clients", response_model=ClientResponce)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = Client(name=client.name,surname=client.surname,patronymic=client.patronymic,numberPasport=client.numberPasport)
    try:
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Успешно")