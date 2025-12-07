from django.db import models

class KnowledgeBaseItem(models.Model):
    category = models.CharField(max_length=100)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.category}] {self.question}"
