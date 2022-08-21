from django.contrib.auth import get_user_model
from core.models import Comment, Category, Reply
from recipe.models import Recipe
from django_seed import Seed

seeder = Seed.seeder(locale="en")


User = get_user_model()

seeder.add_entity(User, 5)
seeder.add_entity(Category, 10)
seeder.add_entity(Recipe, 10)
seeder.add_entity(Comment, 10)
seeder.add_entity(Reply, 10)


inserted_pks = seeder.execute()
