# pip install sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

#Criar base da classe
Base = declarative_base()

# Sistema de uma rede de restaurantes.
# Um restaurante tem vários Pratos no cardápio
# Cada prato pertence a apenas UM restaurante


class Restaurante(Base):
    __tablename__ = "restaurantes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)

    pratos = relationship("Prato", back_populates="restaurante", cascade="all, delete-orphan")

    def __repr__(self):
        return f"- Restaurante = id: {self.id} - nome: {self.nome}"

class Prato(Base):
    __tablename__ = "pratos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    categoria = Column(String(50))

    restaurante_id = Column(Integer, ForeignKey("restaurantes.id"))
    restaurante = relationship("Restaurante", back_populates="pratos")

    def __repr__(self):
        return f"- Prato = id: {self.id} - nome: {self.nome} - preço: {self.preco}"
   

#Conexão com db
engine = create_engine("sqlite:///restaurantes.db")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
 

def cadastrar():
    nome_restaurante1 = input("Digite o nome do seu restaurante: ").capitalize()
    nome_restaurante2 = input("Digite o nome do seu restaurante: ").capitalize()

    prato1 = input("Digite o nome do prato1: ").capitalize()
    prato2 = input("Digite o nome do prato2: ").capitalize()
    prato3 = input("Digite o nome do prato3: ").capitalize()

    with Session() as session:
        try:
            cantina = Restaurante(nome=nome_restaurante1, cidade="São Paulo")
            sushi = Restaurante(nome=nome_restaurante2, cidade="Santa Catarina")

            # opção 1 - vincular pelo atributo restaurante=
            prato_cantina1 = Prato(nome=prato1,
                                   preco=float(input("Digite o preço: ")),
                                   categoria=input("Digite a categoria do prato: "),
                                   restaurante=cantina
                                   )
            prato_cantina2 = Prato(nome=prato2,
                                   preco=float(input("Digite o preço: ")),
                                   categoria=input("Digite a categoria do prato: "),
                                   restaurante=cantina
                                   )
            # opção 2 - vincular pelo .append()
            prato_sushi = Prato(
                                nome=prato3,
                                preco=float(input("Digite o preço: ")),
                                categoria=input("Digite a categoria do prato: "),
            )
            sushi.pratos.append(prato_sushi)

            session.add_all([cantina, sushi])
            session.commit()
            print("Restaurantes e pratos cadastrados!")

        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

cadastrar()