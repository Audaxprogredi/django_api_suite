from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False})

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        # Filtra la lista para incluir solo los elementos donde 'is_active' es True
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        # Validación mínima
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)

        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):
    name = "Demo REST API Item"

    def put(self, request, item_id):
        # PUT: Reemplaza completamente los datos, excepto el ID.
        for i, item in enumerate(data_list):
            if item.get('id') == item_id:
                data = request.data
                if 'name' not in data or 'email' not in data:
                    return Response({'error': 'Faltan campos requeridos para PUT.'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Mantenemos el ID original y actualizamos todo lo demás
                updated_item = {
                    'id': item_id,
                    'name': data['name'],
                    'email': data['email'],
                    'is_active': data.get('is_active', item.get('is_active'))
                }
                data_list[i] = updated_item
                return Response({'message': 'Elemento reemplazado exitosamente (PUT).', 'data': updated_item}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, item_id):
        # PATCH: Actualiza parcialmente los campos enviados.
        for i, item in enumerate(data_list):
            if item.get('id') == item_id:
                data = request.data
                
                if 'name' in data:
                    item['name'] = data['name']
                if 'email' in data:
                    item['email'] = data['email']
                if 'is_active' in data:
                    item['is_active'] = data['is_active']
                
                data_list[i] = item
                return Response({'message': 'Elemento actualizado parcialmente (PATCH).', 'data': item}, status=status.HTTP_200_OK)
                
        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, item_id):
        # DELETE: Eliminación lógica (cambia is_active a False).
        for i, item in enumerate(data_list):
            if item.get('id') == item_id:
                item['is_active'] = False
                data_list[i] = item
                return Response({'message': 'Elemento eliminado lógicamente (DELETE).'}, status=status.HTTP_200_OK)
                
        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)