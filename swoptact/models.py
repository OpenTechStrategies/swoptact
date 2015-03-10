# SWOPTACT is a list of contacts with a history of their event attendance
# Copyright (C) 2015  Open Tech Strategies, LLC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from phonenumber_field import modelfields

from swoptact import mixins

class Address(models.Model):
    """ Representation of an address in Chicago """
    TYPES = (
        ("St", "Street"),
        ("Av", "Avenue"),
        ("Blvd", "Boulevard"),
        ("Rd", "Road"),
    )

    DIRECTIONS = (
        ("N", "North"),
        ("E", "East"),
        ("S", "South"),
        ("W", "West"),
    )

    class Meta:
        verbose_name_plural = "Addresses"

    number = models.IntegerField()
    direction = models.CharField(max_length=1, choices=DIRECTIONS)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPES)

    def __init__(self, *args, **kwargs):
        super(Address, self).__init__(*args, **kwargs)

        # Compile a dictionary of the choices so we can quickly use them
        self.DICT_TYPES = dict(self.TYPES)
        self.DICT_DIRECTIONS = dict(self.DIRECTIONS)

    def __str__(self):
        return "{number} {direction} {name} {type}".format(
            number=self.number,
            direction=self.DICT_DIRECTIONS[self.direction],
            name=self.name,
            type=self.DICT_TYPES[self.type],
        )

class Participant(models.Model):
    """ Representation of a person who can participate in a Event """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = modelfields.PhoneNumberField()
    email = models.EmailField()
    address = models.ForeignKey(Address)

    def __str__(self):
        return "{first_name} {last_name}".format(
            first_name=self.first_name,
            last_name=self.last_name
        )

    def name(self):
        """ The full name of the participant """
        return "{first} {last}".format(
            first=self.first_name,
            last=self.last_name
        )

    @property
    def events(self):
        """ List of all events participant is in """
        return Event.objects.filter(participants__in=[self]).all()


class Event(models.Model, mixins.AdminURLMixin):

    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    site = models.CharField(max_length=255)
    address = models.ForeignKey(Address)
    participants = models.ManyToManyField(Participant)

    def __str__(self):
        return self.name