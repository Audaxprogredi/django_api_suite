from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime, timedelta

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "peticiones_landing" # Puedes cambiar este nombre según tus necesidades

    def get(self, request, *args, **kwargs):
        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')
        
        # get: Obtiene todos los elementos de la colección
        data = ref.get()
        
        # Si la base de datos está vacía, Firebase devuelve None, lo manejamos devolviendo un dict vacío
        if data is None:
            data = {}
            
        # Devuelve un arreglo JSON
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Convertimos los datos a un diccionario para evitar errores de inmutabilidad
        data = dict(request.data)
        
        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')
        
        # Obtiene y formatea la hora actual
        current_time = datetime.now() - timedelta(hours=5)

        # Volvemos al formato original sin el "-5"
        custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')

        data.update({"timestamp": custom_format})
        
        # push: Guarda el objeto en la colección
        new_resource = ref.push(data)
        
        # Devuelve el id del objeto guardado
        return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)