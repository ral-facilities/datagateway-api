from datetime import datetime
import enum
from typing import List, Optional

from pydantic import BaseModel


class Application(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    name: str
    version: str
    facilityID: int

    FACILITY: Optional["Facility"] = None

    jobs: Optional[List["Job"]] = None


class Affiliation(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    name: str
    fullReference: Optional[str] = None
    pid: Optional[str] = None
    dataPublicationUserId: int

    DATAPUBLICATIONUSER: Optional["DataPublicationUser"] = None


class Facility(BaseModel):
    id: int
    createId: str
    createTime: datetime
    daysUntilRelease: Optional[int] = None
    description: Optional[str] = None
    fullName: Optional[str] = None
    modId: str
    modTime: datetime
    name: str
    url: Optional[str] = None

    applications: Optional[List[Application]] = None
    dataPublications: Optional[List["DataPublication"]] = None
    dataPublicationTypes: Optional[List["DataPublicationType"]] = None
    datafileFormats: Optional[List["DatafileFormat"]] = None
    datasetTypes: Optional[List["DatasetType"]] = None
    facilityCycles: Optional[List["FacilityCycle"]] = None
    instruments: Optional[List["Instrument"]] = None
    investigations: Optional[List["Investigation"]] = None
    investigationTypes: Optional[List["InvestigationType"]] = None
    parameterTypes: Optional[List["ParameterType"]] = None
    sampleTypes: Optional[List["SampleType"]] = None


class DataCollection(BaseModel):
    id: int
    createId: str
    createTime: datetime
    doi: Optional[str] = None
    modId: str
    modTime: datetime

    dataCollectionDatafiles: Optional[List["DataCollectionDatafile"]] = None
    dataCollectionDatasets: Optional[List["DataCollectionDataset"]] = None
    dataCollectionParameters: Optional[List["DataCollectionParameter"]] = None
    dataCollectionInvestigations: Optional[List["DataCollectionInvestigation"]] = None
    dataPublications: Optional[List["DataPublication"]] = None
    jobs: Optional[List["Job"]] = None


class DataCollectionDatafile(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    dataCollectionID: int
    datafileID: int

    DATACOLLECTION: Optional["DataCollection"] = None
    DATAFILE: Optional["Datafile"] = None


class DataCollectionDataset(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    dataCollectionID: int
    datasetID: int

    DATACOLLECTION: Optional["DataCollection"] = None
    DATASET: Optional["Dataset"] = None


class DataCollectionParameter(BaseModel):
    id: int
    createId: str
    createTime: datetime
    dateTimeValue: Optional[datetime] = None
    error: Optional[float] = None
    modId: str
    modTime: datetime
    numericValue: Optional[float] = None
    rangeBottom: Optional[float] = None
    rangeTop: Optional[float] = None
    stringValue: Optional[str] = None
    dataCollectionID: int
    parameterTypeID: int

    DATACOLLECTION: Optional["DataCollection"] = None
    PARAMETERTYPE: Optional["ParameterType"] = None


class DataCollectionInvestigation(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    datacollectionId: int
    investigationId: int

    DATACOLLECTION: Optional["DataCollection"] = None
    INVESTIGATION: Optional["Investigation"] = None


class DataPublication(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    publicationDate: Optional[datetime] = None
    title: str
    description: Optional[str] = None
    pid: str
    subject: Optional[str] = None
    datacollectionId: int
    facilityId: int
    datapublicationtypeId: int

    DATACOLLECTION: Optional[DataCollection] = None
    FACILITY: Optional[Facility] = None
    DATAPUBLICATIONTYPE: Optional["DataPublicationType"] = None

    dataPublicationDates: Optional[List["DataPublicationDate"]] = None
    fundingReferences: Optional[List["FundingReference"]] = None
    users: Optional[List["User"]] = None
    relatedItems: Optional[List["RelatedItem"]] = None


class DataPublicationDate(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    dateType: str
    date: str
    datapublicationId: int

    DATAPUBLICATION: Optional[DataPublication] = None


class DataPublicationFunding(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    datapublicationId: int
    fundingId: int

    DATAPUBLICATION: Optional[DataPublication] = None
    FUNDINGREFERENCE: Optional["FundingReference"] = None


class DataPublicationType(BaseModel):
    id: int
    createId: Optional[str] = None
    createTime: Optional[datetime] = None
    modId: str
    modTime: datetime
    name: str
    description: Optional[str] = None
    facilityId: int

    FACILITY: Optional[Facility] = None

    dataPublications: Optional[List[DataPublication]] = None


class DataPublicationUser(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    orderKey: Optional[str] = None
    givenName: Optional[str] = None
    fullName: Optional[str] = None
    familyName: Optional[str] = None
    email: Optional[str] = None
    contributorType: str
    publicationId: int
    userId: int

    USER: Optional["User"] = None
    DATAPUBLICATION: Optional[DataPublication] = None

    affiliations: Optional[List[Affiliation]] = None


class Datafile(BaseModel):
    id: int
    checksum: Optional[str] = None
    createId: str
    createTime: datetime
    datafileCreateTime: Optional[datetime] = None
    datafileModTime: Optional[datetime] = None
    description: Optional[str] = None
    doi: Optional[str] = None
    fileSize: Optional[int] = None
    location: Optional[str] = None
    modId: str
    modTime: datetime
    name: str
    datafileFormatID: Optional[int] = None
    datasetID: int  #

    DATAFILEFORMAT: Optional["DatafileFormat"] = None
    DATASET: Optional["Dataset"] = None

    dataCollectionDatafiles: Optional[List[DataCollectionDatafile]] = None
    datafileParameters: Optional[List["DatafileParameter"]] = None
    relatedDatafiles: Optional[List["RelatedDatafile"]] = None


class DatafileFormat(BaseModel):
    id: int
    createId: str
    createTime: datetime
    description: Optional[str] = None
    modId: str
    modTime: datetime
    name: str
    type: Optional[str] = None
    version: str
    facilityID: int

    FACILITY: Optional[Facility] = None

    datafiles: Optional[List[Datafile]] = None


class DatafileParameter(BaseModel):
    id: int
    createId: str
    createTime: datetime
    dateTimeValue: Optional[datetime] = None
    error: Optional[float] = None
    modId: str
    modTime: datetime
    numericValue: Optional[float] = None
    rangeBottom: Optional[float] = None
    rangeTop: Optional[float] = None
    stringValue: Optional[str] = None
    datafileID: int
    parameterTypeID: int

    DATAFILE: Optional[Datafile] = None
    PARAMETERTYPE: Optional["ParameterType"] = None


class Dataset(BaseModel):
    id: int
    complete: bool
    createId: str
    createTime: datetime
    description: Optional[str] = None
    doi: Optional[str] = None
    endDate: Optional[datetime] = None
    location: Optional[str] = None
    modId: str
    modTime: datetime
    name: str
    startDate: Optional[datetime] = None
    investigationID: int
    sampleID: Optional[int] = None
    typeID: int

    INVESTIGATION: Optional["Investigation"] = None
    SAMPLE: Optional["Sample"] = None
    DATASETTYPE: Optional["DatasetType"] = None

    dataCollectionDatasets: Optional[List[DataCollectionDataset]] = None
    datafiles: Optional[List[Datafile]] = None
    datasetParameters: Optional[List["DatasetParameter"]] = None
    datasetInstruments: Optional[List["DatasetInstrument"]] = None
    datasetTechniques: Optional[List["DatasetTechnique"]] = None


class DatasetParameter(BaseModel):
    id: int
    createId: str
    createTime: datetime
    dateTimeValue: Optional[datetime] = None
    error: Optional[float] = None
    modId: str
    modTime: datetime
    numericValue: Optional[float] = None
    rangeBottom: Optional[float] = None
    rangeTop: Optional[float] = None
    stringValue: Optional[str] = None
    datasetID: int
    parameterTypeID: int

    DATASET: Optional[Dataset] = None
    PARAMETERTYPE: Optional["ParameterType"] = None


class DatasetType(BaseModel):
    id: int
    createId: str
    createTime: datetime
    description: Optional[str] = None
    modId: str
    modTime: datetime
    name: str
    facilityID: int

    FACILITY: Optional[Facility] = None

    datasets: Optional[List[Dataset]] = None


class DatasetInstrument(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    datasetId: int
    instrumentId: int

    DATASET: Optional[Dataset] = None
    INSTRUMENT: Optional["Instrument"] = None


class DatasetTechnique(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    datasetId: int
    techniqueId: int

    DATASET: Optional[Dataset] = None
    TECHNIQUE: Optional["Technique"] = None


class FacilityCycle(BaseModel):
    id: int
    createId: str
    createTime: datetime
    description: Optional[str] = None
    endDate: Optional[datetime] = None
    modId: str
    modTime: datetime
    name: str
    startDate: Optional[datetime] = None
    facilityID: int

    FACILITY: Optional[Facility] = None

    investigationFacilityCycles: Optional[List["InvestigationFacilityCycle"]] = None


class FundingReference(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    funderIdentifier: Optional[str] = None
    funderName: str
    awardNumber: str
    awardTitle: Optional[str] = None

    publications: Optional[List["Publication"]] = None
    investigations: Optional[List["Investigation"]] = None


class Grouping(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    name: str

    investigationGroups: Optional[List["InvestigationGroup"]] = None
    rules: Optional[List["Rule"]] = None
    grouping: Optional[List["Grouping"]] = None


class Instrument(BaseModel):
    id: int
    createId: str
    createTime: datetime
    description: Optional[str] = None
    fullName: Optional[str] = None
    modId: str
    modTime: datetime
    name: str
    type: Optional[str] = None
    url: Optional[str] = None
    facilityID: int

    FACILITY: Optional[Facility] = None

    datasetInstruments: Optional[List[DatasetInstrument]] = None
    instrumentScientists: Optional[List["InstrumentScientist"]] = None
    investigationInstruments: Optional[List["InvestigationInstrument"]] = None


class InstrumentScientist(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    instrumentID: int
    userID: int

    INSTRUMENT: Optional[Instrument] = None
    USER: Optional["User"] = None


class Investigation(BaseModel):
    id: int
    createId: str
    createTime: datetime
    doi: Optional[str] = None
    endDate: Optional[datetime] = None
    modId: str
    modTime: datetime
    name: str
    releaseDate: Optional[datetime] = None
    startDate: Optional[datetime] = None
    summary: Optional[str] = None
    title: str
    visitId: str
    facilityID: int
    typeID: int
    fileSize: Optional[int] = None
    fileCount: Optional[int] = None

    FACILITY: Optional[Facility] = None
    INVESTIGATIONTYPE: Optional["InvestigationType"] = None

    dataCollectionInvestigations: Optional[List[DataCollectionInvestigation]] = None
    datasets: Optional[List[Dataset]] = None
    investigationFacilityCycles: Optional[List["InvestigationFacilityCycle"]] = None
    fundingReferences: Optional[List[FundingReference]] = None
    investigationGroups: Optional[List["InvestigationGroup"]] = None
    investigationInstruments: Optional[List["InvestigationInstrument"]] = None
    investigationParameters: Optional[List["InvestigationParameter"]] = None
    investigationUsers: Optional[List["InvestigationUser"]] = None
    keywords: Optional[List["Keyword"]] = None
    publications: Optional[List["Publication"]] = None
    samples: Optional[List["Sample"]] = None
    shifts: Optional[List["Shift"]] = None
    studyInvestigations: Optional[List["StudyInvestigation"]] = None


class InvestigationFacilityCycle(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    facilityCycleId: int
    investigationId: int

    FACILITYCYCLE: Optional[FacilityCycle] = None
    INVESTIGATION: Optional[Investigation] = None


class InvestigationFunding(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    fundingId: int
    investigationId: int

    FUNDINGREFERENCE: Optional[FundingReference] = None
    INVESTIGATION: Optional[Investigation] = None


class InvestigationGroup(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    role: str
    groupID: int
    investigationID: int

    GROUPING: Optional[Grouping] = None
    INVESTIGATION: Optional[Investigation] = None


class InvestigationInstrument(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    instrumentID: int
    investigationID: int

    INSTRUMENT: Optional[Instrument] = None
    INVESTIGATION: Optional[Investigation] = None


class InvestigationParameter(BaseModel):
    id: int
    createId: str
    createTime: datetime
    dateTimeValue: Optional[datetime] = None
    error: Optional[float] = None
    modId: str
    modTime: datetime
    numericValue: Optional[float] = None
    rangeBottom: Optional[float] = None
    rangeTop: Optional[float] = None
    stringValue: Optional[str] = None
    investigationID: int
    parameterTypeID: int

    INVESTIGATION: Optional[Investigation] = None
    PARAMETERTYPE: Optional["ParameterType"] = None


class InvestigationType(BaseModel):
    id: int
    createId: str
    createTime: datetime
    description: Optional[str] = None
    modId: str
    modTime: datetime
    name: str
    facilityID: int

    FACILITY: Optional[Facility] = None

    investigations: Optional[List[Investigation]] = None


class InvestigationUser(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    role: str
    investigationID: int
    userID: int

    INVESTIGATION: Optional[Investigation] = None
    USER: Optional["User"] = None


class Job(BaseModel):
    id: int
    arguments: Optional[str] = None
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    applicationID: int
    inputDataCollectionID: Optional[int] = None
    outputDataCollectionID: Optional[int] = None

    APPLICATION: Optional[Application] = None
    DATACOLLECTION: Optional[DataCollection] = None


class Keyword(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    name: str
    investigationID: int

    INVESTIGATION: Optional[Investigation] = None


class ParameterType(BaseModel):
    class ValueTypeEnum(enum.Enum):
        DATE_AND_TIME = 0
        NUMERIC = 1
        STRING = 2

    id: int
    applicableToDataCollection: Optional[bool] = None
    applicableToDatafile: Optional[bool] = None
    applicableToDataset: Optional[bool] = None
    applicableToInvestigation: Optional[bool] = None
    applicableToSample: Optional[bool] = None
    createId: str
    createTime: datetime
    description: Optional[str] = None
    enforced: Optional[bool] = None
    maximumNumericValue: Optional[float] = None
    minimumNumericValue: Optional[float] = None
    modId: str
    modTime: datetime
    name: str
    units: str
    unitsFullName: Optional[str] = None
    valueType: ValueTypeEnum
    verified: Optional[bool] = None
    facilityID: int

    FACILITY: Optional[Facility] = None

    dataCollectionParameters: Optional[List[DataCollectionParameter]] = None
    datafileParameters: Optional[List[DatafileParameter]] = None
    datasetParameters: Optional[List[DatasetParameter]] = None
    investigationParameters: Optional[List[InvestigationParameter]] = None
    permissibleStringValues: Optional[List["PermissibleStringValue"]] = None
    sampleParameters: Optional[List["SampleParameter"]] = None


class PermissibleStringValue(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    value: str
    parameterTypeID: int

    PARAMETERTYPE: Optional[ParameterType] = None


class Publication(BaseModel):
    id: int
    createId: str
    createTime: datetime
    doi: Optional[str] = None
    fullReference: str
    modId: str
    modTime: datetime
    repository: Optional[str] = None
    repositoryId: Optional[str] = None
    url: Optional[str] = None
    investigationID: int

    INVESTIGATION: Optional[Investigation] = None


class PublicStep(BaseModel):
    id: int
    createId: str
    createTime: datetime
    field: str
    modId: str
    modTime: datetime
    origin: str


class RelatedDatafile(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    relation: str
    destDatafileID: int
    sourceDatafileID: int

    DATAFILE: Optional[Datafile] = None


class RelatedItem(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    identifier: str
    relationType: str
    fullReference: Optional[str] = None
    relatedItemType: Optional[str] = None
    title: Optional[str] = None
    datapublicationId: int

    PUBLICATION: Optional[DataPublication] = None


class Rule(BaseModel):
    id: int
    attribute: Optional[str] = None
    bean: Optional[str] = None
    c: Optional[int] = None
    createId: str
    createTime: datetime
    crudFlags: str
    crudJPQL: Optional[str] = None
    d: Optional[int] = None
    includeJPQL: Optional[str] = None
    modId: str
    modTime: datetime
    r: Optional[int] = None
    restricted: Optional[int] = None
    searchJPQL: Optional[str] = None
    u: Optional[int] = None
    what: str
    groupingID: Optional[int] = None

    GROUPING: Optional[Grouping] = None


class Sample(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    name: str
    investigationID: int
    sampleTypeID: Optional[int] = None

    INVESTIGATION: Optional[Investigation] = None
    SAMPLETYPE: Optional["SampleType"] = None

    datasets: Optional[List[Dataset]] = None
    sampleParameters: Optional[List["SampleParameter"]] = None


class SampleParameter(BaseModel):
    id: int
    createId: str
    createTime: datetime
    dateTimeValue: Optional[datetime] = None
    error: Optional[float] = None
    modId: str
    modTime: datetime
    numericValue: Optional[float] = None
    rangeBottom: Optional[float] = None
    rangeTop: Optional[float] = None
    stringValue: Optional[str] = None
    sampleID: int
    parameterTypeID: int

    SAMPLE: Optional[Sample] = None
    PARAMETERTYPE: Optional[ParameterType] = None


class Session(BaseModel):
    id: str
    expireDateTime: Optional[datetime] = None
    username: Optional[str] = None


class Shift(BaseModel):
    id: int
    comment: Optional[str] = None
    createId: str
    createTime: datetime
    endDate: datetime
    modId: str
    modTime: datetime
    startDate: datetime
    investigationID: int

    INVESTIGATION: Optional[Investigation] = None


class Technique(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    pid: Optional[str] = None
    description: Optional[str] = None
    name: str

    datasetTechniques: Optional[List[DatasetTechnique]] = None


class User(BaseModel):
    id: int
    createId: str
    createTime: datetime
    email: Optional[str] = None
    fullName: Optional[str] = None
    modId: str
    modTime: datetime
    name: str
    orcidId: Optional[str] = None

    dataPublicationUsers: Optional[List[DataPublicationUser]] = None
    instrumentScientists: Optional[List[InstrumentScientist]] = None
    investigationUsers: Optional[List[InvestigationUser]] = None
    userGroups: Optional[List["UserGroup"]] = None
    studies: Optional[List["Study"]] = None


class UserGroup(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    groupID: int
    userID: int

    GROUPING: Optional[Grouping] = None
    USER: Optional[User] = None


class StudyInvestigation(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    investigationID: int
    studyID: int

    INVESTIGATION: Optional[Investigation] = None
    STUDY: Optional["Study"] = None


class Study(BaseModel):
    id: int
    createId: str
    createTime: datetime
    description: Optional[str] = None
    modId: str
    modTime: datetime
    name: str
    pid: Optional[str] = None
    startDate: Optional[datetime] = None
    status: Optional[int] = None
    userID: Optional[int] = None

    USER: Optional[User] = None

    studyInvestigations: Optional[List[StudyInvestigation]] = None


class SampleType(BaseModel):
    id: int
    createId: str
    createTime: datetime
    modId: str
    modTime: datetime
    molecularFormula: str
    name: str
    safetyInformation: Optional[str] = None
    facilityID: int

    FACILITY: Optional[Facility] = None

    samples: Optional[List[Sample]] = None


Application.model_rebuild()
Affiliation.model_rebuild()
Facility.model_rebuild()
DataCollection.model_rebuild()
DataCollectionDatafile.model_rebuild()
DataCollectionDataset.model_rebuild()
DataCollectionParameter.model_rebuild()
DataCollectionInvestigation.model_rebuild()
DataPublication.model_rebuild()
DataPublicationDate.model_rebuild()
DataPublicationFunding.model_rebuild()
DataPublicationType.model_rebuild()
DataPublicationUser.model_rebuild()
Datafile.model_rebuild()
DatafileFormat.model_rebuild()
DatafileParameter.model_rebuild()
Dataset.model_rebuild()
DatasetParameter.model_rebuild()
DatasetType.model_rebuild()
DatasetInstrument.model_rebuild()
DatasetTechnique.model_rebuild()
FacilityCycle.model_rebuild()
FundingReference.model_rebuild()
Grouping.model_rebuild()
Instrument.model_rebuild()
InstrumentScientist.model_rebuild()
Investigation.model_rebuild()
InvestigationFacilityCycle.model_rebuild()
InvestigationFunding.model_rebuild()
InvestigationGroup.model_rebuild()
InvestigationInstrument.model_rebuild()
InvestigationParameter.model_rebuild()
InvestigationType.model_rebuild()
InvestigationUser.model_rebuild()
Job.model_rebuild()
Keyword.model_rebuild()
ParameterType.model_rebuild()
PermissibleStringValue.model_rebuild()
Publication.model_rebuild()
PublicStep.model_rebuild()
RelatedDatafile.model_rebuild()
RelatedItem.model_rebuild()
Rule.model_rebuild()
Sample.model_rebuild()
SampleParameter.model_rebuild()
Shift.model_rebuild()
Technique.model_rebuild()
User.model_rebuild()
UserGroup.model_rebuild()
StudyInvestigation.model_rebuild()
Study.model_rebuild()
SampleType.model_rebuild()
