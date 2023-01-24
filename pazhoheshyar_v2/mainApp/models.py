from django.db import models
from django.core.validators import FileExtensionValidator
# Create your models here.



class User(models.Model):
  user_id = models.CharField(max_length=4, primary_key=True)
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  joind_date = models.DateTimeField(auto_now_add=True)
  password = models.CharField(max_length=16)  
  TYPE = (
        ('0', 'student'),
        ('1', 'professor'),
        ('2', 'karshenas'),
        ('3', 'head'),
    )
  user_type = models.CharField(max_length=1, choices=TYPE)

  def __str__(self):
    return f"{self.firstname} {self.lastname}"




class Thesis(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField(max_length=512)
#   content = models.file()
  pdf_file = models.FileField(upload_to="thesises/", validators=[FileExtensionValidator(allowed_extensions=["pdf"])])

  supervisor = models.ForeignKey("User",related_name='supervisor', on_delete=models.CASCADE)
  student = models.ForeignKey("User",related_name='student', on_delete=models.CASCADE)
  advisor = models.ForeignKey("User",related_name='advisor', on_delete=models.CASCADE)

  proposal_davar1 = models.ForeignKey("User",related_name='proposal_davar1', on_delete=models.CASCADE, blank=True, null=True)    
  proposal_davar2 = models.ForeignKey("User",related_name='proposal_davar2', on_delete=models.CASCADE, blank=True, null=True)    
  proposal_davar3 = models.ForeignKey("User",related_name='proposal_davar3', on_delete=models.CASCADE, blank=True, null=True)    
  proposal_davar4 = models.ForeignKey("User",related_name='proposal_davar4', on_delete=models.CASCADE, blank=True, null=True)    

  davar1 = models.ForeignKey("User",related_name='davar1', on_delete=models.CASCADE, blank=True, null=True)  
  davar2 = models.ForeignKey("User",related_name='davar2', on_delete=models.CASCADE, blank=True, null=True)


  STATES = (
        ('0', 'student'),
        ('1', 'advisor'),
        ('2', 'supervisor'),
        ('3', 'head of department'),
        ('4', 'karshenas'),
        ('5', 'finished'),
    )
  state = models.CharField(max_length=1, choices=STATES)


  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)




# class Student(Place):
    

# class Place(models.Model):
#     name = models.CharField(max_length=50)
#     address = models.CharField(max_length=80)

# class Restaurant(Place):
#     serves_hot_dogs = models.BooleanField(default=False)
#     serves_pizza = models.BooleanField(default=False)

