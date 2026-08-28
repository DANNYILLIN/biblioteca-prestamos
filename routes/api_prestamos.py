from flask import Blueprint, request, jsonify
from utils.queries_prestamos import buscar_usuario_por_codigo, buscar_libro_bd

api_prestamos_bp = Blueprint('api_prestamos', __name__)

# Busca la función buscar_usuario y déjala así:
@api_prestamos_bp.route('/api/buscar_usuario', methods=['POST'])
def buscar_usuario():
    data = request.get_json()
    codigo = data.get('codigo')
    
    from utils.queries_prestamos import buscar_usuario_por_codigo
    datos, error = buscar_usuario_por_codigo(codigo) # IMPORTANTE: Capturar los dos
    
    if datos:
        return jsonify({'success': True, 'usuario': datos})
    
    return jsonify({'success': False, 'message': error or 'No encontrado'})

@api_prestamos_bp.route('/api/buscar_libro', methods=['POST'])
def buscar_libro():
    # 1. Obtenemos el código de barras del libro
    codigo_barras = request.json.get('codigo_barras', '').strip()
    
    if not codigo_barras:
        return jsonify({'error': 'El código de barras del libro está vacío'})

    # 2. Buscamos el libro en la base de datos
    libro, error = buscar_libro_bd(codigo_barras)

    # 3. Si hay error (Libro no encontrado)
    if error:
        return jsonify({'success': False, 'error': error})

    # 4. Enviamos los datos del libro
    return jsonify({
        'success': True,
        'libro': libro
    })