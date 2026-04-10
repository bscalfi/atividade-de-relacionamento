from sqlalchemy  import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import declarative_base , sessionmaker, relationship

Base = declarative_base()

class Matricula(Base):
    __tablename__ = "matriculas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(Integer,nullable=False)
    telefone = Column(Integer)
    

    alunos = relationship("Alunos", back_populates="matricula")

    def __init__(self, nome):
        self.nome = nome

    #Função para imprimir
    def __repr__(self):
        return f"Matricula: id={self.id} - nome={self.nome}"

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    idade = Column(String(100), nullable=False)
    ra = Column(Integer)
    
    matricula_id = Column(Integer, ForeignKey("matriculas.id"))

    #Relacionamento
    matricula = relationship("Matriculas", back_populates="alunos")

    def __init__(self, nome, idade, ra, matricula):
        self.nome = nome
        self.idade = idade
        self.ra = ra
        self.matricula = matricula

    #Função para imprimir
    def __repr__(self):
        return f"Alunos =  id={self.id} - nome={self.nome} - idade={self.idade} - ra={self.ra}"


engine = create_engine("sqlite:///educacao.db")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


