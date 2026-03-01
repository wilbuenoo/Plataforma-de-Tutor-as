import requests

class StreamlyService:

    BASE_URL = "https://api.streamly.com"  # Cambiar cuando se tenga real

    def create_session(self, tutor_id, student_id):
        """
        Método preparado para conectar con Streamly
        """
        endpoint = f"{self.BASE_URL}/create-session"

        payload = {
            "tutor_id": tutor_id,
            "student_id": student_id
        }

        try:
            response = requests.post(endpoint, json=payload)
            return response.json()
        except Exception as e:
            return {"error": str(e)}