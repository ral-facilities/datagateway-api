import argparse
import datetime
from abc import ABC, abstractmethod
from multiprocessing import Process, Pool
from random import randrange, seed, choice

from faker import Faker

from common.database import models
from common.database.session_manager import session_manager

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
    default=20,
)
args = parser.parse_args()
SEED = args.seed
YEARS = args.years  # 4 Cycles per years generated
faker = Faker()
faker.seed(SEED)
seed(a=SEED)

session = session_manager.get_icat_db_session()


def post_entity(entity):
    """
    Given an entity, insert it into the ICAT DB
    :param entity:  The entity to be inserted
    :return: None
    """
    session.add(entity)
    session.commit()
    session.close()


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
        2000 + i // 4, ((i + 1) * (i + 1)) % 11 + 1, ((i + 1) * (i + 2) % 28 + 1)
    )


def get_end_date(i):
    return datetime.datetime(
        2000 + i // 4, (((i + 1) * (i + 2)) % 11) + 1, ((i + 1) ** 2) % 28 + 1
    )


def apply_common_attributes(entity, iterator):
    entity.CREATE_ID = "user"
    entity.MOD_ID = "user"
    entity.MOD_TIME = get_date_time()
    entity.CREATE_TIME = get_date_time()
    entity.NAME = f"{entity.__tablename__} {iterator}"
    entity.DESCRIPTION = faker.text()
    entity.FACILITY_ID = 1
    entity.STARTDATE = get_start_date(iterator)
    entity.ENDDATE = get_end_date(iterator)
    entity.DOI = faker.isbn10(separator="-")


def apply_common_parameter_attributes(entity, i):
    entity.DATETIME_VALUE = get_start_date(i)
    entity.ERROR = randrange(42342)
    entity.NUMERIC_VALUE = randrange(352352)
    entity.RANGEBOTTOM = randrange(1, 50)
    entity.RANGETOP = randrange(50, 101)
    entity.STRING_VALUE = faker.word() + str(i)


class Generator(ABC):
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

    def pool_map(self, function):
        pool = Pool()
        pool.map(function, range(1, self.amount))
        pool.close()


class FacilityGenerator(Generator):
    tier = 0
    amount = 1

    def generate(self):
        facility = models.FACILITY()
        facility.CREATE_ID = "user"
        facility.MOD_ID = "user"
        facility.MOD_TIME = get_date_time()
        facility.CREATE_TIME = get_date_time()
        facility.DAYSUNTILRELEASE = 10
        facility.DESCRIPTION = "Lorem ipsum light source"
        facility.NAME = "LILS"
        post_entity(facility)


class DataCollectionGenerator(Generator):
    tier = 0
    amount = 1000

    def generate(self):
        self.pool_map(DataCollectionGenerator.generate_data_collection)

    @staticmethod
    def generate_data_collection(i):
        data_collection = models.DATACOLLECTION()
        apply_common_attributes(data_collection, i)
        post_entity(data_collection)


class ApplicationGenerator(Generator):
    tier = 1
    amount = 80

    def generate(self):
        self.pool_map(ApplicationGenerator.generate_applications)

    @staticmethod
    def generate_applications(i):
        application = models.APPLICATION()
        apply_common_attributes(application, i)
        application.VERSION = randrange(1, 4)
        post_entity(application)


class DatasetTypeGenerator(Generator):
    tier = 1
    amount = 4

    def generate(self):
        self.pool_map(DatasetTypeGenerator.generate_dataset_type)

    @staticmethod
    def generate_dataset_type(i):
        dataset_type = models.DATASETTYPE()
        apply_common_attributes(dataset_type, i)
        post_entity(dataset_type)


class FacilityCycleGenerator(Generator):
    tier = 1
    amount = 4 * YEARS  # This gives 4 per year for 20 years

    def generate(self):
        self.pool_map(FacilityCycleGenerator.generate_facility_cycle)

    @staticmethod
    def generate_facility_cycle(i):
        facility_cycle = models.FACILITYCYCLE()
        apply_common_attributes(facility_cycle, i)
        # overwrite the name with a more suitable one
        k = i % 4 + 1  # This will give a repeated 1, 2, 3, 4 for 4 cycles per year
        year = 2000 + i // 4
        facility_cycle.NAME = f"{year} cycle {k}"
        facility_cycle.STARTDATE = datetime.datetime(year, 2 * k, k)
        facility_cycle.ENDDATE = datetime.datetime(year, 2 * k + 3, 5 * k)
        post_entity(facility_cycle)


class SampleTypeGenerator(Generator):
    tier = 1
    amount = 80

    def generate(self):
        self.pool_map(SampleTypeGenerator.generate_sample_type)

    @staticmethod
    def generate_sample_type(i):
        sample_type = models.SAMPLETYPE()
        apply_common_attributes(sample_type, i)
        sample_type.MOLECULARFORMULA = randrange(43, 13323)
        sample_type.SAFETYINFORMATION = faker.text()
        post_entity(sample_type)


class InstrumentGenerator(Generator):
    tier = 2
    amount = 15

    def generate(self):
        self.pool_map(InstrumentGenerator.generate_instruments)

    @staticmethod
    def generate_instruments(i):
        instrument = models.INSTRUMENT()
        apply_common_attributes(instrument, i)
        instrument.FULLNAME = faker.text()
        instrument.URL = faker.url()
        instrument.TYPE = str(i)
        post_entity(instrument)


class UserGenerator(Generator):
    tier = 2
    amount = 500

    def generate(self):
        self.pool_map(UserGenerator.generate_users)

    @staticmethod
    def generate_users(i):
        user = models.USER()
        apply_common_attributes(user, i)
        user.EMAIL = faker.ascii_email()
        user.NAME = faker.first_name() + f"{i}"
        user.FULLNAME = faker.name()
        user.ORCIDID = randrange(2332, 24242)
        post_entity(user)


class DatafileFormatGenerator(Generator):
    tier = 1
    amount = 10

    def generate(self):
        self.pool_map(DatafileFormatGenerator.generate_datafile_format)

    @staticmethod
    def generate_datafile_format(i):
        datafile_format = models.DATAFILEFORMAT()
        apply_common_attributes(datafile_format, i)
        datafile_format.VERSION = randrange(1, 14)
        post_entity(datafile_format)


class InvestigationTypeGenerator(Generator):
    tier = 1
    amount = 4

    def generate(self):
        self.pool_map(InvestigationTypeGenerator.generate_investigation_type)

    @staticmethod
    def generate_investigation_type(i):
        investigation_type = models.INVESTIGATIONTYPE()
        apply_common_attributes(investigation_type, i)
        post_entity(investigation_type)


class GroupingGenerator(Generator):
    tier = 2
    amount = 30

    def generate(self):
        self.pool_map(GroupingGenerator.generate_groupings)

    @staticmethod
    def generate_groupings(i):
        grouping = models.GROUPING()
        apply_common_attributes(grouping, i)
        post_entity(grouping)


class InvestigationGenerator(Generator):
    tier = 2
    amount = 3 * FacilityCycleGenerator.amount  # 60 Investigations per cycle

    def generate(self):
        self.pool_map(InvestigationGenerator.generate_investigations)

    @staticmethod
    def generate_investigations(i):
        investigation = models.INVESTIGATION()
        apply_common_attributes(investigation, i)
        k = i % 4 + 1
        year = 2000 + (i % 80) // 4
        investigation.STARTDATE = datetime.datetime(year, 2 * k, k + 1)
        investigation.ENDDATE = datetime.datetime(year, 2 * k + 3, 5 * k - 1)
        investigation.RELEASEDATE = get_end_date(i)
        investigation.SUMMARY = faker.text()
        investigation.TITLE = faker.text()
        investigation.VISIT_ID = randrange(1, 100)
        investigation.TYPE_ID = randrange(1, 4)
        post_entity(investigation)


class InvestigationUserGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount

    def generate(self):
        self.pool_map(InvestigationUserGenerator.generate_investigation_user)

    @staticmethod
    def generate_investigation_user(i):
        investigation_user = models.INVESTIGATIONUSER()
        apply_common_attributes(investigation_user, i)
        investigation_user.ROLE = ["PI", "CI"][randrange(2)]
        investigation_user.INVESTIGATION_ID = i
        investigation_user.USER_ID = randrange(1, UserGenerator.amount)
        post_entity(investigation_user)


class InstrumentScientistGenerator(Generator):
    tier = 3
    amount = InstrumentGenerator.amount

    def generate(self):
        self.pool_map(InstrumentScientistGenerator.generate_instrument_scientist)

    @staticmethod
    def generate_instrument_scientist(i):
        instrument_scientist = models.INSTRUMENTSCIENTIST()
        apply_common_attributes(instrument_scientist, i)
        instrument_scientist.INSTRUMENT_ID = i
        instrument_scientist.USER_ID = randrange(1, UserGenerator.amount)
        post_entity(instrument_scientist)


class InvestigationInstrumentGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount  # Must equal number of investigations

    def generate(self):
        self.pool_map(
            InvestigationInstrumentGenerator.generate_investigation_instrument
        )

    @staticmethod
    def generate_investigation_instrument(i):
        investigation_instrument = models.INVESTIGATIONINSTRUMENT()
        apply_common_attributes(investigation_instrument, i)
        investigation_instrument.INVESTIGATION_ID = i
        investigation_instrument.INSTRUMENT_ID = randrange(1, 15)
        post_entity(investigation_instrument)


class SampleGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount

    def generate(self):
        self.pool_map(SampleGenerator.generate_sample)

    @staticmethod
    def generate_sample(i):
        sample = models.SAMPLE()
        apply_common_attributes(sample, i)
        sample.INVESTIGATION_ID = i
        sample.SAMPLETYPE_ID = randrange(1, SampleTypeGenerator.amount)
        post_entity(sample)


class UserGroupGenerator(Generator):
    tier = 3
    amount = UserGenerator.amount

    def generate(self):
        self.pool_map(UserGroupGenerator.generate_user_groups)

    @staticmethod
    def generate_user_groups(i):
        user_group = models.USERGROUP()
        apply_common_attributes(user_group, i)
        user_group.GROUP_ID = randrange(1, GroupingGenerator.amount)
        user_group.USER_ID = i
        post_entity(user_group)


class StudyGenerator(Generator):
    tier = 3
    amount = UserGenerator.amount

    def generate(self):
        self.pool_map(StudyGenerator.generate_studies)

    @staticmethod
    def generate_studies(i):
        study = models.STUDY()
        apply_common_attributes(study, i)
        study.STARTDATE = get_start_date(i)
        study.STATUS = randrange(2)
        study.USER_ID = i
        post_entity(study)


class InvestigationGroupGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount

    def generate(self):
        self.pool_map(InvestigationGroupGenerator.generate_investigation_group)

    @staticmethod
    def generate_investigation_group(i):
        investigation_group = models.INVESTIGATIONGROUP()
        apply_common_attributes(investigation_group, i)
        investigation_group.ROLE = faker.text() + str(i)
        investigation_group.GROUP_ID = randrange(1, GroupingGenerator.amount)
        investigation_group.INVESTIGATION_ID = i
        post_entity(investigation_group)


class KeywordGenerator(Generator):
    tier = 3
    amount = 15000

    def generate(self):
        self.pool_map(KeywordGenerator.generate_keyword)

    @staticmethod
    def generate_keyword(i):
        keyword = models.KEYWORD()
        apply_common_attributes(keyword, i)
        keyword.NAME = faker.word() + str(i)
        keyword.INVESTIGATION_ID = randrange(1, InvestigationGenerator.amount)
        post_entity(keyword)


class PublicationGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount * 3

    def generate(self):
        self.pool_map(PublicationGenerator.generate_publication)

    @staticmethod
    def generate_publication(i):
        publication = models.PUBLICATION()
        apply_common_attributes(publication, i)
        publication.FULLREFERENCE = faker.text()
        publication.REPOSITORY = faker.uri()
        publication.REPOSITORYID = randrange(1, 23232234)
        publication.URL = faker.url()
        publication.INVESTIGATION_ID = i % (InvestigationGenerator.amount - 1) + 1
        post_entity(publication)


class ParameterTypeGenerator(Generator):
    tier = 3
    amount = 50

    def generate(self):
        self.pool_map(ParameterTypeGenerator.generate_parameter_type)

    @staticmethod
    def generate_parameter_type(i):
        parameter_type = models.PARAMETERTYPE()
        apply_common_attributes(parameter_type, i)
        parameter_type.APPLICABLETODATACOLLECTION = randrange(2)
        parameter_type.APPLICABLETODATAFILE = randrange(2)
        parameter_type.APPLICABLETODATASET = randrange(2)
        parameter_type.APPLICABLETOSAMPLE = randrange(2)
        parameter_type.ENFORCED = randrange(2)
        parameter_type.MAXIMUMNUMERICVALUE = randrange(10, 100)
        parameter_type.MAXIMUMNUMERICVALUE = randrange(10)
        parameter_type.UNITS = f"unit {i}"
        parameter_type.UNITSFULLNAME = faker.word()
        parameter_type.VALUETYPE = choice(list(models.PARAMETERTYPE.ValueTypeEnum))
        parameter_type.VERIFIED = randrange(2)
        post_entity(parameter_type)


class InvestigationParameterGenerator(Generator):
    tier = 4
    amount = InvestigationGenerator.amount

    def generate(self):
        self.pool_map(generate_investigation_parameter)


def generate_investigation_parameter(i):
    investigation_parameter = models.INVESTIGATIONPARAMETER()
    apply_common_attributes(investigation_parameter, i)
    apply_common_parameter_attributes(investigation_parameter, i)
    investigation_parameter.INVESTIGATION_ID = i
    investigation_parameter.PARAMETER_TYPE_ID = randrange(
        1, ParameterTypeGenerator.amount
    )
    post_entity(investigation_parameter)


class ShiftGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount

    def generate(self):
        self.pool_map(ShiftGenerator.generate_shift)

    @staticmethod
    def generate_shift(i):
        shift = models.SHIFT()
        apply_common_attributes(shift, i)
        shift.COMMENT = faker.text()
        shift.INVESTIGATION_ID = i
        post_entity(shift)


class StudyInvestigationGenerator(Generator):
    tier = 4
    amount = InvestigationGenerator.amount

    def generate(self):
        self.pool_map(StudyInvestigationGenerator.generate_study_investigation)

    @staticmethod
    def generate_study_investigation(i):
        study_investigation = models.STUDYINVESTIGATION()
        apply_common_attributes(study_investigation, i)
        study_investigation.INVESTIGATION_ID = i
        study_investigation.STUDY_ID = randrange(1, StudyGenerator.amount)
        post_entity(study_investigation)


class DatasetGenerator(Generator):
    tier = 4
    amount = InvestigationGenerator.amount * 2  # Two Datasets per investigation

    def generate(self):
        self.pool_map(DatasetGenerator.generate_dataset)

    @staticmethod
    def generate_dataset(i):
        dataset = models.DATASET()
        apply_common_attributes(dataset, i)
        dataset.COMPLETE = randrange(2)
        dataset.LOCATION = faker.file_path()
        investigation_id = i % InvestigationGenerator.amount
        dataset.INVESTIGATION_ID = (
            investigation_id
            if investigation_id != 0
            else InvestigationGenerator.amount - 1
        )
        sample_id = i % SampleGenerator.amount
        dataset.SAMPLE_ID = sample_id if sample_id != 0 else SampleGenerator.amount - 1
        dataset.TYPE_ID = randrange(1, DatasetTypeGenerator.amount)
        post_entity(dataset)


class DatasetParameterGenerator(Generator):
    tier = 5
    amount = ParameterTypeGenerator.amount

    def generate(self):
        self.pool_map(DatasetParameterGenerator.generate_dataset_parameter)

    @staticmethod
    def generate_dataset_parameter(i):
        dataset_param = models.DATASETPARAMETER()
        apply_common_attributes(dataset_param, i)
        apply_common_parameter_attributes(dataset_param, i)
        dataset_param.DATASET_ID = randrange(1, DatasetGenerator.amount)
        dataset_param.PARAMETER_TYPE_ID = i
        post_entity(dataset_param)


class DatafileGenerator(Generator):
    tier = 5
    amount = DatasetGenerator.amount * 55  # 55 files per Dataset

    def generate(self):
        self.pool_map(DatafileGenerator.generate_datafile)

    @staticmethod
    def generate_datafile(i):
        datafile = models.DATAFILE()
        apply_common_attributes(datafile, i % 19)
        datafile.CHECKSUM = faker.md5()
        datafile.DATAFILECREATETIME = datafile.CREATE_TIME
        datafile.DATAFILEMODTIME = datafile.MOD_TIME
        datafile.FILESIZE = randrange(123, 213123121)
        datafile.DATAFILEFORMAT_ID = randrange(1, DatafileFormatGenerator.amount)
        datafile.DATASET_ID = i % (DatasetGenerator.amount - 1) + 1
        datafile.NAME = f"Datafile {i}"
        datafile.LOCATION = faker.file_path(depth=2, category="image")
        post_entity(datafile)


class PermissibleStringValueGenerator(Generator):
    tier = 4
    amount = 50

    def generate(self):
        self.pool_map(generate_permissible_string_value)


def generate_permissible_string_value(i):
    permissible_string_value = models.PERMISSIBLESTRINGVALUE()
    apply_common_attributes(permissible_string_value, i)
    permissible_string_value.VALUE = f"value {i}"
    permissible_string_value.PARAMETERTYPE_ID = i
    post_entity(permissible_string_value)


class DataCollectionParameterGenerator(Generator):
    tier = 4
    amount = DataCollectionGenerator.amount

    def generate(self):
        self.pool_map(
            DataCollectionParameterGenerator.generate_data_collection_parameter
        )

    @staticmethod
    def generate_data_collection_parameter(i):
        datacollection_parameter = models.DATACOLLECTIONPARAMETER()
        apply_common_attributes(datacollection_parameter, i)
        apply_common_parameter_attributes(datacollection_parameter, i)
        datacollection_parameter.DATACOLLECTION_ID = i
        datacollection_parameter.PARAMETER_TYPE_ID = randrange(
            1, ParameterTypeGenerator.amount
        )
        post_entity(datacollection_parameter)


class SampleParameterGenerator(Generator):
    tier = 4
    amount = SampleGenerator.amount

    def generate(self):
        self.pool_map(SampleParameterGenerator.generate_sample_parameter)

    @staticmethod
    def generate_sample_parameter(i):
        sample_parameter = models.SAMPLEPARAMETER()
        apply_common_attributes(sample_parameter, i)
        apply_common_parameter_attributes(sample_parameter, i)
        sample_parameter.SAMPLE_ID = i
        sample_parameter.PARAMETER_TYPE_ID = randrange(1, ParameterTypeGenerator.amount)
        post_entity(sample_parameter)


class DatafileParameterGenerator(Generator):
    tier = 6
    amount = DatafileGenerator.amount

    def generate(self):
        self.pool_map(DatafileParameterGenerator.generate_datafile_parameter)

    @staticmethod
    def generate_datafile_parameter(i):
        datafile_param = models.DATAFILEPARAMETER()
        apply_common_attributes(datafile_param, i)
        apply_common_parameter_attributes(datafile_param, i)
        datafile_param.DATAFILE_ID = i
        datafile_param.PARAMETER_TYPE_ID = randrange(1, ParameterTypeGenerator.amount)
        post_entity(datafile_param)


def generate_all(i, generators):
    processes = []
    for generator in generators:
        if generator.tier == i:
            print(
                f"Adding {type(generator).__name__.replace('Generator', '') + 's'} of"
                f" tier {generator.tier}"
            )
            processes.append(Process(target=generator.generate))

    [process.start() for process in processes]
    [process.join() for process in processes]
    print("Entities added")


def main():
    start_time = datetime.datetime.now()
    generators = [generator() for generator in Generator.__subclasses__()]
    TIERS = 7
    for i in range(TIERS):
        generate_all(i, generators)

    print(
        f"Added {sum(generator.amount for generator in generators)} entities in"
        f" {datetime.datetime.now() - start_time}"
    )


if __name__ == "__main__":
    main()
