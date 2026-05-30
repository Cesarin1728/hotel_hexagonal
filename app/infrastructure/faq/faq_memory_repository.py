from app.domain.ports.faq_port import FAQPort
from typing import Optional

class InMemoryFAQRepository(FAQPort):
    def __init__(self):
        # Respuestas automáticas (FAQ) simuladas para el hotel
        self.faqs = {
            "pago": "Aceptamos tarjetas de crédito, débito, transferencias y efectivo",
            "check-in": "El check-in es a partir de las 3:00 PM y el check-out a las 12:00 PM.",
            "mascotas": "No puede haber mascotass en el hotel",
            "desayuno": "El desayuno se incluye en el servicio si usted es miembro del hotel",
            "cancelacion": "Puedes cancelar sin costo el mismo día de la reserva"
        }

    def get_answer(self, question: str) -> Optional[str]:
        question_lower = question.lower()
        # Búsqueda simple de coincidencias
        for keyword, answer in self.faqs.items():
            if keyword in question_lower:
                return answer
        return "No tengo una respuesta automatizada para eso."