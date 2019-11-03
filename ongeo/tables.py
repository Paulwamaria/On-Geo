import django_tables2 as tables
from .models import AllAtendees


class AttendeesTable(tables.Table):
   
    class Meta:
        
        model = AllAtendees
        template_name = "django_tables2/bootstrap.html"
        fields = ("user","checked_in_on","first_name","last_name" )