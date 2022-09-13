from pyexpat import model
from home.models import Jobs
import django_filters
from accounts.models import Companies

companies = Companies.objects.all()
COUNTRY_NAME = [(i.country,i.country.name) for i in companies]
# print(COUNTRY_NAME)


class JobsFilter(django_filters.FilterSet):
    company__country = django_filters.ChoiceFilter(choices=COUNTRY_NAME)
    class Meta:
        model = Jobs
        fields = {'category':['exact',],
                    'company':['exact'],
                    'location':['icontains'],
                   }
    