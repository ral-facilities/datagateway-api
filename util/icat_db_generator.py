from abc import ABC, abstractmethod
import argparse
import datetime
from multiprocessing import Process

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool

from datagateway_api.src.common.config import config
from datagateway_api.src.datagateway_api.database import models

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
Faker.seed(SEED)


engine = create_engine(
    config.datagateway_api.db_url, poolclass=QueuePool, pool_size=100, max_overflow=0,
)
session_factory = sessionmaker(engine)
session = scoped_session(session_factory)()


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
        2000 + i // 4, ((i + 1) * (i + 1)) % 11 + 1, ((i + 1) * (i + 2) % 28 + 1),
    )


def get_end_date(i):
    return datetime.datetime(
        2000 + i // 4, (((i + 1) * (i + 2)) % 11) + 1, ((i + 1) ** 2) % 28 + 1,
    )


def apply_common_attributes(entity, iterator):
    entity.createId = "user"
    entity.modId = "user"
    entity.modTime = get_date_time()
    entity.createTime = get_date_time()
    entity.name = f"{entity.__tablename__} {iterator}"
    entity.description = faker.text()
    entity.facilityID = 1
    entity.startDate = get_start_date(iterator)
    entity.endDate = get_end_date(iterator)
    entity.doi = faker.isbn10(separator="-")


def apply_common_parameter_attributes(entity, i):
    entity.dateTimeValue = get_start_date(i)
    entity.error = faker.random_int(0, 42341)
    entity.numericValue = faker.random_int(0, 352351)
    entity.rangeBottom = faker.random_int(1, 50)
    entity.rangeTop = faker.random_int(50, 101)
    entity.stringValue = faker.word() + str(i)


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


class FacilityGenerator(Generator):
    tier = 0
    amount = 1

    def generate(self):
        facility = models.FACILITY()
        facility.createId = "user"
        facility.modId = "user"
        facility.modTime = get_date_time()
        facility.createTime = get_date_time()
        facility.daysUntilRelease = 10
        facility.description = "Lorem ipsum light source"
        facility.name = "LILS"
        post_entity(facility)


class DataCollectionGenerator(Generator):
    tier = 0
    amount = 1000

    def generate(self):
        for i in range(1, self.amount):
            DataCollectionGenerator.generate_data_collection(i)

    @staticmethod
    def generate_data_collection(i):
        data_collection = models.DATACOLLECTION()
        apply_common_attributes(data_collection, i)
        post_entity(data_collection)


class ApplicationGenerator(Generator):
    tier = 1
    amount = 80

    def generate(self):
        for i in range(1, self.amount):
            ApplicationGenerator.generate_applications(i)

    @staticmethod
    def generate_applications(i):
        application = models.APPLICATION()
        apply_common_attributes(application, i)
        application.version = faker.random_int(1, 4)
        post_entity(application)


class DatasetTypeGenerator(Generator):
    tier = 1
    amount = 4

    def generate(self):
        for i in range(1, self.amount):
            DatasetTypeGenerator.generate_dataset_type(i)

    @staticmethod
    def generate_dataset_type(i):
        dataset_type = models.DATASETTYPE()
        apply_common_attributes(dataset_type, i)
        post_entity(dataset_type)


class FacilityCycleGenerator(Generator):
    tier = 1
    amount = 4 * YEARS  # This gives 4 per year for 20 years

    def generate(self):
        for i in range(1, self.amount):
            FacilityCycleGenerator.generate_facility_cycle(i)

    @staticmethod
    def generate_facility_cycle(i):
        facility_cycle = models.FACILITYCYCLE()
        apply_common_attributes(facility_cycle, i)
        # overwrite the name with a more suitable one
        k = i % 4 + 1  # This will give a repeated 1, 2, 3, 4 for 4 cycles per year
        year = 2000 + i // 4
        facility_cycle.name = f"{year} cycle {k}"
        facility_cycle.startDate = datetime.datetime(year, 2 * k, k)
        facility_cycle.endDate = datetime.datetime(year, 2 * k + 3, 5 * k)
        post_entity(facility_cycle)


class SampleTypeGenerator(Generator):
    tier = 1
    amount = 80

    def generate(self):

        for i in range(1, self.amount):
            SampleTypeGenerator.generate_sample_type(i)

    @staticmethod
    def generate_sample_type(i):
        sample_type = models.SAMPLETYPE()
        apply_common_attributes(sample_type, i)
        sample_type.molecularFormula = faker.random_int(43, 13323)
        sample_type.safetyInformation = faker.text()
        post_entity(sample_type)


class InstrumentGenerator(Generator):
    tier = 2
    amount = 15

    def generate(self):
        for i in range(1, self.amount):
            InstrumentGenerator.generate_instruments(i)

    @staticmethod
    def generate_instruments(i):
        instrument = models.INSTRUMENT()
        apply_common_attributes(instrument, i)
        instrument.fullName = faker.text()
        instrument.url = faker.url()
        instrument.type = str(i)
        post_entity(instrument)


class UserGenerator(Generator):
    tier = 2
    amount = 500

    def generate(self):
        for i in range(1, self.amount):
            UserGenerator.generate_users(i)

    @staticmethod
    def generate_users(i):
        user = models.USER()
        apply_common_attributes(user, i)
        user.email = faker.ascii_email()
        user.name = faker.first_name() + f"{i}"
        user.fullName = faker.name()
        user.orcidId = faker.random_int(2332, 24242)
        post_entity(user)


class DatafileFormatGenerator(Generator):
    tier = 1
    amount = 10

    def generate(self):
        for i in range(1, self.amount):
            DatafileFormatGenerator.generate_datafile_format(i)

    @staticmethod
    def generate_datafile_format(i):
        datafile_format = models.DATAFILEFORMAT()
        apply_common_attributes(datafile_format, i)
        datafile_format.version = faker.random_int(1, 14)
        post_entity(datafile_format)


class InvestigationTypeGenerator(Generator):
    tier = 1
    amount = 4

    def generate(self):
        for i in range(1, self.amount):
            InvestigationTypeGenerator.generate_investigation_type(i)

    @staticmethod
    def generate_investigation_type(i):
        investigation_type = models.INVESTIGATIONTYPE()
        apply_common_attributes(investigation_type, i)
        post_entity(investigation_type)


class GroupingGenerator(Generator):
    tier = 2
    amount = 30

    def generate(self):
        for i in range(1, self.amount):
            GroupingGenerator.generate_groupings(i)

    @staticmethod
    def generate_groupings(i):
        grouping = models.GROUPING()
        apply_common_attributes(grouping, i)
        post_entity(grouping)


class InvestigationGenerator(Generator):
    tier = 2
    amount = 3 * FacilityCycleGenerator.amount  # 60 Investigations per cycle

    def generate(self):
        for i in range(1, self.amount):
            InvestigationGenerator.generate_investigations(i)

    @staticmethod
    def generate_investigations(i):
        investigation = models.INVESTIGATION()
        apply_common_attributes(investigation, i)
        k = i % 4 + 1
        year = 2000 + (i % 80) // 4
        investigation.startDate = datetime.datetime(year, 2 * k, k + 1)
        investigation.endDate = datetime.datetime(year, 2 * k + 3, 5 * k - 1)
        investigation.releaseDate = get_end_date(i)
        investigation.summary = faker.text()
        investigation.title = faker.text()
        investigation.visitId = faker.random_int(1, 100)
        investigation.typeID = faker.random_int(
            1, InvestigationTypeGenerator.amount - 1,
        )
        post_entity(investigation)


class InvestigationUserGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            InvestigationUserGenerator.generate_investigation_user(i)

    @staticmethod
    def generate_investigation_user(i):
        investigation_user = models.INVESTIGATIONUSER()
        apply_common_attributes(investigation_user, i)
        investigation_user.role = ["PI", "CI"][faker.random_int(0, 1)]
        investigation_user.investigationID = i
        investigation_user.userID = faker.random_int(1, UserGenerator.amount - 1)
        post_entity(investigation_user)


class InstrumentScientistGenerator(Generator):
    tier = 3
    amount = InstrumentGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            InstrumentScientistGenerator.generate_instrument_scientist(i)

    @staticmethod
    def generate_instrument_scientist(i):
        instrument_scientist = models.INSTRUMENTSCIENTIST()
        apply_common_attributes(instrument_scientist, i)
        instrument_scientist.instrumentID = i
        instrument_scientist.userID = faker.random_int(1, UserGenerator.amount - 1)
        post_entity(instrument_scientist)


class InvestigationInstrumentGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount  # Must equal number of investigations

    def generate(self):
        for i in range(1, self.amount):
            InvestigationInstrumentGenerator.generate_investigation_instrument(i)

    @staticmethod
    def generate_investigation_instrument(i):
        investigation_instrument = models.INVESTIGATIONINSTRUMENT()
        apply_common_attributes(investigation_instrument, i)
        investigation_instrument.investigationID = i
        investigation_instrument.instrumentID = faker.random_int(
            1, InstrumentGenerator.amount - 1,
        )
        post_entity(investigation_instrument)


class SampleGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            SampleGenerator.generate_sample(i)

    @staticmethod
    def generate_sample(i):
        sample = models.SAMPLE()
        apply_common_attributes(sample, i)
        sample.investigationID = i
        sample.typeID = faker.random_int(1, SampleTypeGenerator.amount - 1)
        post_entity(sample)


class UserGroupGenerator(Generator):
    tier = 3
    amount = UserGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            UserGroupGenerator.generate_user_groups(i)

    @staticmethod
    def generate_user_groups(i):
        user_group = models.USERGROUP()
        apply_common_attributes(user_group, i)
        user_group.groupID = faker.random_int(1, GroupingGenerator.amount - 1)
        user_group.userID = i
        post_entity(user_group)


class StudyGenerator(Generator):
    tier = 3
    amount = UserGenerator.amount
    pid_faker = Faker()
    pid_faker.seed_instance(SEED)

    def generate(self):
        for i in range(1, self.amount):
            StudyGenerator.generate_studies(i)

    @staticmethod
    def generate_studies(i):
        study = models.STUDY()
        apply_common_attributes(study, i)
        study.startDate = get_start_date(i)
        study.status = faker.random_int(0, 1)
        study.pid = StudyGenerator.pid_faker.isbn10(separator="-")
        study.userID = i
        post_entity(study)


class InvestigationGroupGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            InvestigationGroupGenerator.generate_investigation_group(i)

    @staticmethod
    def generate_investigation_group(i):
        investigation_group = models.INVESTIGATIONGROUP()
        apply_common_attributes(investigation_group, i)
        investigation_group.role = faker.text() + str(i)
        investigation_group.groupID = faker.random_int(1, GroupingGenerator.amount - 1)
        investigation_group.investigationID = i
        post_entity(investigation_group)


class KeywordGenerator(Generator):
    tier = 3
    amount = 15000

    def generate(self):
        for i in range(1, self.amount):
            KeywordGenerator.generate_keyword(i)

    @staticmethod
    def generate_keyword(i):
        keyword = models.KEYWORD()
        apply_common_attributes(keyword, i)
        keyword.name = faker.word() + str(i)
        keyword.investigationID = faker.random_int(1, InvestigationGenerator.amount - 1)
        post_entity(keyword)


class PublicationGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount * 3

    def generate(self):
        for i in range(1, self.amount):
            PublicationGenerator.generate_publication(i)

    @staticmethod
    def generate_publication(i):
        publication = models.PUBLICATION()
        apply_common_attributes(publication, i)
        publication.fullReference = faker.text()
        publication.repository = faker.uri()
        publication.repositoryId = faker.random_int(1, 23232234)
        publication.url = faker.url()
        publication.investigationID = i % (InvestigationGenerator.amount - 1) + 1
        post_entity(publication)


class ParameterTypeGenerator(Generator):
    tier = 3
    amount = 50

    def generate(self):
        for i in range(1, self.amount):
            ParameterTypeGenerator.generate_parameter_type(i)

    @staticmethod
    def generate_parameter_type(i):
        parameter_type = models.PARAMETERTYPE()
        apply_common_attributes(parameter_type, i)
        parameter_type.applicableToDataCollection = faker.random_int(0, 1)
        parameter_type.applicableToDatafile = faker.random_int(0, 1)
        parameter_type.applicableToDataset = faker.random_int(0, 1)
        parameter_type.applicableToSample = faker.random_int(0, 1)
        parameter_type.enforced = faker.random_int(0, 1)
        parameter_type.maximumNumericValue = faker.random_int(10, 100)
        parameter_type.minimumNumericValue = faker.random_int(0, 9)
        parameter_type.units = f"unit {i}"
        parameter_type.unitsFullName = faker.word()
        parameter_type.valueType = list(models.PARAMETERTYPE.ValueTypeEnum)[
            faker.random_int(0, 2)
        ]
        parameter_type.verified = faker.random_int(0, 1)
        post_entity(parameter_type)


class InvestigationParameterGenerator(Generator):
    tier = 4
    amount = InvestigationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            InvestigationParameterGenerator.generate_investigation_parameter(i)

    @staticmethod
    def generate_investigation_parameter(i):
        investigation_parameter = models.INVESTIGATIONPARAMETER()
        apply_common_attributes(investigation_parameter, i)
        apply_common_parameter_attributes(investigation_parameter, i)
        investigation_parameter.investigationID = i
        investigation_parameter.parameterTypeID = faker.random_int(
            1, ParameterTypeGenerator.amount - 1,
        )
        post_entity(investigation_parameter)


class ShiftGenerator(Generator):
    tier = 3
    amount = InvestigationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            ShiftGenerator.generate_shift(i)

    @staticmethod
    def generate_shift(i):
        shift = models.SHIFT()
        apply_common_attributes(shift, i)
        shift.comment = faker.text()
        shift.investigationID = i
        post_entity(shift)


class StudyInvestigationGenerator(Generator):
    tier = 4
    amount = InvestigationGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            StudyInvestigationGenerator.generate_study_investigation(i)

    @staticmethod
    def generate_study_investigation(i):
        study_investigation = models.STUDYINVESTIGATION()
        apply_common_attributes(study_investigation, i)
        study_investigation.investigationID = i
        study_investigation.studyID = faker.random_int(1, StudyGenerator.amount - 1)
        post_entity(study_investigation)


class DatasetGenerator(Generator):
    tier = 4
    amount = InvestigationGenerator.amount * 2  # Two Datasets per investigation

    def generate(self):
        for i in range(1, self.amount):
            DatasetGenerator.generate_dataset(i)

    @staticmethod
    def generate_dataset(i):
        dataset = models.DATASET()
        apply_common_attributes(dataset, i)
        dataset.complete = faker.random_int(0, 1)
        dataset.location = faker.file_path()
        investigation_id = i % InvestigationGenerator.amount
        dataset.investigationID = (
            investigation_id
            if investigation_id != 0
            else InvestigationGenerator.amount - 1
        )
        sample_id = i % SampleGenerator.amount
        dataset.sampleID = sample_id if sample_id != 0 else SampleGenerator.amount - 1
        dataset.typeID = faker.random_int(1, DatasetTypeGenerator.amount - 1)
        post_entity(dataset)


class DatasetParameterGenerator(Generator):
    tier = 5
    amount = ParameterTypeGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            DatasetParameterGenerator.generate_dataset_parameter(i)

    @staticmethod
    def generate_dataset_parameter(i):
        dataset_param = models.DATASETPARAMETER()
        apply_common_attributes(dataset_param, i)
        apply_common_parameter_attributes(dataset_param, i)
        dataset_param.datasetID = faker.random_int(1, DatasetGenerator.amount - 1)
        dataset_param.parameterTypeID = i
        post_entity(dataset_param)


class DatafileGenerator(Generator):
    tier = 5
    amount = DatasetGenerator.amount * 55  # 55 files per Dataset

    def generate(self):
        for i in range(1, self.amount):
            DatafileGenerator.generate_datafile(i)

    @staticmethod
    def generate_datafile(i):
        datafile = models.DATAFILE()
        apply_common_attributes(datafile, i % 19)
        datafile.checksum = faker.md5()
        datafile.datafileCreateTime = datafile.createTime
        datafile.datafileModTime = datafile.modTime
        datafile.fileSize = faker.random_int(123, 213123121)
        datafile.datafileFormatID = faker.random_int(
            1, DatafileFormatGenerator.amount - 1,
        )
        datafile.datasetID = i % (DatasetGenerator.amount - 1) + 1
        datafile.name = f"Datafile {i}"
        datafile.location = faker.file_path(depth=2, category="image")
        post_entity(datafile)


class PermissibleStringValueGenerator(Generator):
    tier = 4
    amount = 50

    def generate(self):
        for i in range(1, self.amount):
            generate_permissible_string_value(i)


def generate_permissible_string_value(i):
    permissible_string_value = models.PERMISSIBLESTRINGVALUE()
    apply_common_attributes(permissible_string_value, i)
    permissible_string_value.value = f"value {i}"
    permissible_string_value.parameterTypeID = i
    post_entity(permissible_string_value)


class DataCollectionParameterGenerator(Generator):
    tier = 4
    amount = DataCollectionGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            DataCollectionParameterGenerator.generate_data_collection_parameter(i)

    @staticmethod
    def generate_data_collection_parameter(i):
        datacollection_parameter = models.DATACOLLECTIONPARAMETER()
        apply_common_attributes(datacollection_parameter, i)
        apply_common_parameter_attributes(datacollection_parameter, i)
        datacollection_parameter.dataCollectionID = i
        datacollection_parameter.parameterTypeID = faker.random_int(
            1, ParameterTypeGenerator.amount - 1,
        )
        post_entity(datacollection_parameter)


class SampleParameterGenerator(Generator):
    tier = 4
    amount = SampleGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            SampleParameterGenerator.generate_sample_parameter(i)

    @staticmethod
    def generate_sample_parameter(i):
        sample_parameter = models.SAMPLEPARAMETER()
        apply_common_attributes(sample_parameter, i)
        apply_common_parameter_attributes(sample_parameter, i)
        sample_parameter.sampleID = i
        sample_parameter.parameterTypeID = faker.random_int(
            1, ParameterTypeGenerator.amount - 1,
        )
        post_entity(sample_parameter)


class DatafileParameterGenerator(Generator):
    tier = 6
    amount = DatafileGenerator.amount

    def generate(self):
        for i in range(1, self.amount):
            DatafileParameterGenerator.generate_datafile_parameter(i)

    @staticmethod
    def generate_datafile_parameter(i):
        datafile_param = models.DATAFILEPARAMETER()
        apply_common_attributes(datafile_param, i)
        apply_common_parameter_attributes(datafile_param, i)
        datafile_param.datafileID = i
        datafile_param.parameterTypeID = faker.random_int(
            1, ParameterTypeGenerator.amount - 1,
        )
        post_entity(datafile_param)


def generate_all(i, generators):
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
    start_time = datetime.datetime.now()
    generators = [generator() for generator in Generator.__subclasses__()]
    tiers = 7
    for i in range(tiers):
        generate_all(i, generators)

    print(
        f"Added {sum(generator.amount for generator in generators)} entities in"
        f" {datetime.datetime.now() - start_time}",
    )


if __name__ == "__main__":
    main()
