from sqlalchemy import Index, Column, BigInteger, String, DateTime, ForeignKey, Integer, Float, FetchedValue
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import InstrumentedList

Base = declarative_base()


class EntityHelper(object):
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
            dictionary[column.name] = str(getattr(self, column.name))
        return dictionary

    def to_nested_dict(self, included_relations):
        """
        Given related models return a nested dictionary with the child or parent rows nested.


        :param included_relations: string/list/dict - The related models to include.
        :return: A nested dictionary with the included models
        """
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = str(getattr(self, column.name))
        if type(included_relations) is not dict:
            for attr in dir(self):
                if attr in included_relations:
                    relation = getattr(self, attr)
                    if isinstance(relation, EntityHelper):
                        dictionary[attr + "_ID"] = relation.to_dict()
                    elif isinstance(relation, InstrumentedList):  # Instrumented list is when the inclusion is a child
                        dictionary[attr + "_ID"] = []
                        for entity in getattr(self, attr):
                            dictionary[attr + "_ID"].append(entity.to_dict())
        else:
            for attr in dir(self):
                if attr == list(included_relations.keys())[0]:
                    dictionary[attr + "_ID"] = getattr(self, attr).to_nested_dict(list(included_relations.values()))

        dictionary = {k: v for k, v in dictionary.items() if
                          "ID" in k or k != "MOD_ID" or k != "CREATE_ID" or k != "ID"}
        return dictionary

    def update_from_dict(self, dictionary):
        """
        Given a dictionary containing field names and variables, updates the entity from the given dictionary
        :param dictionary: dict: dictionary containing the new values
        """
        for key in dictionary:
            setattr(self, key.upper(), dictionary[key])


class APPLICATION(Base, EntityHelper):
    __tablename__ = 'APPLICATION'
    __table_args__ = (
        Index('UNQ_APPLICATION_0', 'FACILITY_ID', 'NAME', 'VERSION'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NAME = Column(String(255), nullable=False)
    VERSION = Column(String(255), nullable=False)
    FACILITY_ID = Column(ForeignKey('FACILITY.ID'), nullable=False)

    FACILITY = relationship('FACILITY', primaryjoin='APPLICATION.FACILITY_ID == FACILITY.ID', backref='APPLICATION')


class FACILITY(Base, EntityHelper):
    __tablename__ = 'FACILITY'

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DAYSUNTILRELEASE = Column(Integer)
    DESCRIPTION = Column(String(1023))
    FULLNAME = Column(String(255))
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NAME = Column(String(255), nullable=False, unique=True)
    URL = Column(String(255))


class DATACOLLECTION(Base, EntityHelper):
    __tablename__ = 'DATACOLLECTION'

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DOI = Column(String(255))
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)


class DATACOLLECTIONDATAFILE(Base, EntityHelper):
    __tablename__ = 'DATACOLLECTIONDATAFILE'
    __table_args__ = (
        Index('UNQ_DATACOLLECTIONDATAFILE_0', 'DATACOLLECTION_ID', 'DATAFILE_ID'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    DATACOLLECTION_ID = Column(ForeignKey('DATACOLLECTION.ID'), nullable=False)
    DATAFILE_ID = Column(ForeignKey('DATAFILE.ID'), nullable=False, index=True)

    DATACOLLECTION = relationship('DATACOLLECTION',
                                  primaryjoin='DATACOLLECTIONDATAFILE.DATACOLLECTION_ID == DATACOLLECTION.ID',
                                  backref='DATACOLLECTIONDATAFILE')
    DATAFILE = relationship('DATAFILE', primaryjoin='DATACOLLECTIONDATAFILE.DATAFILE_ID == DATAFILE.ID',
                            backref='DATACOLLECTIONDATAFILE')


class DATACOLLECTIONDATASET(Base, EntityHelper):
    __tablename__ = 'DATACOLLECTIONDATASET'
    __table_args__ = (
        Index('UNQ_DATACOLLECTIONDATASET_0', 'DATACOLLECTION_ID', 'DATASET_ID'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    DATACOLLECTION_ID = Column(ForeignKey('DATACOLLECTION.ID'), nullable=False)
    DATASET_ID = Column(ForeignKey('DATASET.ID'), nullable=False, index=True)

    DATACOLLECTION = relationship('DATACOLLECTION',
                                  primaryjoin='DATACOLLECTIONDATASET.DATACOLLECTION_ID == DATACOLLECTION.ID',
                                  backref='DATACOLLECTIONDATASET')
    DATASET = relationship('DATASET', primaryjoin='DATACOLLECTIONDATASET.DATASET_ID == DATASET.ID',
                           backref='DATACOLLECTIONDATASET')


class DATACOLLECTIONPARAMETER(Base, EntityHelper):
    __tablename__ = 'DATACOLLECTIONPARAMETER'
    __table_args__ = (
        Index('UNQ_DATACOLLECTIONPARAMETER_0', 'DATACOLLECTION_ID', 'PARAMETER_TYPE_ID'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DATETIME_VALUE = Column(DateTime)
    ERROR = Column(Float(asdecimal=True))
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NUMERIC_VALUE = Column(Float(asdecimal=True))
    RANGEBOTTOM = Column(Float(asdecimal=True))
    RANGETOP = Column(Float(asdecimal=True))
    STRING_VALUE = Column(String(4000))
    DATACOLLECTION_ID = Column(ForeignKey('DATACOLLECTION.ID'), nullable=False)
    PARAMETER_TYPE_ID = Column(ForeignKey('PARAMETERTYPE.ID'), nullable=False, index=True)

    DATACOLLECTION = relationship('DATACOLLECTION',
                                  primaryjoin='DATACOLLECTIONPARAMETER.DATACOLLECTION_ID == DATACOLLECTION.ID',
                                  backref='DATACOLLECTIONPARAMETER')
    PARAMETERTYPE = relationship('PARAMETERTYPE',
                                 primaryjoin='DATACOLLECTIONPARAMETER.PARAMETER_TYPE_ID == PARAMETERTYPE.ID',
                                 backref='DATACOLLECTIONPARAMETER')


class DATAFILE(Base, EntityHelper):
    __tablename__ = 'DATAFILE'
    __table_args__ = (
        Index('UNQ_DATAFILE_0', 'DATASET_ID', 'NAME'),
    )

    ID = Column(BigInteger, primary_key=True)
    CHECKSUM = Column(String(255))
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DATAFILECREATETIME = Column(DateTime)
    DATAFILEMODTIME = Column(DateTime)
    DESCRIPTION = Column(String(255))
    DOI = Column(String(255))
    FILESIZE = Column(BigInteger)
    LOCATION = Column(String(255), index=True)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NAME = Column(String(255), nullable=False)
    DATAFILEFORMAT_ID = Column(ForeignKey('DATAFILEFORMAT.ID'), index=True)
    DATASET_ID = Column(ForeignKey('DATASET.ID'), nullable=False)

    DATAFILEFORMAT = relationship('DATAFILEFORMAT', primaryjoin='DATAFILE.DATAFILEFORMAT_ID == DATAFILEFORMAT.ID',
                                  backref='DATAFILE')
    DATASET = relationship('DATASET', primaryjoin='DATAFILE.DATASET_ID == DATASET.ID', backref='DATAFILE')


class DATAFILEFORMAT(Base, EntityHelper):
    __tablename__ = 'DATAFILEFORMAT'
    __table_args__ = (
        Index('UNQ_DATAFILEFORMAT_0', 'FACILITY_ID', 'NAME', 'VERSION'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DESCRIPTION = Column(String(255))
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NAME = Column(String(255), nullable=False)
    TYPE = Column(String(255))
    VERSION = Column(String(255), nullable=False)
    FACILITY_ID = Column(ForeignKey('FACILITY.ID'), nullable=False)

    FACILITY = relationship('FACILITY', primaryjoin='DATAFILEFORMAT.FACILITY_ID == FACILITY.ID',
                            backref='DATAFILEFORMAT')


class DATAFILEPARAMETER(Base, EntityHelper):
    __tablename__ = 'DATAFILEPARAMETER'
    __table_args__ = (
        Index('UNQ_DATAFILEPARAMETER_0', 'DATAFILE_ID', 'PARAMETER_TYPE_ID'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DATETIME_VALUE = Column(DateTime)
    ERROR = Column(Float(asdecimal=True))
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NUMERIC_VALUE = Column(Float(asdecimal=True))
    RANGEBOTTOM = Column(Float(asdecimal=True))
    RANGETOP = Column(Float(asdecimal=True))
    STRING_VALUE = Column(String(4000))
    DATAFILE_ID = Column(ForeignKey('DATAFILE.ID'), nullable=False)
    PARAMETER_TYPE_ID = Column(ForeignKey('PARAMETERTYPE.ID'), nullable=False, index=True)

    DATAFILE = relationship('DATAFILE', primaryjoin='DATAFILEPARAMETER.DATAFILE_ID == DATAFILE.ID',
                            backref='DATAFILEPARAMETER')
    PARAMETERTYPE = relationship('PARAMETERTYPE', primaryjoin='DATAFILEPARAMETER.PARAMETER_TYPE_ID == PARAMETERTYPE.ID',
                                 backref='DATAFILEPARAMETER')


class DATASET(Base, EntityHelper):
    __tablename__ = 'DATASET'
    __table_args__ = (
        Index('UNQ_DATASET_0', 'INVESTIGATION_ID', 'NAME'),
    )

    ID = Column(BigInteger, primary_key=True)
    COMPLETE = Column(Integer, nullable=False, server_default=FetchedValue())
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DESCRIPTION = Column(String(255))
    DOI = Column(String(255))
    END_DATE = Column(DateTime)
    LOCATION = Column(String(255))
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NAME = Column(String(255), nullable=False)
    STARTDATE = Column(DateTime)
    INVESTIGATION_ID = Column(ForeignKey('INVESTIGATION.ID'), nullable=False)
    SAMPLE_ID = Column(ForeignKey('SAMPLE.ID'), index=True)
    TYPE_ID = Column(ForeignKey('DATASETTYPE.ID'), nullable=False, index=True)

    INVESTIGATION = relationship('INVESTIGATION', primaryjoin='DATASET.INVESTIGATION_ID == INVESTIGATION.ID',
                                 backref='DATASET')
    SAMPLE = relationship('SAMPLE', primaryjoin='DATASET.SAMPLE_ID == SAMPLE.ID', backref='DATASET')
    DATASETTYPE = relationship('DATASETTYPE', primaryjoin='DATASET.TYPE_ID == DATASETTYPE.ID', backref='DATASET')


class DATASETPARAMETER(Base, EntityHelper):
    __tablename__ = 'DATASETPARAMETER'
    __table_args__ = (
        Index('UNQ_DATASETPARAMETER_0', 'DATASET_ID', 'PARAMETER_TYPE_ID'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DATETIME_VALUE = Column(DateTime)
    ERROR = Column(Float(asdecimal=True))
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NUMERIC_VALUE = Column(Float(asdecimal=True))
    RANGEBOTTOM = Column(Float(asdecimal=True))
    RANGETOP = Column(Float(asdecimal=True))
    STRING_VALUE = Column(String(4000))
    DATASET_ID = Column(ForeignKey('DATASET.ID'), nullable=False)
    PARAMETER_TYPE_ID = Column(ForeignKey('PARAMETERTYPE.ID'), nullable=False, index=True)

    DATASET = relationship('DATASET', primaryjoin='DATASETPARAMETER.DATASET_ID == DATASET.ID',
                           backref='DATASETPARAMETER')
    PARAMETERTYPE = relationship('PARAMETERTYPE', primaryjoin='DATASETPARAMETER.PARAMETER_TYPE_ID == PARAMETERTYPE.ID',
                                 backref='DATASETPARAMETER')


class DATASETTYPE(Base, EntityHelper):
    __tablename__ = 'DATASETTYPE'
    __table_args__ = (
        Index('UNQ_DATASETTYPE_0', 'FACILITY_ID', 'NAME'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DESCRIPTION = Column(String(255))
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NAME = Column(String(255), nullable=False)
    FACILITY_ID = Column(ForeignKey('FACILITY.ID'), nullable=False)

    FACILITY = relationship('FACILITY', primaryjoin='DATASETTYPE.FACILITY_ID == FACILITY.ID', backref='DATASETTYPE')


class FACILITYCYCLE(Base, EntityHelper):
    __tablename__ = 'FACILITYCYCLE'
    __table_args__ = (
        Index('UNQ_FACILITYCYCLE_0', 'FACILITY_ID', 'NAME'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DESCRIPTION = Column(String(255))
    ENDDATE = Column(DateTime)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NAME = Column(String(255), nullable=False)
    STARTDATE = Column(DateTime)
    FACILITY_ID = Column(ForeignKey('FACILITY.ID'), nullable=False)

    FACILITY = relationship('FACILITY', primaryjoin='FACILITYCYCLE.FACILITY_ID == FACILITY.ID',
                            backref='FACILITYCYCLE')


class GROUPING(Base, EntityHelper):
    __tablename__ = 'GROUPING'

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NAME = Column(String(255), nullable=False, unique=True)


class INSTRUMENT(Base, EntityHelper):
    __tablename__ = 'INSTRUMENT'
    __table_args__ = (
        Index('UNQ_INSTRUMENT_0', 'FACILITY_ID', 'NAME'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DESCRIPTION = Column(String(4000))
    FULLNAME = Column(String(255))
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NAME = Column(String(255), nullable=False)
    TYPE = Column(String(255))
    URL = Column(String(255))
    FACILITY_ID = Column(ForeignKey('FACILITY.ID'), nullable=False)

    FACILITY = relationship('FACILITY', primaryjoin='INSTRUMENT.FACILITY_ID == FACILITY.ID', backref='INSTRUMENT')


class INSTRUMENTSCIENTIST(Base, EntityHelper):
    __tablename__ = 'INSTRUMENTSCIENTIST'
    __table_args__ = (
        Index('UNQ_INSTRUMENTSCIENTIST_0', 'USER_ID', 'INSTRUMENT_ID'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    INSTRUMENT_ID = Column(ForeignKey('INSTRUMENT.ID'), nullable=False, index=True)
    USER_ID = Column(ForeignKey('USER_.ID'), nullable=False)

    INSTRUMENT = relationship('INSTRUMENT', primaryjoin='INSTRUMENTSCIENTIST.INSTRUMENT_ID == INSTRUMENT.ID',
                              backref='INSTRUMENTSCIENTIST')
    USER_ = relationship('USER', primaryjoin='INSTRUMENTSCIENTIST.USER_ID == USER.ID', backref='INSTRUMENTSCIENTIST')


class INVESTIGATION(Base, EntityHelper):
    __tablename__ = 'INVESTIGATION'
    __table_args__ = (
        Index('UNQ_INVESTIGATION_0', 'FACILITY_ID', 'NAME', 'VISIT_ID'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DOI = Column(String(255))
    ENDDATE = Column(DateTime)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NAME = Column(String(255), nullable=False)
    RELEASEDATE = Column(DateTime)
    STARTDATE = Column(DateTime)
    SUMMARY = Column(String(4000))
    TITLE = Column(String(255), nullable=False)
    VISIT_ID = Column(String(255), nullable=False)
    FACILITY_ID = Column(ForeignKey('FACILITY.ID'), nullable=False)
    TYPE_ID = Column(ForeignKey('INVESTIGATIONTYPE.ID'), nullable=False, index=True)

    FACILITY = relationship('FACILITY', primaryjoin='INVESTIGATION.FACILITY_ID == FACILITY.ID',
                            backref='INVESTIGATION')
    INVESTIGATIONTYPE = relationship('INVESTIGATIONTYPE', primaryjoin='INVESTIGATION.TYPE_ID == INVESTIGATIONTYPE.ID',
                                     backref='INVESTIGATION')


class INVESTIGATIONGROUP(Base, EntityHelper):
    __tablename__ = 'INVESTIGATIONGROUP'
    __table_args__ = (
        Index('UNQ_INVESTIGATIONGROUP_0', 'GROUP_ID', 'INVESTIGATION_ID', 'ROLE'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    ROLE = Column(String(255), nullable=False)
    GROUP_ID = Column(ForeignKey('GROUPING.ID'), nullable=False)
    INVESTIGATION_ID = Column(ForeignKey('INVESTIGATION.ID'), nullable=False, index=True)

    GROUPING = relationship('GROUPING', primaryjoin='INVESTIGATIONGROUP.GROUP_ID == GROUPING.ID',
                            backref='INVESTIGATIONGROUP')
    INVESTIGATION = relationship('INVESTIGATION', primaryjoin='INVESTIGATIONGROUP.INVESTIGATION_ID == INVESTIGATION.ID',
                                 backref='INVESTIGATIONGROUP')


class INVESTIGATIONINSTRUMENT(Base, EntityHelper):
    __tablename__ = 'INVESTIGATIONINSTRUMENT'
    __table_args__ = (
        Index('UNQ_INVESTIGATIONINSTRUMENT_0', 'INVESTIGATION_ID', 'INSTRUMENT_ID'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    INSTRUMENT_ID = Column(ForeignKey('INSTRUMENT.ID'), nullable=False, index=True)
    INVESTIGATION_ID = Column(ForeignKey('INVESTIGATION.ID'), nullable=False)

    INSTRUMENT = relationship('INSTRUMENT', primaryjoin='INVESTIGATIONINSTRUMENT.INSTRUMENT_ID == INSTRUMENT.ID',
                              backref='INVESTIGATIONINSTRUMENT')
    INVESTIGATION = relationship('INVESTIGATION',
                                 primaryjoin='INVESTIGATIONINSTRUMENT.INVESTIGATION_ID == INVESTIGATION.ID',
                                 backref='INVESTIGATIONINSTRUMENT')


class INVESTIGATIONPARAMETER(Base, EntityHelper):
    __tablename__ = 'INVESTIGATIONPARAMETER'
    __table_args__ = (
        Index('UNQ_INVESTIGATIONPARAMETER_0', 'INVESTIGATION_ID', 'PARAMETER_TYPE_ID'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DATETIME_VALUE = Column(DateTime)
    ERROR = Column(Float(asdecimal=True))
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NUMERIC_VALUE = Column(Float(asdecimal=True))
    RANGEBOTTOM = Column(Float(asdecimal=True))
    RANGETOP = Column(Float(asdecimal=True))
    STRING_VALUE = Column(String(4000))
    INVESTIGATION_ID = Column(ForeignKey('INVESTIGATION.ID'), nullable=False)
    PARAMETER_TYPE_ID = Column(ForeignKey('PARAMETERTYPE.ID'), nullable=False, index=True)

    INVESTIGATION = relationship('INVESTIGATION',
                                 primaryjoin='INVESTIGATIONPARAMETER.INVESTIGATION_ID == INVESTIGATION.ID',
                                 backref='INVESTIGATIONPARAMETER')
    PARAMETERTYPE = relationship('PARAMETERTYPE',
                                 primaryjoin='INVESTIGATIONPARAMETER.PARAMETER_TYPE_ID == PARAMETERTYPE.ID',
                                 backref='INVESTIGATIONPARAMETER')


class INVESTIGATIONTYPE(Base, EntityHelper):
    __tablename__ = 'INVESTIGATIONTYPE'
    __table_args__ = (
        Index('UNQ_INVESTIGATIONTYPE_0', 'NAME', 'FACILITY_ID'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DESCRIPTION = Column(String(255))
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NAME = Column(String(255), nullable=False)
    FACILITY_ID = Column(ForeignKey('FACILITY.ID'), nullable=False, index=True)

    FACILITY = relationship('FACILITY', primaryjoin='INVESTIGATIONTYPE.FACILITY_ID == FACILITY.ID',
                            backref='INVESTIGATIONTYPE')


class INVESTIGATIONUSER(Base, EntityHelper):
    __tablename__ = 'INVESTIGATIONUSER'
    __table_args__ = (
        Index('UNQ_INVESTIGATIONUSER_0', 'USER_ID', 'INVESTIGATION_ID', 'ROLE'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    ROLE = Column(String(255), nullable=False)
    INVESTIGATION_ID = Column(ForeignKey('INVESTIGATION.ID'), nullable=False, index=True)
    USER_ID = Column(ForeignKey('USER_.ID'), nullable=False)

    INVESTIGATION = relationship('INVESTIGATION', primaryjoin='INVESTIGATIONUSER.INVESTIGATION_ID == INVESTIGATION.ID',
                                 backref='INVESTIGATIONUSER')
    USER_ = relationship('USER', primaryjoin='INVESTIGATIONUSER.USER_ID == USER.ID', backref='INVESTIGATIONUSER')


class JOB(Base, EntityHelper):
    __tablename__ = 'JOB'

    ID = Column(BigInteger, primary_key=True)
    ARGUMENTS = Column(String(255))
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    APPLICATION_ID = Column(ForeignKey('APPLICATION.ID'), nullable=False, index=True)
    INPUTDATACOLLECTION_ID = Column(ForeignKey('DATACOLLECTION.ID'), index=True)
    OUTPUTDATACOLLECTION_ID = Column(ForeignKey('DATACOLLECTION.ID'), index=True)

    APPLICATION = relationship('APPLICATION', primaryjoin='JOB.APPLICATION_ID == APPLICATION.ID', backref='JOB')
    DATACOLLECTION = relationship('DATACOLLECTION', primaryjoin='JOB.INPUTDATACOLLECTION_ID == DATACOLLECTION.ID',
                                  backref='JOB')



class KEYWORD(Base, EntityHelper):
    __tablename__ = 'KEYWORD'
    __table_args__ = (
        Index('UNQ_KEYWORD_0', 'NAME', 'INVESTIGATION_ID'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NAME = Column(String(255), nullable=False)
    INVESTIGATION_ID = Column(ForeignKey('INVESTIGATION.ID'), nullable=False, index=True)

    INVESTIGATION = relationship('INVESTIGATION', primaryjoin='KEYWORD.INVESTIGATION_ID == INVESTIGATION.ID',
                                 backref='KEYWORD')


class PARAMETERTYPE(Base, EntityHelper):
    __tablename__ = 'PARAMETERTYPE'
    __table_args__ = (
        Index('UNQ_PARAMETERTYPE_0', 'FACILITY_ID', 'NAME', 'UNITS'),
    )

    ID = Column(BigInteger, primary_key=True)
    APPLICABLETODATACOLLECTION = Column(Integer, server_default=FetchedValue())
    APPLICABLETODATAFILE = Column(Integer, server_default=FetchedValue())
    APPLICABLETODATASET = Column(Integer, server_default=FetchedValue())
    APPLICABLETOINVESTIGATION = Column(Integer, server_default=FetchedValue())
    APPLICABLETOSAMPLE = Column(Integer, server_default=FetchedValue())
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DESCRIPTION = Column(String(255))
    ENFORCED = Column(Integer, server_default=FetchedValue())
    MAXIMUMNUMERICVALUE = Column(Float(asdecimal=True))
    MINIMUMNUMERICVALUE = Column(Float(asdecimal=True))
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NAME = Column(String(255), nullable=False)
    UNITS = Column(String(255), nullable=False)
    UNITSFULLNAME = Column(String(255))
    VALUETYPE = Column(Integer, nullable=False)
    VERIFIED = Column(Integer, server_default=FetchedValue())
    FACILITY_ID = Column(ForeignKey('FACILITY.ID'), nullable=False)

    FACILITY = relationship('FACILITY', primaryjoin='PARAMETERTYPE.FACILITY_ID == FACILITY.ID',
                            backref='PARAMETERTYPE')


class PERMISSIBLESTRINGVALUE(Base, EntityHelper):
    __tablename__ = 'PERMISSIBLESTRINGVALUE'
    __table_args__ = (
        Index('UNQ_PERMISSIBLESTRINGVALUE_0', 'VALUE', 'PARAMETERTYPE_ID'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    VALUE = Column(String(255), nullable=False)
    PARAMETERTYPE_ID = Column(ForeignKey('PARAMETERTYPE.ID'), nullable=False, index=True)

    PARAMETERTYPE = relationship('PARAMETERTYPE',
                                 primaryjoin='PERMISSIBLESTRINGVALUE.PARAMETERTYPE_ID == PARAMETERTYPE.ID',
                                 backref='PERMISSIBLESTRINGVALUE')


class PUBLICATION(Base, EntityHelper):
    __tablename__ = 'PUBLICATION'

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DOI = Column(String(255))
    FULLREFERENCE = Column(String(511), nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    REPOSITORY = Column(String(255))
    REPOSITORYID = Column(String(255))
    URL = Column(String(255))
    INVESTIGATION_ID = Column(ForeignKey('INVESTIGATION.ID'), nullable=False, index=True)

    INVESTIGATION = relationship('INVESTIGATION', primaryjoin='PUBLICATION.INVESTIGATION_ID == INVESTIGATION.ID',
                                 backref='PUBLICATION')


class PUBLICSTEP(Base, EntityHelper):
    __tablename__ = 'PUBLICSTEP'
    __table_args__ = (
        Index('UNQ_PUBLICSTEP_0', 'ORIGIN', 'FIELD'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    FIELD = Column(String(32), nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    ORIGIN = Column(String(32), nullable=False)


class RELATEDDATAFILE(Base, EntityHelper):
    __tablename__ = 'RELATEDDATAFILE'
    __table_args__ = (
        Index('UNQ_RELATEDDATAFILE_0', 'SOURCE_DATAFILE_ID', 'DEST_DATAFILE_ID'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    RELATION = Column(String(255), nullable=False)
    DEST_DATAFILE_ID = Column(ForeignKey('DATAFILE.ID'), nullable=False, index=True)
    SOURCE_DATAFILE_ID = Column(ForeignKey('DATAFILE.ID'), nullable=False)

    DATAFILE = relationship('DATAFILE', primaryjoin='RELATEDDATAFILE.DEST_DATAFILE_ID == DATAFILE.ID',
                            backref='RELATEDDATAFILE')


class RULE(Base, EntityHelper):
    __tablename__ = 'RULE_'

    ID = Column(BigInteger, primary_key=True)
    ATTRIBUTE = Column(String(255))
    BEAN = Column(String(255))
    C = Column(Integer, server_default=FetchedValue())
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    CRUDFLAGS = Column(String(4), nullable=False)
    CRUDJPQL = Column(String(1024))
    D = Column(Integer, server_default=FetchedValue())
    INCLUDEJPQL = Column(String(1024))
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    R = Column(Integer, server_default=FetchedValue())
    RESTRICTED = Column(Integer, server_default=FetchedValue())
    SEARCHJPQL = Column(String(1024))
    U = Column(Integer, server_default=FetchedValue())
    WHAT = Column(String(1024), nullable=False)
    GROUPING_ID = Column(ForeignKey('GROUPING.ID'), index=True)

    GROUPING = relationship('GROUPING', primaryjoin='RULE.GROUPING_ID == GROUPING.ID', backref='RULE')


class SAMPLE(Base, EntityHelper):
    __tablename__ = 'SAMPLE'
    __table_args__ = (
        Index('UNQ_SAMPLE_0', 'INVESTIGATION_ID', 'NAME'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NAME = Column(String(255), nullable=False)
    INVESTIGATION_ID = Column(ForeignKey('INVESTIGATION.ID'), nullable=False)
    SAMPLETYPE_ID = Column(ForeignKey('SAMPLETYPE.ID'), index=True)

    INVESTIGATION = relationship('INVESTIGATION', primaryjoin='SAMPLE.INVESTIGATION_ID == INVESTIGATION.ID',
                                 backref='SAMPLE')
    SAMPLETYPE = relationship('SAMPLETYPE', primaryjoin='SAMPLE.SAMPLETYPE_ID == SAMPLETYPE.ID', backref='SAMPLE')


class SAMPLEPARAMETER(Base, EntityHelper):
    __tablename__ = 'SAMPLEPARAMETER'
    __table_args__ = (
        Index('UNQ_SAMPLEPARAMETER_0', 'SAMPLE_ID', 'PARAMETER_TYPE_ID'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DATETIME_VALUE = Column(DateTime)
    ERROR = Column(Float(asdecimal=True))
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NUMERIC_VALUE = Column(Float(asdecimal=True))
    RANGEBOTTOM = Column(Float(asdecimal=True))
    RANGETOP = Column(Float(asdecimal=True))
    STRING_VALUE = Column(String(4000))
    SAMPLE_ID = Column(ForeignKey('SAMPLE.ID'), nullable=False)
    PARAMETER_TYPE_ID = Column(ForeignKey('PARAMETERTYPE.ID'), nullable=False, index=True)

    PARAMETERTYPE = relationship('PARAMETERTYPE', primaryjoin='SAMPLEPARAMETER.PARAMETER_TYPE_ID == PARAMETERTYPE.ID',
                                 backref='SAMPLEPARAMETER')
    SAMPLE = relationship('SAMPLE', primaryjoin='SAMPLEPARAMETER.SAMPLE_ID == SAMPLE.ID', backref='SAMPLEPARAMETER')


class SESSION(Base, EntityHelper):
    __tablename__ = 'SESSION_'

    ID = Column(String(255), primary_key=True)
    EXPIREDATETIME = Column(DateTime)
    USERNAME = Column(String(255))


class SHIFT(Base, EntityHelper):
    __tablename__ = 'SHIFT'
    __table_args__ = (
        Index('UNQ_SHIFT_0', 'INVESTIGATION_ID', 'STARTDATE', 'ENDDATE'),
    )

    ID = Column(BigInteger, primary_key=True)
    COMMENT = Column(String(255))
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    ENDDATE = Column(DateTime, nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    STARTDATE = Column(DateTime, nullable=False)
    INVESTIGATION_ID = Column(ForeignKey('INVESTIGATION.ID'), nullable=False)

    INVESTIGATION = relationship('INVESTIGATION', primaryjoin='SHIFT.INVESTIGATION_ID == INVESTIGATION.ID',
                                 backref='SHIFT')


class USER(Base, EntityHelper):
    __tablename__ = 'USER_'

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    EMAIL = Column(String(255))
    FULLNAME = Column(String(255))
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NAME = Column(String(255), nullable=False, unique=True)
    ORCIDID = Column(String(255))


class USERGROUP(Base, EntityHelper):
    __tablename__ = 'USERGROUP'
    __table_args__ = (
        Index('UNQ_USERGROUP_0', 'USER_ID', 'GROUP_ID'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    GROUP_ID = Column(ForeignKey('GROUPING.ID'), nullable=False, index=True)
    USER_ID = Column(ForeignKey('USER_.ID'), nullable=False)

    GROUPING = relationship('GROUPING', primaryjoin='USERGROUP.GROUP_ID == GROUPING.ID', backref='USERGROUP')
    USER_ = relationship('USER', primaryjoin='USERGROUP.USER_ID == USER.ID', backref='USERGROUP')


class STUDYINVESTIGATION(Base, EntityHelper):
    __tablename__ = 'STUDYINVESTIGATION'
    __table_args__ = (
        Index('UNQ_STUDYINVESTIGATION_0', 'STUDY_ID', 'INVESTIGATION_ID'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    INVESTIGATION_ID = Column(ForeignKey('INVESTIGATION.ID'), nullable=False, index=True)
    STUDY_ID = Column(ForeignKey('STUDY.ID'), nullable=False)

    INVESTIGATION = relationship('INVESTIGATION', primaryjoin='STUDYINVESTIGATION.INVESTIGATION_ID == INVESTIGATION.ID',
                                 backref='STUDYINVESTIGATION')
    STUDY = relationship('STUDY', primaryjoin='STUDYINVESTIGATION.STUDY_ID == STUDY.ID', backref='STUDYINVESTIGATION')


class STUDY(Base, EntityHelper):
    __tablename__ = 'STUDY'

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    DESCRIPTION = Column(String(4000))
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    NAME = Column(String(255), nullable=False)
    STARTDATE = Column(DateTime)
    STATUS = Column(Integer)
    USER_ID = Column(ForeignKey('USER_.ID'), index=True)

    USER_ = relationship('USER', primaryjoin='STUDY.USER_ID == USER.ID', backref='STUDY')


class SAMPLETYPE(Base, EntityHelper):
    __tablename__ = 'SAMPLETYPE'
    __table_args__ = (
        Index('UNQ_SAMPLETYPE_0', 'FACILITY_ID', 'NAME', 'MOLECULARFORMULA'),
    )

    ID = Column(BigInteger, primary_key=True)
    CREATE_ID = Column(String(255), nullable=False)
    CREATE_TIME = Column(DateTime, nullable=False)
    MOD_ID = Column(String(255), nullable=False)
    MOD_TIME = Column(DateTime, nullable=False)
    MOLECULARFORMULA = Column(String(255), nullable=False)
    NAME = Column(String(255), nullable=False)
    SAFETYINFORMATION = Column(String(4000))
    FACILITY_ID = Column(ForeignKey('FACILITY.ID'), nullable=False)

    FACILITY = relationship('FACILITY', primaryjoin='SAMPLETYPE.FACILITY_ID == FACILITY.ID', backref='SAMPLETYPE')
