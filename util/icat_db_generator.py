from abc import ABC, abstractmethod
import argparse
import datetime
import enum
from multiprocessing import Process

from faker import Faker
from icat.client import Client
from icat.query import Query

from datagateway_api.src.common.config import Config

parser = argparse.ArgumentParser()
parser.add_argument(
    "--seed",
    "-s",
    dest="seed",
    help="Provide seed for random and faker",
    type=int,
    default=1,
)
parser.add_argument(
    "--years",
    "-y",
    dest="years",
    help="Provide number of years to generate",
    type=int,
    default=5,
)
args = parser.parse_args()
SEED = args.seed
YEARS = args.years  # 4 Cycles per years generated
faker = Faker()
Faker.seed(SEED)


def get_date_time():
    """
    Generates a datetime
    :return: the datetime
    """
    return faker.date_time_between_dates(
        datetime_start=datetime.datetime(2000, 10, 4),
        datetime_end=datetime.datetime(2019, 10, 5),
    )


def get_start_date(i):
    """
    Generates a datetime from a number i
    :param i:
    :return:
    """
    return datetime.datetime(
        2000 + i // 4, ((i + 1) * (i + 1)) % 11 + 1, ((i + 1) * (i + 2) % 28 + 1),
    )


def get_end_date(i):
    return datetime.datetime(
        2000 + i // 4, (((i + 1) * (i + 2)) % 11) + 1, ((i + 1) ** 2) % 28 + 1,
    )


def apply_common_parameter_attributes(entity, i, client):
    if entity.type.valueType == "NUMERIC":
        entity.numericValue = faker.random_int(
            entity.type.minimumNumericValue, entity.type.maximumNumericValue - 1,
        )

    if entity.type.valueType == "DATE_AND_TIME":
        entity.dateTimeValue = get_start_date(i)

    if entity.type.valueType == "STRING":
        entity.stringValue = client.search(
            Query(
                client,
                "PermissibleStringValue",
                conditions={"type.id": f"= '{entity.type.id}'"},
            ),
        )[0].value

    entity.error = faker.random_int(0, 42341)
    entity.rangeBottom = faker.random_int(1, 50)
    entity.rangeTop = faker.random_int(50, 101)


def icat_client():
    client = Client(
        Config.config.datagateway_api.icat_url,
        checkCert=Config.config.datagateway_api.icat_check_cert,
    )
    client.login(
        Config.config.test_mechanism, Config.config.test_user_credentials.dict(),
    )
    return client


class Generator(ABC):
    client = icat_client()

    @property
    @abstractmethod
    def tier(self):
        pass

    @property
    @abstractmethod
    def amount(self):
        pass

    @abstractmethod
    def generate(self):
        pass


class FacilityGenerator(Generator):
    tier = 0
    amount = 1

    def generate(self):
        facility = self.client.new("facility")
        facility.daysUntilRelease = 10
        facility.description = "Lorem ipsum light source"
        facility.name = "LILS"
        facility.create()


class DataCollectionGenerator(Generator):
    tier = 0
    amount = 100

    def generate(self):
        for i in range(1, self.amount):
            DataCollectionGenerator.generate_data_collection(self, i)

    def generate_data_collection(self, i):
        data_collection = self.client.new("dataCollection")
        data_collection.doi = faker.isbn10(separator="-")
        data_collection.create()


class FundingReferenceGenerator(Generator):
    tier = 0
    amount = 100

    def generate(self):
        for i in range(1, self.amount):
            FundingReferenceGenerator.generate_funding_reference(self, i)

    def generate_funding_reference(self, i):
        funding_reference = self.client.new("fundingReference")
        funding_reference.funderIdentifier = faker.ssn()
        funding_reference.funderName = faker.company()
        funding_reference.awardNumber = faker.isbn10(separator="")
        funding_reference.awardTitle = faker.text()
        funding_reference.create()


class TechniqueGenerator(Generator):
    tier = 0
    amount = 100

    def generate(self):
        for i in range(1, self.amount):
            TechniqueGenerator.generate_technique(self, i)

    def generate_technique(self, i):
        technique = self.client.new("technique")
        technique.pid = faker.word()
        technique.description = faker.text()
        technique.name = faker.text()
        technique.create()


class ApplicationGenerator(Generator):
    tier = 1
    amount = 80

    def generate(self):
        for i in range(1, self.amount):
            ApplicationGenerator.generate_applications(self, i)

    def generate_applications(self, i):
        tablename = "APPLICATION"
        application = self.client.new("application")
        application.name = f"{tablename} {i}"
        application.version = faker.random_int(1, 4)
        application.facility = self.client.get("Facility", 1)
        application.create()


class DatasetTypeGenerator(Generator):
    tier = 1
    amount = 4

    def generate(self):
        for i in range(1, self.amount):
            DatasetTypeGenerator.generate_dataset_type(self, i)

    def generate_dataset_type(self, i):
        tablename = "DATASETTYPE"
        dataset_type = self.client.new("datasetType")
        dataset_type.name = f"{tablename} {i}"
        dataset_type.description = faker.text()
        dataset_type.facility = self.client.get("Facility", 1)
        dataset_type.create()


class FacilityCycleGenerator(Generator):
    tier = 1
    amount = 4 * YEARS  # This gives 4 per year for 20 years

    def generate(self):
        for i in range(1, self.amount):
            FacilityCycleGenerator.generate_facility_cycle(self, i)

    def generate_facility_cycle(self, i):
        facility_cycle = self.client.new("facilityCycle")
        facility_cycle.description = faker.text()
        # overwrite the name with a more suitable one
        k = i % 4 + 1  # This will give a repeated 1, 2, 3, 4 for 4 cycles per year
        year = 2000 + i // 4
        facility_cycle.name = f"{year} cycle {k}"
        facility_cycle.startDate = datetime.datetime(year, 2 * k, k)
        facility_cycle.endDate = datetime.datetime(year, 2 * k + 3, 5 * k)
        facility_cycle.facility = self.client.get("Facility", 1)
        facility_cycle.create()


class SampleTypeGenerator(Generator):
    tier = 1
    amount = 80

    def generate(self):

        for i in range(1, self.amount):
            SampleTypeGenerator.generate_sample_type(self, i)

    def generate_sample_type(self, i):
        tablename = "SAMPLETYPE"
        sample_type = self.client.new("sampleType")
        sample_type.name = f"{tablename} {i}"
        sample_type.molecularFormula = faker.random_int(43, 13323)
        sample_type.safetyInformation = faker.text()
        sample_type.facility = self.client.get("Facility", 1)
        sample_type.create()


class InstrumentGenerator(Generator):
    tier = 2
    amount = 15

    def generate(self):
        for i in range(1, self.amount):
            InstrumentGenerator.generate_instruments(self, i)

    def generate_instruments(self, i):
        tablename = "INSTRUMENT"
        instrument = self.client.new("instrument")
        instrument.name = f"{tablename} {i}"
        instrument.description = faker.text()
        instrument.fullName = faker.text()
        instrument.url = faker.url()
        instrument.type = str(i)
        instrument.facility = self.client.get("Facility", 1)
        instrument.create()


class UserGenerator(Generator):
    tier = 2
    amount = 500

    def generate(self):
        for i in range(1, self.amount):
            UserGenerator.generate_users(self, i)

    def generate_users(self, i):
        user = self.client.new("user")
        user.email = faker.ascii_email()
        user.name = faker.first_name() + f"{i}"
        user.fullName = faker.name()
        user.orcidId = faker.random_int(2332, 24242)
        user.create()


class DatafileFormatGenerator(Generator):
    tier = 1
    amount = 10

    def generate(self):
        for i in range(1, self.amount):
            DatafileFormatGenerator.generate_datafile_format(self, i)

    def generate_datafile_format(self, i):
        tablename = "DATAFILEFORMAT"
        datafile_format = self.client.new("datafileFormat")
        datafile_format.name = f"{tablename} {i}"
        datafile_format.description = faker.text()
        datafile_format.version = faker.random_int(1, 14)
        datafile_format.facility = self.client.get("Facility", 1)
        datafile_format.create()


class InvestigationTypeGenerator(Generator):
    tier = 1
    amount = 4

    def generate(self):
        for i in range(1, self.amount):
            InvestigationTypeGenerator.generate_investigation_type(self, i)

    def generate_investigation_type(self, i):
        tablename = "INVESTIGATIONTYPE"
        investigation_type = self.client.new("investigationType")
        investigation_type.facility = self.client.get("Facility", 1)
        investigation_type.name = f"{tablename} {i}"
        investigation_type.description = faker.text()
        investigation_type.create()


class GroupingGenerator(Generator):
    tier = 2
    amount = 30

    def generate(self):
        for i in range(1, self.amount):
            GroupingGenerator.generate_groupings(self, i)

    def generate_groupings(self, i):
        tablename = "GROUPING"
        grouping = self.client.new("grouping")
        grouping.name = f"{tablename} {i}"
        grouping.create()


class InvestigationGenerator(Generator):
    tier = 2
    amount = 3 * FacilityCycleGenerator.amount  # 3 Investigations per cycle (60)

    def generate(self):
        for i in range(1, self.amount):
            InvestigationGenerator.generate_investigations(self, i)

    def generate_investigations(self, i):
        tablename = "INVESTIGATION"
        investigation = self.client.new("investigation")
        investigation.name = f"{tablename} {i}"
        investigation.doi = faker.isbn10(separator="-")
        k = i % 4 + 1
        year = 2000 + (i % 80) // 4
        investigation.startDate = datetime.datetime(year, 2 * k, k + 1)
        investigation.endDate = datetime.datetime(year, 2 * k + 3, 5 * k - 1)
        investigation.releaseDate = get_end_date(i)
        investigation.summary = faker.text()
        investigation.title = faker.text()
        investigation.visitId = faker.random_int(1, 100)
        investigation.type = self.client.get(
            "InvestigationType",
            faker.random_int(1, InvestigationTypeGenerator.amount - 1),
        )
        investigation.facility = self.client.get("Facility", 1)
        investigation.create()


class InvestigationUserGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            InvestigationUserGenerator.generate_investigation_user(self, i)

    def generate_investigation_user(self, i):
        investigation_user = self.client.new("investigationUser")
        investigation_user.role = ["PI", "CI"][faker.random_int(0, 1)]
        investigation_user.investigation = self.client.get("Investigation", i)
        investigation_user.user = self.client.get(
            "User", faker.random_int(1, UserGenerator.amount - 1),
        )
        investigation_user.create()


class InstrumentScientistGenerator(Generator):
    tier = 3
    amount = InstrumentGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            InstrumentScientistGenerator.generate_instrument_scientist(self, i)

    def generate_instrument_scientist(self, i):
        instrument_scientist = self.client.new("instrumentScientist")
        instrument_scientist.instrument = self.client.get("Instrument", i)
        instrument_scientist.user = self.client.get(
            "User", faker.random_int(1, UserGenerator.amount - 1),
        )
        instrument_scientist.create()


class InvestigationInstrumentGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount  # Must equal number of investigations

    def generate(self):
        for i in range(1, self.amount):
            InvestigationInstrumentGenerator.generate_investigation_instrument(self, i)

    def generate_investigation_instrument(self, i):
        investigation_instrument = self.client.new("investigationInstrument")
        investigation_instrument.investigation = self.client.get("Investigation", i)
        investigation_instrument.instrument = self.client.get(
            "Instrument", faker.random_int(1, InstrumentGenerator.amount - 1),
        )
        investigation_instrument.create()


class SampleGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            SampleGenerator.generate_sample(self, i)

    def generate_sample(self, i):
        tablename = "SAMPLE"
        sample = self.client.new("sample")
        sample.name = f"{tablename} {i}"
        sample.investigation = self.client.get("Investigation", i)
        sample.type = self.client.get(
            "SampleType", faker.random_int(1, SampleTypeGenerator.amount - 1),
        )
        sample.create()


class UserGroupGenerator(Generator):
    tier = 3
    amount = UserGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            UserGroupGenerator.generate_user_groups(self, i)

    def generate_user_groups(self, i):
        user_group = self.client.new("userGroup")
        user_group.grouping = self.client.get(
            "Grouping", faker.random_int(1, GroupingGenerator.amount - 1),
        )
        user_group.user = self.client.get("User", i)
        user_group.create()


class StudyGenerator(Generator):
    tier = 3
    amount = UserGenerator.amount
    pid_faker = Faker()
    pid_faker.seed_instance(SEED)

    def generate(self):
        for i in range(1, self.amount):
            StudyGenerator.generate_studies(self, i)

    def generate_studies(self, i):
        tablename = "STUDY"
        study = self.client.new("study")
        study.name = f"{tablename} {i}"
        study.description = faker.text()
        study.startDate = get_start_date(i)
        study.endDate = get_end_date(i)
        study.status = faker.random_int(0, 1)
        study.pid = StudyGenerator.pid_faker.isbn10(separator="-")
        study.user = self.client.get("User", i)
        study.create()


class InvestigationGroupGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            InvestigationGroupGenerator.generate_investigation_group(self, i)

    def generate_investigation_group(self, i):
        investigation_group = self.client.new("investigationGroup")
        investigation_group.role = faker.text() + str(i)
        investigation_group.grouping = self.client.get(
            "Grouping", faker.random_int(1, GroupingGenerator.amount - 1),
        )
        investigation_group.investigation = self.client.get("Investigation", i)
        investigation_group.create()


class KeywordGenerator(Generator):
    tier = 3
    amount = 500
    keywords = []

    def generate(self):
        for i in range(1, self.amount):
            KeywordGenerator.generate_keyword(i)
        self.client.createMany(self.keywords)

    @classmethod
    def generate_keyword(cls, i):
        keyword = cls.client.new("keyword")
        keyword.name = faker.word() + str(i)
        keyword.investigation = cls.client.get(
            "Investigation", faker.random_int(1, InvestigationGenerator.amount - 1),
        )
        cls.keywords.append(keyword)


class PublicationGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount * 3

    def generate(self):
        for i in range(1, self.amount):
            PublicationGenerator.generate_publication(self, i)

    def generate_publication(self, i):
        publication = self.client.new("publication")
        publication.doi = faker.isbn10(separator="-")
        publication.fullReference = faker.text()
        publication.repository = faker.uri()
        publication.repositoryId = faker.random_int(1, 23232234)
        publication.url = faker.url()
        publication.investigation = self.client.get(
            "Investigation", i % (InvestigationGenerator.amount - 1) + 1,
        )
        publication.create()


class ParameterTypeGenerator(Generator):
    tier = 3
    amount = 50

    class ValueTypeEnum(enum.Enum):
        DATE_AND_TIME = 0
        NUMERIC = 1
        STRING = 2

    def generate(self):
        for i in range(1, self.amount):
            ParameterTypeGenerator.generate_parameter_type(self, i)

    def generate_parameter_type(self, i):
        tablename = "PARAMETERTYPE"
        parameter_type = self.client.new("parameterType")
        parameter_type.name = f"{tablename} {i}"
        parameter_type.description = faker.text()
        parameter_type.applicableToDataCollection = 1
        parameter_type.applicableToDatafile = 1
        parameter_type.applicableToDataset = 1
        parameter_type.applicableToSample = 1
        parameter_type.applicableToInvestigation = 1
        parameter_type.enforced = faker.random_int(0, 1)
        parameter_type.maximumNumericValue = faker.random_int(10, 100)
        parameter_type.minimumNumericValue = faker.random_int(0, 9)
        parameter_type.units = f"unit {i}"
        parameter_type.unitsFullName = faker.word()
        parameter_type.valueType = list(self.ValueTypeEnum)[faker.random_int(0, 2)].name
        parameter_type.verified = faker.random_int(0, 1)
        parameter_type.facility = self.client.get("Facility", 1)
        parameter_type.create()


class InvestigationParameterGenerator(Generator):
    tier = 5
    amount = InvestigationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            InvestigationParameterGenerator.generate_investigation_parameter(self, i)

    def generate_investigation_parameter(self, i):
        investigation_parameter = self.client.new("investigationParameter")
        investigation_parameter.type = self.client.get(
            "ParameterType", faker.random_int(1, ParameterTypeGenerator.amount - 1),
        )
        apply_common_parameter_attributes(investigation_parameter, i, self.client)
        investigation_parameter.investigation = self.client.get("Investigation", i)
        investigation_parameter.create()


class ShiftGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            ShiftGenerator.generate_shift(self, i)

    def generate_shift(self, i):
        shift = self.client.new("shift")
        shift.startDate = get_start_date(i)
        shift.endDate = get_end_date(i)
        shift.comment = faker.text()
        shift.investigation = self.client.get("Investigation", i)
        shift.create()


class DataCollectionInvestigationGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            DataCollectionInvestigationGenerator.generate_data_collection_investigation(
                self, i,
            )

    def generate_data_collection_investigation(self, i):
        data_collection_investigation = self.client.new("dataCollectionInvestigation")
        data_collection_investigation.dataCollection = self.client.get(
            "DataCollection", faker.random_int(1, DataCollectionGenerator.amount - 1),
        )
        data_collection_investigation.investigation = self.client.get(
            "Investigation", i,
        )
        data_collection_investigation.create()


class InvestigationFacilityCycleGenerator(Generator):
    tier = 3
    amount = FacilityCycleGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            InvestigationFacilityCycleGenerator.generate_investigation_facility_cycle(
                self, i,
            )

    def generate_investigation_facility_cycle(self, i):
        investigation_facility_cycle = self.client.new("investigationFacilityCycle")
        investigation_facility_cycle.investigation = self.client.get(
            "Investigation", faker.random_int(1, InvestigationGenerator.amount - 1),
        )
        investigation_facility_cycle.facilityCycle = self.client.get("FacilityCycle", i)
        investigation_facility_cycle.create()


class InvestigationFundingGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            InvestigationFundingGenerator.generate_investigation_funding(self, i)

    def generate_investigation_funding(self, i):
        investigation_funding = self.client.new("investigationFunding")
        investigation_funding.funding = self.client.get(
            "FundingReference",
            faker.random_int(1, FundingReferenceGenerator.amount - 1),
        )
        investigation_funding.investigation = self.client.get("Investigation", i)
        investigation_funding.create()


class DataPublicationGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            DataPublicationGenerator().generate_data_publication(i)

    def generate_data_publication(self, i):
        data_publication = self.client.new("dataPublication")
        data_publication.title = faker.text()
        data_publication.description = faker.text()
        data_publication.pid = faker.isbn10(separator="-")
        data_publication.publicationDate = faker.date_between(
            start_date=datetime.datetime(2008, 1, 1),
            end_date=datetime.datetime(2023, 1, 1),
        )
        data_publication.subject = faker.words()
        data_publication.facility = self.client.get("Facility", 1)
        data_publication.content = self.client.get(
            "DataCollection", faker.random_int(1, DataCollectionGenerator.amount - 1),
        )

        data_publication.create()


class DataPublicationFundingGenerator(Generator):
    tier = 4
    amount = DataPublicationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            DataPublicationFundingGenerator.generate_data_publication_funding(self, i)

    def generate_data_publication_funding(self, i):
        data_publication_funding = self.client.new("dataPublicationFunding")
        data_publication_funding.funding = self.client.get(
            "FundingReference",
            faker.random_int(1, FundingReferenceGenerator.amount - 1),
        )
        data_publication_funding.dataPublication = self.client.get("DataPublication", i)
        data_publication_funding.create()


class DataPublicationDateGenerator(Generator):
    tier = 4
    amount = DataPublicationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            DataPublicationDateGenerator.generate_data_publication_date(self, i)

    def generate_data_publication_date(self, i):
        data_publication_date = self.client.new("dataPublicationDate")
        # Elements of list taken from https://support.datacite.org/docs/schema-40
        data_publication_date.dateType = faker.random_element(
            elements=(
                "Accepted",
                "Available",
                "Copyrighted",
                "Collected",
                "Created",
                "Issued",
                "Submitted",
                "Updated",
                "Valid",
            ),
        )
        data_publication_date.publication = self.client.get("DataPublication", i)
        data_publication_date.date = faker.date_between(
            start_date=datetime.datetime(2008, 1, 1),
            end_date=datetime.datetime(2023, 1, 1),
        )
        data_publication_date.create()


class DataPublicationTypeGenerator(Generator):
    tier = 4
    amount = 20

    def generate(self):
        for i in range(1, self.amount):
            DataPublicationTypeGenerator.generate_data_publication_type(self, i)

    def generate_data_publication_type(self, i):
        data_publication_type = self.client.new("dataPublicationType")
        data_publication_type.name = faker.word()
        data_publication_type.description = faker.text()
        data_publication_type.facility = self.client.get("Facility", 1)
        data_publication_type.create()


class DataPublicationUserGenerator(Generator):
    tier = 4
    amount = DataPublicationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            DataPublicationUserGenerator.generate_data_publication_user(self, i)

    def generate_data_publication_user(self, i):
        data_publication_user = self.client.new("dataPublicationUser")
        data_publication_user.orderKey = str(faker.random_int(1, 9))
        data_publication_user.user = self.client.get(
            "User", faker.random_int(1, UserGenerator.amount - 1),
        )
        data_publication_user.givenName = data_publication_user.user.fullName.split()[0]
        data_publication_user.fullName = data_publication_user.user.fullName
        data_publication_user.familyName = data_publication_user.fullName.split()[1]
        data_publication_user.contributorType = faker.random_element(
            elements=(
                "ContactPerson",
                "DataCollector",
                "DataCurator",
                "DataManager",
                "Distributor",
                "Editor",
                "Producer",
                "ProjectLeader",
                "ProjectManager",
                "ProjectMember",
                "RelatedPerson",
                "Researcher",
            ),
        )
        data_publication_user.email = data_publication_user.user.email
        data_publication_user.publication = self.client.get("DataPublication", i)
        data_publication_user.create()


class RelatedItemGenerator(Generator):
    tier = 4
    amount = DataPublicationGenerator.amount * 2

    def generate(self):
        for i in range(1, self.amount):
            RelatedItemGenerator.generate_related_item(self, i)

    def generate_related_item(self, i):
        related_item = self.client.new("relatedItem")
        related_item.identifier = faker.isbn10(separator="-")
        related_item.relationType = faker.random_element(
            elements=(
                "IsCitedBy",
                "Cites",
                "IsPublishedIn",
                "IsReferencedBy",
                "References",
                "IsReviewedBy",
                "Reviews",
                "IsObseletedBy",
            ),
        )
        related_item.relatedItemType = faker.random_element(
            elements=(
                "Book",
                "ComputationalNotebook",
                "ConferencePaper",
                "DataPaper",
                "Dataset",
                "Dissertation",
                "Model",
                "PeerReview",
                "Preprint",
                "Report",
                "Text",
                "Other",
            ),
        )
        related_item.title = faker.text()
        related_item.fullReference = faker.text()
        related_item.publication = self.client.get(
            "DataPublication", i % (DataPublicationGenerator.amount - 1) + 1,
        )
        related_item.create()


class StudyInvestigationGenerator(Generator):
    tier = 4
    amount = InvestigationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            StudyInvestigationGenerator.generate_study_investigation(self, i)

    def generate_study_investigation(self, i):
        study_investigation = self.client.new("studyInvestigation")
        study_investigation.investigation = self.client.get("Investigation", i)
        study_investigation.study = self.client.get(
            "Study", faker.random_int(1, StudyGenerator.amount - 1),
        )
        study_investigation.create()


class DatasetGenerator(Generator):
    tier = 4
    amount = InvestigationGenerator.amount * 2  # Two Datasets per investigation (120)

    def generate(self):
        for i in range(1, self.amount):
            DatasetGenerator.generate_dataset(self, i)

    def generate_dataset(self, i):
        tablename = "DATASET"
        dataset = self.client.new("dataset")
        dataset.name = f"{tablename} {i}"
        dataset.description = faker.text()
        dataset.fileCount = 15
        dataset.doi = faker.isbn10(separator="-")
        dataset.startDate = get_start_date(i)
        dataset.endDate = get_end_date(i)
        dataset.complete = faker.random_int(0, 1)
        dataset.location = faker.file_path()
        investigation_id = i % InvestigationGenerator.amount
        dataset.investigation = self.client.get(
            "Investigation",
            investigation_id
            if investigation_id != 0
            else InvestigationGenerator.amount - 1,
        )
        sample_id = i % SampleGenerator.amount
        dataset.sample = self.client.get(
            "Sample", sample_id if sample_id != 0 else SampleGenerator.amount - 1,
        )
        dataset.type = self.client.get(
            "DatasetType", faker.random_int(1, DatasetTypeGenerator.amount - 1),
        )
        dataset.create()


class DatasetParameterGenerator(Generator):
    tier = 5
    amount = ParameterTypeGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            DatasetParameterGenerator.generate_dataset_parameter(self, i)

    def generate_dataset_parameter(self, i):
        dataset_param = self.client.new("datasetParameter")
        dataset_param.type = self.client.get("ParameterType", i)
        apply_common_parameter_attributes(dataset_param, i, self.client)
        dataset_param.dataset = self.client.get(
            "Dataset", faker.random_int(1, DatasetGenerator.amount - 1),
        )
        dataset_param.create()


class DatasetTechniqueGenerator(Generator):
    tier = 5
    amount = TechniqueGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            DatasetTechniqueGenerator.generate_dataset_technique(self, i)

    def generate_dataset_technique(self, i):
        dataset_technique = self.client.new("datasetTechnique")
        dataset_technique.dataset = self.client.get(
            "Dataset", faker.random_int(1, DatasetGenerator.amount - 1),
        )
        dataset_technique.technique = self.client.get("Technique", i)
        dataset_technique.create()


class DatasetInstrumentGenerator(Generator):
    tier = 5
    amount = InstrumentGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            DatasetInstrumentGenerator.generate_dataset_instrument(self, i)

    def generate_dataset_instrument(self, i):
        dataset_instrument = self.client.new("datasetInstrument")
        dataset_instrument.dataset = self.client.get(
            "Dataset", faker.random_int(1, DatasetGenerator.amount - 1),
        )
        dataset_instrument.instrument = self.client.get("Instrument", i)
        dataset_instrument.create()


class DatafileGenerator(Generator):
    tier = 5
    amount = DatasetGenerator.amount * 15  # 15 files per Dataset (1800)
    datafiles = []

    def generate(self):
        for i in range(1, self.amount):
            DatafileGenerator.generate_datafile(i)
        # timer = datetime.datetime.now()
        # with multiprocessing.get_context("spawn").Pool() as pool:
        #    pool.map(DatafileGenerator.generate_datafile, range(1, self.amount))

    @classmethod
    def generate_datafile(cls, i):
        tablename = "DATAFILE"
        datafile = cls.client.new("datafile")
        datafile.name = f"{tablename} {i}"
        datafile.description = faker.text()
        datafile.doi = faker.isbn10(separator="-")
        datafile.checksum = faker.md5()
        datafile.datafileCreateTime = datafile.createTime
        datafile.datafileModTime = datafile.modTime
        datafile.fileSize = faker.random_int(123, 213123121)
        datafile.datafileFormat = cls.client.get(
            "DatafileFormat", faker.random_int(1, DatafileFormatGenerator.amount - 1),
        )
        datafile.dataset = cls.client.get(
            "Dataset", i % (DatasetGenerator.amount - 1) + 1,
        )
        datafile.name = f"Datafile {i}"
        datafile.location = faker.file_path(depth=2, category="image")
        datafile.create()


class PermissibleStringValueGenerator(Generator):
    tier = 4
    amount = 50

    def generate(self):
        for i in range(1, self.amount):
            PermissibleStringValueGenerator.generate_permissible_string_value(self, i)

    def generate_permissible_string_value(self, i):
        permissible_string_value = self.client.new("permissibleStringValue")
        permissible_string_value.value = f"value {i}"
        permissible_string_value.type = self.client.get("ParameterType", i)
        permissible_string_value.create()


class DataCollectionParameterGenerator(Generator):
    tier = 5
    amount = DataCollectionGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            DataCollectionParameterGenerator.generate_data_collection_parameter(self, i)

    def generate_data_collection_parameter(self, i):
        datacollection_parameter = self.client.new("dataCollectionParameter")
        datacollection_parameter.type = self.client.get(
            "ParameterType", faker.random_int(1, ParameterTypeGenerator.amount - 1),
        )
        apply_common_parameter_attributes(datacollection_parameter, i, self.client)
        datacollection_parameter.dataCollection = self.client.get("DataCollection", i)
        datacollection_parameter.create()


class SampleParameterGenerator(Generator):
    tier = 5
    amount = SampleGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            SampleParameterGenerator.generate_sample_parameter(self, i)

    def generate_sample_parameter(self, i):
        sample_parameter = self.client.new("sampleParameter")
        sample_parameter.type = self.client.get(
            "ParameterType", faker.random_int(1, ParameterTypeGenerator.amount - 1),
        )
        apply_common_parameter_attributes(sample_parameter, i, self.client)
        sample_parameter.sample = self.client.get("Sample", i)
        sample_parameter.create()


class AffiliationGenerator(Generator):
    tier = 5
    amount = DataPublicationUserGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            AffiliationGenerator.generate_affiliation(self, i)

    def generate_affiliation(self, i):
        affiliation = self.client.new("affiliation")
        affiliation.fullReference = faker.text()
        affiliation.pid = faker.isbn10(separator="-")
        affiliation.name = faker.text()
        affiliation.user = self.client.get("DataPublicationUser", i)
        affiliation.create()


class DatafileParameterGenerator(Generator):
    tier = 6
    amount = DatafileGenerator.amount  # 1800

    def generate(self):
        for i in range(1, self.amount):
            DatafileParameterGenerator.generate_datafile_parameter(i)

    @classmethod
    def generate_datafile_parameter(cls, i):
        datafile_param = cls.client.new("datafileParameter")
        datafile_param.type = cls.client.get(
            "ParameterType", faker.random_int(1, ParameterTypeGenerator.amount - 1),
        )
        apply_common_parameter_attributes(datafile_param, i, cls.client)
        datafile_param.datafile = cls.client.get("Datafile", i)
        datafile_param.create()


def generate_all(i, generators, client):
    processes = []
    for generator in generators:
        if generator.tier == i:
            print(
                f"Adding {type(generator).__name__.replace('Generator', '') + 's'} of"
                f" tier {generator.tier}",
            )
            processes.append(Process(target=generator.generate))

    [process.start() for process in processes]
    [process.join() for process in processes]
    print("Entities added")


def main():
    client = icat_client()
    start_time = datetime.datetime.now()
    generators = [generator() for generator in Generator.__subclasses__()]
    tiers = 7
    for i in range(tiers):
        generate_all(i, generators, client)

    print(
        f"Added {sum(generator.amount for generator in generators)} entities in"
        f" {datetime.datetime.now() - start_time}",
    )


if __name__ == "__main__":
    main()
