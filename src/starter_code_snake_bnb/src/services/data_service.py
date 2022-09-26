from src.starter_code_snake_bnb.src.data.cages import Cage
from src.starter_code_snake_bnb.src.data.owners import Owner


def create_account(name: str, email: str) -> Owner:
    owner = Owner()
    owner.name = name
    owner.email = email

    # All default values are set when save() is called, primary key is auto generated
    owner.save()

    return owner


def find_account_by_email(email: str) -> Owner:
    owner = Owner.objects(email=email).first()
    return owner


def register_cage(active_account: Owner, name, allow_dangerous, has_toys, carpeted, meters) -> Cage:
    cage = Cage()

    cage.name = name
    cage.square_meters = meters
    cage.allow_dangerous_snakes = allow_dangerous
    cage.is_carpeted = carpeted
    cage.has_toys = has_toys

    # Must call save before appending to make sure cage is actually a generated value
    cage.save()

    # Make sure we aren't getting stale data for the account
    account = find_account_by_email(active_account.email)
    account.cage_ids.append(cage.id)
    account.save()

    return cage
