from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import KnowledgeBaseItem
import json

class ChatbotMessageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        message = request.data.get('message', '').lower()
        
        if not message:
            return Response(
                {"error": "Empty message received"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Basic keyword matching
        response_text = "Sorry, I don't understand. Please ask your question differently."
        
        # More specific keywords first
        if 'hours' in message or 'open' in message or 'close' in message:
            response_text = "The clinic is open from 9 AM to 5 PM, Monday to Friday."
        elif 'location' in message or 'address' in message:
            response_text = "The clinic is located at 123 Health St, Wellness City."
        elif 'appointment' in message or 'book' in message:
            response_text = "You can book an appointment by calling our reception or using the online portal."
        elif 'services' in message:
            response_text = "We offer a range of services including general check-ups, specialist consultations, and emergency care."
        else:
            # Fallback to knowledge base
            knowledge_items = KnowledgeBaseItem.objects.all()
            for item in knowledge_items:
                if item.question.lower() in message:
                    response_text = item.answer
                    break
        
        return Response({"response": response_text}, status=status.HTTP_200_OK)