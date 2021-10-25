"""
Code to define the PaNOSC data model
TODO - Implement these using pydantic
"""


from abc import ABC, abstractclassmethod, abstractmethod


class PaNOSCAttribute(ABC):
    @abstractclassmethod
    def from_icat(cls):
        pass

    @abstractmethod
    def to_icat(self):
        pass


class Affiliation(PaNOSCAttribute):
    """Information about which facility a member is located at"""

    def __init__(self, id_, name=None, address=None, city=None, country=None):
        # TODO - Inconsistency in data models regarding id and pid's
        self.id = id_
        self.name = name
        self.address = address
        self.city = city
        self.country = country

        self.affiliations = None

    @classmethod
    def from_icat(cls):
        pass

    def to_icat(self):
        pass


class Dataset(PaNOSCAttribute):
    """
    Information about an experimental run, including optional File, Sample, Instrument
    and Technique
    """

    def __init__(self, pid, title, is_public, creation_date, size=None):
        self.pid = pid  # TODO - dataset.doi, field not filled out by ISIS
        self.title = title  # TODO - dataset.name, only ~1k of ISIS' 159k datasets aren't called "raw"
        self.isPublic = is_public  # Evaluate 3 years from date
        self.creationDate = creation_date  # TODO - dataset.startDate or creationDate? startDate is null on ISIS
        self.size = size  # TODO - Would require TopCAT request, but not mandatory

        self.documents = Document()
        self.techniques = Technique()
        self.instrument = None
        self.files = None
        self.parameters = None
        self.samples = None

    @classmethod
    def from_icat(cls):
        pass

    def to_icat(self):
        pass


class Document(PaNOSCAttribute):
    """
    Proposal which includes the dataset or published paper which references the dataset
    """

    def __init__(
        self,
        pid,
        is_public,
        type_,
        title,
        summary=None,
        doi=None,
        start_date=None,
        end_date=None,
        release_date=None,
        license_=None,
        keywords=None,
    ):
        self.pid = pid  # investigation.doi
        self.isPublic = is_public  # TODO - Evaluate 3 years of startDate or releaseDate
        self.type = type_  # TODO - investigation.type.name
        self.title = title  # investigaton.name
        self.summary = summary  # investigation.summary
        self.doi = doi  # TODO - investigation.doi but we already use that for pid
        self.startDate = start_date  # investigation.startDate
        self.endDate = end_date  # investigation.endDate
        self.releaseDate = release_date  # investigation.releaseDate
        self.license = license_  # Not stored in ICAT but not mandatory, ignore
        self.keywords = keywords  # TODO - Iterate through keywords.name?

        self.datasets = Dataset()
        self.members = None
        self.parameters = None

    @classmethod
    def from_icat(cls):
        pass

    def to_icat(self):
        pass


class File(PaNOSCAttribute):
    """Name of file and optionally location"""

    def __init__(self, id_, name, path=None, size=None):
        self.id = id_  # datafile.id
        self.name = name  # datafile.name
        self.path = path  # datafile.location
        self.size = size  # datafile.fileSize

        self.dataset = Dataset()

    @classmethod
    def from_icat(cls):
        pass

    def to_icat(self):
        pass


class Instrument(PaNOSCAttribute):
    """Beam line where experiment took place"""

    def __init__(self, id_, name, facility):
        self.id = id_  # instrument.id
        self.name = name  # instrument.name
        self.facility = facility  # TODO - instrument.facility.name or fullName

        self.datasets = None

    @classmethod
    def from_icat(cls):
        pass

    def to_icat(self):
        pass


class Member(PaNOSCAttribute):
    """Proposal team member or paper co-author"""

    def __init__(self, role=None):
        self.role = role  # investigationUser.role

        self.person = Person()
        self.affiliations = None

    @classmethod
    def from_icat(cls):
        pass

    def to_icat(self):
        pass


class Parameter(PaNOSCAttribute):
    """
    Scalar measurement with value and units.
    Note: a parameter is either related to a dataset or a document, but not both.
    """

    def __init__(self, name, value, unit=None):
        self.name = name  # investigationParameter.type.name
        """
        Value can be a number or a string so either field can be used, ICAT also has
        dateTimeValue which we could check and convert into a string if there's no
        stringValue or numericValue
        """
        self.value = value  # investigationParameter.numericValue or stringValue
        self.unit = unit  # TODO - investigationParameter.type.units or unitsFullName. In ISIS, units is just "None", full name is null

    @classmethod
    def from_icat(cls):
        pass

    def to_icat(self):
        pass


class Person(PaNOSCAttribute):
    """Human who carried out experiment"""

    def __init__(
        self,
        id_,
        full_name,
        orcidid=None,
        researcher_id=None,
        first_name=None,
        last_name=None,
    ):
        # TODO - anon doesn't have permissions to query users on ISIS, has to be on an include
        self.id = id_  # user.id
        self.full_name = full_name  # user.fullName
        self.orcidid = orcidid  # user.orcidId
        self.researcherId = researcher_id  # TODO - not sure, not mandatory, keep blank?
        # TODO - These can be null on ISIS data?
        self.firstName = first_name  # user.givenName
        self.lastName = last_name  # user.familyName

    @classmethod
    def from_icat(cls):
        pass

    def to_icat(self):
        pass


class Sample(PaNOSCAttribute):
    """Extract of material used in the experiment"""

    def __init__(self, name, pid=None, description=None):
        self.name = name  # sample.name
        self.pid = pid  # TODO - sample.pid, seems to be null on ISIS
        # parameters will be a list, description isn't mandatory, maybe just leave?
        self.description = description  # TODO - sample.parameters.type.description

        self.datasets = None

    @classmethod
    def from_icat(cls):
        pass

    def to_icat(self):
        pass


class Technique(PaNOSCAttribute):
    """Common name of scientific method used"""

    def __init__(self, pid, name):
        self.pid = pid
        self.name = name

    @classmethod
    def from_icat(cls):
        pass

    def to_icat(self):
        pass
