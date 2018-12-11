
from pullenti.ner.Referent import Referent as RawReferent
from pullenti.ner.person.PersonReferent import PersonReferent as RawPersonReferent
from pullenti.ner.person.PersonPropertyReferent import PersonPropertyReferent as RawPersonPropertyReferent
from pullenti.ner.person.PersonIdentityReferent import PersonIdentityReferent as RawPersonIdentityReferent
from pullenti.ner.org.OrganizationReferent import OrganizationReferent as RawOrganizationReferent
from pullenti.ner.geo.GeoReferent import GeoReferent as RawGeoReferent
from pullenti.ner.date.DateReferent import DateReferent as RawDateReferent
from pullenti.ner.date.DateRangeReferent import DateRangeReferent as RawDateRangeReferent
from pullenti.ner.money.MoneyReferent import MoneyReferent as RawMoneyReferent
from pullenti.ner.phone.PhoneReferent import PhoneReferent as RawPhoneReferent
from pullenti.ner.address.AddressReferent import AddressReferent as RawAddressReferent
from pullenti.ner.address.StreetReferent import StreetReferent as RawStreetReferent

from pullenti_client.referent import (
    Slot,
    Referent as Referent_
)


class Referent(Referent_):
    raw = None


def slot_property(key):
    @property
    def get_first_slot(referent):
        for slot in referent.slots:
            if slot.key == key:
                return slot.value
    return get_first_slot


def raw_property(method):
    @property
    def get_raw_property(referent):
        raw = referent.raw
        return method.fget(raw)
    return get_raw_property


class PersonReferent(Referent):
    __shortcuts__ = [
        'sex', 'firstname', 'middlename', 'lastname', 'nickname',
        'attribute', 'age', 'born', 'die'
    ]

    sex = slot_property(RawPersonReferent.ATTR_SEX)
    firstname = slot_property(RawPersonReferent.ATTR_FIRSTNAME)
    middlename = slot_property(RawPersonReferent.ATTR_MIDDLENAME)
    lastname = slot_property(RawPersonReferent.ATTR_LASTNAME)
    nickname = slot_property(RawPersonReferent.ATTR_NICKNAME)
    attribute = slot_property(RawPersonReferent.ATTR_ATTR)
    age = raw_property(RawPersonReferent.age)
    born = slot_property(RawPersonReferent.ATTR_BORN)
    die = slot_property(RawPersonReferent.ATTR_DIE)


class PersonPropertyReferent(Referent):
    __shortcuts__ = ['name', 'attribute', 'ref', 'higher']

    name = raw_property(RawPersonPropertyReferent.name)
    attribute = slot_property(RawPersonPropertyReferent.ATTR_ATTR)
    ref = slot_property(RawPersonPropertyReferent.ATTR_REF)
    higher = slot_property(RawPersonPropertyReferent.ATTR_HIGHER)


class PersonIdentityReferent(Referent):
    __shortcuts__ = [
        'type', 'number', 'date', 'org', 'state', 'address'
    ]

    type = raw_property(RawPersonIdentityReferent.typ)
    number = raw_property(RawPersonIdentityReferent.number)
    date = slot_property(RawPersonIdentityReferent.ATTR_DATE)
    org = slot_property(RawPersonIdentityReferent.ATTR_ORG)
    state = raw_property(RawPersonIdentityReferent.state)
    address = raw_property(RawPersonIdentityReferent.address)


class OrganizationReferent(Referent):
    __shortcuts__ = [
        'type', 'number', 'eponym', 'higher', 'geo', 'misc',
        'profile'
    ]

    type = slot_property(RawOrganizationReferent.ATTR_TYPE)
    number = raw_property(RawOrganizationReferent.number)
    eponym = slot_property(RawOrganizationReferent.ATTR_EPONYM)
    higher = slot_property(RawOrganizationReferent.ATTR_HIGHER)
    geo = slot_property(RawOrganizationReferent.ATTR_GEO)
    misc = slot_property(RawOrganizationReferent.ATTR_MISC)
    profile = slot_property(RawOrganizationReferent.ATTR_PROFILE)


class GeoReferent(Referent):
    __shortcuts__ = ['name', 'type', 'alpha2', 'higher', 'ref']

    name = slot_property(RawGeoReferent.ATTR_NAME)
    type = slot_property(RawGeoReferent.ATTR_TYPE)
    alpha2 = slot_property(RawGeoReferent.ATTR_ALPHA2)
    higher = slot_property(RawGeoReferent.ATTR_HIGHER)
    ref = slot_property(RawGeoReferent.ATTR_REF)


class DateReferent(Referent):
    __shortcuts__ = [
        'as_datetime', 'century', 'year', 'month', 'day',
        'day_of_week', 'hour', 'minute', 'second',
        'higher', 'pointer'
    ]

    as_datetime = raw_property(RawDateReferent.dt)
    century = raw_property(RawDateReferent.century)
    year = raw_property(RawDateReferent.year)
    month = raw_property(RawDateReferent.month)
    day = raw_property(RawDateReferent.day)
    day_of_week = raw_property(RawDateReferent.day_of_week)
    hour = raw_property(RawDateReferent.hour)
    minute = raw_property(RawDateReferent.minute)
    second = raw_property(RawDateReferent.second)
    higher = slot_property(RawDateReferent.ATTR_HIGHER)
    pointer = slot_property(RawDateReferent.ATTR_POINTER)


class DateRangeReferent(Referent):
    __shortcuts__ = ['from_', 'to']

    from_ = slot_property(RawDateRangeReferent.ATTR_TO)
    to = slot_property(RawDateRangeReferent.ATTR_FROM)


class MoneyReferent(Referent):
    __shortcuts__ = [
        'currency', 'value', 'alt_value', 'rest',
        'alt_rest', 'real_value'
    ]

    currency = raw_property(RawMoneyReferent.currency)
    value = raw_property(RawMoneyReferent.value)
    alt_value = raw_property(RawMoneyReferent.alt_value)
    rest = raw_property(RawMoneyReferent.rest)
    alt_rest = raw_property(RawMoneyReferent.alt_rest)
    real_value = raw_property(RawMoneyReferent.real_value)


class PhoneReferent(Referent):
    __shortcuts__ = ['number', 'add_number', 'country_code', 'kind']

    number = raw_property(RawPhoneReferent.number)
    add_number = raw_property(RawPhoneReferent.add_number)
    country_code = raw_property(RawPhoneReferent.country_code)
    kind = raw_property(RawPhoneReferent.kind)


class AddressReferent(Referent):
    __shortcuts__ = [
        'street', 'house', 'house_type', 'corpus', 'building',
        'building_type', 'corpus_or_flat', 'porch', 'floor',
        'office', 'flat', 'block', 'box', 'geo', 'zip',
        'postoffice_box'
    ]

    street = slot_property(RawAddressReferent.ATTR_STREET)
    house = slot_property(RawAddressReferent.ATTR_HOUSE)
    house_type = slot_property(RawAddressReferent.ATTR_HOUSETYPE)
    corpus = slot_property(RawAddressReferent.ATTR_CORPUS)
    building = slot_property(RawAddressReferent.ATTR_BUILDING)
    building_type = slot_property(RawAddressReferent.ATTR_BUILDINGTYPE)
    corpus_or_flat = slot_property(RawAddressReferent.ATTR_CORPUSORFLAT)
    porch = slot_property(RawAddressReferent.ATTR_PORCH)
    floor = slot_property(RawAddressReferent.ATTR_FLOOR)
    office = slot_property(RawAddressReferent.ATTR_OFFICE)
    flat = slot_property(RawAddressReferent.ATTR_FLAT)
    block = slot_property(RawAddressReferent.ATTR_BLOCK)
    box = slot_property(RawAddressReferent.ATTR_BOX)
    geo = slot_property(RawAddressReferent.ATTR_GEO)
    zip = slot_property(RawAddressReferent.ATTR_ZIP)
    postoffice_box = slot_property(RawAddressReferent.ATTR_POSTOFFICEBOX)


class StreetReferent(Referent):
    __shortcuts__ = ['type', 'name', 'number', 'second_number', 'geo']

    type = slot_property(RawStreetReferent.ATTR_TYP)
    name = slot_property(RawStreetReferent.ATTR_NAME)
    number = slot_property(RawStreetReferent.ATTR_NUMBER)
    second_number = slot_property(RawStreetReferent.ATTR_SECNUMBER)
    geo = slot_property(RawStreetReferent.ATTR_GEO)


REFERENTS = {
    RawPersonReferent: PersonReferent,
    RawPersonPropertyReferent: PersonPropertyReferent,
    RawPersonIdentityReferent: PersonIdentityReferent,
    RawOrganizationReferent: OrganizationReferent,
    RawGeoReferent: GeoReferent,
    RawDateReferent: DateReferent,
    RawDateRangeReferent: DateRangeReferent,
    RawMoneyReferent: MoneyReferent,
    RawPhoneReferent: PhoneReferent,
    RawAddressReferent: AddressReferent,
    RawStreetReferent: StreetReferent
}


def convert_referent(raw):
    Raw = type(raw)
    Referent = REFERENTS.get(Raw)
    if Referent:
        referent = Referent(raw.type_name)
        referent.raw = raw
        return referent
    raise TypeError('not supported type: {type}'.format(
        type=type(raw)
    ))


def convert_slots(raw, referents):
    for slot in raw:
        key = slot.type_name
        value = slot.value
        if isinstance(value, RawReferent):
            value_id = id(value)
            if value_id not in referents:
                # TODO rare
                continue
            value = referents[value_id]
        yield Slot(key, value)


def convert_referents(raws):
    referents = {}
    for raw in raws:
        raw_id = id(raw)
        if raw_id not in referents:
            referent = convert_referent(raw)
            referents[raw_id] = referent
    for raw in raws:
        slots = list(convert_slots(raw.slots, referents))
        referent = referents[id(raw)]
        referent.slots = slots
    return referents
