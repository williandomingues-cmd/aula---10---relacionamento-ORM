from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


#criar base da classe
base = declarative_base()

#Tabelas do banco:
class usuario(base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100))

    #Relacionamento com pedidos
    pedidos = relationship("Pedido", back_populates="usuario")

    def __repr__(self):
        return f"usuario - id={self.id}, nome={self.nome}"

class Pedido(base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produto = Column(String(150))

    #Chave estrangeira
    # Onde tem o foreignky, tem o relacionamento muitos para um (Muitos pedidos para um usuario)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    #Relacionamento
    usuario = relationship("usuario", back_populates="pedidos")

    def __repr__(self):
        return f"Pedido - id={self.id}, produto={self.produto}"
    
#conexao co db
engine = create_engine("sqlite:///loja.db")

base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()



# #criar um usuario - objeto

# Usuario1 = usuario(nome="willian")
# Usuario2 = usuario(nome="laiza")

# #criar pedidos
# Pedido1 = Pedido(produto="iphone 17")
# Pedido2 = Pedido(produto="Notebook")

# #associando  pedidos ao usuario 
# Usuario1.pedidos.append(Pedido1)
# Usuario2.pedodos.append(Pedido2)

# #salvar no banco 
# session.add(Usuario1)
# session.commit()

# print(f"usuario cadastrado: {Usuario1.nome}")

#todos os pedidos do gabriel 
todos_usuarios = session.query(usuario).all()
for usuario in todos_usuarios:
    print(f"nome: {usuario.nome}")
    for pedido in usuario.pedidos:
        print(f"pedido: {pedido.produto}")