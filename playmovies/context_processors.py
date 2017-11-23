from playmovies.models import Day

def daysProcessor(request):
    days = Day.objects.all()
    return {'days': days}



