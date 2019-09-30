create table if not exists DATACOLLECTION
(
    ID          bigint auto_increment
        primary key,
    CREATE_ID   varchar(255) not null,
    CREATE_TIME datetime     not null,
    DOI         varchar(255) null,
    MOD_ID      varchar(255) not null,
    MOD_TIME    datetime     not null
);

create table if not exists FACILITY
(
    ID               bigint auto_increment
        primary key,
    CREATE_ID        varchar(255)  not null,
    CREATE_TIME      datetime      not null,
    DAYSUNTILRELEASE int           null,
    DESCRIPTION      varchar(1023) null,
    FULLNAME         varchar(255)  null,
    MOD_ID           varchar(255)  not null,
    MOD_TIME         datetime      not null,
    NAME             varchar(255)  not null,
    URL              varchar(255)  null,
    constraint UNQ_FACILITY_0
        unique (NAME)
);

create table if not exists APPLICATION
(
    ID          bigint auto_increment
        primary key,
    CREATE_ID   varchar(255) not null,
    CREATE_TIME datetime     not null,
    MOD_ID      varchar(255) not null,
    MOD_TIME    datetime     not null,
    NAME        varchar(255) not null,
    VERSION     varchar(255) not null,
    FACILITY_ID bigint       not null,
    constraint UNQ_APPLICATION_0
        unique (FACILITY_ID, NAME, VERSION),
    constraint FK_APPLICATION_FACILITY_ID
        foreign key (FACILITY_ID) references FACILITY (ID)
);

create table if not exists DATAFILEFORMAT
(
    ID          bigint auto_increment
        primary key,
    CREATE_ID   varchar(255) not null,
    CREATE_TIME datetime     not null,
    DESCRIPTION varchar(255) null,
    MOD_ID      varchar(255) not null,
    MOD_TIME    datetime     not null,
    NAME        varchar(255) not null,
    TYPE        varchar(255) null,
    VERSION     varchar(255) not null,
    FACILITY_ID bigint       not null,
    constraint UNQ_DATAFILEFORMAT_0
        unique (FACILITY_ID, NAME, VERSION),
    constraint FK_DATAFILEFORMAT_FACILITY_ID
        foreign key (FACILITY_ID) references FACILITY (ID)
);

create table if not exists DATASETTYPE
(
    ID          bigint auto_increment
        primary key,
    CREATE_ID   varchar(255) not null,
    CREATE_TIME datetime     not null,
    DESCRIPTION varchar(255) null,
    MOD_ID      varchar(255) not null,
    MOD_TIME    datetime     not null,
    NAME        varchar(255) not null,
    FACILITY_ID bigint       not null,
    constraint UNQ_DATASETTYPE_0
        unique (FACILITY_ID, NAME),
    constraint FK_DATASETTYPE_FACILITY_ID
        foreign key (FACILITY_ID) references FACILITY (ID)
);

create table if not exists FACILITYCYCLE
(
    ID          bigint auto_increment
        primary key,
    CREATE_ID   varchar(255) not null,
    CREATE_TIME datetime     not null,
    DESCRIPTION varchar(255) null,
    ENDDATE     datetime     null,
    MOD_ID      varchar(255) not null,
    MOD_TIME    datetime     not null,
    NAME        varchar(255) not null,
    STARTDATE   datetime     null,
    FACILITY_ID bigint       not null,
    constraint UNQ_FACILITYCYCLE_0
        unique (FACILITY_ID, NAME),
    constraint FK_FACILITYCYCLE_FACILITY_ID
        foreign key (FACILITY_ID) references FACILITY (ID)
);

create table if not exists `GROUPING`
(
    ID          bigint auto_increment
        primary key,
    CREATE_ID   varchar(255) not null,
    CREATE_TIME datetime     not null,
    MOD_ID      varchar(255) not null,
    MOD_TIME    datetime     not null,
    NAME        varchar(255) not null,
    constraint UNQ_GROUPING_0
        unique (NAME)
);

create table if not exists INSTRUMENT
(
    ID          bigint auto_increment
        primary key,
    CREATE_ID   varchar(255)  not null,
    CREATE_TIME datetime      not null,
    DESCRIPTION varchar(4000) null,
    FULLNAME    varchar(255)  null,
    MOD_ID      varchar(255)  not null,
    MOD_TIME    datetime      not null,
    NAME        varchar(255)  not null,
    TYPE        varchar(255)  null,
    URL         varchar(255)  null,
    FACILITY_ID bigint        not null,
    constraint UNQ_INSTRUMENT_0
        unique (FACILITY_ID, NAME),
    constraint FK_INSTRUMENT_FACILITY_ID
        foreign key (FACILITY_ID) references FACILITY (ID)
);

create table if not exists INVESTIGATIONTYPE
(
    ID          bigint auto_increment
        primary key,
    CREATE_ID   varchar(255) not null,
    CREATE_TIME datetime     not null,
    DESCRIPTION varchar(255) null,
    MOD_ID      varchar(255) not null,
    MOD_TIME    datetime     not null,
    NAME        varchar(255) not null,
    FACILITY_ID bigint       not null,
    constraint UNQ_INVESTIGATIONTYPE_0
        unique (NAME, FACILITY_ID),
    constraint FK_INVESTIGATIONTYPE_FACILITY_ID
        foreign key (FACILITY_ID) references FACILITY (ID)
);

create table if not exists INVESTIGATION
(
    ID          bigint auto_increment
        primary key,
    CREATE_ID   varchar(255)  not null,
    CREATE_TIME datetime      not null,
    DOI         varchar(255)  null,
    ENDDATE     datetime      null,
    MOD_ID      varchar(255)  not null,
    MOD_TIME    datetime      not null,
    NAME        varchar(255)  not null,
    RELEASEDATE datetime      null,
    STARTDATE   datetime      null,
    SUMMARY     varchar(4000) null,
    TITLE       varchar(255)  not null,
    VISIT_ID    varchar(255)  not null,
    FACILITY_ID bigint        not null,
    TYPE_ID     bigint        not null,
    constraint UNQ_INVESTIGATION_0
        unique (FACILITY_ID, NAME, VISIT_ID),
    constraint FK_INVESTIGATION_FACILITY_ID
        foreign key (FACILITY_ID) references FACILITY (ID),
    constraint FK_INVESTIGATION_TYPE_ID
        foreign key (TYPE_ID) references INVESTIGATIONTYPE (ID)
);

create table if not exists INVESTIGATIONGROUP
(
    ID               bigint auto_increment
        primary key,
    CREATE_ID        varchar(255) not null,
    CREATE_TIME      datetime     not null,
    MOD_ID           varchar(255) not null,
    MOD_TIME         datetime     not null,
    ROLE             varchar(255) not null,
    GROUP_ID         bigint       not null,
    INVESTIGATION_ID bigint       not null,
    constraint UNQ_INVESTIGATIONGROUP_0
        unique (GROUP_ID, INVESTIGATION_ID, ROLE),
    constraint FK_INVESTIGATIONGROUP_GROUP_ID
        foreign key (GROUP_ID) references `GROUPING` (ID),
    constraint FK_INVESTIGATIONGROUP_INVESTIGATION_ID
        foreign key (INVESTIGATION_ID) references INVESTIGATION (ID)
);

create table if not exists INVESTIGATIONINSTRUMENT
(
    ID               bigint auto_increment
        primary key,
    CREATE_ID        varchar(255) not null,
    CREATE_TIME      datetime     not null,
    MOD_ID           varchar(255) not null,
    MOD_TIME         datetime     not null,
    INSTRUMENT_ID    bigint       not null,
    INVESTIGATION_ID bigint       not null,
    constraint UNQ_INVESTIGATIONINSTRUMENT_0
        unique (INVESTIGATION_ID, INSTRUMENT_ID),
    constraint FK_INVESTIGATIONINSTRUMENT_INSTRUMENT_ID
        foreign key (INSTRUMENT_ID) references INSTRUMENT (ID),
    constraint FK_INVESTIGATIONINSTRUMENT_INVESTIGATION_ID
        foreign key (INVESTIGATION_ID) references INVESTIGATION (ID)
);

create table if not exists JOB
(
    ID                      bigint auto_increment
        primary key,
    ARGUMENTS               varchar(255) null,
    CREATE_ID               varchar(255) not null,
    CREATE_TIME             datetime     not null,
    MOD_ID                  varchar(255) not null,
    MOD_TIME                datetime     not null,
    APPLICATION_ID          bigint       not null,
    INPUTDATACOLLECTION_ID  bigint       null,
    OUTPUTDATACOLLECTION_ID bigint       null,
    constraint FK_JOB_APPLICATION_ID
        foreign key (APPLICATION_ID) references APPLICATION (ID),
    constraint FK_JOB_INPUTDATACOLLECTION_ID
        foreign key (INPUTDATACOLLECTION_ID) references DATACOLLECTION (ID),
    constraint FK_JOB_OUTPUTDATACOLLECTION_ID
        foreign key (OUTPUTDATACOLLECTION_ID) references DATACOLLECTION (ID)
);

create table if not exists KEYWORD
(
    ID               bigint auto_increment
        primary key,
    CREATE_ID        varchar(255) not null,
    CREATE_TIME      datetime     not null,
    MOD_ID           varchar(255) not null,
    MOD_TIME         datetime     not null,
    NAME             varchar(255) not null,
    INVESTIGATION_ID bigint       not null,
    constraint UNQ_KEYWORD_0
        unique (NAME, INVESTIGATION_ID),
    constraint FK_KEYWORD_INVESTIGATION_ID
        foreign key (INVESTIGATION_ID) references INVESTIGATION (ID)
);

create table if not exists PARAMETERTYPE
(
    ID                         bigint auto_increment
        primary key,
    APPLICABLETODATACOLLECTION tinyint(1) default 0 null,
    APPLICABLETODATAFILE       tinyint(1) default 0 null,
    APPLICABLETODATASET        tinyint(1) default 0 null,
    APPLICABLETOINVESTIGATION  tinyint(1) default 0 null,
    APPLICABLETOSAMPLE         tinyint(1) default 0 null,
    CREATE_ID                  varchar(255)         not null,
    CREATE_TIME                datetime             not null,
    DESCRIPTION                varchar(255)         null,
    ENFORCED                   tinyint(1) default 0 null,
    MAXIMUMNUMERICVALUE        double               null,
    MINIMUMNUMERICVALUE        double               null,
    MOD_ID                     varchar(255)         not null,
    MOD_TIME                   datetime             not null,
    NAME                       varchar(255)         not null,
    UNITS                      varchar(255)         not null,
    UNITSFULLNAME              varchar(255)         null,
    VALUETYPE                  int                  not null,
    VERIFIED                   tinyint(1) default 0 null,
    FACILITY_ID                bigint               not null,
    constraint UNQ_PARAMETERTYPE_0
        unique (FACILITY_ID, NAME, UNITS),
    constraint FK_PARAMETERTYPE_FACILITY_ID
        foreign key (FACILITY_ID) references FACILITY (ID)
);

create table if not exists DATACOLLECTIONPARAMETER
(
    ID                bigint auto_increment
        primary key,
    CREATE_ID         varchar(255)  not null,
    CREATE_TIME       datetime      not null,
    DATETIME_VALUE    datetime      null,
    ERROR             double        null,
    MOD_ID            varchar(255)  not null,
    MOD_TIME          datetime      not null,
    NUMERIC_VALUE     double        null,
    RANGEBOTTOM       double        null,
    RANGETOP          double        null,
    STRING_VALUE      varchar(4000) null,
    DATACOLLECTION_ID bigint        not null,
    PARAMETER_TYPE_ID bigint        not null,
    constraint UNQ_DATACOLLECTIONPARAMETER_0
        unique (DATACOLLECTION_ID, PARAMETER_TYPE_ID),
    constraint FK_DATACOLLECTIONPARAMETER_DATACOLLECTION_ID
        foreign key (DATACOLLECTION_ID) references DATACOLLECTION (ID),
    constraint FK_DATACOLLECTIONPARAMETER_PARAMETER_TYPE_ID
        foreign key (PARAMETER_TYPE_ID) references PARAMETERTYPE (ID)
);

create table if not exists INVESTIGATIONPARAMETER
(
    ID                bigint auto_increment
        primary key,
    CREATE_ID         varchar(255)  not null,
    CREATE_TIME       datetime      not null,
    DATETIME_VALUE    datetime      null,
    ERROR             double        null,
    MOD_ID            varchar(255)  not null,
    MOD_TIME          datetime      not null,
    NUMERIC_VALUE     double        null,
    RANGEBOTTOM       double        null,
    RANGETOP          double        null,
    STRING_VALUE      varchar(4000) null,
    INVESTIGATION_ID  bigint        not null,
    PARAMETER_TYPE_ID bigint        not null,
    constraint UNQ_INVESTIGATIONPARAMETER_0
        unique (INVESTIGATION_ID, PARAMETER_TYPE_ID),
    constraint FK_INVESTIGATIONPARAMETER_INVESTIGATION_ID
        foreign key (INVESTIGATION_ID) references INVESTIGATION (ID),
    constraint FK_INVESTIGATIONPARAMETER_PARAMETER_TYPE_ID
        foreign key (PARAMETER_TYPE_ID) references PARAMETERTYPE (ID)
);

create table if not exists PERMISSIBLESTRINGVALUE
(
    ID               bigint auto_increment
        primary key,
    CREATE_ID        varchar(255) not null,
    CREATE_TIME      datetime     not null,
    MOD_ID           varchar(255) not null,
    MOD_TIME         datetime     not null,
    VALUE            varchar(255) not null,
    PARAMETERTYPE_ID bigint       not null,
    constraint UNQ_PERMISSIBLESTRINGVALUE_0
        unique (VALUE, PARAMETERTYPE_ID),
    constraint FK_PERMISSIBLESTRINGVALUE_PARAMETERTYPE_ID
        foreign key (PARAMETERTYPE_ID) references PARAMETERTYPE (ID)
);

create table if not exists PUBLICATION
(
    ID               bigint auto_increment
        primary key,
    CREATE_ID        varchar(255) not null,
    CREATE_TIME      datetime     not null,
    DOI              varchar(255) null,
    FULLREFERENCE    varchar(511) not null,
    MOD_ID           varchar(255) not null,
    MOD_TIME         datetime     not null,
    REPOSITORY       varchar(255) null,
    REPOSITORYID     varchar(255) null,
    URL              varchar(255) null,
    INVESTIGATION_ID bigint       not null,
    constraint FK_PUBLICATION_INVESTIGATION_ID
        foreign key (INVESTIGATION_ID) references INVESTIGATION (ID)
);

create table if not exists PUBLICSTEP
(
    ID          bigint auto_increment
        primary key,
    CREATE_ID   varchar(255) not null,
    CREATE_TIME datetime     not null,
    FIELD       varchar(32)  not null,
    MOD_ID      varchar(255) not null,
    MOD_TIME    datetime     not null,
    ORIGIN      varchar(32)  not null,
    constraint UNQ_PUBLICSTEP_0
        unique (ORIGIN, FIELD)
);

create table if not exists RULE_
(
    ID          bigint auto_increment
        primary key,
    ATTRIBUTE   varchar(255)         null,
    BEAN        varchar(255)         null,
    C           tinyint(1) default 0 null,
    CREATE_ID   varchar(255)         not null,
    CREATE_TIME datetime             not null,
    CRUDFLAGS   varchar(4)           not null,
    CRUDJPQL    varchar(1024)        null,
    D           tinyint(1) default 0 null,
    INCLUDEJPQL varchar(1024)        null,
    MOD_ID      varchar(255)         not null,
    MOD_TIME    datetime             not null,
    R           tinyint(1) default 0 null,
    RESTRICTED  tinyint(1) default 0 null,
    SEARCHJPQL  varchar(1024)        null,
    U           tinyint(1) default 0 null,
    WHAT        varchar(1024)        not null,
    GROUPING_ID bigint               null,
    constraint FK_RULE__GROUPING_ID
        foreign key (GROUPING_ID) references `GROUPING` (ID)
);

create table if not exists SAMPLETYPE
(
    ID                bigint auto_increment
        primary key,
    CREATE_ID         varchar(255)  not null,
    CREATE_TIME       datetime      not null,
    MOD_ID            varchar(255)  not null,
    MOD_TIME          datetime      not null,
    MOLECULARFORMULA  varchar(255)  not null,
    NAME              varchar(255)  not null,
    SAFETYINFORMATION varchar(4000) null,
    FACILITY_ID       bigint        not null,
    constraint UNQ_SAMPLETYPE_0
        unique (FACILITY_ID, NAME, MOLECULARFORMULA),
    constraint FK_SAMPLETYPE_FACILITY_ID
        foreign key (FACILITY_ID) references FACILITY (ID)
);

create table if not exists SAMPLE
(
    ID               bigint auto_increment
        primary key,
    CREATE_ID        varchar(255) not null,
    CREATE_TIME      datetime     not null,
    MOD_ID           varchar(255) not null,
    MOD_TIME         datetime     not null,
    NAME             varchar(255) not null,
    INVESTIGATION_ID bigint       not null,
    SAMPLETYPE_ID    bigint       null,
    constraint UNQ_SAMPLE_0
        unique (INVESTIGATION_ID, NAME),
    constraint FK_SAMPLE_INVESTIGATION_ID
        foreign key (INVESTIGATION_ID) references INVESTIGATION (ID),
    constraint FK_SAMPLE_SAMPLETYPE_ID
        foreign key (SAMPLETYPE_ID) references SAMPLETYPE (ID)
);

create table if not exists DATASET
(
    ID               bigint auto_increment
        primary key,
    COMPLETE         tinyint(1) default 0 not null,
    CREATE_ID        varchar(255)         not null,
    CREATE_TIME      datetime             not null,
    DESCRIPTION      varchar(255)         null,
    DOI              varchar(255)         null,
    END_DATE         datetime             null,
    LOCATION         varchar(255)         null,
    MOD_ID           varchar(255)         not null,
    MOD_TIME         datetime             not null,
    NAME             varchar(255)         not null,
    STARTDATE        datetime             null,
    INVESTIGATION_ID bigint               not null,
    SAMPLE_ID        bigint               null,
    TYPE_ID          bigint               not null,
    constraint UNQ_DATASET_0
        unique (INVESTIGATION_ID, NAME),
    constraint FK_DATASET_INVESTIGATION_ID
        foreign key (INVESTIGATION_ID) references INVESTIGATION (ID),
    constraint FK_DATASET_SAMPLE_ID
        foreign key (SAMPLE_ID) references SAMPLE (ID),
    constraint FK_DATASET_TYPE_ID
        foreign key (TYPE_ID) references DATASETTYPE (ID)
);

create table if not exists DATACOLLECTIONDATASET
(
    ID                bigint auto_increment
        primary key,
    CREATE_ID         varchar(255) not null,
    CREATE_TIME       datetime     not null,
    MOD_ID            varchar(255) not null,
    MOD_TIME          datetime     not null,
    DATACOLLECTION_ID bigint       not null,
    DATASET_ID        bigint       not null,
    constraint UNQ_DATACOLLECTIONDATASET_0
        unique (DATACOLLECTION_ID, DATASET_ID),
    constraint FK_DATACOLLECTIONDATASET_DATACOLLECTION_ID
        foreign key (DATACOLLECTION_ID) references DATACOLLECTION (ID),
    constraint FK_DATACOLLECTIONDATASET_DATASET_ID
        foreign key (DATASET_ID) references DATASET (ID)
);

create table if not exists DATAFILE
(
    ID                 bigint auto_increment
        primary key,
    CHECKSUM           varchar(255) null,
    CREATE_ID          varchar(255) not null,
    CREATE_TIME        datetime     not null,
    DATAFILECREATETIME datetime     null,
    DATAFILEMODTIME    datetime     null,
    DESCRIPTION        varchar(255) null,
    DOI                varchar(255) null,
    FILESIZE           bigint       null,
    LOCATION           varchar(255) null,
    MOD_ID             varchar(255) not null,
    MOD_TIME           datetime     not null,
    NAME               varchar(255) not null,
    DATAFILEFORMAT_ID  bigint       null,
    DATASET_ID         bigint       not null,
    constraint UNQ_DATAFILE_0
        unique (DATASET_ID, NAME),
    constraint FK_DATAFILE_DATAFILEFORMAT_ID
        foreign key (DATAFILEFORMAT_ID) references DATAFILEFORMAT (ID),
    constraint FK_DATAFILE_DATASET_ID
        foreign key (DATASET_ID) references DATASET (ID)
);

create table if not exists DATACOLLECTIONDATAFILE
(
    ID                bigint auto_increment
        primary key,
    CREATE_ID         varchar(255) not null,
    CREATE_TIME       datetime     not null,
    MOD_ID            varchar(255) not null,
    MOD_TIME          datetime     not null,
    DATACOLLECTION_ID bigint       not null,
    DATAFILE_ID       bigint       not null,
    constraint UNQ_DATACOLLECTIONDATAFILE_0
        unique (DATACOLLECTION_ID, DATAFILE_ID),
    constraint FK_DATACOLLECTIONDATAFILE_DATACOLLECTION_ID
        foreign key (DATACOLLECTION_ID) references DATACOLLECTION (ID),
    constraint FK_DATACOLLECTIONDATAFILE_DATAFILE_ID
        foreign key (DATAFILE_ID) references DATAFILE (ID)
);

create table if not exists DATAFILEPARAMETER
(
    ID                bigint auto_increment
        primary key,
    CREATE_ID         varchar(255)  not null,
    CREATE_TIME       datetime      not null,
    DATETIME_VALUE    datetime      null,
    ERROR             double        null,
    MOD_ID            varchar(255)  not null,
    MOD_TIME          datetime      not null,
    NUMERIC_VALUE     double        null,
    RANGEBOTTOM       double        null,
    RANGETOP          double        null,
    STRING_VALUE      varchar(4000) null,
    DATAFILE_ID       bigint        not null,
    PARAMETER_TYPE_ID bigint        not null,
    constraint UNQ_DATAFILEPARAMETER_0
        unique (DATAFILE_ID, PARAMETER_TYPE_ID),
    constraint FK_DATAFILEPARAMETER_DATAFILE_ID
        foreign key (DATAFILE_ID) references DATAFILE (ID),
    constraint FK_DATAFILEPARAMETER_PARAMETER_TYPE_ID
        foreign key (PARAMETER_TYPE_ID) references PARAMETERTYPE (ID)
);

create table if not exists DATASETPARAMETER
(
    ID                bigint auto_increment
        primary key,
    CREATE_ID         varchar(255)  not null,
    CREATE_TIME       datetime      not null,
    DATETIME_VALUE    datetime      null,
    ERROR             double        null,
    MOD_ID            varchar(255)  not null,
    MOD_TIME          datetime      not null,
    NUMERIC_VALUE     double        null,
    RANGEBOTTOM       double        null,
    RANGETOP          double        null,
    STRING_VALUE      varchar(4000) null,
    DATASET_ID        bigint        not null,
    PARAMETER_TYPE_ID bigint        not null,
    constraint UNQ_DATASETPARAMETER_0
        unique (DATASET_ID, PARAMETER_TYPE_ID),
    constraint FK_DATASETPARAMETER_DATASET_ID
        foreign key (DATASET_ID) references DATASET (ID),
    constraint FK_DATASETPARAMETER_PARAMETER_TYPE_ID
        foreign key (PARAMETER_TYPE_ID) references PARAMETERTYPE (ID)
);

create table if not exists RELATEDDATAFILE
(
    ID                 bigint auto_increment
        primary key,
    CREATE_ID          varchar(255) not null,
    CREATE_TIME        datetime     not null,
    MOD_ID             varchar(255) not null,
    MOD_TIME           datetime     not null,
    RELATION           varchar(255) not null,
    DEST_DATAFILE_ID   bigint       not null,
    SOURCE_DATAFILE_ID bigint       not null,
    constraint UNQ_RELATEDDATAFILE_0
        unique (SOURCE_DATAFILE_ID, DEST_DATAFILE_ID),
    constraint FK_RELATEDDATAFILE_DEST_DATAFILE_ID
        foreign key (DEST_DATAFILE_ID) references DATAFILE (ID),
    constraint FK_RELATEDDATAFILE_SOURCE_DATAFILE_ID
        foreign key (SOURCE_DATAFILE_ID) references DATAFILE (ID)
);

create table if not exists SAMPLEPARAMETER
(
    ID                bigint auto_increment
        primary key,
    CREATE_ID         varchar(255)  not null,
    CREATE_TIME       datetime      not null,
    DATETIME_VALUE    datetime      null,
    ERROR             double        null,
    MOD_ID            varchar(255)  not null,
    MOD_TIME          datetime      not null,
    NUMERIC_VALUE     double        null,
    RANGEBOTTOM       double        null,
    RANGETOP          double        null,
    STRING_VALUE      varchar(4000) null,
    SAMPLE_ID         bigint        not null,
    PARAMETER_TYPE_ID bigint        not null,
    constraint UNQ_SAMPLEPARAMETER_0
        unique (SAMPLE_ID, PARAMETER_TYPE_ID),
    constraint FK_SAMPLEPARAMETER_PARAMETER_TYPE_ID
        foreign key (PARAMETER_TYPE_ID) references PARAMETERTYPE (ID),
    constraint FK_SAMPLEPARAMETER_SAMPLE_ID
        foreign key (SAMPLE_ID) references SAMPLE (ID)
);

create table if not exists SESSION_
(
    ID             varchar(255) not null
        primary key,
    EXPIREDATETIME datetime     null,
    USERNAME       varchar(255) null
);

create table if not exists SHIFT
(
    ID               bigint auto_increment
        primary key,
    COMMENT          varchar(255) null,
    CREATE_ID        varchar(255) not null,
    CREATE_TIME      datetime     not null,
    ENDDATE          datetime     not null,
    MOD_ID           varchar(255) not null,
    MOD_TIME         datetime     not null,
    STARTDATE        datetime     not null,
    INVESTIGATION_ID bigint       not null,
    constraint UNQ_SHIFT_0
        unique (INVESTIGATION_ID, STARTDATE, ENDDATE),
    constraint FK_SHIFT_INVESTIGATION_ID
        foreign key (INVESTIGATION_ID) references INVESTIGATION (ID)
);

create table if not exists USER_
(
    ID          bigint auto_increment
        primary key,
    CREATE_ID   varchar(255) not null,
    CREATE_TIME datetime     not null,
    EMAIL       varchar(255) null,
    FULLNAME    varchar(255) null,
    MOD_ID      varchar(255) not null,
    MOD_TIME    datetime     not null,
    NAME        varchar(255) not null,
    ORCIDID     varchar(255) null,
    constraint UNQ_USER__0
        unique (NAME)
);

create table if not exists INSTRUMENTSCIENTIST
(
    ID            bigint auto_increment
        primary key,
    CREATE_ID     varchar(255) not null,
    CREATE_TIME   datetime     not null,
    MOD_ID        varchar(255) not null,
    MOD_TIME      datetime     not null,
    INSTRUMENT_ID bigint       not null,
    USER_ID       bigint       not null,
    constraint UNQ_INSTRUMENTSCIENTIST_0
        unique (USER_ID, INSTRUMENT_ID),
    constraint FK_INSTRUMENTSCIENTIST_INSTRUMENT_ID
        foreign key (INSTRUMENT_ID) references INSTRUMENT (ID),
    constraint FK_INSTRUMENTSCIENTIST_USER_ID
        foreign key (USER_ID) references USER_ (ID)
);

create table if not exists INVESTIGATIONUSER
(
    ID               bigint auto_increment
        primary key,
    CREATE_ID        varchar(255) not null,
    CREATE_TIME      datetime     not null,
    MOD_ID           varchar(255) not null,
    MOD_TIME         datetime     not null,
    ROLE             varchar(255) not null,
    INVESTIGATION_ID bigint       not null,
    USER_ID          bigint       not null,
    constraint UNQ_INVESTIGATIONUSER_0
        unique (USER_ID, INVESTIGATION_ID, ROLE),
    constraint FK_INVESTIGATIONUSER_INVESTIGATION_ID
        foreign key (INVESTIGATION_ID) references INVESTIGATION (ID),
    constraint FK_INVESTIGATIONUSER_USER_ID
        foreign key (USER_ID) references USER_ (ID)
);

create table if not exists STUDY
(
    ID          bigint auto_increment
        primary key,
    CREATE_ID   varchar(255)  not null,
    CREATE_TIME datetime      not null,
    DESCRIPTION varchar(4000) null,
    MOD_ID      varchar(255)  not null,
    MOD_TIME    datetime      not null,
    NAME        varchar(255)  not null,
    STARTDATE   datetime      null,
    STATUS      int           null,
    USER_ID     bigint        null,
    constraint FK_STUDY_USER_ID
        foreign key (USER_ID) references USER_ (ID)
);

create table if not exists STUDYINVESTIGATION
(
    ID               bigint auto_increment
        primary key,
    CREATE_ID        varchar(255) not null,
    CREATE_TIME      datetime     not null,
    MOD_ID           varchar(255) not null,
    MOD_TIME         datetime     not null,
    INVESTIGATION_ID bigint       not null,
    STUDY_ID         bigint       not null,
    constraint UNQ_STUDYINVESTIGATION_0
        unique (STUDY_ID, INVESTIGATION_ID),
    constraint FK_STUDYINVESTIGATION_INVESTIGATION_ID
        foreign key (INVESTIGATION_ID) references INVESTIGATION (ID),
    constraint FK_STUDYINVESTIGATION_STUDY_ID
        foreign key (STUDY_ID) references STUDY (ID)
);

create table if not exists USERGROUP
(
    ID          bigint auto_increment
        primary key,
    CREATE_ID   varchar(255) not null,
    CREATE_TIME datetime     not null,
    MOD_ID      varchar(255) not null,
    MOD_TIME    datetime     not null,
    GROUP_ID    bigint       not null,
    USER_ID     bigint       not null,
    constraint UNQ_USERGROUP_0
        unique (USER_ID, GROUP_ID),
    constraint FK_USERGROUP_GROUP_ID
        foreign key (GROUP_ID) references `GROUPING` (ID),
    constraint FK_USERGROUP_USER_ID
        foreign key (USER_ID) references USER_ (ID)
);

