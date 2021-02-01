from abc import ABC
from datetime import datetime
from decimal import Decimal
import enum

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    FetchedValue,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    TypeDecorator,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import InstrumentedList

from datagateway_api.common.exceptions import DatabaseError, FilterError

Base = declarative_base()


class EnumAsInteger(TypeDecorator):
    """
    Column type for storing Python enums in a database INTEGER column.
    """

    impl = Integer

    def __init__(self, enum_type):
        super(EnumAsInteger, self).__init__()
        self.enum_type = enum_type

    def process_bind_param(self, value, dialect):
        if isinstance(value, self.enum_type):
            return value.value
        raise DatabaseError(f"value {value} not in {self.enum_type.__name__}")

    def process_result_value(self, value, dialect):
        try:
            # Strips the enum class name
            return f"{self.enum_type(value)}".replace(f"{self.enum_type.__name__}.", "")
        except ValueError:
            # This will force a 500 response
            raise DatabaseError(f"value {value} not in {self.enum_type.__name__}")

    def copy(self, **kwargs):
        return EnumAsInteger(self.enum_type)


class EntityHelper(ABC):
    """
    EntityHelper class that contains methods to be shared across all entities
    """

    def to_dict(self):
        """
        Turns the columns and values of an entity into a dictionary
        :return: dict: dictionary containing the fields and values of an entity
        """
        dictionary = {}
        for column in self.__table__.columns:
            attribute_field_name = self.__mapper__.get_property_by_column(column).key
            attribute = getattr(self, attribute_field_name)
            dictionary[attribute_field_name] = self._make_serializable(attribute)

        return dictionary

    def _make_serializable(self, field):
        """
        Given a field, convert to a JSON serializable type
        :param field: The field to be converted
        :return: The converted field
        """
        if isinstance(field, datetime):
            return str(field)
        elif isinstance(field, Decimal):
            return float(field)
        else:
            return field

    def to_nested_dict(self, includes):
        """
        Given related models return a nested dictionary with the child or parent rows
        nested.

        :param includes: string/list/dict - The related models to include.
        :return: A nested dictionary with the included models
        """
        dictionary = self.to_dict()
        try:
            includes = includes if type(includes) is list else [includes]
            for include in includes:
                if type(include) is str:
                    self._nest_string_include(dictionary, include)
                elif type(include) is dict:
                    self._nest_dictionary_include(dictionary, include)
        except TypeError:
            raise FilterError(f" Bad include relations provided: {includes}")
        return dictionary

    def _nest_dictionary_include(self, dictionary, include):
        """
        Given a dictionary of related entities names, nest the related entities into the
        given dictionary representation, of the original entity.

        :param dictionary: The dictionary representation of the original entity
        :param include: The dictionary of related entity names to be nested.
        """
        related_entity = self.get_related_entity(list(include)[0])
        if not isinstance(related_entity, InstrumentedList):
            dictionary[
                related_entity.__singularfieldname__
            ] = related_entity.to_nested_dict(include[list(include)[0]])
        else:
            for entity in related_entity:
                if entity.__pluralfieldname__ in dictionary.keys():
                    dictionary[entity.__pluralfieldname__].append(
                        entity.to_nested_dict(include[list(include)[0]]),
                    )
                else:
                    dictionary[entity.__pluralfieldname__] = [
                        entity.to_nested_dict(include[list(include)[0]]),
                    ]

    def _nest_string_include(self, dictionary, include):
        """
        Given the name of a single related entity, nest the related entity into the
        given dictionary representation of the original entity.

        :param dictionary: The dictionary representation of an entity to be nested in.
        :param include: The name of the related entity to be nested
        """
        related_entity = self.get_related_entity(include)
        if not isinstance(related_entity, InstrumentedList):
            dictionary[related_entity.__singularfieldname__] = related_entity.to_dict()
        else:
            for entity in related_entity:
                if entity.__pluralfieldname__ in dictionary.keys():
                    dictionary[entity.__pluralfieldname__].append(entity.to_dict())
                else:
                    dictionary[entity.__pluralfieldname__] = [entity.to_dict()]

    def get_related_entity(self, entity):
        """
        Given a string for the related entity name, return the related entity
        :param entity: String - The name of the entity
        :return: The entity
        """
        try:
            return getattr(self, entity if entity[-1] == "s" else entity.upper())
        except AttributeError:
            raise FilterError(f" No related entity: {entity}")

    def update_from_dict(self, dictionary):
        """
        Given a dictionary containing field names and variables, updates the entity from
        the given dictionary

        :param dictionary: dict: dictionary containing the new values
        :returns: The updated dict
        """
        for key in dictionary:
            setattr(self, key, dictionary[key])
        return self.to_dict()


class EntityMeta(type(Base), type(EntityHelper)):
    """
    This class is used as a way of ensuring classes that inherit from both `Base` and
    `EntityHelper` don't have metaclass conflicts. `EntityHelper`'s metaclass is
    `ABCMeta`, but this isn't the case for `Base`. Further explanation regarding this
    issue (and how this class fixes the problem) can be found here:
    https://stackoverflow.com/a/28727066/8752408
    """

    pass


class APPLICATION(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "APPLICATION"
    __singularfieldname__ = "application"
    __pluralfieldname__ = "applications"
    __table_args__ = (Index("UNQ_APPLICATION_0", "FACILITY_ID", "NAME", "VERSION"),)

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    name = Column("NAME", String(255), nullable=False)
    version = Column("VERSION", String(255), nullable=False)
    facility = Column("FACILITY_ID", ForeignKey("FACILITY.ID"), nullable=False)

    FACILITY = relationship(
        "FACILITY",
        primaryjoin="APPLICATION.facility == FACILITY.id",
        backref="applications",
    )


class FACILITY(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "FACILITY"
    __singularfieldname__ = "facility"
    __pluralfieldname__ = "facilities"

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    daysUntilRelease = Column("DAYSUNTILRELEASE", Integer)
    description = Column("DESCRIPTION", String(1023))
    fullName = Column("FULLNAME", String(255))
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    name = Column("NAME", String(255), nullable=False, unique=True)
    url = Column("URL", String(255))


class DATACOLLECTION(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "DATACOLLECTION"
    __singularfieldname__ = "dataCollection"
    __pluralfieldname__ = "dataCollections"

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    doi = Column("DOI", String(255))
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)


class DATACOLLECTIONDATAFILE(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "DATACOLLECTIONDATAFILE"
    __singularfieldname__ = "dataCollectionDatafile"
    __pluralfieldname__ = "dataCollectionDatafiles"
    __table_args__ = (
        Index("UNQ_DATACOLLECTIONDATAFILE_0", "DATACOLLECTION_ID", "DATAFILE_ID"),
    )

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    dataCollection = Column(
        "DATACOLLECTION_ID", ForeignKey("DATACOLLECTION.ID"), nullable=False,
    )
    datafile = Column(
        "DATAFILE_ID", ForeignKey("DATAFILE.ID"), nullable=False, index=True,
    )

    DATACOLLECTION = relationship(
        "DATACOLLECTION",
        primaryjoin="DATACOLLECTIONDATAFILE.dataCollection == DATACOLLECTION.id",
        backref="dataCollectionDatafiles",
    )
    DATAFILE = relationship(
        "DATAFILE",
        primaryjoin="DATACOLLECTIONDATAFILE.datafile == DATAFILE.id",
        backref="dataCollectionDatafiles",
    )


class DATACOLLECTIONDATASET(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "DATACOLLECTIONDATASET"
    __singularfieldname__ = "dataCollectionDataset"
    __pluralfieldname__ = "dataCollectionDatasets"
    __table_args__ = (
        Index("UNQ_DATACOLLECTIONDATASET_0", "DATACOLLECTION_ID", "DATASET_ID"),
    )

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    dataCollection = Column(
        "DATACOLLECTION_ID", ForeignKey("DATACOLLECTION.ID"), nullable=False,
    )
    dataset = Column("DATASET_ID", ForeignKey("DATASET.ID"), nullable=False, index=True)

    DATACOLLECTION = relationship(
        "DATACOLLECTION",
        primaryjoin="DATACOLLECTIONDATASET.dataCollection == DATACOLLECTION.id",
        backref="dataCollectionDatasets",
    )
    DATASET = relationship(
        "DATASET",
        primaryjoin="DATACOLLECTIONDATASET.dataset == DATASET.id",
        backref="dataCollectionDatasets",
    )


class DATACOLLECTIONPARAMETER(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "DATACOLLECTIONPARAMETER"
    __singularfieldname__ = "dataCollectionParameter"
    __pluralfieldname__ = "dataCollectionParameters"
    __table_args__ = (
        Index(
            "UNQ_DATACOLLECTIONPARAMETER_0", "DATACOLLECTION_ID", "PARAMETER_TYPE_ID",
        ),
    )

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    dateTimeValue = Column("DATETIME_VALUE", DateTime)
    error = Column("ERROR", Float(asdecimal=True))
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    numericValue = Column("NUMERIC_VALUE", Float(asdecimal=True))
    rangeBottom = Column("RANGEBOTTOM", Float(asdecimal=True))
    rangeTop = Column("RANGETOP", Float(asdecimal=True))
    stringValue = Column("STRING_VALUE", String(4000))
    dataCollection = Column(
        "DATACOLLECTION_ID", ForeignKey("DATACOLLECTION.ID"), nullable=False,
    )
    type = Column(
        "PARAMETER_TYPE_ID", ForeignKey("PARAMETERTYPE.ID"), nullable=False, index=True,
    )

    DATACOLLECTION = relationship(
        "DATACOLLECTION",
        primaryjoin="DATACOLLECTIONPARAMETER.dataCollection == DATACOLLECTION.id",
        backref="dataCollectionParameters",
    )
    PARAMETERTYPE = relationship(
        "PARAMETERTYPE",
        primaryjoin="DATACOLLECTIONPARAMETER.type == PARAMETERTYPE.id",
        backref="dataCollectionParameters",
    )


class DATAFILE(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "DATAFILE"
    __singularfieldname__ = "datafile"
    __pluralfieldname__ = "datafiles"
    __table_args__ = (Index("UNQ_DATAFILE_0", "DATASET_ID", "NAME"),)

    id = Column("ID", BigInteger, primary_key=True)
    checksum = Column("CHECKSUM", String(255))
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    datafileCreateTime = Column("DATAFILECREATETIME", DateTime)
    datafileModTime = Column("DATAFILEMODTIME", DateTime)
    description = Column("DESCRIPTION", String(255))
    doi = Column("DOI", String(255))
    fileSize = Column("FILESIZE", BigInteger)
    location = Column("LOCATION", String(255), index=True)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    name = Column("NAME", String(255), nullable=False)
    datafileFormat = Column(
        "DATAFILEFORMAT_ID", ForeignKey("DATAFILEFORMAT.ID"), index=True,
    )
    dataset = Column("DATASET_ID", ForeignKey("DATASET.ID"), nullable=False)

    DATAFILEFORMAT = relationship(
        "DATAFILEFORMAT",
        primaryjoin="DATAFILE.datafileFormat == DATAFILEFORMAT.id",
        backref="datafiles",
    )
    DATASET = relationship(
        "DATASET", primaryjoin="DATAFILE.dataset == DATASET.id", backref="datafiles",
    )


class DATAFILEFORMAT(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "DATAFILEFORMAT"
    __singularfieldname__ = "datafileFormat"
    __pluralfieldname__ = "datafileFormats"
    __table_args__ = (Index("UNQ_DATAFILEFORMAT_0", "FACILITY_ID", "NAME", "VERSION"),)

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    description = Column("DESCRIPTION", String(255))
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    name = Column("NAME", String(255), nullable=False)
    type = Column("TYPE", String(255))
    version = Column("VERSION", String(255), nullable=False)
    facility = Column("FACILITY_ID", ForeignKey("FACILITY.ID"), nullable=False)

    FACILITY = relationship(
        "FACILITY",
        primaryjoin="DATAFILEFORMAT.facility == FACILITY.id",
        backref="datafileFormats",
    )


class DATAFILEPARAMETER(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "DATAFILEPARAMETER"
    __singularfieldname__ = "datafileParameter"
    __pluralfieldname__ = "datafileParameters"
    __table_args__ = (
        Index("UNQ_DATAFILEPARAMETER_0", "DATAFILE_ID", "PARAMETER_TYPE_ID"),
    )

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    dateTimeValue = Column("DATETIME_VALUE", DateTime)
    error = Column("ERROR", Float(asdecimal=True))
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    numericValue = Column("NUMERIC_VALUE", Float(asdecimal=True))
    rangeBottom = Column("RANGEBOTTOM", Float(asdecimal=True))
    rangeTop = Column("RANGETOP", Float(asdecimal=True))
    stringValue = Column("STRING_VALUE", String(4000))
    datafile = Column("DATAFILE_ID", ForeignKey("DATAFILE.ID"), nullable=False)
    type = Column(
        "PARAMETER_TYPE_ID", ForeignKey("PARAMETERTYPE.ID"), nullable=False, index=True,
    )

    DATAFILE = relationship(
        "DATAFILE",
        primaryjoin="DATAFILEPARAMETER.datafile == DATAFILE.id",
        backref="datafileParameters",
    )
    PARAMETERTYPE = relationship(
        "PARAMETERTYPE",
        primaryjoin="DATAFILEPARAMETER.type == PARAMETERTYPE.id",
        backref="datafileParameters",
    )


class DATASET(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "DATASET"
    __singularfieldname__ = "dataset"
    __pluralfieldname__ = "datasets"
    __table_args__ = (Index("UNQ_DATASET_0", "INVESTIGATION_ID", "NAME"),)

    id = Column("ID", BigInteger, primary_key=True)
    complete = Column(
        "COMPLETE", Boolean, nullable=False, server_default=FetchedValue(),
    )
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    description = Column("DESCRIPTION", String(255))
    doi = Column("DOI", String(255))
    endDate = Column("END_DATE", DateTime)
    location = Column("LOCATION", String(255))
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    name = Column("NAME", String(255), nullable=False)
    startDate = Column("STARTDATE", DateTime)
    investigation = Column(
        "INVESTIGATION_ID", ForeignKey("INVESTIGATION.ID"), nullable=False,
    )
    sample = Column("SAMPLE_ID", ForeignKey("SAMPLE.ID"), index=True)
    type = Column("TYPE_ID", ForeignKey("DATASETTYPE.ID"), nullable=False, index=True)

    INVESTIGATION = relationship(
        "INVESTIGATION",
        primaryjoin="DATASET.investigation == INVESTIGATION.id",
        backref="datasets",
    )
    SAMPLE = relationship(
        "SAMPLE", primaryjoin="DATASET.sample == SAMPLE.id", backref="datasets",
    )
    DATASETTYPE = relationship(
        "DATASETTYPE", primaryjoin="DATASET.type == DATASETTYPE.id", backref="datasets",
    )


class DATASETPARAMETER(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "DATASETPARAMETER"
    __singularfieldname__ = "datasetParameter"
    __pluralfieldname__ = "datasetParameters"
    __table_args__ = (
        Index("UNQ_DATASETPARAMETER_0", "DATASET_ID", "PARAMETER_TYPE_ID"),
    )

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    dateTimeValue = Column("DATETIME_VALUE", DateTime)
    error = Column("ERROR", Float(asdecimal=True))
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    numericValue = Column("NUMERIC_VALUE", Float(asdecimal=True))
    rangeBottom = Column("RANGEBOTTOM", Float(asdecimal=True))
    rangeTop = Column("RANGETOP", Float(asdecimal=True))
    stringValue = Column("STRING_VALUE", String(4000))
    dataset = Column("DATASET_ID", ForeignKey("DATASET.ID"), nullable=False)
    type = Column(
        "PARAMETER_TYPE_ID", ForeignKey("PARAMETERTYPE.ID"), nullable=False, index=True,
    )

    DATASET = relationship(
        "DATASET",
        primaryjoin="DATASETPARAMETER.dataset == DATASET.id",
        backref="datasetParameters",
    )
    PARAMETERTYPE = relationship(
        "PARAMETERTYPE",
        primaryjoin="DATASETPARAMETER.type == PARAMETERTYPE.id",
        backref="datasetParameters",
    )


class DATASETTYPE(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "DATASETTYPE"
    __singularfieldname__ = "type"
    __pluralfieldname__ = "datasetTypes"
    __table_args__ = (Index("UNQ_DATASETTYPE_0", "FACILITY_ID", "NAME"),)

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    description = Column("DESCRIPTION", String(255))
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    name = Column("NAME", String(255), nullable=False)
    facility = Column("FACILITY_ID", ForeignKey("FACILITY.ID"), nullable=False)

    FACILITY = relationship(
        "FACILITY",
        primaryjoin="DATASETTYPE.facility == FACILITY.id",
        backref="datasetTypes",
    )


class FACILITYCYCLE(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "FACILITYCYCLE"
    __singularfieldname__ = "facilityCycle"
    __pluralfieldname__ = "facilityCycles"
    __table_args__ = (Index("UNQ_FACILITYCYCLE_0", "FACILITY_ID", "NAME"),)

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    description = Column("DESCRIPTION", String(255))
    endDate = Column("ENDDATE", DateTime)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    name = Column("NAME", String(255), nullable=False)
    startDate = Column("STARTDATE", DateTime)
    facility = Column("FACILITY_ID", ForeignKey("FACILITY.ID"), nullable=False)

    FACILITY = relationship(
        "FACILITY",
        primaryjoin="FACILITYCYCLE.facility == FACILITY.id",
        backref="facilityCycles",
    )


class GROUPING(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "GROUPING"
    __singularfieldname__ = "grouping"
    __pluralfieldname__ = "groupings"

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    name = Column("NAME", String(255), nullable=False, unique=True)


class INSTRUMENT(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "INSTRUMENT"
    __singularfieldname__ = "instrument"
    __pluralfieldname__ = "instruments"
    __table_args__ = (Index("UNQ_INSTRUMENT_0", "FACILITY_ID", "NAME"),)

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    description = Column("DESCRIPTION", String(4000))
    fullName = Column("FULLNAME", String(255))
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    name = Column("NAME", String(255), nullable=False)
    type = Column("TYPE", String(255))
    url = Column("URL", String(255))
    facility = Column("FACILITY_ID", ForeignKey("FACILITY.ID"), nullable=False)

    FACILITY = relationship(
        "FACILITY",
        primaryjoin="INSTRUMENT.facility == FACILITY.id",
        backref="instruments",
    )


class INSTRUMENTSCIENTIST(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "INSTRUMENTSCIENTIST"
    __singularfieldname__ = "instrumentScientist"
    __pluralfieldname__ = "instrumentScientists"
    __table_args__ = (Index("UNQ_INSTRUMENTSCIENTIST_0", "USER_ID", "INSTRUMENT_ID"),)

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    instrument = Column(
        "INSTRUMENT_ID", ForeignKey("INSTRUMENT.ID"), nullable=False, index=True,
    )
    user = Column("USER_ID", ForeignKey("USER_.ID"), nullable=False)

    INSTRUMENT = relationship(
        "INSTRUMENT",
        primaryjoin="INSTRUMENTSCIENTIST.instrument == INSTRUMENT.id",
        backref="instrumentScientists",
    )
    USER = relationship(
        "USER",
        primaryjoin="INSTRUMENTSCIENTIST.user == USER.id",
        backref="instrumentScientists",
    )


class INVESTIGATION(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "INVESTIGATION"
    __singularfieldname__ = "investigation"
    __pluralfieldname__ = "investigations"
    __table_args__ = (Index("UNQ_INVESTIGATION_0", "FACILITY_ID", "NAME", "VISIT_ID"),)

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    doi = Column("DOI", String(255))
    endDate = Column("ENDDATE", DateTime)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    name = Column("NAME", String(255), nullable=False)
    releaseDate = Column("RELEASEDATE", DateTime)
    startDate = Column("STARTDATE", DateTime)
    summary = Column("SUMMARY", String(4000))
    title = Column("TITLE", String(255), nullable=False)
    visitId = Column("VISIT_ID", String(255), nullable=False)
    facility = Column("FACILITY_ID", ForeignKey("FACILITY.ID"), nullable=False)
    type = Column(
        "TYPE_ID", ForeignKey("INVESTIGATIONTYPE.ID"), nullable=False, index=True,
    )

    FACILITY = relationship(
        "FACILITY",
        primaryjoin="INVESTIGATION.facility == FACILITY.id",
        backref="investigations",
    )
    INVESTIGATIONTYPE = relationship(
        "INVESTIGATIONTYPE",
        primaryjoin="INVESTIGATION.type == INVESTIGATIONTYPE.id",
        backref="investigations",
    )


class INVESTIGATIONGROUP(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "INVESTIGATIONGROUP"
    __singularfieldname__ = "investigationGroup"
    __pluralfieldname__ = "investigationGroups"
    __table_args__ = (
        Index("UNQ_INVESTIGATIONGROUP_0", "GROUP_ID", "INVESTIGATION_ID", "ROLE"),
    )

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    role = Column("ROLE", String(255), nullable=False)
    grouping = Column("GROUP_ID", ForeignKey("GROUPING.ID"), nullable=False)
    investigation = Column(
        "INVESTIGATION_ID", ForeignKey("INVESTIGATION.ID"), nullable=False, index=True,
    )

    GROUPING = relationship(
        "GROUPING",
        primaryjoin="INVESTIGATIONGROUP.grouping == GROUPING.id",
        backref="investigationGroups",
    )
    INVESTIGATION = relationship(
        "INVESTIGATION",
        primaryjoin="INVESTIGATIONGROUP.investigation == INVESTIGATION.id",
        backref="investigationGroups",
    )


class INVESTIGATIONINSTRUMENT(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "INVESTIGATIONINSTRUMENT"
    __singularfieldname__ = "investigationInstrument"
    __pluralfieldname__ = "investigationInstruments"
    __table_args__ = (
        Index("UNQ_INVESTIGATIONINSTRUMENT_0", "INVESTIGATION_ID", "INSTRUMENT_ID"),
    )

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    instrument = Column(
        "INSTRUMENT_ID", ForeignKey("INSTRUMENT.ID"), nullable=False, index=True,
    )
    investigation = Column(
        "INVESTIGATION_ID", ForeignKey("INVESTIGATION.ID"), nullable=False,
    )

    INSTRUMENT = relationship(
        "INSTRUMENT",
        primaryjoin="INVESTIGATIONINSTRUMENT.instrument == INSTRUMENT.id",
        backref="investigationInstruments",
    )
    INVESTIGATION = relationship(
        "INVESTIGATION",
        primaryjoin="INVESTIGATIONINSTRUMENT.investigation == INVESTIGATION.id",
        backref="investigationInstruments",
    )


class INVESTIGATIONPARAMETER(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "INVESTIGATIONPARAMETER"
    __singularfieldname__ = "investigationParameter"
    __pluralfieldname__ = "investigationParameters"
    __table_args__ = (
        Index("UNQ_INVESTIGATIONPARAMETER_0", "INVESTIGATION_ID", "PARAMETER_TYPE_ID"),
    )

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    dateTimeValue = Column("DATETIME_VALUE", DateTime)
    error = Column("ERROR", Float(asdecimal=True))
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    numericValue = Column("NUMERIC_VALUE", Float(asdecimal=True))
    rangeBottom = Column("RANGEBOTTOM", Float(asdecimal=True))
    rangeTop = Column("RANGETOP", Float(asdecimal=True))
    stringValue = Column("STRING_VALUE", String(4000))
    investigation = Column(
        "INVESTIGATION_ID", ForeignKey("INVESTIGATION.ID"), nullable=False,
    )
    type = Column(
        "PARAMETER_TYPE_ID", ForeignKey("PARAMETERTYPE.ID"), nullable=False, index=True,
    )

    INVESTIGATION = relationship(
        "INVESTIGATION",
        primaryjoin="INVESTIGATIONPARAMETER.investigation == INVESTIGATION.id",
        backref="investigationParameters",
    )
    PARAMETERTYPE = relationship(
        "PARAMETERTYPE",
        primaryjoin="INVESTIGATIONPARAMETER.type == PARAMETERTYPE.id",
        backref="investigationParameters",
    )


class INVESTIGATIONTYPE(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "INVESTIGATIONTYPE"
    __singularfieldname__ = "type"
    __pluralfieldname__ = "investigationTypes"
    __table_args__ = (Index("UNQ_INVESTIGATIONTYPE_0", "NAME", "FACILITY_ID"),)

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    description = Column("DESCRIPTION", String(255))
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    name = Column("NAME", String(255), nullable=False)
    facility = Column(
        "FACILITY_ID", ForeignKey("FACILITY.ID"), nullable=False, index=True,
    )

    FACILITY = relationship(
        "FACILITY",
        primaryjoin="INVESTIGATIONTYPE.facility == FACILITY.id",
        backref="investigationTypes",
    )


class INVESTIGATIONUSER(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "INVESTIGATIONUSER"
    __singularfieldname__ = "investigationUser"
    __pluralfieldname__ = "investigationUsers"
    __table_args__ = (
        Index("UNQ_INVESTIGATIONUSER_0", "USER_ID", "INVESTIGATION_ID", "ROLE"),
    )

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    role = Column("ROLE", String(255), nullable=False)
    investigation = Column(
        "INVESTIGATION_ID", ForeignKey("INVESTIGATION.ID"), nullable=False, index=True,
    )
    user = Column("USER_ID", ForeignKey("USER_.ID"), nullable=False)

    INVESTIGATION = relationship(
        "INVESTIGATION",
        primaryjoin="INVESTIGATIONUSER.investigation == INVESTIGATION.id",
        backref="investigationUsers",
    )
    USER = relationship(
        "USER",
        primaryjoin="INVESTIGATIONUSER.user == USER.id",
        backref="investigationUsers",
    )


class JOB(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "JOB"
    __singularfieldname__ = "job"
    __pluralfieldname__ = "jobs"

    id = Column("ID", BigInteger, primary_key=True)
    arguments = Column("ARGUMENTS", String(255))
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    application = Column(
        "APPLICATION_ID", ForeignKey("APPLICATION.ID"), nullable=False, index=True,
    )
    inputDataCollection = Column(
        "INPUTDATACOLLECTION_ID", ForeignKey("DATACOLLECTION.ID"), index=True,
    )
    outputDataCollection = Column(
        "OUTPUTDATACOLLECTION_ID", ForeignKey("DATACOLLECTION.ID"), index=True,
    )

    APPLICATION = relationship(
        "APPLICATION", primaryjoin="JOB.application == APPLICATION.id", backref="jobs",
    )
    DATACOLLECTION = relationship(
        "DATACOLLECTION",
        primaryjoin="JOB.inputDataCollection == DATACOLLECTION.id",
        backref="jobs",
    )


class KEYWORD(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "KEYWORD"
    __singularfieldname__ = "keyword"
    __pluralfieldname__ = "keywords"
    __table_args__ = (Index("UNQ_KEYWORD_0", "NAME", "INVESTIGATION_ID"),)

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    name = Column("NAME", String(255), nullable=False)
    investigation = Column(
        "INVESTIGATION_ID", ForeignKey("INVESTIGATION.ID"), nullable=False, index=True,
    )

    INVESTIGATION = relationship(
        "INVESTIGATION",
        primaryjoin="KEYWORD.investigation == INVESTIGATION.id",
        backref="keywords",
    )


class PARAMETERTYPE(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "PARAMETERTYPE"
    __singularfieldname__ = "type"
    __pluralfieldname__ = "parameterTypes"
    __table_args__ = (Index("UNQ_PARAMETERTYPE_0", "FACILITY_ID", "NAME", "UNITS"),)

    class ValueTypeEnum(enum.Enum):
        DATE_AND_TIME = 0
        NUMERIC = 1
        STRING = 2

    id = Column("ID", BigInteger, primary_key=True)
    applicableToDataCollection = Column(
        "APPLICABLETODATACOLLECTION", Boolean, server_default=FetchedValue(),
    )
    applicableToDatafile = Column(
        "APPLICABLETODATAFILE", Boolean, server_default=FetchedValue(),
    )
    applicableToDataset = Column(
        "APPLICABLETODATASET", Boolean, server_default=FetchedValue(),
    )
    applicableToInvestigation = Column(
        "APPLICABLETOINVESTIGATION", Boolean, server_default=FetchedValue(),
    )
    applicableToSample = Column(
        "APPLICABLETOSAMPLE", Boolean, server_default=FetchedValue(),
    )
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    description = Column("DESCRIPTION", String(255))
    enforced = Column("ENFORCED", Boolean, server_default=FetchedValue())
    maximumNumericValue = Column("MAXIMUMNUMERICVALUE", Float(asdecimal=True))
    minimumNumericValue = Column("MINIMUMNUMERICVALUE", Float(asdecimal=True))
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    name = Column("NAME", String(255), nullable=False)
    units = Column("UNITS", String(255), nullable=False)
    unitsFullName = Column("UNITSFULLNAME", String(255))
    valueType = Column("VALUETYPE", EnumAsInteger(ValueTypeEnum), nullable=False)
    verified = Column("VERIFIED", Boolean, server_default=FetchedValue())
    facility = Column("FACILITY_ID", ForeignKey("FACILITY.ID"), nullable=False)

    FACILITY = relationship(
        "FACILITY",
        primaryjoin="PARAMETERTYPE.facility == FACILITY.id",
        backref="parameterTypes",
    )


class PERMISSIBLESTRINGVALUE(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "PERMISSIBLESTRINGVALUE"
    __singularfieldname__ = "permissibleStringValue"
    __pluralfieldname__ = "permissibleStringValues"
    __table_args__ = (
        Index("UNQ_PERMISSIBLESTRINGVALUE_0", "VALUE", "PARAMETERTYPE_ID"),
    )

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    value = Column("VALUE", String(255), nullable=False)
    type = Column(
        "PARAMETERTYPE_ID", ForeignKey("PARAMETERTYPE.ID"), nullable=False, index=True,
    )

    PARAMETERTYPE = relationship(
        "PARAMETERTYPE",
        primaryjoin="PERMISSIBLESTRINGVALUE.type == PARAMETERTYPE.id",
        backref="permissibleStringValues",
    )


class PUBLICATION(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "PUBLICATION"
    __singularfieldname__ = "publication"
    __pluralfieldname__ = "publications"

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    doi = Column("DOI", String(255))
    fullReference = Column("FULLREFERENCE", String(511), nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    repository = Column("REPOSITORY", String(255))
    repositoryId = Column("REPOSITORYID", String(255))
    url = Column("URL", String(255))
    investigation = Column(
        "INVESTIGATION_ID", ForeignKey("INVESTIGATION.ID"), nullable=False, index=True,
    )

    INVESTIGATION = relationship(
        "INVESTIGATION",
        primaryjoin="PUBLICATION.investigation == INVESTIGATION.id",
        backref="publications",
    )


class PUBLICSTEP(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "PUBLICSTEP"
    __singularfieldname__ = "publicStep"
    __pluralfieldname__ = "publicSteps"
    __table_args__ = (Index("UNQ_PUBLICSTEP_0", "ORIGIN", "FIELD"),)

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    field = Column("FIELD", String(32), nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    origin = Column("ORIGIN", String(32), nullable=False)


class RELATEDDATAFILE(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "RELATEDDATAFILE"
    __singularfieldname__ = "relatedDatafile"
    __pluralfieldname__ = "relatedDatafiles"
    __table_args__ = (
        Index("UNQ_RELATEDDATAFILE_0", "SOURCE_DATAFILE_ID", "DEST_DATAFILE_ID"),
    )

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    relation = Column("RELATION", String(255), nullable=False)
    destDatafile = Column(
        "DEST_DATAFILE_ID", ForeignKey("DATAFILE.ID"), nullable=False, index=True,
    )
    sourceDatafile = Column(
        "SOURCE_DATAFILE_ID", ForeignKey("DATAFILE.ID"), nullable=False,
    )

    DATAFILE = relationship(
        "DATAFILE",
        primaryjoin="RELATEDDATAFILE.destDatafile == DATAFILE.id",
        backref="relatedDatafiles",
    )


class RULE(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "RULE_"
    __singularfieldname__ = "rule"
    __pluralfieldname__ = "rules"

    id = Column("ID", BigInteger, primary_key=True)
    attribute = Column("ATTRIBUTE", String(255))
    bean = Column("BEAN", String(255))
    c = Column("C", Integer, server_default=FetchedValue())
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    crudFlags = Column("CRUDFLAGS", String(4), nullable=False)
    crudJPQL = Column("CRUDJPQL", String(1024))
    d = Column("D", Integer, server_default=FetchedValue())
    includeJPQL = Column("INCLUDEJPQL", String(1024))
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    r = Column("R", Integer, server_default=FetchedValue())
    restricted = Column("RESTRICTED", Integer, server_default=FetchedValue())
    searchJPQL = Column("SEARCHJPQL", String(1024))
    u = Column("U", Integer, server_default=FetchedValue())
    what = Column("WHAT", String(1024), nullable=False)
    grouping = Column("GROUPING_ID", ForeignKey("GROUPING.ID"), index=True)

    GROUPING = relationship(
        "GROUPING", primaryjoin="RULE.grouping == GROUPING.id", backref="rules",
    )


class SAMPLE(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "SAMPLE"
    __singularfieldname__ = "sample"
    __pluralfieldname__ = "samples"
    __table_args__ = (Index("UNQ_SAMPLE_0", "INVESTIGATION_ID", "NAME"),)

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    name = Column("NAME", String(255), nullable=False)
    investigation = Column(
        "INVESTIGATION_ID", ForeignKey("INVESTIGATION.ID"), nullable=False,
    )
    type = Column("SAMPLETYPE_ID", ForeignKey("SAMPLETYPE.ID"), index=True)

    INVESTIGATION = relationship(
        "INVESTIGATION",
        primaryjoin="SAMPLE.investigation == INVESTIGATION.id",
        backref="samples",
    )
    SAMPLETYPE = relationship(
        "SAMPLETYPE", primaryjoin="SAMPLE.type == SAMPLETYPE.id", backref="samples",
    )


class SAMPLEPARAMETER(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "SAMPLEPARAMETER"
    __singularfieldname__ = "sampleParameter"
    __pluralfieldname__ = "sampleParameters"
    __table_args__ = (Index("UNQ_SAMPLEPARAMETER_0", "SAMPLE_ID", "PARAMETER_TYPE_ID"),)

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    dateTimeValue = Column("DATETIME_VALUE", DateTime)
    error = Column("ERROR", Float(asdecimal=True))
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    numericValue = Column("NUMERIC_VALUE", Float(asdecimal=True))
    rangeBottom = Column("RANGEBOTTOM", Float(asdecimal=True))
    rangeTop = Column("RANGETOP", Float(asdecimal=True))
    stringValue = Column("STRING_VALUE", String(4000))
    sample = Column("SAMPLE_ID", ForeignKey("SAMPLE.ID"), nullable=False)
    type = Column(
        "PARAMETER_TYPE_ID", ForeignKey("PARAMETERTYPE.ID"), nullable=False, index=True,
    )

    PARAMETERTYPE = relationship(
        "PARAMETERTYPE",
        primaryjoin="SAMPLEPARAMETER.type == PARAMETERTYPE.id",
        backref="sampleParameters",
    )
    SAMPLE = relationship(
        "SAMPLE",
        primaryjoin="SAMPLEPARAMETER.sample == SAMPLE.id",
        backref="sampleParameters",
    )


class SESSION(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "SESSION_"

    id = Column("ID", String(255), primary_key=True)
    expireDateTime = Column("EXPIREDATETIME", DateTime)
    username = Column("USERNAME", String(255))


class SHIFT(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "SHIFT"
    __singularfieldname__ = "shift"
    __pluralfieldname__ = "shifts"
    __table_args__ = (Index("UNQ_SHIFT_0", "INVESTIGATION_ID", "STARTDATE", "ENDDATE"),)

    id = Column("ID", BigInteger, primary_key=True)
    comment = Column("COMMENT", String(255))
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    endDate = Column("ENDDATE", DateTime, nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    startDate = Column("STARTDATE", DateTime, nullable=False)
    investigation = Column(
        "INVESTIGATION_ID", ForeignKey("INVESTIGATION.ID"), nullable=False,
    )

    INVESTIGATION = relationship(
        "INVESTIGATION",
        primaryjoin="SHIFT.investigation == INVESTIGATION.id",
        backref="shifts",
    )


class USER(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "USER_"
    __singularfieldname__ = "user"
    __pluralfieldname__ = "users"

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    email = Column("EMAIL", String(255))
    fullName = Column("FULLNAME", String(255))
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    name = Column("NAME", String(255), nullable=False, unique=True)
    orcidId = Column("ORCIDID", String(255))


class USERGROUP(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "USERGROUP"
    __singularfieldname__ = "userGroup"
    __pluralfieldname__ = "userGroups"
    __table_args__ = (Index("UNQ_USERGROUP_0", "USER_ID", "GROUP_ID"),)

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    grouping = Column("GROUP_ID", ForeignKey("GROUPING.ID"), nullable=False, index=True)
    user = Column("USER_ID", ForeignKey("USER_.ID"), nullable=False)

    GROUPING = relationship(
        "GROUPING", primaryjoin="USERGROUP.grouping == GROUPING.id", backref="grouping",
    )
    USER = relationship(
        "USER", primaryjoin="USERGROUP.user == USER.id", backref="userGroups",
    )


class STUDYINVESTIGATION(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "STUDYINVESTIGATION"
    __singularfieldname__ = "studyInvestigation"
    __pluralfieldname__ = "studyInvestigations"
    __table_args__ = (
        Index("UNQ_STUDYINVESTIGATION_0", "STUDY_ID", "INVESTIGATION_ID"),
    )

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    investigation = Column(
        "INVESTIGATION_ID", ForeignKey("INVESTIGATION.ID"), nullable=False, index=True,
    )
    study = Column("STUDY_ID", ForeignKey("STUDY.ID"), nullable=False)

    INVESTIGATION = relationship(
        "INVESTIGATION",
        primaryjoin="STUDYINVESTIGATION.investigation == INVESTIGATION.id",
        backref="studyInvestigations",
    )
    STUDY = relationship(
        "STUDY",
        primaryjoin="STUDYINVESTIGATION.study == STUDY.id",
        backref="studyInvestigations",
    )


class STUDY(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "STUDY"
    __singularfieldname__ = "study"
    __pluralfieldname__ = "studies"

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    description = Column("DESCRIPTION", String(4000))
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    name = Column("NAME", String(255), nullable=False)
    startDate = Column("STARTDATE", DateTime)
    status = Column("STATUS", Integer)
    user = Column("USER_ID", ForeignKey("USER_.ID"), index=True)

    USER = relationship("USER", primaryjoin="STUDY.user == USER.id", backref="studies")


class SAMPLETYPE(Base, EntityHelper, metaclass=EntityMeta):
    __tablename__ = "SAMPLETYPE"
    __singularfieldname = "sampleType"
    __pluralfieldname__ = "sampleTypes"
    __table_args__ = (
        Index("UNQ_SAMPLETYPE_0", "FACILITY_ID", "NAME", "MOLECULARFORMULA"),
    )

    id = Column("ID", BigInteger, primary_key=True)
    createId = Column("CREATE_ID", String(255), nullable=False)
    createTime = Column("CREATE_TIME", DateTime, nullable=False)
    modId = Column("MOD_ID", String(255), nullable=False)
    modTime = Column("MOD_TIME", DateTime, nullable=False)
    molecularFormula = Column("MOLECULARFORMULA", String(255), nullable=False)
    name = Column("NAME", String(255), nullable=False)
    safetyInformation = Column("SAFETYINFORMATION", String(4000))
    facility = Column("FACILITY_ID", ForeignKey("FACILITY.ID"), nullable=False)

    FACILITY = relationship(
        "FACILITY",
        primaryjoin="SAMPLETYPE.facility == FACILITY.id",
        backref="sampleTypes",
    )
