from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cantico(db.Model):
    __tablename__ = 'canticos'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    tom = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'nome': self.nome,
            'tom': self.tom,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

