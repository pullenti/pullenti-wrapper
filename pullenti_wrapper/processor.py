
from pullenti.ner.Processor import Processor as RawProcessor
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.ProcessorService import ProcessorService

from pullenti.ner.money.MoneyAnalyzer import MoneyAnalyzer
from pullenti.ner.uri.UriAnalyzer import UriAnalyzer
from pullenti.ner.phone.PhoneAnalyzer import PhoneAnalyzer
from pullenti.ner.date.DateAnalyzer import DateAnalyzer
from pullenti.ner.keyword.KeywordAnalyzer import KeywordAnalyzer
from pullenti.ner.definition.DefinitionAnalyzer import DefinitionAnalyzer
from pullenti.ner.denomination.DenominationAnalyzer import DenominationAnalyzer
from pullenti.ner.measure.MeasureAnalyzer import MeasureAnalyzer
from pullenti.ner.bank.BankAnalyzer import BankAnalyzer
from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
from pullenti.ner.address.AddressAnalyzer import AddressAnalyzer
from pullenti.ner.org.OrganizationAnalyzer import OrganizationAnalyzer
from pullenti.ner.person.PersonAnalyzer import PersonAnalyzer
from pullenti.ner.mail.MailAnalyzer import MailAnalyzer
from pullenti.ner.transport.TransportAnalyzer import TransportAnalyzer
from pullenti.ner.decree.DecreeAnalyzer import DecreeAnalyzer
from pullenti.ner.instrument.InstrumentAnalyzer import InstrumentAnalyzer
from pullenti.ner.titlepage.TitlePageAnalyzer import TitlePageAnalyzer
from pullenti.ner.booklink.BookLinkAnalyzer import BookLinkAnalyzer
from pullenti.ner.business.BusinessAnalyzer import BusinessAnalyzer
from pullenti.ner.named.NamedEntityAnalyzer import NamedEntityAnalyzer
from pullenti.ner.weapon.WeaponAnalyzer import WeaponAnalyzer

from .utils import assert_one_of
from .langs import (
    DEFAULT_LANGS,
    loaded_langs,
    langs_to_raw
)
from .preprocess import preprocess
from .result import convert_result


MONEY = MoneyAnalyzer.ANALYZER_NAME
URI = UriAnalyzer.ANALYZER_NAME
PHONE = PhoneAnalyzer.ANALYZER_NAME
DATE = DateAnalyzer.ANALYZER_NAME
KEYWORD = KeywordAnalyzer.ANALYZER_NAME
DEFINITION = DefinitionAnalyzer.ANALYZER_NAME
DENOMINATION = DenominationAnalyzer.ANALYZER_NAME
MEASURE = MeasureAnalyzer.ANALYZER_NAME
BANK = BankAnalyzer.ANALYZER_NAME
GEO = GeoAnalyzer.ANALYZER_NAME
ADDRESS = AddressAnalyzer.ANALYZER_NAME
ORGANIZATION = OrganizationAnalyzer.ANALYZER_NAME
PERSON = PersonAnalyzer.ANALYZER_NAME
MAIL = MailAnalyzer.ANALYZER_NAME
TRANSPORT = TransportAnalyzer.ANALYZER_NAME
DECREE = DecreeAnalyzer.ANALYZER_NAME
INSTRUMENT = InstrumentAnalyzer.ANALYZER_NAME
TITLEPAGE = TitlePageAnalyzer.ANALYZER_NAME
BOOKLINK = BookLinkAnalyzer.ANALYZER_NAME
BUSINESS = BusinessAnalyzer.ANALYZER_NAME
NAMEDENTITY = NamedEntityAnalyzer.ANALYZER_NAME
WEAPON = WeaponAnalyzer.ANALYZER_NAME

ANALYZERS = [
    MONEY,
    URI,
    PHONE,
    DATE,
    KEYWORD,
    DEFINITION,
    DENOMINATION,
    MEASURE,
    BANK,
    GEO,
    ADDRESS,
    ORGANIZATION,
    PERSON,
    MAIL,
    TRANSPORT,
    DECREE,
    INSTRUMENT,
    TITLEPAGE,
    BOOKLINK,
    BUSINESS,
    NAMEDENTITY,
    WEAPON,
]

TYPE_ANALYZERS = {
    MONEY: MoneyAnalyzer,
    URI: UriAnalyzer,
    PHONE: PhoneAnalyzer,
    DATE: DateAnalyzer,
    KEYWORD: KeywordAnalyzer,
    DEFINITION: DefinitionAnalyzer,
    DENOMINATION: DenominationAnalyzer,
    MEASURE: MeasureAnalyzer,
    BANK: BankAnalyzer,
    GEO: GeoAnalyzer,
    ADDRESS: AddressAnalyzer,
    ORGANIZATION: OrganizationAnalyzer,
    PERSON: PersonAnalyzer,
    MAIL: MailAnalyzer,
    TRANSPORT: TransportAnalyzer,
    DECREE: DecreeAnalyzer,
    INSTRUMENT: InstrumentAnalyzer,
    TITLEPAGE: TitlePageAnalyzer,
    BOOKLINK: BookLinkAnalyzer,
    BUSINESS: BusinessAnalyzer,
    NAMEDENTITY: NamedEntityAnalyzer,
    WEAPON: WeaponAnalyzer,
}

INITIALIZED = set()


def select_analyzers(selected):
    for analyzer in ProcessorService.get_analyzers():
        if analyzer.name in selected:
            analyzer = analyzer.clone()
            if analyzer is not None:  # TODO why would it happen?
                yield analyzer


class Processor(object):
    def __init__(self, analyzers):
        for analyzer in analyzers:
            assert_one_of(analyzer, ANALYZERS)
        self.analyzers = analyzers

        langs = loaded_langs() or DEFAULT_LANGS
        raw = langs_to_raw(langs)
        ProcessorService.initialize(raw)

        for analyzer in ANALYZERS:
            if analyzer not in INITIALIZED:
                TYPE_ANALYZERS[analyzer].initialize()
                INITIALIZED.add(analyzer)

        self.raw = RawProcessor()
        for analyzer in select_analyzers(self.analyzers):
            self.raw.add_analyzer(analyzer)

    def __call__(self, text):
        text = preprocess(text)
        sofa = SourceOfAnalysis(text)
        raw = self.raw.process(sofa)
        return convert_result(text, raw)

    def __repr__(self):
        return 'Processor([{analyzers}])'.format(
            analyzers=', '.join(self.analyzers)
        )
