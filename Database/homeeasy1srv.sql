CREATE DATABASE userTestData;

GO
USE userTestData;

CREATE TABLE [dbo].[appAccountTypes] (
    [accountTypeID]   INT           NOT NULL,
    [typeName]        VARCHAR (40)  NOT NULL,
    [typeDescription] VARCHAR (100) NULL,
    CONSTRAINT [PK_appAccountTypes] PRIMARY KEY CLUSTERED ([accountTypeID] ASC)
);

CREATE TABLE [dbo].[appFeeTypes] (
    [feeID]             INT            NOT NULL,
    [feeName]           TEXT           NOT NULL,
    [description]       TEXT           NOT NULL,
    [defaultPrice]      DECIMAL (8, 2) NULL,
    [defaultOccurrence] INT            NULL,
    CONSTRAINT [PK_appFeeTypes] PRIMARY KEY CLUSTERED ([feeID] ASC)
);

CREATE TABLE [dbo].[appOccurrences] (
    [occurrenceID] INT NOT NULL,
    [occurrence]   INT NOT NULL,
    [perPeriod]    INT NULL,
    CONSTRAINT [PK_appOccurrences] PRIMARY KEY CLUSTERED ([occurrenceID] ASC)
);

CREATE TABLE [dbo].[appPaymentMethods] (
    [methodID]   INT          NOT NULL,
    [methodName] VARCHAR (30) NOT NULL,
    CONSTRAINT [PK_appPaymentMethods] PRIMARY KEY CLUSTERED ([methodID] ASC)
);

CREATE TABLE [dbo].[appPaymentStatus] (
    [statusID]    INT          NOT NULL,
    [statusName]  VARCHAR (25) NOT NULL,
    [isCompleted] BIT          CONSTRAINT [DEFAULT_appPaymentStatus_isCompleted] DEFAULT ((0)) NOT NULL,
    CONSTRAINT [PK_appPaymentStatus] PRIMARY KEY CLUSTERED ([statusID] ASC)
);

CREATE TABLE [dbo].[appPeriods] (
    [periodID]     INT          NOT NULL,
    [name]         VARCHAR (20) NOT NULL,
    [abbreviation] VARCHAR (8)  NOT NULL,
    CONSTRAINT [PK_appPeriods] PRIMARY KEY CLUSTERED ([periodID] ASC)
);

CREATE TABLE [dbo].[userAccounts] (
    [userID]                 INT          NOT NULL,
    [accountTypeID]          INT          NOT NULL,
    [emailAddress]           INT          NOT NULL,
    [emailVerified]          BIT          CONSTRAINT [DEFAULT_userAccounts_emailVerified] DEFAULT ((0)) NOT NULL,
    [passHash]               VARCHAR (50) NOT NULL,
    [salt]                   VARCHAR (50) NULL,
    [createDate]             DATE         NOT NULL,
    [attemptsSinceLastLogin] INT          CONSTRAINT [DEFAULT_userAccounts_attemptsSinceLastLogin] DEFAULT ((0)) NOT NULL,
    CONSTRAINT [PK_userAccounts] PRIMARY KEY CLUSTERED ([userID] ASC)
);

CREATE TABLE [dbo].[userAddresses] (
    [addressID]   INT          NOT NULL,
    [houseNumber] INT          NOT NULL,
    [streetName]  VARCHAR (30) NOT NULL,
    [apptNo]      VARCHAR (6)  NULL,
    [city]        VARCHAR (30) NOT NULL,
    [state]       VARCHAR (2)  NOT NULL,
    [zipCode]     NUMERIC (5)  NOT NULL,
    CONSTRAINT [PK_userAddresses] PRIMARY KEY CLUSTERED ([addressID] ASC)
);

CREATE TABLE [dbo].[userApplications] (
    [applicationID]        INT           NOT NULL,
    [leaseID]              INT           NOT NULL,
    [applicantID]          INT           NOT NULL,
    [coApplicantID]        INT           NULL,
    [currentAddressID]     INT           NOT NULL,
    [currentMonthlyRent]   VARCHAR (15)  NOT NULL,
    [currentMoveIn]        DATE          NOT NULL,
    [currentLeaveReason]   VARCHAR (120) NULL,
    [currentOwnerID]       INT           NOT NULL,
    [previousAddressID]    INT           NULL,
    [previousMonthlyRent]  VARCHAR (15)  NULL,
    [previousMoveIn]       DATE          NULL,
    [previousLeaveReason]  VARCHAR (120) NULL,
    [previousOwnerID]      INT           NULL,
    [lastYearLatePayments] BIT           NOT NULL,
    [refusedPayments]      BIT           NOT NULL,
    [everEvicted]          BIT           NOT NULL,
    [additionalInfo]       VARCHAR (200) NULL,
    [bestDayPhoneNo]       VARCHAR (20)  NULL,
    [bestEveningPhoneNo]   VARCHAR (20)  NULL,
    [informationReleaseID] INT           NOT NULL,
    [agree]                BIT           NOT NULL,
    [dateTime]             DATETIME      NOT NULL,
    [ipAddress]            VARCHAR (15)  NOT NULL,
    [applicationStatus]    INT           CONSTRAINT [DEFAULT_userApplications_applicationStatus] DEFAULT ((0)) NOT NULL,
    [landlordComments]     VARCHAR (500) NULL,
    CONSTRAINT [PK_userApplications] PRIMARY KEY CLUSTERED ([applicationID] ASC)
);

CREATE TABLE [dbo].[userCompanies] (
    [companyID]           INT          NOT NULL,
    [companyName]         VARCHAR (50) NOT NULL,
    [phoneNumber]         CHAR (10)    NOT NULL,
    [mailingAddress]      INT          NOT NULL,
    [billingAddress]      INT          NULL,
    [emailInvoiceAddress] VARCHAR (50) NULL,
    [EIN]                 INT          NULL,
    [createdBy]           INT          NOT NULL,
    [createDate]          DATETIME     NOT NULL,
    CONSTRAINT [PK_companies] PRIMARY KEY CLUSTERED ([companyID] ASC)
);

CREATE TABLE [dbo].[userCompanyRoles] (
    [roleID]       INT NOT NULL,
    [companyID]    INT NOT NULL,
    [userID]       INT NOT NULL,
    [roleTypeID]   INT NOT NULL,
    [role_begin]   INT NOT NULL,
    [assignedUser] INT NOT NULL,
    [role_end]     INT NULL,
    [endedUser]    INT NULL,
    CONSTRAINT [PK_userCompanyPeople] PRIMARY KEY CLUSTERED ([roleID] ASC)
);

CREATE TABLE [dbo].[userDependants] (
    [dependantID]            INT          NOT NULL,
    [applicationID]          INT          NULL,
    [leaseID]                INT          NULL,
    [order]                  INT          CONSTRAINT [DEFAULT_userDependants_order] DEFAULT ((1)) NOT NULL,
    [dependantName]          VARCHAR (50) NOT NULL,
    [dependantDOB]           DATE         NOT NULL,
    [applicantsRelationship] VARCHAR (50) NULL,
    CONSTRAINT [PK_userDependants] PRIMARY KEY CLUSTERED ([dependantID] ASC)
);

CREATE TABLE [dbo].[userDetailOptions] (
    [detailID]     INT  NOT NULL,
    [propertyName] TEXT NULL,
    CONSTRAINT [PK_userDetailOptions] PRIMARY KEY CLUSTERED ([detailID] ASC)
);

CREATE TABLE [dbo].[userEmploymentHistory] (
    [employmentID]       INT          NOT NULL,
    [applicationID]      INT          NOT NULL,
    [applicantID]        INT          NULL,
    [employmentStatus]   INT          NOT NULL,
    [employerName]       VARCHAR (50) NOT NULL,
    [employmentBegin]    DATE         NOT NULL,
    [employedAs]         VARCHAR (50) NOT NULL,
    [supervisorID]       INT          NOT NULL,
    [salary]             FLOAT (53)   NOT NULL,
    [salaryPeriod]       INT          NOT NULL,
    [landlordReviewUser] INT          NULL,
    [landlordComment]    INT          NULL,
    CONSTRAINT [PK_userEmploymentHistory] PRIMARY KEY CLUSTERED ([employmentID] ASC)
);

CREATE TABLE [dbo].[userLease] (
    [leaseID]                   INT          NOT NULL,
    [propertyID]                INT          NOT NULL,
    [leaseStatus]               VARCHAR (25) NULL,
    [availableDate]             DATE         NOT NULL,
    [moveInDate]                DATE         NULL,
    [terminationDate]           DATE         NULL,
    [leaseOccurrence]           INT          NOT NULL,
    [leaseSuccessionOccurrence] INT          NULL,
    [securityDeposit]           FLOAT (53)   NOT NULL,
    [contractDocID]             VARCHAR (50) NULL,
    [createUser]                INT          NOT NULL,
    [createDate]                DATETIME     NOT NULL,
    CONSTRAINT [PK_userLease] PRIMARY KEY CLUSTERED ([leaseID] ASC)
);

CREATE TABLE [dbo].[userLeaseFees] (
    [leaseFeeID]       INT          NOT NULL,
    [leaseID]          INT          NOT NULL,
    [feeID]            INT          NOT NULL,
    [feeName]          VARCHAR (30) NOT NULL,
    [feeAmount]        FLOAT (53)   NOT NULL,
    [occurrence]       INT          NOT NULL,
    [startAfterLength] INT          NOT NULL,
    [startAfterPeriod] INT          NOT NULL,
    [createUser]       INT          NOT NULL,
    [createDate]       DATETIME     NOT NULL,
    CONSTRAINT [PK_userLeaseFees] PRIMARY KEY CLUSTERED ([leaseFeeID] ASC)
);

CREATE TABLE [dbo].[userLeasePeople] (
    [leaseID]  INT          NOT NULL,
    [personID] INT          NOT NULL,
    [role]     VARCHAR (50) NOT NULL,
    CONSTRAINT [PK_userLeasePeople] PRIMARY KEY CLUSTERED ([leaseID] ASC, [personID] ASC)
);

CREATE TABLE [dbo].[userPaymentItems] (
    [paymentItemID] INT          NOT NULL,
    [paymentID]     INT          NOT NULL,
    [dueDate]       DATE         NOT NULL,
    [itemName]      VARCHAR (50) NOT NULL,
    [leaseFeeID]    INT          NOT NULL,
    [amountPaid]    FLOAT (53)   NULL,
    [createUser]    INT          NOT NULL,
    [createDate]    DATETIME     NOT NULL,
    CONSTRAINT [PK_userPaymentItems] PRIMARY KEY CLUSTERED ([paymentItemID] ASC)
);

CREATE TABLE [dbo].[userPayments] (
    [paymentID]      INT        NOT NULL,
    [dueDate]        DATE       NOT NULL,
    [paymentStatus]  INT        NULL,
    [paymentMethod]  INT        NULL,
    [amountReceived] FLOAT (53) NULL,
    [dateReceived]   DATE       NOT NULL,
    [createUser]     INT        NOT NULL,
    [createDate]     DATETIME   NOT NULL,
    CONSTRAINT [PK_userPayments] PRIMARY KEY CLUSTERED ([paymentID] ASC)
);

CREATE TABLE [dbo].[userPeople] (
    [personID]    INT          NOT NULL,
    [firstName]   VARCHAR (50) NOT NULL,
    [lastName]    VARCHAR (50) NULL,
    [phoneNumber] CHAR (10)    NOT NULL,
    [addressID]   INT          NULL,
    [createdOn]   DATETIME     NOT NULL,
    CONSTRAINT [PK_userPeople] PRIMARY KEY CLUSTERED ([personID] ASC)
);

CREATE TABLE [dbo].[userPersonDetails] (
    [personID]      INT          NOT NULL,
    [detailID]      INT          NOT NULL,
    [rev]           INT          CONSTRAINT [DEFAULT_userPersonDetails_rev] DEFAULT ((0)) NOT NULL,
    [propertyValue] VARCHAR (50) NULL,
    [setDate]       DATETIME     NOT NULL,
    [setPersonID]   INT          NOT NULL,
    CONSTRAINT [PK_userPersonDetails] PRIMARY KEY CLUSTERED ([personID] ASC, [detailID] ASC, [rev] ASC)
);

CREATE TABLE [dbo].[userProperties] (
    [propertyID]     INT          NOT NULL,
    [companyID]      INT          NOT NULL,
    [addressID]      INT          NOT NULL,
    [bedroomCount]   INT          NOT NULL,
    [bathroomCount]  FLOAT (53)   NOT NULL,
    [parkingCount]   INT          NULL,
    [garageCount]    INT          NULL,
    [storiesCount]   FLOAT (53)   NULL,
    [homeType]       VARCHAR (50) NOT NULL,
    [yearBuilt]      NUMERIC (4)  NULL,
    [purchasePrice]  INT          NULL,
    [purchaseDate]   DATE         NULL,
    [schoolDistrict] VARCHAR (50) NOT NULL,
    [nickname]       VARCHAR (50) NOT NULL,
    [createUser]     INT          NOT NULL,
    [createDate]     DATETIME     NOT NULL,
    CONSTRAINT [PK_userProperties] PRIMARY KEY CLUSTERED ([propertyID] ASC)
);

CREATE TABLE [dbo].[userReferences] (
    [referenceID]      INT           NOT NULL,
    [applicationID]    INT           NOT NULL,
    [sortOrder]        INT           CONSTRAINT [DEFAULT_userReferences_sortOrder] DEFAULT ((1)) NOT NULL,
    [personID]         INT           NOT NULL,
    [relationship]     VARCHAR (20)  NOT NULL,
    [landlordReviewed] BIT           CONSTRAINT [DEFAULT_userReferences_landlordReviewed] DEFAULT ((0)) NOT NULL,
    [landlordComments] VARCHAR (500) NULL,
    CONSTRAINT [PK_userReferences] PRIMARY KEY CLUSTERED ([referenceID] ASC)
);

CREATE TABLE [dbo].[userSessions] (
    [sessionID]       INT      NOT NULL,
    [userID]          INT      NOT NULL,
    [loginDatetime]   DATETIME NOT NULL,
    [expiredDatetime] DATETIME NOT NULL,
    [nextDatetime]    DATETIME NOT NULL,
    CONSTRAINT [PK_userSessions] PRIMARY KEY CLUSTERED ([sessionID] ASC)
);

CREATE TABLE [dbo].[userVehicles] (
    [vehicleID]     INT          NOT NULL,
    [applicationID] INT          NULL,
    [leaseID]       INT          NULL,
    [year]          NUMERIC (4)  NULL,
    [make]          VARCHAR (20) NULL,
    [model]         VARCHAR (20) NULL,
    [color]         VARCHAR (20) NULL,
    [plateNo]       VARCHAR (10) NULL,
    CONSTRAINT [PK_userVehicles] PRIMARY KEY CLUSTERED ([vehicleID] ASC)
);

GO

/* Setup Foreign Keys */

ALTER TABLE [dbo].[appFeeTypes] (
    CONSTRAINT [FK_defaultOccurrence] FOREIGN KEY ([defaultOccurrence]) REFERENCES [dbo].[appOccurrences] ([occurrenceID])
);

ALTER TABLE [dbo].[appOccurrences] (
    CONSTRAINT [FK_perPeriod] FOREIGN KEY ([perPeriod]) REFERENCES [dbo].[appPeriods] ([periodID])
);

ALTER TABLE [dbo].[userAccounts](
    CONSTRAINT [FK_userAccounts_appAccountTypes] FOREIGN KEY ([accountTypeID]) REFERENCES [dbo].[appAccountTypes] ([accountTypeID]),
    CONSTRAINT [FK_userAccounts_userPeople] FOREIGN KEY ([userID]) REFERENCES [dbo].[userPeople] ([personID])
);

ALTER TABLE [dbo].[userApplications] (
    CONSTRAINT [FK_userApplications_userAddresses-currentAddress] FOREIGN KEY ([currentAddressID]) REFERENCES [dbo].[userAddresses] ([addressID]),
    CONSTRAINT [FK_userApplications_userApplications-previousAddress] FOREIGN KEY ([previousAddressID]) REFERENCES [dbo].[userAddresses] ([addressID]),
    CONSTRAINT [FK_userApplications_userLease] FOREIGN KEY ([leaseID]) REFERENCES [dbo].[userLease] ([leaseID]),
    CONSTRAINT [FK_userApplications_userPeople-applicant] FOREIGN KEY ([applicantID]) REFERENCES [dbo].[userPeople] ([personID]),
    CONSTRAINT [FK_userApplications_userPeople-coapplicant] FOREIGN KEY ([coApplicantID]) REFERENCES [dbo].[userPeople] ([personID]),
    CONSTRAINT [FK_userApplications_userPeople-currentOwner] FOREIGN KEY ([currentOwnerID]) REFERENCES [dbo].[userPeople] ([personID]),
    CONSTRAINT [FK_userApplications_userPeople-previousOwner] FOREIGN KEY ([previousOwnerID]) REFERENCES [dbo].[userPeople] ([personID])
);

ALTER TABLE [dbo].[userCompanies] (
    CONSTRAINT [FK_billingAddress] FOREIGN KEY ([billingAddress]) REFERENCES [dbo].[userAddresses] ([addressID]),
    CONSTRAINT [FK_mailingAddress] FOREIGN KEY ([mailingAddress]) REFERENCES [dbo].[userAddresses] ([addressID])
);

ALTER TABLE [dbo].[userCompanyRoles] (
    CONSTRAINT [FK_userCompanyPeople_appAccountTypes] FOREIGN KEY ([roleTypeID]) REFERENCES [dbo].[appAccountTypes] ([accountTypeID]),
    CONSTRAINT [FK_userCompanyPeople_userAccounts] FOREIGN KEY ([userID]) REFERENCES [dbo].[userAccounts] ([userID]),
    CONSTRAINT [FK_userCompanyPeople_userAccounts_linked] FOREIGN KEY ([assignedUser]) REFERENCES [dbo].[userAccounts] ([userID]),
    CONSTRAINT [FK_userCompanyPeople_userAccounts_unlinked] FOREIGN KEY ([endedUser]) REFERENCES [dbo].[userAccounts] ([userID]),
    CONSTRAINT [FK_userCompanyPeople_userCompanies] FOREIGN KEY ([companyID]) REFERENCES [dbo].[userCompanies] ([companyID])
);

ALTER TABLE [dbo].[userDependants] (
    CONSTRAINT [FK_userDependants_userApplications] FOREIGN KEY ([applicationID]) REFERENCES [dbo].[userApplications] ([applicationID]),
    CONSTRAINT [FK_userDependants_userLease] FOREIGN KEY ([leaseID]) REFERENCES [dbo].[userLease] ([leaseID])
);

ALTER TABLE [dbo].[userEmploymentHistory] (
    CONSTRAINT [FK_applicantID] FOREIGN KEY ([applicantID]) REFERENCES [dbo].[userPeople] ([personID]),
    CONSTRAINT [FK_supervisorID] FOREIGN KEY ([supervisorID]) REFERENCES [dbo].[userPeople] ([personID]),
    CONSTRAINT [FK_userEmploymentHistory_appPeriods] FOREIGN KEY ([salaryPeriod]) REFERENCES [dbo].[appPeriods] ([periodID]),
    CONSTRAINT [FK_userEmploymentHistory_userApplications] FOREIGN KEY ([applicationID]) REFERENCES [dbo].[userApplications] ([applicationID])
);

ALTER TABLE [dbo].[userLease] (
    CONSTRAINT [FK_userLease_appOccurrences] FOREIGN KEY ([leaseOccurrence]) REFERENCES [dbo].[appOccurrences] ([occurrenceID]),
    CONSTRAINT [FK_userLease_appOccurrences_leaseSuccession] FOREIGN KEY ([leaseSuccessionOccurrence]) REFERENCES [dbo].[appOccurrences] ([occurrenceID]),
    CONSTRAINT [FK_userLease_userAccounts] FOREIGN KEY ([createUser]) REFERENCES [dbo].[userAccounts] ([userID]),
    CONSTRAINT [FK_userLease_userProperties] FOREIGN KEY ([propertyID]) REFERENCES [dbo].[userProperties] ([propertyID])
);

ALTER TABLE [dbo].[userLeaseFees] (
    CONSTRAINT [FK_userLeaseFees_appFeeTypes] FOREIGN KEY ([feeID]) REFERENCES [dbo].[appFeeTypes] ([feeID]),
    CONSTRAINT [FK_userLeaseFees_appOccurrences] FOREIGN KEY ([occurrence]) REFERENCES [dbo].[appOccurrences] ([occurrenceID]),
    CONSTRAINT [FK_userLeaseFees_appPeriods] FOREIGN KEY ([startAfterPeriod]) REFERENCES [dbo].[appPeriods] ([periodID]),
    CONSTRAINT [FK_userLeaseFees_userAccounts] FOREIGN KEY ([createUser]) REFERENCES [dbo].[userAccounts] ([userID]),
    CONSTRAINT [FK_userLeaseFees_userLease] FOREIGN KEY ([leaseID]) REFERENCES [dbo].[userLease] ([leaseID])
);

ALTER TABLE [dbo].[userLeasePeople] (
    CONSTRAINT [FK_userLeasePeople_userLease] FOREIGN KEY ([leaseID]) REFERENCES [dbo].[userLease] ([leaseID]),
    CONSTRAINT [FK_userLeasePeople_userPeople] FOREIGN KEY ([personID]) REFERENCES [dbo].[userPeople] ([personID])
);

ALTER TABLE [dbo].[userPaymentItems] (
    CONSTRAINT [FK_userPaymentItems_userAccounts] FOREIGN KEY ([createUser]) REFERENCES [dbo].[userAccounts] ([userID]),
    CONSTRAINT [FK_userPaymentItems_userLeaseFees] FOREIGN KEY ([leaseFeeID]) REFERENCES [dbo].[userLeaseFees] ([leaseFeeID]),
    CONSTRAINT [FK_userPaymentItems_userPayments] FOREIGN KEY ([paymentID]) REFERENCES [dbo].[userPayments] ([paymentID])
);

ALTER TABLE [dbo].[userPayments] (
    CONSTRAINT [FK_userPayments_appPaymentMethods] FOREIGN KEY ([paymentMethod]) REFERENCES [dbo].[appPaymentMethods] ([methodID]),
    CONSTRAINT [FK_userPayments_appPaymentStatus] FOREIGN KEY ([paymentStatus]) REFERENCES [dbo].[appPaymentStatus] ([statusID]),
    CONSTRAINT [FK_userPayments_userAccounts] FOREIGN KEY ([createUser]) REFERENCES [dbo].[userAccounts] ([userID])
);

ALTER TABLE [dbo].[userPeople] (
    CONSTRAINT [FK_addressID] FOREIGN KEY ([addressID]) REFERENCES [dbo].[userAddresses] ([addressID])
);

ALTER TABLE [dbo].[userPersonDetails] (
    CONSTRAINT [FK_detailID] FOREIGN KEY ([detailID]) REFERENCES [dbo].[userDetailOptions] ([detailID]),
    CONSTRAINT [FK_personID] FOREIGN KEY ([personID]) REFERENCES [dbo].[userPeople] ([personID]),
    CONSTRAINT [FK_setPersonID] FOREIGN KEY ([setPersonID]) REFERENCES [dbo].[userPeople] ([personID])
);

ALTER TABLE [dbo].[userProperties] (
    CONSTRAINT [FK_userProperties_userAccounts] FOREIGN KEY ([createUser]) REFERENCES [dbo].[userAccounts] ([userID]),
    CONSTRAINT [FK_userProperties_userAddresses] FOREIGN KEY ([addressID]) REFERENCES [dbo].[userAddresses] ([addressID]),
    CONSTRAINT [FK_userProperties_userCompanies] FOREIGN KEY ([companyID]) REFERENCES [dbo].[userCompanies] ([companyID])
);

ALTER TABLE [dbo].[userReferences] (
    CONSTRAINT [FK_references_applicationID] FOREIGN KEY ([applicationID]) REFERENCES [dbo].[userApplications] ([applicationID]),
    CONSTRAINT [FK_references_personID] FOREIGN KEY ([personID]) REFERENCES [dbo].[userPeople] ([personID])
);

ALTER TABLE [dbo].[userSessions] (
    CONSTRAINT [FK_userSessions_userAccounts] FOREIGN KEY ([userID]) REFERENCES [dbo].[userAccounts] ([userID])
);

ALTER TABLE [dbo].[userVehicles] (
    CONSTRAINT [FK_applicationID] FOREIGN KEY ([applicationID]) REFERENCES [dbo].[userApplications] ([applicationID])
);