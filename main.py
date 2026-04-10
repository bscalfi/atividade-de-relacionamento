from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Matricula(Base):
    __tablename__ = "matriculas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(20), nullable=False)
    telefone = Column(String(20))
    
    alunos = relationship("Aluno", back_populates="matriculas")

    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone

    def __repr__(self):
        return f"Matricula: id={self.id} - nome={self.nome} - cpf={self.cpf} - telefone={self.telefone}"


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    ra = Column(Integer)
    
    matricula_id = Column(Integer, ForeignKey("matriculas.id"))

    matriculas = relationship("Matricula", back_populates="alunos")

    def __init__(self, nome, idade, ra):
        self.nome = nome
        self.idade = idade
        self.ra = ra

    def __repr__(self):
        return f"Aluno = id={self.id} - nome={self.nome} - idade={self.idade} - ra={self.ra}"


engine = create_engine("sqlite:///educacao.db")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def cadastrar_matricula():
    with Session() as session:
        try:
            nome = input("Digite o nome da matricula: ")
            cpf = input("Digite seu CPF: ")
            telefone = input("Digite seu telefone: ")

            matricula = Matricula(nome=nome, cpf=cpf, telefone=telefone)

            session.add(matricula)
            session.commit()

            print(f"Matricula {nome} cadastrada com sucesso!")

        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro: {erro}")


def cadastrar_aluno():
    with Session() as session:
        try:
            nome_matricula = input("Digite o nome da matricula: ")

            matricula = session.query(Matricula).filter_by(nome=nome_matricula).first()

            if not matricula:
                print(f"Nenhuma matricula encontrada com o nome {nome_matricula}")
                return

            nome = input("Digite o nome do aluno: ")
            idade = int(input("Digite a idade: "))
            ra = int(input("Digite o RA: "))

            aluno = Aluno(nome=nome, idade=idade, ra=ra)
            aluno.matriculas = matricula
            session.add(aluno)
            session.commit()

            print(f"Aluno {nome} cadastrado com sucesso!")

        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro: {erro}")


cadastrar_aluno()