from flask import Flask
from flask_restful import Api

from common.config import config
from common.logger_setup import setup_logger
from src.resources.entities.applications_endpoints import *
from src.resources.entities.datacollection_datafiles_endpoints import *
from src.resources.entities.datacollection_datasets_endpoints import *
from src.resources.entities.datacollection_parameters_endpoints import *
from src.resources.entities.datacollections_endpoints import *
from src.resources.entities.datafile_formats_endpoints import *
from src.resources.entities.datafile_parameters_endpoints import *
from src.resources.entities.datafiles_endpoints import *
from src.resources.entities.dataset_type_endpoints import *
from src.resources.entities.datasets_endpoints import *
from src.resources.entities.facilities_endpoints import *
from src.resources.entities.facility_cycles_endpoints import *
from src.resources.entities.groupings_endpoints import *
from src.resources.entities.instrument_scientists_endpoints import *
from src.resources.entities.instruments_endpoints import *
from src.resources.entities.investigation_groups_endpoints import *
from src.resources.entities.investigation_instruments_endpoints import *
from src.resources.entities.investigation_parameters_endpoints import *
from src.resources.entities.investigation_types_endpoints import *
from src.resources.entities.investigation_users_endpoints import *
from src.resources.entities.investigations_endpoints import *
from src.resources.entities.jobs_endpoints import *
from src.resources.entities.keywords_endpoints import *
from src.resources.entities.parameter_types_endpoints import *
from src.resources.entities.permissible_string_values_endpoints import *
from src.resources.entities.public_steps_endpoints import *
from src.resources.entities.publications_endpoints import *
from src.resources.entities.related_datafiles_endpoints import *
from src.resources.entities.rules_endpoints import *
from src.resources.entities.sample_parameters_endpoints import *
from src.resources.entities.sample_types_endpoints import *
from src.resources.entities.samples_endpoints import *
from src.resources.entities.shifts_endpoints import *
from src.resources.entities.studies_endpoints import *
from src.resources.entities.study_investigations_endpoints import *
from src.resources.entities.user_groups_endpoints import *
from src.resources.entities.users_endpoints import *
from src.resources.non_entities.sessions_endpoints import *
from src.resources.table_endpoints.table_endpoints import UsersInvestigations, UsersInvestigationsCount, \
    InstrumentsFacilityCycles, InstrumentsFacilityCyclesCount, InstrumentsFacilityCyclesInvestigations, \
    InstrumentsFacilityCyclesInvestigationsCount
from src.swagger.swagger_generator import swagger_gen

swagger_gen.write_swagger_spec()

app = Flask(__name__)
api = Api(app)

setup_logger()

api.add_resource(Applications, "/applications")
api.add_resource(ApplicationsWithID, "/applications/<int:id>")
api.add_resource(ApplicationsCount, "/applications/count")
api.add_resource(ApplicationsFindOne, "/applications/findOne")
api.add_resource(DataCollections, "/datacollections")
api.add_resource(DataCollectionsWithID, "/datacollections/<int:id>")
api.add_resource(DataCollectionsCount, "/datacollections/count")
api.add_resource(DataCollectionsFindOne, "/datacollections/findOne")
api.add_resource(DataCollectionDatafiles, "/datacollectiondatafiles")
api.add_resource(DataCollectionDatafilesWithID, "/datacollectiondatafiles/<int:id>")
api.add_resource(DataCollectionDatafilesCount, "/datacollectiondatafiles/count")
api.add_resource(DataCollectionDatafilesFindOne, "/datacollectiondatafiles/findOne")
api.add_resource(DataCollectionDatasets, "/datacollectiondatasets")
api.add_resource(DataCollectionDatasetsWithID, "/datacollectiondatasets/<int:id>")
api.add_resource(DataCollectionDatasetsCount, "/datacollectiondatasets/count")
api.add_resource(DataCollectionDatasetsFindOne, "/datacollectiondatasets/findOne")
api.add_resource(DataCollectionParameters, "/datacollectionparameters")
api.add_resource(DataCollectionParametersWithID, "/datacollectionparameters/<int:id>")
api.add_resource(DataCollectionParametersCount, "/datacollectionparameters/count")
api.add_resource(DataCollectionParametersFindOne, "/datacollectionparameters/findOne")
api.add_resource(Datafiles, "/datafiles")
api.add_resource(DatafilesWithID, "/datafiles/<int:id>")
api.add_resource(DatafilesFindOne, "/datafiles/findOne")
api.add_resource(DatafilesCount, "/datafiles/count")
api.add_resource(DatafileFormats, "/datafileformats")
api.add_resource(DatafileFormatsWithID, "/datafileformats/<int:id>")
api.add_resource(DatafileFormatsCount, "/datafileformats/count")
api.add_resource(DatafileFormatsFindOne, "/datafileformats/findOne")
api.add_resource(DatafileParameters, "/datafileparameters")
api.add_resource(DatafileParametersWithID, "/datafileparameters/<int:id>")
api.add_resource(DatafileParametersCount, "/datafileparameters/count")
api.add_resource(DatafileParametersFindOne, "/datafileparameters/findOne")
api.add_resource(Datasets, "/datasets")
api.add_resource(DatasetsWithID, "/datasets/<int:id>")
api.add_resource(DatasetsCount, "/datasets/count")
api.add_resource(DatasetsFindOne, "/datasets/findOne")
api.add_resource(DatasetTypes, "/datasettypes")
api.add_resource(DatasetTypesWithID, "/datasettypes/<int:id>")
api.add_resource(DatasetTypesCount, "/datasettypes/count")
api.add_resource(DatasetTypesFindOne, "/datasettypes/findOne")
api.add_resource(Facilities, "/facilities")
api.add_resource(FacilitiesWithID, "/facilities/<int:id>")
api.add_resource(FacilitiesCount, "/facilities/count")
api.add_resource(FacilitiesFindOne, "/facilities/findOne")
api.add_resource(FacilityCycles, "/facilitycycles")
api.add_resource(FacilityCyclesWithID, "/facilitycycles/<int:id>")
api.add_resource(FacilityCyclesCount, "/facilitycycles/count")
api.add_resource(FacilityCyclesFindOne, "/facilitycycles/findOne")
api.add_resource(Groupings, "/groupings")
api.add_resource(GroupingsWithID, "/groupings/<int:id>")
api.add_resource(GroupingsCount, "/groupings/count")
api.add_resource(GroupingsFindOne, "/groupings/findOne")
api.add_resource(Instruments, "/instruments")
api.add_resource(InstrumentsWithID, "/instruments/<int:id>")
api.add_resource(InstrumentsCount, "/instruments/count")
api.add_resource(InstrumentsFindOne, "/instruments/findOne")
api.add_resource(InstrumentScientists, "/instrumentscientists")
api.add_resource(InstrumentScientistsWithID, "/instrumentscientists/<int:id>")
api.add_resource(InstrumentScientistsCount, "/instrumentscientists/count")
api.add_resource(InstrumentScientistsFindOne, "/instrumentscientists/findOne")
api.add_resource(Investigations, "/investigations")
api.add_resource(InvestigationsWithID, "/investigations/<int:id>")
api.add_resource(InvestigationsCount, "/investigations/count")
api.add_resource(InvestigationsFindOne, "/investigations/findOne")
api.add_resource(InvestigationGroups, "/investigationgroups")
api.add_resource(InvestigationGroupsWithID, "/investigationgroups/<int:id>")
api.add_resource(InvestigationGroupsCount, "/investigationgroups/count")
api.add_resource(InvestigationGroupsFindOne, "/investigationgroups/findOne")
api.add_resource(InvestigationInstruments, "/investigationinstruments")
api.add_resource(InvestigationInstrumentsWithID, "/investigationinstruments/<int:id>")
api.add_resource(InvestigationInstrumentsCount, "/investigationinstruments/count")
api.add_resource(InvestigationInstrumentsFindOne, "/investigationinstruments/findOne")
api.add_resource(InvestigationParameters, "/investigationparameters")
api.add_resource(InvestigationParametersWithID, "/investigationparameters/<int:id>")
api.add_resource(InvestigationParametersCount, "/investigationparameters/count")
api.add_resource(InvestigationParametersFindOne, "/investigationparameters/findOne")
api.add_resource(InvestigationTypes, "/investigationtypes")
api.add_resource(InvestigationTypesWithID, "/investigationtypes/<int:id>")
api.add_resource(InvestigationTypesCount, "/investigationtypes/count")
api.add_resource(InvestigationTypesFindOne, "/investigationtypes/findOne")
api.add_resource(InvestigationUsers, "/investigationusers")
api.add_resource(InvestigationUsersWithID, "/investigationusers/<int:id>")
api.add_resource(InvestigationUsersCount, "/investigationusers/count")
api.add_resource(InvestigationUsersFindOne, "/investigationusers/findOne")
api.add_resource(Jobs, "/jobs")
api.add_resource(JobsWithID, "/jobs/<int:id>")
api.add_resource(JobsCount, "/jobs/count")
api.add_resource(JobsFindOne, "/jobs/findOne")
api.add_resource(Keywords, "/keywords")
api.add_resource(KeywordsWithID, "/keywords/<int:id>")
api.add_resource(KeywordsCount, "/keywords/count")
api.add_resource(KeywordsFindOne, "/keywords/findOne")
api.add_resource(ParameterTypes, "/parametertypes")
api.add_resource(ParameterTypesWithID, "/parametertypes/<int:id>")
api.add_resource(ParameterTypesCount, "/parametertypes/count")
api.add_resource(ParameterTypesFindOne, "/parametertypes/findOne")
api.add_resource(PermissibleStringValues, "/permissiblestringvalues")
api.add_resource(PermissibleStringValuesWithID, "/permissiblestringvalues/<int:id>")
api.add_resource(PermissibleStringValuesCount, "/permissiblestringvalues/count")
api.add_resource(PermissibleStringValuesFindOne, "/permissiblestringvalues/findOne")
api.add_resource(Publications, "/publications")
api.add_resource(PublicationsWithID, "/publications/<int:id>")
api.add_resource(PublicationsCount, "/publications/count")
api.add_resource(PublicationsFindOne, "/publications/findOne")
api.add_resource(PublicSteps, "/publicsteps")
api.add_resource(PublicStepsWithID, "/publicsteps/<int:id>")
api.add_resource(PublicStepsCount, "/publicsteps/count")
api.add_resource(PublicStepsFindOne, "/publicsteps/findOne")
api.add_resource(RelatedDatafiles, "/relateddatafiles")
api.add_resource(RelatedDatafilesWithID, "/relateddatafiles/<int:id>")
api.add_resource(RelatedDatafilesCount, "/relateddatafiles/count")
api.add_resource(RelatedDatafilesFindOne, "/relateddatafiles/findOne")
api.add_resource(Rules, "/rules")
api.add_resource(RulesWithID, "/rules/<int:id>")
api.add_resource(RulesCount, "/rules/count")
api.add_resource(RulesFindOne, "/rules/findOne")
api.add_resource(Samples, "/samples")
api.add_resource(SamplesWithID, "/samples/<int:id>")
api.add_resource(SamplesCount, "/samples/count")
api.add_resource(SamplesFindOne, "/samples/findOne")
api.add_resource(SampleParameters, "/sampleparameters")
api.add_resource(SampleParametersWithID, "/sampleparameters/<int:id>")
api.add_resource(SampleParametersCount, "/sampleparameters/count")
api.add_resource(SampleParametersFindOne, "/sampleparameters/findOne")
api.add_resource(SampleTypes, "/sampletypes")
api.add_resource(SampleTypesWithID, "/sampletypes/<int:id>")
api.add_resource(SampleTypesCount, "/sampletypes/count")
api.add_resource(SampleTypesFindOne, "/sampletypes/findOne")
api.add_resource(Sessions, "/sessions")
api.add_resource(Shifts, "/shifts")
api.add_resource(ShiftsWithID, "/shifts/<int:id>")
api.add_resource(ShiftsCount, "/shifts/count")
api.add_resource(ShiftsFindOne, "/shifts/findOne")
api.add_resource(Studies, "/studies")
api.add_resource(StudiesWithID, "/studies/<int:id>")
api.add_resource(StudiesCount, "/studies/count")
api.add_resource(StudiesFindOne, "/studies/findOne")
api.add_resource(StudyInvestigations, "/studyinvestigations")
api.add_resource(StudyInvestigationsWithID, "/studyinvestigations/<int:id>")
api.add_resource(StudyInvestigationsCount, "/studyinvestigations/count")
api.add_resource(StudyInvestigationsFindOne, "/studyinvestigations/findOne")
api.add_resource(Users, "/users")
api.add_resource(UsersWithID, "/users/<int:id>")
api.add_resource(UsersCount, "/users/count")
api.add_resource(UsersFindOne, "/users/findOne")
api.add_resource(UserGroups, "/usergroups")
api.add_resource(UserGroupsWithID, "/usergroups/<int:id>")
api.add_resource(UserGroupsCount, "/usergroups/count")
api.add_resource(UserGroupsFindOne, "/usergroups/findOne")

# Table specific endpoints
api.add_resource(UsersInvestigations, "/users/<int:id>/investigations")
api.add_resource(UsersInvestigationsCount, "/users/<int:id>/investigations/count")
api.add_resource(InstrumentsFacilityCycles, "/instruments/<int:id>/facilitycycles")
api.add_resource(InstrumentsFacilityCyclesCount, "/instruments/<int:id>/facilitycycles/count")
api.add_resource(InstrumentsFacilityCyclesInvestigations,
                 "/instruments/<int:instrument_id>/facilitycycles/<int:cycle_id>/investigations")
api.add_resource(InstrumentsFacilityCyclesInvestigationsCount,
                 "/instruments/<int:instrument_id>/facilitycycles/<int:cycle_id>/investigations/count")

if __name__ == "__main__":
    app.run(debug=config.is_debug_mode())
