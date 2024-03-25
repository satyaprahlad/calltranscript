from faker import Faker

from search_admin_autocomplete.models import DummyModel


# Replace 'your_app' with the actual app name

def create_test_data():
    fake = Faker()

    for _ in range(100):
        name = fake.word()
        description = fake.sentence()

        DummyModel.objects.create(
            name=name,
            description=description
        )

# Call the function to create test data
create_test_data()