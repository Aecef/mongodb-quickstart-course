from datetime import datetime, timedelta
from typing import List

import bson

from src.starter_code_snake_bnb.src.data.bookings import Booking
from src.starter_code_snake_bnb.src.data.cages import Cage
from src.starter_code_snake_bnb.src.data.owners import Owner
from src.starter_code_snake_bnb.src.data.snakes import Snake


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


def register_cage(active_account: Owner, name, allow_dangerous, has_toys, carpeted, meters, price) -> Cage:
    cage = Cage()

    cage.name = name
    cage.square_meters = meters
    cage.allow_dangerous_snakes = allow_dangerous
    cage.is_carpeted = carpeted
    cage.has_toys = has_toys
    cage.price = price

    # Must call save before appending to make sure cage is actually a generated value
    cage.save()

    # Make sure we aren't getting stale data for the account
    account = find_account_by_email(active_account.email)
    account.cage_ids.append(cage.id)
    account.save()

    return cage


def find_cages_for_user(account: Owner) -> List[Cage]:
    query = Cage.objects(id__in = account.cage_ids)
    cages = list(query)

    return cages


def add_available_date(selected_cage: Cage, start_date: datetime, days: int) -> Cage:
    booking = Booking()

    booking.checked_in_date = start_date
    booking.checked_out_date = start_date + timedelta(days=days)

    cage = Cage.objects(id=selected_cage.id).first()
    cage.bookings.append(booking)
    cage.save()

    return cage


    return None


def add_snake(account: Owner, name: str, is_venomous: bool, length: float, species: str) -> Snake:
    snake = Snake()

    snake.name = name
    snake.is_venomous = is_venomous
    snake.length = length
    snake.species = species
    snake.save()

    account = find_account_by_email(account.email)
    account.snake_ids.append(snake.id)
    account.save()

    return snake


def get_snakes_for_user(user_id: bson.ObjectId) -> List[Snake]:
    owner = Owner.objects(id=user_id).first()
    snakes = Snake.objects(id__in=owner.snake_ids).all()
    return list(snakes)