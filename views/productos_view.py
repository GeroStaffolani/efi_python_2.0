from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Producto
from app import db
from schemas import ProductoSchema

productos_blueprint = Blueprint('productos', __name__)
producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

# Crear producto (solo para administradores)
@productos_blueprint.route('/productos', methods=['POST'])
@jwt_required()
def create_producto():
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"msg": "No tienes permiso para realizar esta acción"}), 403

    data = request.get_json()
    nuevo_producto = Producto(
        nombre=data['nombre'],
        descripcion=data.get('descripcion'),
        precio=data['precio'],
        stock=data.get('stock', 0)
    )
    db.session.add(nuevo_producto)
    db.session.commit()
    return producto_schema.jsonify(nuevo_producto), 201

# Obtener todos los productos
@productos_blueprint.route('/productos', methods=['GET'])
@jwt_required()
def get_productos():
    productos = Producto.query.all()
    return jsonify(productos_schema.dump(productos))

# Actualizar producto (solo para administradores)
@productos_blueprint.route('/productos/<int:id>', methods=['PUT'])
@jwt_required()
def update_producto(id):
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"msg": "No tienes permiso para realizar esta acción"}), 403

    producto = Producto.query.get_or_404(id)
    data = request.get_json()
    producto.nombre = data.get('nombre', producto.nombre)
    producto.descripcion = data.get('descripcion', producto.descripcion)
    producto.precio = data.get('precio', producto.precio)
    producto.stock = data.get('stock', producto.stock)
    db.session.commit()
    return producto_schema.jsonify(producto)

# Eliminar producto (solo para administradores)
@productos_blueprint.route('/productos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_producto(id):
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"msg": "No tienes permiso para realizar esta acción"}), 403

    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return jsonify({"msg": "Producto eliminado"})
