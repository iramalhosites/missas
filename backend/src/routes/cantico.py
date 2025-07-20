from flask import Blueprint, request, jsonify
from src.models.cantico import db, Cantico

cantico_bp = Blueprint('cantico', __name__)

@cantico_bp.route('/canticos', methods=['GET'])
def get_canticos():
    """Buscar todos os cânticos"""
    try:
        canticos = Cantico.query.order_by(Cantico.created_at.desc()).all()
        return jsonify([cantico.to_dict() for cantico in canticos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cantico_bp.route('/canticos', methods=['POST'])
def create_cantico():
    """Criar um novo cântico"""
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['tipo', 'nome', 'tom']):
            return jsonify({'error': 'Dados incompletos. Necessário: tipo, nome, tom'}), 400
        
        novo_cantico = Cantico(
            tipo=data['tipo'],
            nome=data['nome'],
            tom=data['tom']
        )
        
        db.session.add(novo_cantico)
        db.session.commit()
        
        return jsonify(novo_cantico.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cantico_bp.route('/canticos/<int:cantico_id>', methods=['DELETE'])
def delete_cantico(cantico_id):
    """Excluir um cântico"""
    try:
        cantico = Cantico.query.get_or_404(cantico_id)
        db.session.delete(cantico)
        db.session.commit()
        return jsonify({'message': 'Cântico excluído com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cantico_bp.route('/canticos/clear', methods=['DELETE'])
def clear_canticos():
    """Limpar todos os cânticos (para o botão Novo)"""
    try:
        Cantico.query.delete()
        db.session.commit()
        return jsonify({'message': 'Todos os cânticos foram removidos'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

