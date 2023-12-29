USE [master]
GO
/****** Object:  Database [userData]    Script Date: 12/28/23 11:39:49 PM ******/
CREATE DATABASE [userData]
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [userData].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [userData] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [userData] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [userData] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [userData] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [userData] SET ARITHABORT OFF 
GO
ALTER DATABASE [userData] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [userData] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [userData] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [userData] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [userData] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [userData] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [userData] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [userData] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [userData] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [userData] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [userData] SET ALLOW_SNAPSHOT_ISOLATION ON 
GO
ALTER DATABASE [userData] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [userData] SET READ_COMMITTED_SNAPSHOT ON 
GO
ALTER DATABASE [userData] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [userData] SET  MULTI_USER 
GO
ALTER DATABASE [userData] SET DB_CHAINING OFF 
GO
ALTER DATABASE [userData] SET ENCRYPTION ON
GO
ALTER DATABASE [userData] SET QUERY_STORE = ON
GO
ALTER DATABASE [userData] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 100, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO)
GO
USE [userData]
GO
ALTER DATABASE SCOPED CONFIGURATION SET ACCELERATED_PLAN_FORCING = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET ASYNC_STATS_UPDATE_WAIT_AT_LOW_PRIORITY = OFF;
GO
ALTER DATABASE SCOPED CONFIGURATION SET BATCH_MODE_ADAPTIVE_JOINS = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET BATCH_MODE_MEMORY_GRANT_FEEDBACK = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET BATCH_MODE_ON_ROWSTORE = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET CE_FEEDBACK = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET DEFERRED_COMPILATION_TV = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET ELEVATE_ONLINE = OFF;
GO
ALTER DATABASE SCOPED CONFIGURATION SET ELEVATE_RESUMABLE = OFF;
GO
ALTER DATABASE SCOPED CONFIGURATION SET EXEC_QUERY_STATS_FOR_SCALAR_FUNCTIONS = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET FORCE_SHOWPLAN_RUNTIME_PARAMETER_COLLECTION = OFF;
GO
ALTER DATABASE SCOPED CONFIGURATION SET GLOBAL_TEMPORARY_TABLE_AUTO_DROP = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET IDENTITY_CACHE = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET INTERLEAVED_EXECUTION_TVF = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET ISOLATE_SECURITY_POLICY_CARDINALITY = OFF;
GO
ALTER DATABASE SCOPED CONFIGURATION SET LAST_QUERY_PLAN_STATS = OFF;
GO
ALTER DATABASE SCOPED CONFIGURATION SET LEGACY_CARDINALITY_ESTIMATION = OFF;
GO
ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET LEGACY_CARDINALITY_ESTIMATION = PRIMARY;
GO
ALTER DATABASE SCOPED CONFIGURATION SET LIGHTWEIGHT_QUERY_PROFILING = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET MAXDOP = 8;
GO
ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET MAXDOP = PRIMARY;
GO
ALTER DATABASE SCOPED CONFIGURATION SET MEMORY_GRANT_FEEDBACK_PERCENTILE_GRANT = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET MEMORY_GRANT_FEEDBACK_PERSISTENCE = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET OPTIMIZED_SP_EXECUTESQL = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET OPTIMIZE_FOR_AD_HOC_WORKLOADS = OFF;
GO
ALTER DATABASE SCOPED CONFIGURATION SET PARAMETER_SENSITIVE_PLAN_OPTIMIZATION = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET PARAMETER_SNIFFING = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET PARAMETER_SNIFFING = PRIMARY;
GO
ALTER DATABASE SCOPED CONFIGURATION SET PAUSED_RESUMABLE_INDEX_ABORT_DURATION_MINUTES = 1440;
GO
ALTER DATABASE SCOPED CONFIGURATION SET QUERY_OPTIMIZER_HOTFIXES = OFF;
GO
ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET QUERY_OPTIMIZER_HOTFIXES = PRIMARY;
GO
ALTER DATABASE SCOPED CONFIGURATION SET READABLE_SECONDARY_TEMPORARY_STATS_AUTO_CREATE = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET READABLE_SECONDARY_TEMPORARY_STATS_AUTO_UPDATE = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET ROW_MODE_MEMORY_GRANT_FEEDBACK = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET TSQL_SCALAR_UDF_INLINING = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET VERBOSE_TRUNCATION_WARNINGS = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET XTP_PROCEDURE_EXECUTION_STATISTICS = OFF;
GO
ALTER DATABASE SCOPED CONFIGURATION SET XTP_QUERY_EXECUTION_STATISTICS = OFF;
GO
USE [userData]
GO
/****** Object:  Table [dbo].[appAccountTypes]    Script Date: 12/28/23 11:39:51 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[appAccountTypes](
	[accountTypeID] [int] IDENTITY(1,1) NOT NULL,
	[typeName] [varchar](40) NOT NULL,
	[typeDescription] [varchar](100) NULL,
 CONSTRAINT [PK_appAccountTypes] PRIMARY KEY CLUSTERED 
(
	[accountTypeID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[appFeeTypes]    Script Date: 12/28/23 11:39:52 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[appFeeTypes](
	[feeID] [int] IDENTITY(1,1) NOT NULL,
	[feeName] [text] NOT NULL,
	[description] [text] NOT NULL,
	[defaultPrice] [decimal](8, 2) NULL,
	[defaultOccurrence] [int] NULL,
	[displayOrder] [int] NOT NULL,
 CONSTRAINT [PK_appFeeTypes] PRIMARY KEY CLUSTERED 
(
	[feeID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[appOccurrences]    Script Date: 12/28/23 11:39:52 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[appOccurrences](
	[occurrenceID] [int] NOT NULL,
	[occurrence] [int] NOT NULL,
	[perPeriod] [int] NULL,
 CONSTRAINT [PK_appOccurrences] PRIMARY KEY CLUSTERED 
(
	[occurrenceID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[appPaymentMethods]    Script Date: 12/28/23 11:39:52 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[appPaymentMethods](
	[methodID] [int] NOT NULL,
	[methodName] [varchar](30) NOT NULL,
 CONSTRAINT [PK_appPaymentMethods] PRIMARY KEY CLUSTERED 
(
	[methodID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[appPaymentStatus]    Script Date: 12/28/23 11:39:52 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[appPaymentStatus](
	[statusID] [int] NOT NULL,
	[statusName] [varchar](25) NOT NULL,
	[isCompleted] [bit] NOT NULL,
	[statusIcon] [varchar](100) NULL,
 CONSTRAINT [PK_appPaymentStatus] PRIMARY KEY CLUSTERED 
(
	[statusID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[appPeriods]    Script Date: 12/28/23 11:39:52 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[appPeriods](
	[periodID] [int] NOT NULL,
	[name] [varchar](20) NOT NULL,
	[abbreviation] [varchar](8) NOT NULL,
	[isLeasePeriod] [bit] NOT NULL,
 CONSTRAINT [PK_appPeriods] PRIMARY KEY CLUSTERED 
(
	[periodID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userAccounts]    Script Date: 12/28/23 11:39:52 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userAccounts](
	[userID] [int] NOT NULL,
	[accountTypeID] [int] NOT NULL,
	[emailAddress] [varchar](50) NOT NULL,
	[emailVerified] [bit] NOT NULL,
	[passHash] [varchar](72) NOT NULL,
	[createDate] [date] NOT NULL,
	[attemptsSinceLastLogin] [int] NOT NULL,
 CONSTRAINT [PK_userAccounts] PRIMARY KEY CLUSTERED 
(
	[userID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userAddresses]    Script Date: 12/28/23 11:39:52 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userAddresses](
	[addressID] [int] IDENTITY(1,1) NOT NULL,
	[houseNumber] [int] NOT NULL,
	[streetName] [varchar](30) NOT NULL,
	[apptNo] [varchar](6) NULL,
	[city] [varchar](30) NOT NULL,
	[state] [varchar](2) NOT NULL,
	[zipCode] [numeric](5, 0) NOT NULL,
 CONSTRAINT [PK_userAddresses] PRIMARY KEY CLUSTERED 
(
	[addressID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userApplications]    Script Date: 12/28/23 11:39:52 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userApplications](
	[applicationID] [int] IDENTITY(1,1) NOT NULL,
	[leaseID] [int] NOT NULL,
	[applicantID] [int] NOT NULL,
	[coApplicantID] [int] NULL,
	[currentAddressID] [int] NOT NULL,
	[currentMonthlyRent] [varchar](15) NOT NULL,
	[currentMoveIn] [date] NOT NULL,
	[currentLeaveReason] [varchar](120) NULL,
	[currentOwnerID] [int] NOT NULL,
	[previousAddressID] [int] NULL,
	[previousMonthlyRent] [varchar](15) NULL,
	[previousMoveIn] [date] NULL,
	[previousLeaveReason] [varchar](120) NULL,
	[previousOwnerID] [int] NULL,
	[lastYearLatePayments] [bit] NOT NULL,
	[refusedPayments] [bit] NOT NULL,
	[everEvicted] [bit] NOT NULL,
	[additionalInfo] [varchar](200) NULL,
	[bestDayPhoneNo] [varchar](20) NULL,
	[bestEveningPhoneNo] [varchar](20) NULL,
	[informationReleaseID] [int] NOT NULL,
	[agree] [bit] NOT NULL,
	[dateTime] [datetime] NOT NULL,
	[ipAddress] [varchar](15) NOT NULL,
	[applicationStatus] [int] NOT NULL,
	[landlordComments] [varchar](500) NULL,
 CONSTRAINT [PK_userApplications] PRIMARY KEY CLUSTERED 
(
	[applicationID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userCompanies]    Script Date: 12/28/23 11:39:52 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userCompanies](
	[companyID] [int] IDENTITY(1,1) NOT NULL,
	[companyName] [varchar](50) NOT NULL,
	[phoneNumber] [char](10) NOT NULL,
	[mailingAddress] [int] NOT NULL,
	[billingAddress] [int] NULL,
	[emailInvoiceAddress] [varchar](50) NULL,
	[EIN] [int] NULL,
	[createdBy] [int] NOT NULL,
	[createDate] [datetime] NOT NULL,
 CONSTRAINT [PK_companies] PRIMARY KEY CLUSTERED 
(
	[companyID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userCompanyRoles]    Script Date: 12/28/23 11:39:53 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userCompanyRoles](
	[roleID] [int] IDENTITY(1,1) NOT NULL,
	[companyID] [int] NOT NULL,
	[userID] [int] NOT NULL,
	[roleTypeID] [int] NOT NULL,
	[role_begin] [datetime] NOT NULL,
	[assignedUser] [int] NOT NULL,
	[role_end] [datetime] NULL,
	[endedUser] [int] NULL,
 CONSTRAINT [PK_userCompanyPeople] PRIMARY KEY CLUSTERED 
(
	[roleID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userDependants]    Script Date: 12/28/23 11:39:53 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userDependants](
	[dependantID] [int] IDENTITY(1,1) NOT NULL,
	[applicationID] [int] NULL,
	[leaseID] [int] NULL,
	[order] [int] NOT NULL,
	[dependantName] [varchar](50) NOT NULL,
	[dependantDOB] [date] NOT NULL,
	[applicantsRelationship] [varchar](50) NULL,
 CONSTRAINT [PK_userDependants] PRIMARY KEY CLUSTERED 
(
	[dependantID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userDetailOptions]    Script Date: 12/28/23 11:39:53 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userDetailOptions](
	[detailID] [int] IDENTITY(1,1) NOT NULL,
	[propertyName] [varchar](100) NULL,
 CONSTRAINT [PK_userDetailOptions] PRIMARY KEY CLUSTERED 
(
	[detailID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userEmploymentHistory]    Script Date: 12/28/23 11:39:53 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userEmploymentHistory](
	[employmentID] [int] NOT NULL,
	[applicationID] [int] NOT NULL,
	[applicantID] [int] NULL,
	[employmentStatus] [int] NOT NULL,
	[employerName] [varchar](50) NOT NULL,
	[employmentBegin] [date] NOT NULL,
	[employedAs] [varchar](50) NOT NULL,
	[supervisorID] [int] NOT NULL,
	[salary] [float] NOT NULL,
	[salaryPeriod] [int] NOT NULL,
	[landlordReviewUser] [int] NULL,
	[landlordComment] [int] NULL,
 CONSTRAINT [PK_userEmploymentHistory] PRIMARY KEY CLUSTERED 
(
	[employmentID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userLeaseFees]    Script Date: 12/28/23 11:39:53 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userLeaseFees](
	[leaseFeeID] [int] IDENTITY(1,1) NOT NULL,
	[leaseID] [int] NOT NULL,
	[feeID] [int] NOT NULL,
	[feeName] [varchar](30) NOT NULL,
	[feeAmount] [float] NOT NULL,
	[occurrence] [int] NOT NULL,
	[startAfterLength] [int] NOT NULL,
	[startAfterPeriod] [int] NOT NULL,
	[createUser] [int] NOT NULL,
	[createDate] [datetime] NOT NULL,
 CONSTRAINT [PK_userLeaseFees] PRIMARY KEY CLUSTERED 
(
	[leaseFeeID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userLeasePeople]    Script Date: 12/28/23 11:39:53 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userLeasePeople](
	[leaseID] [int] NOT NULL,
	[personID] [int] NOT NULL,
	[role] [varchar](50) NOT NULL,
 CONSTRAINT [PK_userLeasePeople] PRIMARY KEY CLUSTERED 
(
	[leaseID] ASC,
	[personID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userLeases]    Script Date: 12/28/23 11:39:53 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userLeases](
	[leaseID] [int] IDENTITY(1,1) NOT NULL,
	[propertyID] [int] NOT NULL,
	[leaseStatus] [varchar](25) NULL,
	[availableDate] [date] NOT NULL,
	[moveInDate] [date] NULL,
	[terminationDate] [date] NULL,
	[lastPaidPeriodStartingDate] [date] NULL,
	[lastPeriodRemainingBalance] [float] NOT NULL,
	[leasePeriod] [int] NOT NULL,
	[leaseSuccessionPeriod] [int] NULL,
	[securityDeposit] [float] NOT NULL,
	[contractDocID] [varchar](50) NULL,
	[createUser] [int] NOT NULL,
	[createDate] [datetime] NOT NULL,
 CONSTRAINT [PK_userLease] PRIMARY KEY CLUSTERED 
(
	[leaseID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userPaymentItems]    Script Date: 12/28/23 11:39:53 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userPaymentItems](
	[paymentItemID] [int] IDENTITY(1,1) NOT NULL,
	[paymentID] [int] NOT NULL,
	[dueDate] [date] NOT NULL,
	[itemName] [varchar](50) NOT NULL,
	[leaseFeeID] [int] NULL,
	[qty] [int] NOT NULL,
	[amountPaid] [float] NULL,
	[createUser] [int] NULL,
	[createDate] [datetime] NOT NULL,
 CONSTRAINT [PK_userPaymentItems] PRIMARY KEY CLUSTERED 
(
	[paymentItemID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userPayments]    Script Date: 12/28/23 11:39:53 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userPayments](
	[paymentID] [int] IDENTITY(1,1) NOT NULL,
	[leaseID] [int] NOT NULL,
	[periodNo] [int] NOT NULL,
	[periodStartDate] [date] NOT NULL,
	[dueDate] [date] NOT NULL,
	[paymentStatus] [int] NULL,
	[paymentMethod] [int] NULL,
	[amountReceived] [float] NOT NULL,
	[dateReceived] [date] NULL,
	[comments] [varchar](120) NULL,
	[createUser] [int] NOT NULL,
	[createDate] [datetime] NOT NULL,
 CONSTRAINT [PK_userPayments] PRIMARY KEY CLUSTERED 
(
	[paymentID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userPeople]    Script Date: 12/28/23 11:39:53 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userPeople](
	[personID] [int] IDENTITY(1,1) NOT NULL,
	[firstName] [varchar](50) NOT NULL,
	[lastName] [varchar](50) NULL,
	[phoneNumber] [char](10) NOT NULL,
	[addressID] [int] NULL,
	[createdOn] [datetime] NOT NULL,
 CONSTRAINT [PK_userPeople] PRIMARY KEY CLUSTERED 
(
	[personID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userPersonDetails]    Script Date: 12/28/23 11:39:53 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userPersonDetails](
	[personID] [int] NOT NULL,
	[detailID] [int] NOT NULL,
	[rev] [int] NULL,
	[propertyValue] [varchar](50) NULL,
	[setDate] [datetime] NOT NULL,
	[setPersonID] [int] NOT NULL,
 CONSTRAINT [PK_userPersonDetails] PRIMARY KEY CLUSTERED 
(
	[personID] ASC,
	[detailID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userProperties]    Script Date: 12/28/23 11:39:54 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userProperties](
	[propertyID] [int] IDENTITY(1,1) NOT NULL,
	[companyID] [int] NOT NULL,
	[addressID] [int] NOT NULL,
	[bedroomCount] [int] NOT NULL,
	[bathroomCount] [float] NOT NULL,
	[parkingCount] [int] NULL,
	[garageCount] [int] NULL,
	[storiesCount] [float] NULL,
	[homeType] [varchar](50) NOT NULL,
	[yearBuilt] [numeric](4, 0) NULL,
	[purchasePrice] [int] NULL,
	[purchaseDate] [date] NULL,
	[schoolDistrict] [varchar](50) NOT NULL,
	[nickname] [varchar](50) NOT NULL,
	[createUser] [int] NOT NULL,
	[createDate] [datetime] NOT NULL,
 CONSTRAINT [PK_userProperties] PRIMARY KEY CLUSTERED 
(
	[propertyID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userReferences]    Script Date: 12/28/23 11:39:54 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userReferences](
	[referenceID] [int] NOT NULL,
	[applicationID] [int] NOT NULL,
	[sortOrder] [int] NOT NULL,
	[personID] [int] NOT NULL,
	[relationship] [varchar](20) NOT NULL,
	[landlordReviewed] [bit] NOT NULL,
	[landlordComments] [varchar](500) NULL,
 CONSTRAINT [PK_userReferences] PRIMARY KEY CLUSTERED 
(
	[referenceID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userSessions]    Script Date: 12/28/23 11:39:54 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userSessions](
	[sessionID] [nvarchar](50) NOT NULL,
	[userID] [int] NOT NULL,
	[IPv4_ipAddress] [varchar](15) NOT NULL,
	[loginDatetime] [datetime] NOT NULL,
	[expiredDatetime] [datetime] NOT NULL,
	[nextDatetime] [datetime] NOT NULL,
 CONSTRAINT [PK_userSessions] PRIMARY KEY CLUSTERED 
(
	[sessionID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[userVehicles]    Script Date: 12/28/23 11:39:54 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userVehicles](
	[vehicleID] [int] NOT NULL,
	[applicationID] [int] NULL,
	[leaseID] [int] NULL,
	[year] [numeric](4, 0) NULL,
	[make] [varchar](20) NULL,
	[model] [varchar](20) NULL,
	[color] [varchar](20) NULL,
	[plateNo] [varchar](10) NULL,
 CONSTRAINT [PK_userVehicles] PRIMARY KEY CLUSTERED 
(
	[vehicleID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
SET IDENTITY_INSERT [dbo].[appAccountTypes] ON 

INSERT [dbo].[appAccountTypes] ([accountTypeID], [typeName], [typeDescription]) VALUES (1, N'level1Admin', N'Level 1 admin has ability to see and change everything')
INSERT [dbo].[appAccountTypes] ([accountTypeID], [typeName], [typeDescription]) VALUES (2, N'level2Admin', N'Level 2 admin can change some things')
INSERT [dbo].[appAccountTypes] ([accountTypeID], [typeName], [typeDescription]) VALUES (3, N'tenant', N'Tenant account type')
INSERT [dbo].[appAccountTypes] ([accountTypeID], [typeName], [typeDescription]) VALUES (4, N'landlord', N'Landlord account type')
INSERT [dbo].[appAccountTypes] ([accountTypeID], [typeName], [typeDescription]) VALUES (5, N'companyAdmin', N'A user in-charge of a company. Should be at least 1 companyAdmin for each company. Can be changed')
INSERT [dbo].[appAccountTypes] ([accountTypeID], [typeName], [typeDescription]) VALUES (6, N'companyEntry', N'A user associated with a company that has access to enter and change data. No delete authority')
INSERT [dbo].[appAccountTypes] ([accountTypeID], [typeName], [typeDescription]) VALUES (7, N'companyRead', N'A user associated with a company that can read data. No write, change, or delete authority.')
SET IDENTITY_INSERT [dbo].[appAccountTypes] OFF
SET IDENTITY_INSERT [dbo].[appFeeTypes] ON 

INSERT [dbo].[appFeeTypes] ([feeID], [feeName], [description], [defaultPrice], [defaultOccurrence], [displayOrder]) VALUES (1, N'Late Fee', N'Fee added to the rent due to delyed payment', CAST(5.00 AS Decimal(8, 2)), 2, 3)
INSERT [dbo].[appFeeTypes] ([feeID], [feeName], [description], [defaultPrice], [defaultOccurrence], [displayOrder]) VALUES (2, N'Bounced Check Fee', N'Fee added to bill when check has bounced', CAST(35.00 AS Decimal(8, 2)), 3, 4)
INSERT [dbo].[appFeeTypes] ([feeID], [feeName], [description], [defaultPrice], [defaultOccurrence], [displayOrder]) VALUES (3, N'Pet Fee', N'Fee added to invoice to cover additional costs and depreciation associated with pets living in the unit', CAST(35.00 AS Decimal(8, 2)), 1, 2)
INSERT [dbo].[appFeeTypes] ([feeID], [feeName], [description], [defaultPrice], [defaultOccurrence], [displayOrder]) VALUES (4, N'Rent', N'Major ''fee'' associated with paying the monthly rent', NULL, 1, 1)
INSERT [dbo].[appFeeTypes] ([feeID], [feeName], [description], [defaultPrice], [defaultOccurrence], [displayOrder]) VALUES (5, N'Security Deposit', N'Funds held by the landlord to cover any costs associated with damage caused by tenants', NULL, 3, 99)
SET IDENTITY_INSERT [dbo].[appFeeTypes] OFF
INSERT [dbo].[appOccurrences] ([occurrenceID], [occurrence], [perPeriod]) VALUES (1, 1, 2)
INSERT [dbo].[appOccurrences] ([occurrenceID], [occurrence], [perPeriod]) VALUES (2, 1, 3)
INSERT [dbo].[appOccurrences] ([occurrenceID], [occurrence], [perPeriod]) VALUES (3, 1, 5)
INSERT [dbo].[appPaymentMethods] ([methodID], [methodName]) VALUES (1, N'Cash')
INSERT [dbo].[appPaymentMethods] ([methodID], [methodName]) VALUES (2, N'Personal Check')
INSERT [dbo].[appPaymentMethods] ([methodID], [methodName]) VALUES (3, N'Direct Deposit')
INSERT [dbo].[appPaymentMethods] ([methodID], [methodName]) VALUES (4, N'Bank Check')
INSERT [dbo].[appPaymentStatus] ([statusID], [statusName], [isCompleted], [statusIcon]) VALUES (1, N'upcoming', 0, NULL)
INSERT [dbo].[appPaymentStatus] ([statusID], [statusName], [isCompleted], [statusIcon]) VALUES (2, N'pending', 0, N'<i class="fa-regular fa-hourglass-half" style="height: 50px;"></i>')
INSERT [dbo].[appPaymentStatus] ([statusID], [statusName], [isCompleted], [statusIcon]) VALUES (3, N'completed', 1, N'<i class="fa-solid fa-square-check" style="height: 50px;"></i>')
INSERT [dbo].[appPaymentStatus] ([statusID], [statusName], [isCompleted], [statusIcon]) VALUES (4, N'late', 0, N'<i class="fa-solid fa-triangle-exclamation" style="height: 50px;"></i>')
INSERT [dbo].[appPaymentStatus] ([statusID], [statusName], [isCompleted], [statusIcon]) VALUES (5, N'missing', 0, N'<i class="fa-solid fa-square-minus" style="height: 50px;"></i>')
INSERT [dbo].[appPeriods] ([periodID], [name], [abbreviation], [isLeasePeriod]) VALUES (1, N'week', N'wk', 0)
INSERT [dbo].[appPeriods] ([periodID], [name], [abbreviation], [isLeasePeriod]) VALUES (2, N'month', N'mo', 0)
INSERT [dbo].[appPeriods] ([periodID], [name], [abbreviation], [isLeasePeriod]) VALUES (3, N'day', N'day', 0)
INSERT [dbo].[appPeriods] ([periodID], [name], [abbreviation], [isLeasePeriod]) VALUES (4, N'year', N'yr', 1)
INSERT [dbo].[appPeriods] ([periodID], [name], [abbreviation], [isLeasePeriod]) VALUES (5, N'occurrence', N'occr', 0)
INSERT [dbo].[userAccounts] ([userID], [accountTypeID], [emailAddress], [emailVerified], [passHash], [createDate], [attemptsSinceLastLogin]) VALUES (36, 4, N'thartzler1@live.maryville.edu', 0, N'$2b$12$BMPCJQxdlkUI9iBIYLF5WuOkGyoXVpL/OZKUkvSHKPxxpNw0iStN.', CAST(N'2023-12-08' AS Date), 0)
INSERT [dbo].[userAccounts] ([userID], [accountTypeID], [emailAddress], [emailVerified], [passHash], [createDate], [attemptsSinceLastLogin]) VALUES (38, 4, N'newemail@live.maryville.edu', 0, N'$2b$12$GWwdQp5Lw/YVWKydVtuhC.TUVFvWGpo3jrfxOawAESXrB2JcMn2nG', CAST(N'2023-12-09' AS Date), 0)
INSERT [dbo].[userAccounts] ([userID], [accountTypeID], [emailAddress], [emailVerified], [passHash], [createDate], [attemptsSinceLastLogin]) VALUES (39, 4, N'thartzler3@live.maryville.edu', 0, N'$2b$12$icsKAkZ6Lk1eDbiv57jETux/cbU98iXvG1TfRNCUOwaE3s7st5h6q', CAST(N'2023-12-09' AS Date), 0)
INSERT [dbo].[userAccounts] ([userID], [accountTypeID], [emailAddress], [emailVerified], [passHash], [createDate], [attemptsSinceLastLogin]) VALUES (48, 4, N'tom@mot.com', 0, N'$2b$12$SIoGL4Y9xmvSsSfEelB0zedpfQpvcUMib8dh1vojRsba9jIyRUNgq', CAST(N'2023-12-14' AS Date), 0)
INSERT [dbo].[userAccounts] ([userID], [accountTypeID], [emailAddress], [emailVerified], [passHash], [createDate], [attemptsSinceLastLogin]) VALUES (49, 4, N'ph@test.com', 0, N'$2b$12$Ojw4USQSqSZfleghJlMfk.aHUW6I.Exuy5kcWCjk.jhfkRxW03G6i', CAST(N'2023-12-14' AS Date), 0)
INSERT [dbo].[userAccounts] ([userID], [accountTypeID], [emailAddress], [emailVerified], [passHash], [createDate], [attemptsSinceLastLogin]) VALUES (50, 3, N'mr@kingsway.com', 0, N'$2b$12$7mTV19ebMe9y.V66/CnDI.RIFO/q5hQoLBMtiELlXew2P.YRtjR5y', CAST(N'2023-12-14' AS Date), 0)
INSERT [dbo].[userAccounts] ([userID], [accountTypeID], [emailAddress], [emailVerified], [passHash], [createDate], [attemptsSinceLastLogin]) VALUES (51, 4, N'hhswest2@hartzler.xyz', 0, N'$2b$12$P0IFtG3.ti2UxmtRCktPce/paU6bMpvoDEtxb/OBTGSRrTmiYbZUK', CAST(N'2023-12-15' AS Date), 0)
INSERT [dbo].[userAccounts] ([userID], [accountTypeID], [emailAddress], [emailVerified], [passHash], [createDate], [attemptsSinceLastLogin]) VALUES (53, 4, N'bob.ruff@dwleasing.net', 0, N'$2b$12$BF2zeTRTgB94jEeY8P1TjO5etV2y9iJnl7WtljU0jYzza7BjLrcN6', CAST(N'2023-12-17' AS Date), 0)
INSERT [dbo].[userAccounts] ([userID], [accountTypeID], [emailAddress], [emailVerified], [passHash], [createDate], [attemptsSinceLastLogin]) VALUES (54, 4, N'Actor@none.com', 0, N'$2b$12$S9Sabk/UWAacXpZAoiFJ6.yNrxCLo26sZn1qUiYA2WyVhoEr048ty', CAST(N'2023-12-17' AS Date), 0)
INSERT [dbo].[userAccounts] ([userID], [accountTypeID], [emailAddress], [emailVerified], [passHash], [createDate], [attemptsSinceLastLogin]) VALUES (55, 3, N'Gbmatt@aol.com', 0, N'$2b$12$1h2MY84TYBcw3PJztjNPFeyrxPQNC3dZWFuXHdPBGwPXVhIygK8ji', CAST(N'2023-12-17' AS Date), 0)
INSERT [dbo].[userAccounts] ([userID], [accountTypeID], [emailAddress], [emailVerified], [passHash], [createDate], [attemptsSinceLastLogin]) VALUES (56, 3, N'Fancy.Nancy@yahoo.com', 0, N'$2b$12$Up5GveKIw1Ab4KsnOWGCB.J4sqD0RANmnFAUiY7yc3Xu1iiQUdZyW', CAST(N'2023-12-18' AS Date), 0)
INSERT [dbo].[userAccounts] ([userID], [accountTypeID], [emailAddress], [emailVerified], [passHash], [createDate], [attemptsSinceLastLogin]) VALUES (57, 4, N'iag7@1870.uakron.edu', 0, N'$2b$12$.8rn2yliEI7ZGhqL7n3rUuDadyzO7tknBOCLmcAcEouVxLgtQaMwK', CAST(N'2023-12-22' AS Date), 0)
INSERT [dbo].[userAccounts] ([userID], [accountTypeID], [emailAddress], [emailVerified], [passHash], [createDate], [attemptsSinceLastLogin]) VALUES (58, 3, N'miller.robert@hankooktech.com', 0, N'$2b$12$8hUhLLWCFsw.Y2wfctFvweTCCgWXI2G9l.zfNVFtHM5rxsSeNaNn6', CAST(N'2023-12-22' AS Date), 0)
SET IDENTITY_INSERT [dbo].[userAddresses] ON 

INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (4, 9335, N'Steiner Road', N'', N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (5, 12345, N'Some Road', N'', N'St. Louis', N'MO', CAST(98765 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (6, 12345, N'Some Circle', N'', N'SmallTown', N'OH', CAST(98765 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (7, 12345, N'Some Circle', N'', N'SmallTown', N'OH', CAST(98765 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (8, 12345, N'Some Circle', N'', N'SmallTown', N'OH', CAST(98765 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (9, 12345, N'Some Circle', N'', N'SmallTown', N'OH', CAST(98765 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (10, 12345, N'Some Circle', N'', N'SmallTown', N'OH', CAST(98765 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (11, 12345, N'Some Circle', N'', N'SmallTown', N'OH', CAST(98765 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (12, 12345, N'Some Circle', N'', N'SmallTown', N'OH', CAST(98765 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (13, 12345, N'Some Circle', N'', N'SmallTown', N'OH', CAST(98765 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (14, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (15, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (16, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (17, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (18, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (19, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (20, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (21, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (22, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (23, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (24, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (25, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (26, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (27, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (28, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (29, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (30, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (31, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (32, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (33, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (34, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (35, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (36, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (37, 9335, N'9335 Steiner Road', N'15', N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (38, 9335, N'Steiner', N'', N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (40, 9335, N'Steiner Road', N'', N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (41, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (42, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (43, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (44, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (45, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (46, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (47, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (48, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (49, 9335, N'Steiner Road', NULL, N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (52, 9335, N'steiner', N'', N'road', N'MN', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (53, 12345, N'123456', N'', N'12d5', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (54, 1740, N'Eastern Road', NULL, N'Rittman', N'OH', CAST(44720 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (55, 1740, N'Eastern Road', NULL, N'Rittman', N'OH', CAST(44720 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (60, 1234, N'Upside Street', N'', N'DownTown', N'UL', CAST(42242 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (61, 2344, N'That', NULL, N'Those', N'No', CAST(38337 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (62, 2324, N'sldkfj', NULL, N'sldfkj', N'oj', CAST(44255 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (63, 98203, N'slkdtj', NULL, N'lksjf', N'lk', CAST(23323 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (64, 890, N'9335 Steiner Road', N'', N'Rittman', N'OH', CAST(44270 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (65, 90, N'Thornton', N'', N'Akron', N'OH', CAST(44276 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (66, 1251, N'Wellesley Ave', N'102', N'Los Angeles', N'CA', CAST(90025 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (67, 1940, N'Westwood Dr', NULL, N'Marshton', N'FL', CAST(72777 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (68, 9244, N'Spruce Lane', N'', N'Montgomery', N'IL', CAST(54336 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (69, 9244, N'Spruce Lane', N'', N'Montgomery', N'IL', CAST(54336 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (70, 1234, N'You can drive', N'', N'Mono', N'CA', CAST(12345 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (71, 1234, N'Not my Lane', NULL, N'Grossburg', N'MA', CAST(96352 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (72, 777, N'Stridecourt Circle', NULL, N'Mountain Heights', N'SC', CAST(23994 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (73, 2987, N'Clark Mill Rd', N'', N'Norton', N'OH', CAST(44203 AS Numeric(5, 0)))
INSERT [dbo].[userAddresses] ([addressID], [houseNumber], [streetName], [apptNo], [city], [state], [zipCode]) VALUES (74, 3535, N'Forest Lake Drive', NULL, N'Uniontown', N'OH', CAST(44685 AS Numeric(5, 0)))
SET IDENTITY_INSERT [dbo].[userAddresses] OFF
SET IDENTITY_INSERT [dbo].[userCompanies] ON 

INSERT [dbo].[userCompanies] ([companyID], [companyName], [phoneNumber], [mailingAddress], [billingAddress], [emailInvoiceAddress], [EIN], [createdBy], [createDate]) VALUES (8, N'HHS, INC', N'3306041958', 36, 36, N'thartzler1@live.maryville.edu', NULL, 36, CAST(N'2023-12-08T06:30:15.893' AS DateTime))
INSERT [dbo].[userCompanies] ([companyID], [companyName], [phoneNumber], [mailingAddress], [billingAddress], [emailInvoiceAddress], [EIN], [createdBy], [createDate]) VALUES (11, N'newcompany4', N'3306041958', 40, 40, N'thartzler3@live.maryville.edu', NULL, 39, CAST(N'2023-12-09T17:08:38.817' AS DateTime))
INSERT [dbo].[userCompanies] ([companyID], [companyName], [phoneNumber], [mailingAddress], [billingAddress], [emailInvoiceAddress], [EIN], [createdBy], [createDate]) VALUES (16, N'PoundaHounda', N'2342352423', 65, 65, N'ph@test.com', NULL, 49, CAST(N'2023-12-14T17:08:27.183' AS DateTime))
INSERT [dbo].[userCompanies] ([companyID], [companyName], [phoneNumber], [mailingAddress], [billingAddress], [emailInvoiceAddress], [EIN], [createdBy], [createDate]) VALUES (17, N'HHS West', N'0987654321', 66, 66, N'hhswest2@hartzler.xyz', NULL, 51, CAST(N'2023-12-15T02:35:39.820' AS DateTime))
INSERT [dbo].[userCompanies] ([companyID], [companyName], [phoneNumber], [mailingAddress], [billingAddress], [emailInvoiceAddress], [EIN], [createdBy], [createDate]) VALUES (19, N'Dogwood leasing', N'7621327753', 69, 69, N'Bob.ruff@dwleasing.net', NULL, 53, CAST(N'2023-12-17T06:02:55.740' AS DateTime))
INSERT [dbo].[userCompanies] ([companyID], [companyName], [phoneNumber], [mailingAddress], [billingAddress], [emailInvoiceAddress], [EIN], [createdBy], [createDate]) VALUES (20, N'None actor ', N'7765433212', 70, 70, N'Actor@none.com', NULL, 54, CAST(N'2023-12-17T07:27:17.180' AS DateTime))
INSERT [dbo].[userCompanies] ([companyID], [companyName], [phoneNumber], [mailingAddress], [billingAddress], [emailInvoiceAddress], [EIN], [createdBy], [createDate]) VALUES (21, N'Hankook Tire Co. LTD.', N'3309786224', 73, 73, N'iag7@1870.uakron.edu', NULL, 57, CAST(N'2023-12-22T19:10:52.443' AS DateTime))
SET IDENTITY_INSERT [dbo].[userCompanies] OFF
SET IDENTITY_INSERT [dbo].[userCompanyRoles] ON 

INSERT [dbo].[userCompanyRoles] ([roleID], [companyID], [userID], [roleTypeID], [role_begin], [assignedUser], [role_end], [endedUser]) VALUES (6, 8, 36, 5, CAST(N'2023-12-08T06:30:16.240' AS DateTime), 36, NULL, NULL)
INSERT [dbo].[userCompanyRoles] ([roleID], [companyID], [userID], [roleTypeID], [role_begin], [assignedUser], [role_end], [endedUser]) VALUES (9, 11, 39, 5, CAST(N'2023-12-09T17:08:38.833' AS DateTime), 39, NULL, NULL)
INSERT [dbo].[userCompanyRoles] ([roleID], [companyID], [userID], [roleTypeID], [role_begin], [assignedUser], [role_end], [endedUser]) VALUES (13, 16, 49, 5, CAST(N'2023-12-14T17:08:27.223' AS DateTime), 49, NULL, NULL)
INSERT [dbo].[userCompanyRoles] ([roleID], [companyID], [userID], [roleTypeID], [role_begin], [assignedUser], [role_end], [endedUser]) VALUES (14, 17, 51, 5, CAST(N'2023-12-15T02:35:39.847' AS DateTime), 51, NULL, NULL)
INSERT [dbo].[userCompanyRoles] ([roleID], [companyID], [userID], [roleTypeID], [role_begin], [assignedUser], [role_end], [endedUser]) VALUES (15, 19, 53, 5, CAST(N'2023-12-17T06:02:55.767' AS DateTime), 53, NULL, NULL)
INSERT [dbo].[userCompanyRoles] ([roleID], [companyID], [userID], [roleTypeID], [role_begin], [assignedUser], [role_end], [endedUser]) VALUES (16, 20, 54, 5, CAST(N'2023-12-17T07:27:17.210' AS DateTime), 54, NULL, NULL)
INSERT [dbo].[userCompanyRoles] ([roleID], [companyID], [userID], [roleTypeID], [role_begin], [assignedUser], [role_end], [endedUser]) VALUES (17, 21, 57, 5, CAST(N'2023-12-22T19:10:52.477' AS DateTime), 57, NULL, NULL)
SET IDENTITY_INSERT [dbo].[userCompanyRoles] OFF
SET IDENTITY_INSERT [dbo].[userDetailOptions] ON 

INSERT [dbo].[userDetailOptions] ([detailID], [propertyName]) VALUES (2, N'DOB')
INSERT [dbo].[userDetailOptions] ([detailID], [propertyName]) VALUES (3, N'middleName')
INSERT [dbo].[userDetailOptions] ([detailID], [propertyName]) VALUES (4, N'cellPhoneNumber')
INSERT [dbo].[userDetailOptions] ([detailID], [propertyName]) VALUES (5, N'cars')
INSERT [dbo].[userDetailOptions] ([detailID], [propertyName]) VALUES (6, N'comments')
INSERT [dbo].[userDetailOptions] ([detailID], [propertyName]) VALUES (7, N'creator')
SET IDENTITY_INSERT [dbo].[userDetailOptions] OFF
SET IDENTITY_INSERT [dbo].[userLeaseFees] ON 

INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (1, 4, 1, N'Late Fee', 25, 1, 4, 3, 49, CAST(N'2023-12-16T09:15:39.780' AS DateTime))
INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (2, 4, 1, N'Late Fee', 5, 2, 4, 3, 49, CAST(N'2023-12-16T09:15:39.943' AS DateTime))
INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (3, 4, 2, N'Bounced Check Fee', 35, 3, 0, 5, 49, CAST(N'2023-12-16T09:15:40.103' AS DateTime))
INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (4, 4, 4, N'Rent', 1120, 1, 0, 3, 49, CAST(N'2023-12-16T09:15:40.260' AS DateTime))
INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (5, 4, 5, N'Security Deposit', 1120, 3, 0, 5, 49, CAST(N'2023-12-16T09:15:40.430' AS DateTime))
INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (11, 6, 4, N'Rent', 675, 1, 0, 3, 53, CAST(N'2023-12-17T09:39:28.500' AS DateTime))
INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (12, 6, 1, N'Late Fee', 25, 1, 5, 3, 53, CAST(N'2023-12-17T09:39:28.513' AS DateTime))
INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (13, 6, 1, N'Late Fee', 5, 2, 5, 3, 53, CAST(N'2023-12-17T09:39:28.523' AS DateTime))
INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (14, 6, 3, N'Pet Fee', 35, 1, 0, 3, 53, CAST(N'2023-12-17T09:39:28.530' AS DateTime))
INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (15, 6, 2, N'Bounced Check Fee', 45, 3, 0, 5, 53, CAST(N'2023-12-17T09:39:28.540' AS DateTime))
INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (16, 7, 4, N'Rent', 950, 1, 0, 3, 53, CAST(N'2023-12-18T08:09:08.440' AS DateTime))
INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (17, 7, 3, N'Pet Fee', 15, 1, 0, 3, 53, CAST(N'2023-12-18T08:09:08.450' AS DateTime))
INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (18, 7, 1, N'Late Fee', 25, 1, 4, 3, 53, CAST(N'2023-12-18T08:09:08.460' AS DateTime))
INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (19, 7, 1, N'Late Fee', 2, 2, 4, 3, 53, CAST(N'2023-12-18T08:09:08.470' AS DateTime))
INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (20, 7, 2, N'Bounced Check Fee', 50, 3, 0, 5, 53, CAST(N'2023-12-18T08:09:08.480' AS DateTime))
INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (21, 7, 5, N'Security Deposit', 950, 3, 0, 5, 53, CAST(N'2023-12-18T08:09:08.490' AS DateTime))
INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (22, 8, 4, N'Rent', 5000, 1, 1, 2, 57, CAST(N'2023-12-22T19:14:55.833' AS DateTime))
INSERT [dbo].[userLeaseFees] ([leaseFeeID], [leaseID], [feeID], [feeName], [feeAmount], [occurrence], [startAfterLength], [startAfterPeriod], [createUser], [createDate]) VALUES (23, 8, 1, N'Late Fee', 5000, 2, 5, 3, 57, CAST(N'2023-12-22T19:14:55.857' AS DateTime))
SET IDENTITY_INSERT [dbo].[userLeaseFees] OFF
INSERT [dbo].[userLeasePeople] ([leaseID], [personID], [role]) VALUES (4, 50, N'tenant')
INSERT [dbo].[userLeasePeople] ([leaseID], [personID], [role]) VALUES (6, 55, N'tenant')
INSERT [dbo].[userLeasePeople] ([leaseID], [personID], [role]) VALUES (7, 56, N'tenant')
INSERT [dbo].[userLeasePeople] ([leaseID], [personID], [role]) VALUES (8, 58, N'tenant')
SET IDENTITY_INSERT [dbo].[userLeases] ON 

INSERT [dbo].[userLeases] ([leaseID], [propertyID], [leaseStatus], [availableDate], [moveInDate], [terminationDate], [lastPaidPeriodStartingDate], [lastPeriodRemainingBalance], [leasePeriod], [leaseSuccessionPeriod], [securityDeposit], [contractDocID], [createUser], [createDate]) VALUES (4, 5, N'leaseStatus', CAST(N'2023-12-01' AS Date), CAST(N'2023-12-16' AS Date), NULL, NULL, 0, 4, 2, 0, NULL, 49, CAST(N'2023-12-16T09:15:39.217' AS DateTime))
INSERT [dbo].[userLeases] ([leaseID], [propertyID], [leaseStatus], [availableDate], [moveInDate], [terminationDate], [lastPaidPeriodStartingDate], [lastPeriodRemainingBalance], [leasePeriod], [leaseSuccessionPeriod], [securityDeposit], [contractDocID], [createUser], [createDate]) VALUES (6, 8, N'Leased', CAST(N'2023-08-01' AS Date), CAST(N'2023-09-17' AS Date), NULL, NULL, 0, 4, 2, 0, NULL, 53, CAST(N'2023-12-17T09:39:28.453' AS DateTime))
INSERT [dbo].[userLeases] ([leaseID], [propertyID], [leaseStatus], [availableDate], [moveInDate], [terminationDate], [lastPaidPeriodStartingDate], [lastPeriodRemainingBalance], [leasePeriod], [leaseSuccessionPeriod], [securityDeposit], [contractDocID], [createUser], [createDate]) VALUES (7, 9, N'Leased', CAST(N'2023-04-07' AS Date), CAST(N'2023-05-01' AS Date), NULL, NULL, 0, 4, 2, 0, NULL, 53, CAST(N'2023-12-18T08:09:08.373' AS DateTime))
INSERT [dbo].[userLeases] ([leaseID], [propertyID], [leaseStatus], [availableDate], [moveInDate], [terminationDate], [lastPaidPeriodStartingDate], [lastPeriodRemainingBalance], [leasePeriod], [leaseSuccessionPeriod], [securityDeposit], [contractDocID], [createUser], [createDate]) VALUES (8, 10, N'its on', CAST(N'2023-12-22' AS Date), CAST(N'2023-12-22' AS Date), NULL, NULL, 0, 4, 2, 0, NULL, 57, CAST(N'2023-12-22T19:14:55.760' AS DateTime))
SET IDENTITY_INSERT [dbo].[userLeases] OFF
SET IDENTITY_INSERT [dbo].[userPayments] ON 

INSERT [dbo].[userPayments] ([paymentID], [leaseID], [periodNo], [periodStartDate], [dueDate], [paymentStatus], [paymentMethod], [amountReceived], [dateReceived], [comments], [createUser], [createDate]) VALUES (1, 4, 0, CAST(N'2023-07-01' AS Date), CAST(N'2023-07-17' AS Date), 1, 4, 0, CAST(N'2023-07-19' AS Date), N'Initial payment with security Deposit', 53, CAST(N'2023-07-17T05:04:03.000' AS DateTime))
INSERT [dbo].[userPayments] ([paymentID], [leaseID], [periodNo], [periodStartDate], [dueDate], [paymentStatus], [paymentMethod], [amountReceived], [dateReceived], [comments], [createUser], [createDate]) VALUES (2, 4, 1, CAST(N'2023-08-01' AS Date), CAST(N'2023-08-01' AS Date), 3, 2, 0, CAST(N'2023-08-01' AS Date), NULL, 53, CAST(N'2023-07-19T23:18:45.000' AS DateTime))
INSERT [dbo].[userPayments] ([paymentID], [leaseID], [periodNo], [periodStartDate], [dueDate], [paymentStatus], [paymentMethod], [amountReceived], [dateReceived], [comments], [createUser], [createDate]) VALUES (3, 6, 2, CAST(N'2023-09-01' AS Date), CAST(N'2023-09-17' AS Date), 1, 2, 0, CAST(N'2023-09-03' AS Date), NULL, 53, CAST(N'2023-09-17T23:18:45.000' AS DateTime))
INSERT [dbo].[userPayments] ([paymentID], [leaseID], [periodNo], [periodStartDate], [dueDate], [paymentStatus], [paymentMethod], [amountReceived], [dateReceived], [comments], [createUser], [createDate]) VALUES (4, 4, 3, CAST(N'2023-10-01' AS Date), CAST(N'2023-10-01' AS Date), 3, 2, 0, CAST(N'2023-10-02' AS Date), NULL, 53, CAST(N'2023-09-03T05:17:06.000' AS DateTime))
INSERT [dbo].[userPayments] ([paymentID], [leaseID], [periodNo], [periodStartDate], [dueDate], [paymentStatus], [paymentMethod], [amountReceived], [dateReceived], [comments], [createUser], [createDate]) VALUES (5, 4, 4, CAST(N'2023-11-01' AS Date), CAST(N'2023-11-01' AS Date), 3, 2, 0, CAST(N'2023-11-05' AS Date), NULL, 53, CAST(N'2023-10-02T22:18:16.000' AS DateTime))
INSERT [dbo].[userPayments] ([paymentID], [leaseID], [periodNo], [periodStartDate], [dueDate], [paymentStatus], [paymentMethod], [amountReceived], [dateReceived], [comments], [createUser], [createDate]) VALUES (6, 4, 5, CAST(N'2023-12-01' AS Date), CAST(N'2023-12-01' AS Date), 1, NULL, 0, NULL, NULL, 53, CAST(N'2023-11-05T04:22:14.000' AS DateTime))
INSERT [dbo].[userPayments] ([paymentID], [leaseID], [periodNo], [periodStartDate], [dueDate], [paymentStatus], [paymentMethod], [amountReceived], [dateReceived], [comments], [createUser], [createDate]) VALUES (7, 7, 0, CAST(N'2023-05-01' AS Date), CAST(N'2023-05-01' AS Date), 3, NULL, 725, CAST(N'2023-05-04' AS Date), NULL, 53, CAST(N'2023-12-18T08:09:08.400' AS DateTime))
INSERT [dbo].[userPayments] ([paymentID], [leaseID], [periodNo], [periodStartDate], [dueDate], [paymentStatus], [paymentMethod], [amountReceived], [dateReceived], [comments], [createUser], [createDate]) VALUES (8, 7, 1, CAST(N'2023-06-01' AS Date), CAST(N'2023-06-01' AS Date), 3, NULL, 710, CAST(N'2023-06-01' AS Date), NULL, 53, CAST(N'2023-05-04T09:22:16.000' AS DateTime))
INSERT [dbo].[userPayments] ([paymentID], [leaseID], [periodNo], [periodStartDate], [dueDate], [paymentStatus], [paymentMethod], [amountReceived], [dateReceived], [comments], [createUser], [createDate]) VALUES (9, 7, 2, CAST(N'2023-07-01' AS Date), CAST(N'2023-07-01' AS Date), 1, NULL, 0, NULL, NULL, 53, CAST(N'2023-06-01T13:17:22.300' AS DateTime))
INSERT [dbo].[userPayments] ([paymentID], [leaseID], [periodNo], [periodStartDate], [dueDate], [paymentStatus], [paymentMethod], [amountReceived], [dateReceived], [comments], [createUser], [createDate]) VALUES (10, 8, 0, CAST(N'2023-12-01' AS Date), CAST(N'2023-12-22' AS Date), 1, NULL, 0, NULL, NULL, 57, CAST(N'2023-12-22T19:14:55.787' AS DateTime))
SET IDENTITY_INSERT [dbo].[userPayments] OFF
SET IDENTITY_INSERT [dbo].[userPeople] ON 

INSERT [dbo].[userPeople] ([personID], [firstName], [lastName], [phoneNumber], [addressID], [createdOn]) VALUES (36, N'Trevin', N'Hartzler', N'3306041958', 36, CAST(N'2023-12-08T06:30:15.390' AS DateTime))
INSERT [dbo].[userPeople] ([personID], [firstName], [lastName], [phoneNumber], [addressID], [createdOn]) VALUES (38, N'Trevin', N'Hartzler', N'3306041958', 38, CAST(N'2023-12-09T15:18:36.990' AS DateTime))
INSERT [dbo].[userPeople] ([personID], [firstName], [lastName], [phoneNumber], [addressID], [createdOn]) VALUES (39, N'Trevin', N'Hartzler', N'3306041958', 40, CAST(N'2023-12-09T17:08:38.793' AS DateTime))
INSERT [dbo].[userPeople] ([personID], [firstName], [lastName], [phoneNumber], [addressID], [createdOn]) VALUES (48, N'Trevin', N'Hartzler', N'1234567890', 64, CAST(N'2023-12-14T09:15:57.760' AS DateTime))
INSERT [dbo].[userPeople] ([personID], [firstName], [lastName], [phoneNumber], [addressID], [createdOn]) VALUES (49, N'John', N'Hound', N'0019292389', 65, CAST(N'2023-12-14T17:08:27.137' AS DateTime))
INSERT [dbo].[userPeople] ([personID], [firstName], [lastName], [phoneNumber], [addressID], [createdOn]) VALUES (50, N'Mary', N'Round', N'8895424451', NULL, CAST(N'2023-12-14T17:11:13.447' AS DateTime))
INSERT [dbo].[userPeople] ([personID], [firstName], [lastName], [phoneNumber], [addressID], [createdOn]) VALUES (51, N'Trenton', N'Hartzler', N'1234567890', 66, CAST(N'2023-12-15T02:35:39.780' AS DateTime))
INSERT [dbo].[userPeople] ([personID], [firstName], [lastName], [phoneNumber], [addressID], [createdOn]) VALUES (53, N'Bob', N'Ruff', N'8856426643', 69, CAST(N'2023-12-17T06:02:55.703' AS DateTime))
INSERT [dbo].[userPeople] ([personID], [firstName], [lastName], [phoneNumber], [addressID], [createdOn]) VALUES (54, N'Trevin', N'Hartzler', N'8876756543', 70, CAST(N'2023-12-17T07:27:17.143' AS DateTime))
INSERT [dbo].[userPeople] ([personID], [firstName], [lastName], [phoneNumber], [addressID], [createdOn]) VALUES (55, N'Gordon', N'Matthews', N'4437652322', NULL, CAST(N'2023-12-17T09:29:57.513' AS DateTime))
INSERT [dbo].[userPeople] ([personID], [firstName], [lastName], [phoneNumber], [addressID], [createdOn]) VALUES (56, N'Warren & Nancy', N'Poppy', N'4567891245', NULL, CAST(N'2023-12-18T08:02:53.633' AS DateTime))
INSERT [dbo].[userPeople] ([personID], [firstName], [lastName], [phoneNumber], [addressID], [createdOn]) VALUES (57, N'Ian', N'Gallatin', N'3309786224', 73, CAST(N'2023-12-22T19:10:52.400' AS DateTime))
INSERT [dbo].[userPeople] ([personID], [firstName], [lastName], [phoneNumber], [addressID], [createdOn]) VALUES (58, N'Bob', N'Miller', N'3306209826', NULL, CAST(N'2023-12-22T19:11:59.130' AS DateTime))
SET IDENTITY_INSERT [dbo].[userPeople] OFF
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (50, 2, 0, N'1981-10-02', CAST(N'2023-12-14T17:11:13.530' AS DateTime), 49)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (50, 3, 0, N'Florence', CAST(N'2023-12-14T17:11:13.477' AS DateTime), 49)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (50, 4, 0, N'5549575584', CAST(N'2023-12-14T17:11:13.507' AS DateTime), 49)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (50, 5, 0, N'Red Impala, black pickup', CAST(N'2023-12-14T17:11:13.557' AS DateTime), 49)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (50, 6, 0, N'2 Children', CAST(N'2023-12-14T17:11:13.583' AS DateTime), 49)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (50, 7, 0, N'', CAST(N'2023-12-14T17:11:13.603' AS DateTime), 49)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (55, 2, 0, N'2008-09-17', CAST(N'2023-12-17T09:29:57.600' AS DateTime), 53)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (55, 3, 0, N'B', CAST(N'2023-12-17T09:29:57.550' AS DateTime), 53)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (55, 4, 0, N'8867785643', CAST(N'2023-12-17T09:29:57.573' AS DateTime), 53)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (55, 5, 0, N'23 maverick, 18 malibu', CAST(N'2023-12-17T09:29:57.623' AS DateTime), 53)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (55, 6, 0, N'Works night shift ', CAST(N'2023-12-17T09:29:57.650' AS DateTime), 53)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (55, 7, 0, N'', CAST(N'2023-12-17T09:29:57.673' AS DateTime), 53)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (56, 2, 0, N'1988-12-22', CAST(N'2023-12-18T08:02:53.723' AS DateTime), 53)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (56, 3, 0, N' ', CAST(N'2023-12-18T08:02:53.667' AS DateTime), 53)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (56, 4, 0, N'9987548845', CAST(N'2023-12-18T08:02:53.697' AS DateTime), 53)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (56, 5, 0, N'White VW ID.4, Grey Pickup', CAST(N'2023-12-18T08:02:53.747' AS DateTime), 53)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (56, 6, 0, N'-', CAST(N'2023-12-18T08:02:53.773' AS DateTime), 53)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (56, 7, 0, N'', CAST(N'2023-12-18T08:02:53.797' AS DateTime), 53)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (58, 2, 0, N'2023-12-22', CAST(N'2023-12-22T19:11:59.290' AS DateTime), 57)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (58, 3, 0, N's', CAST(N'2023-12-22T19:11:59.167' AS DateTime), 57)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (58, 4, 0, N'3306209826', CAST(N'2023-12-22T19:11:59.263' AS DateTime), 57)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (58, 5, 0, N'1', CAST(N'2023-12-22T19:11:59.310' AS DateTime), 57)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (58, 6, 0, N'2', CAST(N'2023-12-22T19:11:59.333' AS DateTime), 57)
INSERT [dbo].[userPersonDetails] ([personID], [detailID], [rev], [propertyValue], [setDate], [setPersonID]) VALUES (58, 7, 0, N'', CAST(N'2023-12-22T19:11:59.353' AS DateTime), 57)
SET IDENTITY_INSERT [dbo].[userProperties] ON 

INSERT [dbo].[userProperties] ([propertyID], [companyID], [addressID], [bedroomCount], [bathroomCount], [parkingCount], [garageCount], [storiesCount], [homeType], [yearBuilt], [purchasePrice], [purchaseDate], [schoolDistrict], [nickname], [createUser], [createDate]) VALUES (2, 11, 49, 4, 3, 6, 4, 2, N'Single-Family', CAST(1984 AS Numeric(4, 0)), 250000, CAST(N'1984-11-12' AS Date), N'Norwayne LSD', N'Home', 39, CAST(N'2023-12-11T07:19:00.510' AS DateTime))
INSERT [dbo].[userProperties] ([propertyID], [companyID], [addressID], [bedroomCount], [bathroomCount], [parkingCount], [garageCount], [storiesCount], [homeType], [yearBuilt], [purchasePrice], [purchaseDate], [schoolDistrict], [nickname], [createUser], [createDate]) VALUES (3, 11, 55, 3, 1, 3, 1, 1, N'Single-Family', CAST(1967 AS Numeric(4, 0)), 98000, CAST(N'2009-09-01' AS Date), N'Chippewa', N'1740', 39, CAST(N'2023-12-12T09:58:15.990' AS DateTime))
INSERT [dbo].[userProperties] ([propertyID], [companyID], [addressID], [bedroomCount], [bathroomCount], [parkingCount], [garageCount], [storiesCount], [homeType], [yearBuilt], [purchasePrice], [purchaseDate], [schoolDistrict], [nickname], [createUser], [createDate]) VALUES (4, 11, 61, 1, 1, 1, 1, 2, N'New', CAST(1716 AS Numeric(4, 0)), 76393, CAST(N'2022-02-10' AS Date), N'Nothing', N'This', 39, CAST(N'2023-12-14T03:49:02.820' AS DateTime))
INSERT [dbo].[userProperties] ([propertyID], [companyID], [addressID], [bedroomCount], [bathroomCount], [parkingCount], [garageCount], [storiesCount], [homeType], [yearBuilt], [purchasePrice], [purchaseDate], [schoolDistrict], [nickname], [createUser], [createDate]) VALUES (5, 16, 62, 2, 2, 2, 2, 2, N'2', CAST(2222 AS Numeric(4, 0)), 2222, CAST(N'2222-02-02' AS Date), N'222', N'nick', 49, CAST(N'2023-12-14T08:01:10.167' AS DateTime))
INSERT [dbo].[userProperties] ([propertyID], [companyID], [addressID], [bedroomCount], [bathroomCount], [parkingCount], [garageCount], [storiesCount], [homeType], [yearBuilt], [purchasePrice], [purchaseDate], [schoolDistrict], [nickname], [createUser], [createDate]) VALUES (6, 11, 63, 3, 3, 3, 3, 3, N'3', CAST(3333 AS Numeric(4, 0)), 3333, CAST(N'3333-03-03' AS Date), N'333', N'Nick', 39, CAST(N'2023-12-14T08:02:19.903' AS DateTime))
INSERT [dbo].[userProperties] ([propertyID], [companyID], [addressID], [bedroomCount], [bathroomCount], [parkingCount], [garageCount], [storiesCount], [homeType], [yearBuilt], [purchasePrice], [purchaseDate], [schoolDistrict], [nickname], [createUser], [createDate]) VALUES (7, 16, 67, 2, 3, 3, 1, 2, N'Duplex', CAST(2001 AS Numeric(4, 0)), 187000, CAST(N'2015-08-22' AS Date), N'Marshton', N'NewProperty', 49, CAST(N'2023-12-16T03:21:51.843' AS DateTime))
INSERT [dbo].[userProperties] ([propertyID], [companyID], [addressID], [bedroomCount], [bathroomCount], [parkingCount], [garageCount], [storiesCount], [homeType], [yearBuilt], [purchasePrice], [purchaseDate], [schoolDistrict], [nickname], [createUser], [createDate]) VALUES (8, 19, 71, 3, 1.5, 2, 2, 2, N'Single-family', CAST(1957 AS Numeric(4, 0)), 265300, CAST(N'2023-07-06' AS Date), N'Grossburg LSD', N'Prop1', 53, CAST(N'2023-12-17T09:27:57.180' AS DateTime))
INSERT [dbo].[userProperties] ([propertyID], [companyID], [addressID], [bedroomCount], [bathroomCount], [parkingCount], [garageCount], [storiesCount], [homeType], [yearBuilt], [purchasePrice], [purchaseDate], [schoolDistrict], [nickname], [createUser], [createDate]) VALUES (9, 19, 72, 4, 3, 4, 2, 2, N'Duplex', CAST(1974 AS Numeric(4, 0)), 175000, CAST(N'2020-08-01' AS Date), N'Mountville LSD', N'Unit14', 53, CAST(N'2023-12-18T08:00:58.630' AS DateTime))
INSERT [dbo].[userProperties] ([propertyID], [companyID], [addressID], [bedroomCount], [bathroomCount], [parkingCount], [garageCount], [storiesCount], [homeType], [yearBuilt], [purchasePrice], [purchaseDate], [schoolDistrict], [nickname], [createUser], [createDate]) VALUES (10, 21, 74, 34, 4, 100, 3, 1.5, N'industrial', CAST(1980 AS Numeric(4, 0)), 1, CAST(N'2023-12-22' AS Date), N'green', N'work', 57, CAST(N'2023-12-22T19:13:08.343' AS DateTime))
SET IDENTITY_INSERT [dbo].[userProperties] OFF
INSERT [dbo].[userSessions] ([sessionID], [userID], [IPv4_ipAddress], [loginDatetime], [expiredDatetime], [nextDatetime]) VALUES (N'DTSAPBplMZLebK2qw3CbRfzMrNgW_YePSNhDH2VBek3TGOLnkA', 49, N'162.155.182.98', CAST(N'2023-12-28T19:47:08.393' AS DateTime), CAST(N'2024-01-04T19:47:08.393' AS DateTime), CAST(N'2023-12-29T19:58:22.763' AS DateTime))
INSERT [dbo].[userSessions] ([sessionID], [userID], [IPv4_ipAddress], [loginDatetime], [expiredDatetime], [nextDatetime]) VALUES (N'eDAMyZoDcVCSQM4lLmkkoyUzLbgrbYV_bC3M6udTZ-BVr2kdtQ', 51, N'76.94.194.49', CAST(N'2023-12-15T02:36:17.157' AS DateTime), CAST(N'2023-12-22T02:36:17.157' AS DateTime), CAST(N'2023-12-16T02:37:17.450' AS DateTime))
INSERT [dbo].[userSessions] ([sessionID], [userID], [IPv4_ipAddress], [loginDatetime], [expiredDatetime], [nextDatetime]) VALUES (N'eJvFGUH79e3NiaegM3PPWkS-GvSpeAFrSYD3ZHT71T50_9yFEQ', 57, N'162.155.182.98', CAST(N'2023-12-22T19:20:55.387' AS DateTime), CAST(N'2023-12-29T19:20:55.387' AS DateTime), CAST(N'2023-12-23T19:21:00.470' AS DateTime))
INSERT [dbo].[userSessions] ([sessionID], [userID], [IPv4_ipAddress], [loginDatetime], [expiredDatetime], [nextDatetime]) VALUES (N'LqqHBg_v1FzvCnbciyoW9ABhDya_PIBIW3nK2HqX8G8pfjFMyg', 49, N'162.155.182.98', CAST(N'2023-12-28T19:47:08.397' AS DateTime), CAST(N'2024-01-04T19:47:08.397' AS DateTime), CAST(N'2023-12-29T19:47:08.397' AS DateTime))
INSERT [dbo].[userSessions] ([sessionID], [userID], [IPv4_ipAddress], [loginDatetime], [expiredDatetime], [nextDatetime]) VALUES (N'-WWiF-27yiYd9u4YKD6FF4zVJTqe2d9VvTmiZRhbQRvyNYcKIw', 58, N'162.155.182.98', CAST(N'2023-12-22T19:21:23.663' AS DateTime), CAST(N'2023-12-29T19:21:23.663' AS DateTime), CAST(N'2023-12-23T19:21:23.663' AS DateTime))
INSERT [dbo].[userSessions] ([sessionID], [userID], [IPv4_ipAddress], [loginDatetime], [expiredDatetime], [nextDatetime]) VALUES (N'X9BX_WUq9Gqd5qgelXFX6QD4G56_fNL3B8N9jon4jaTPHlTFmg', 53, N'24.101.69.174', CAST(N'2023-12-21T04:28:26.157' AS DateTime), CAST(N'2023-12-28T04:28:26.157' AS DateTime), CAST(N'2023-12-22T04:32:23.030' AS DateTime))
ALTER TABLE [dbo].[appFeeTypes] ADD  CONSTRAINT [DEFAULT_appFeeTypes_sortOrder]  DEFAULT ((99)) FOR [displayOrder]
GO
ALTER TABLE [dbo].[appPaymentStatus] ADD  CONSTRAINT [DEFAULT_appPaymentStatus_isCompleted]  DEFAULT ((0)) FOR [isCompleted]
GO
ALTER TABLE [dbo].[appPeriods] ADD  CONSTRAINT [DEFAULT_appPeriods_isRentPeriod]  DEFAULT ((0)) FOR [isLeasePeriod]
GO
ALTER TABLE [dbo].[userAccounts] ADD  CONSTRAINT [DEFAULT_userAccounts_emailVerified]  DEFAULT ((0)) FOR [emailVerified]
GO
ALTER TABLE [dbo].[userAccounts] ADD  CONSTRAINT [DEFAULT_userAccounts_attemptsSinceLastLogin]  DEFAULT ((0)) FOR [attemptsSinceLastLogin]
GO
ALTER TABLE [dbo].[userApplications] ADD  CONSTRAINT [DEFAULT_userApplications_applicationStatus]  DEFAULT ((0)) FOR [applicationStatus]
GO
ALTER TABLE [dbo].[userDependants] ADD  CONSTRAINT [DEFAULT_userDependants_order]  DEFAULT ((1)) FOR [order]
GO
ALTER TABLE [dbo].[userLeases] ADD  CONSTRAINT [DEFAULT_userLeases_lastPeriodRemainingBalance]  DEFAULT ((0)) FOR [lastPeriodRemainingBalance]
GO
ALTER TABLE [dbo].[userPayments] ADD  CONSTRAINT [DEFAULT_userPayments_amountReceived]  DEFAULT ((0)) FOR [amountReceived]
GO
ALTER TABLE [dbo].[userReferences] ADD  CONSTRAINT [DEFAULT_userReferences_sortOrder]  DEFAULT ((1)) FOR [sortOrder]
GO
ALTER TABLE [dbo].[userReferences] ADD  CONSTRAINT [DEFAULT_userReferences_landlordReviewed]  DEFAULT ((0)) FOR [landlordReviewed]
GO
ALTER TABLE [dbo].[appFeeTypes]  WITH CHECK ADD  CONSTRAINT [FK_defaultOccurrence] FOREIGN KEY([defaultOccurrence])
REFERENCES [dbo].[appOccurrences] ([occurrenceID])
GO
ALTER TABLE [dbo].[appFeeTypes] CHECK CONSTRAINT [FK_defaultOccurrence]
GO
ALTER TABLE [dbo].[appOccurrences]  WITH CHECK ADD  CONSTRAINT [FK_perPeriod] FOREIGN KEY([perPeriod])
REFERENCES [dbo].[appPeriods] ([periodID])
GO
ALTER TABLE [dbo].[appOccurrences] CHECK CONSTRAINT [FK_perPeriod]
GO
ALTER TABLE [dbo].[userAccounts]  WITH CHECK ADD  CONSTRAINT [FK_userAccounts_appAccountTypes] FOREIGN KEY([accountTypeID])
REFERENCES [dbo].[appAccountTypes] ([accountTypeID])
ON UPDATE CASCADE
GO
ALTER TABLE [dbo].[userAccounts] CHECK CONSTRAINT [FK_userAccounts_appAccountTypes]
GO
ALTER TABLE [dbo].[userAccounts]  WITH CHECK ADD  CONSTRAINT [FK_userAccounts_userPeople] FOREIGN KEY([userID])
REFERENCES [dbo].[userPeople] ([personID])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[userAccounts] CHECK CONSTRAINT [FK_userAccounts_userPeople]
GO
ALTER TABLE [dbo].[userApplications]  WITH CHECK ADD  CONSTRAINT [FK_userApplications_userAddresses-currentAddress] FOREIGN KEY([currentAddressID])
REFERENCES [dbo].[userAddresses] ([addressID])
GO
ALTER TABLE [dbo].[userApplications] CHECK CONSTRAINT [FK_userApplications_userAddresses-currentAddress]
GO
ALTER TABLE [dbo].[userApplications]  WITH CHECK ADD  CONSTRAINT [FK_userApplications_userApplications-previousAddress] FOREIGN KEY([previousAddressID])
REFERENCES [dbo].[userAddresses] ([addressID])
GO
ALTER TABLE [dbo].[userApplications] CHECK CONSTRAINT [FK_userApplications_userApplications-previousAddress]
GO
ALTER TABLE [dbo].[userApplications]  WITH CHECK ADD  CONSTRAINT [FK_userApplications_userLease] FOREIGN KEY([leaseID])
REFERENCES [dbo].[userLeases] ([leaseID])
GO
ALTER TABLE [dbo].[userApplications] CHECK CONSTRAINT [FK_userApplications_userLease]
GO
ALTER TABLE [dbo].[userApplications]  WITH CHECK ADD  CONSTRAINT [FK_userApplications_userPeople-applicant] FOREIGN KEY([applicantID])
REFERENCES [dbo].[userPeople] ([personID])
GO
ALTER TABLE [dbo].[userApplications] CHECK CONSTRAINT [FK_userApplications_userPeople-applicant]
GO
ALTER TABLE [dbo].[userApplications]  WITH CHECK ADD  CONSTRAINT [FK_userApplications_userPeople-coapplicant] FOREIGN KEY([coApplicantID])
REFERENCES [dbo].[userPeople] ([personID])
GO
ALTER TABLE [dbo].[userApplications] CHECK CONSTRAINT [FK_userApplications_userPeople-coapplicant]
GO
ALTER TABLE [dbo].[userApplications]  WITH CHECK ADD  CONSTRAINT [FK_userApplications_userPeople-currentOwner] FOREIGN KEY([currentOwnerID])
REFERENCES [dbo].[userPeople] ([personID])
GO
ALTER TABLE [dbo].[userApplications] CHECK CONSTRAINT [FK_userApplications_userPeople-currentOwner]
GO
ALTER TABLE [dbo].[userApplications]  WITH CHECK ADD  CONSTRAINT [FK_userApplications_userPeople-previousOwner] FOREIGN KEY([previousOwnerID])
REFERENCES [dbo].[userPeople] ([personID])
GO
ALTER TABLE [dbo].[userApplications] CHECK CONSTRAINT [FK_userApplications_userPeople-previousOwner]
GO
ALTER TABLE [dbo].[userCompanies]  WITH CHECK ADD  CONSTRAINT [FK_billingAddress] FOREIGN KEY([billingAddress])
REFERENCES [dbo].[userAddresses] ([addressID])
GO
ALTER TABLE [dbo].[userCompanies] CHECK CONSTRAINT [FK_billingAddress]
GO
ALTER TABLE [dbo].[userCompanies]  WITH CHECK ADD  CONSTRAINT [FK_mailingAddress] FOREIGN KEY([mailingAddress])
REFERENCES [dbo].[userAddresses] ([addressID])
GO
ALTER TABLE [dbo].[userCompanies] CHECK CONSTRAINT [FK_mailingAddress]
GO
ALTER TABLE [dbo].[userCompanies]  WITH CHECK ADD  CONSTRAINT [FK_userCompanies_userAccounts] FOREIGN KEY([createdBy])
REFERENCES [dbo].[userAccounts] ([userID])
ON UPDATE CASCADE
GO
ALTER TABLE [dbo].[userCompanies] CHECK CONSTRAINT [FK_userCompanies_userAccounts]
GO
ALTER TABLE [dbo].[userCompanyRoles]  WITH CHECK ADD  CONSTRAINT [FK_userCompanyPeople_appAccountTypes] FOREIGN KEY([roleTypeID])
REFERENCES [dbo].[appAccountTypes] ([accountTypeID])
GO
ALTER TABLE [dbo].[userCompanyRoles] CHECK CONSTRAINT [FK_userCompanyPeople_appAccountTypes]
GO
ALTER TABLE [dbo].[userCompanyRoles]  WITH CHECK ADD  CONSTRAINT [FK_userCompanyPeople_userAccounts] FOREIGN KEY([userID])
REFERENCES [dbo].[userAccounts] ([userID])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[userCompanyRoles] CHECK CONSTRAINT [FK_userCompanyPeople_userAccounts]
GO
ALTER TABLE [dbo].[userCompanyRoles]  WITH CHECK ADD  CONSTRAINT [FK_userCompanyPeople_userAccounts_linked] FOREIGN KEY([assignedUser])
REFERENCES [dbo].[userAccounts] ([userID])
GO
ALTER TABLE [dbo].[userCompanyRoles] CHECK CONSTRAINT [FK_userCompanyPeople_userAccounts_linked]
GO
ALTER TABLE [dbo].[userCompanyRoles]  WITH CHECK ADD  CONSTRAINT [FK_userCompanyPeople_userAccounts_unlinked] FOREIGN KEY([endedUser])
REFERENCES [dbo].[userAccounts] ([userID])
GO
ALTER TABLE [dbo].[userCompanyRoles] CHECK CONSTRAINT [FK_userCompanyPeople_userAccounts_unlinked]
GO
ALTER TABLE [dbo].[userCompanyRoles]  WITH CHECK ADD  CONSTRAINT [FK_userCompanyPeople_userCompanies] FOREIGN KEY([companyID])
REFERENCES [dbo].[userCompanies] ([companyID])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[userCompanyRoles] CHECK CONSTRAINT [FK_userCompanyPeople_userCompanies]
GO
ALTER TABLE [dbo].[userDependants]  WITH CHECK ADD  CONSTRAINT [FK_userDependants_userApplications] FOREIGN KEY([applicationID])
REFERENCES [dbo].[userApplications] ([applicationID])
ON UPDATE CASCADE
ON DELETE SET NULL
GO
ALTER TABLE [dbo].[userDependants] CHECK CONSTRAINT [FK_userDependants_userApplications]
GO
ALTER TABLE [dbo].[userDependants]  WITH CHECK ADD  CONSTRAINT [FK_userDependants_userLease] FOREIGN KEY([leaseID])
REFERENCES [dbo].[userLeases] ([leaseID])
ON UPDATE CASCADE
ON DELETE SET NULL
GO
ALTER TABLE [dbo].[userDependants] CHECK CONSTRAINT [FK_userDependants_userLease]
GO
ALTER TABLE [dbo].[userEmploymentHistory]  WITH CHECK ADD  CONSTRAINT [FK_applicantID] FOREIGN KEY([applicantID])
REFERENCES [dbo].[userPeople] ([personID])
GO
ALTER TABLE [dbo].[userEmploymentHistory] CHECK CONSTRAINT [FK_applicantID]
GO
ALTER TABLE [dbo].[userEmploymentHistory]  WITH CHECK ADD  CONSTRAINT [FK_supervisorID] FOREIGN KEY([supervisorID])
REFERENCES [dbo].[userPeople] ([personID])
GO
ALTER TABLE [dbo].[userEmploymentHistory] CHECK CONSTRAINT [FK_supervisorID]
GO
ALTER TABLE [dbo].[userEmploymentHistory]  WITH CHECK ADD  CONSTRAINT [FK_userEmploymentHistory_appPeriods] FOREIGN KEY([salaryPeriod])
REFERENCES [dbo].[appPeriods] ([periodID])
GO
ALTER TABLE [dbo].[userEmploymentHistory] CHECK CONSTRAINT [FK_userEmploymentHistory_appPeriods]
GO
ALTER TABLE [dbo].[userEmploymentHistory]  WITH CHECK ADD  CONSTRAINT [FK_userEmploymentHistory_userApplications] FOREIGN KEY([applicationID])
REFERENCES [dbo].[userApplications] ([applicationID])
GO
ALTER TABLE [dbo].[userEmploymentHistory] CHECK CONSTRAINT [FK_userEmploymentHistory_userApplications]
GO
ALTER TABLE [dbo].[userLeaseFees]  WITH CHECK ADD  CONSTRAINT [FK_userLeaseFees_appFeeTypes] FOREIGN KEY([feeID])
REFERENCES [dbo].[appFeeTypes] ([feeID])
ON UPDATE CASCADE
GO
ALTER TABLE [dbo].[userLeaseFees] CHECK CONSTRAINT [FK_userLeaseFees_appFeeTypes]
GO
ALTER TABLE [dbo].[userLeaseFees]  WITH CHECK ADD  CONSTRAINT [FK_userLeaseFees_appOccurrences] FOREIGN KEY([occurrence])
REFERENCES [dbo].[appOccurrences] ([occurrenceID])
ON UPDATE CASCADE
GO
ALTER TABLE [dbo].[userLeaseFees] CHECK CONSTRAINT [FK_userLeaseFees_appOccurrences]
GO
ALTER TABLE [dbo].[userLeaseFees]  WITH CHECK ADD  CONSTRAINT [FK_userLeaseFees_appPeriods] FOREIGN KEY([startAfterPeriod])
REFERENCES [dbo].[appPeriods] ([periodID])
ON UPDATE CASCADE
GO
ALTER TABLE [dbo].[userLeaseFees] CHECK CONSTRAINT [FK_userLeaseFees_appPeriods]
GO
ALTER TABLE [dbo].[userLeaseFees]  WITH CHECK ADD  CONSTRAINT [FK_userLeaseFees_userAccounts] FOREIGN KEY([createUser])
REFERENCES [dbo].[userAccounts] ([userID])
ON UPDATE CASCADE
GO
ALTER TABLE [dbo].[userLeaseFees] CHECK CONSTRAINT [FK_userLeaseFees_userAccounts]
GO
ALTER TABLE [dbo].[userLeaseFees]  WITH CHECK ADD  CONSTRAINT [FK_userLeaseFees_userLease] FOREIGN KEY([leaseID])
REFERENCES [dbo].[userLeases] ([leaseID])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[userLeaseFees] CHECK CONSTRAINT [FK_userLeaseFees_userLease]
GO
ALTER TABLE [dbo].[userLeasePeople]  WITH CHECK ADD  CONSTRAINT [FK_userLeasePeople_userLease] FOREIGN KEY([leaseID])
REFERENCES [dbo].[userLeases] ([leaseID])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[userLeasePeople] CHECK CONSTRAINT [FK_userLeasePeople_userLease]
GO
ALTER TABLE [dbo].[userLeasePeople]  WITH CHECK ADD  CONSTRAINT [FK_userLeasePeople_userPeople] FOREIGN KEY([personID])
REFERENCES [dbo].[userPeople] ([personID])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[userLeasePeople] CHECK CONSTRAINT [FK_userLeasePeople_userPeople]
GO
ALTER TABLE [dbo].[userLeases]  WITH CHECK ADD  CONSTRAINT [FK_userLease_appOccurrences] FOREIGN KEY([leasePeriod])
REFERENCES [dbo].[appPeriods] ([periodID])
GO
ALTER TABLE [dbo].[userLeases] CHECK CONSTRAINT [FK_userLease_appOccurrences]
GO
ALTER TABLE [dbo].[userLeases]  WITH CHECK ADD  CONSTRAINT [FK_userLease_appOccurrences_leaseSuccession] FOREIGN KEY([leaseSuccessionPeriod])
REFERENCES [dbo].[appPeriods] ([periodID])
GO
ALTER TABLE [dbo].[userLeases] CHECK CONSTRAINT [FK_userLease_appOccurrences_leaseSuccession]
GO
ALTER TABLE [dbo].[userLeases]  WITH CHECK ADD  CONSTRAINT [FK_userLease_userAccounts] FOREIGN KEY([createUser])
REFERENCES [dbo].[userAccounts] ([userID])
GO
ALTER TABLE [dbo].[userLeases] CHECK CONSTRAINT [FK_userLease_userAccounts]
GO
ALTER TABLE [dbo].[userLeases]  WITH CHECK ADD  CONSTRAINT [FK_userLease_userProperties] FOREIGN KEY([propertyID])
REFERENCES [dbo].[userProperties] ([propertyID])
GO
ALTER TABLE [dbo].[userLeases] CHECK CONSTRAINT [FK_userLease_userProperties]
GO
ALTER TABLE [dbo].[userPaymentItems]  WITH CHECK ADD  CONSTRAINT [FK_userPaymentItems_userAccounts] FOREIGN KEY([createUser])
REFERENCES [dbo].[userAccounts] ([userID])
ON DELETE SET NULL
GO
ALTER TABLE [dbo].[userPaymentItems] CHECK CONSTRAINT [FK_userPaymentItems_userAccounts]
GO
ALTER TABLE [dbo].[userPaymentItems]  WITH CHECK ADD  CONSTRAINT [FK_userPaymentItems_userLeaseFees] FOREIGN KEY([leaseFeeID])
REFERENCES [dbo].[userLeaseFees] ([leaseFeeID])
GO
ALTER TABLE [dbo].[userPaymentItems] CHECK CONSTRAINT [FK_userPaymentItems_userLeaseFees]
GO
ALTER TABLE [dbo].[userPaymentItems]  WITH CHECK ADD  CONSTRAINT [FK_userPaymentItems_userPayments] FOREIGN KEY([paymentID])
REFERENCES [dbo].[userPayments] ([paymentID])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[userPaymentItems] CHECK CONSTRAINT [FK_userPaymentItems_userPayments]
GO
ALTER TABLE [dbo].[userPayments]  WITH CHECK ADD  CONSTRAINT [FK_userPayments_appPaymentMethods] FOREIGN KEY([paymentMethod])
REFERENCES [dbo].[appPaymentMethods] ([methodID])
ON UPDATE CASCADE
GO
ALTER TABLE [dbo].[userPayments] CHECK CONSTRAINT [FK_userPayments_appPaymentMethods]
GO
ALTER TABLE [dbo].[userPayments]  WITH CHECK ADD  CONSTRAINT [FK_userPayments_appPaymentStatus] FOREIGN KEY([paymentStatus])
REFERENCES [dbo].[appPaymentStatus] ([statusID])
ON UPDATE CASCADE
GO
ALTER TABLE [dbo].[userPayments] CHECK CONSTRAINT [FK_userPayments_appPaymentStatus]
GO
ALTER TABLE [dbo].[userPayments]  WITH CHECK ADD  CONSTRAINT [FK_userPayments_userAccounts] FOREIGN KEY([createUser])
REFERENCES [dbo].[userAccounts] ([userID])
ON UPDATE CASCADE
GO
ALTER TABLE [dbo].[userPayments] CHECK CONSTRAINT [FK_userPayments_userAccounts]
GO
ALTER TABLE [dbo].[userPayments]  WITH CHECK ADD  CONSTRAINT [FK_userPayments_userLeases] FOREIGN KEY([leaseID])
REFERENCES [dbo].[userLeases] ([leaseID])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[userPayments] CHECK CONSTRAINT [FK_userPayments_userLeases]
GO
ALTER TABLE [dbo].[userPeople]  WITH CHECK ADD  CONSTRAINT [FK_addressID] FOREIGN KEY([addressID])
REFERENCES [dbo].[userAddresses] ([addressID])
ON UPDATE CASCADE
GO
ALTER TABLE [dbo].[userPeople] CHECK CONSTRAINT [FK_addressID]
GO
ALTER TABLE [dbo].[userPersonDetails]  WITH CHECK ADD  CONSTRAINT [FK_detailID] FOREIGN KEY([detailID])
REFERENCES [dbo].[userDetailOptions] ([detailID])
GO
ALTER TABLE [dbo].[userPersonDetails] CHECK CONSTRAINT [FK_detailID]
GO
ALTER TABLE [dbo].[userPersonDetails]  WITH CHECK ADD  CONSTRAINT [FK_personID] FOREIGN KEY([personID])
REFERENCES [dbo].[userPeople] ([personID])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[userPersonDetails] CHECK CONSTRAINT [FK_personID]
GO
ALTER TABLE [dbo].[userPersonDetails]  WITH CHECK ADD  CONSTRAINT [FK_setPersonID] FOREIGN KEY([setPersonID])
REFERENCES [dbo].[userPeople] ([personID])
GO
ALTER TABLE [dbo].[userPersonDetails] CHECK CONSTRAINT [FK_setPersonID]
GO
ALTER TABLE [dbo].[userProperties]  WITH CHECK ADD  CONSTRAINT [FK_userProperties_userAccounts] FOREIGN KEY([createUser])
REFERENCES [dbo].[userAccounts] ([userID])
GO
ALTER TABLE [dbo].[userProperties] CHECK CONSTRAINT [FK_userProperties_userAccounts]
GO
ALTER TABLE [dbo].[userProperties]  WITH CHECK ADD  CONSTRAINT [FK_userProperties_userAddresses] FOREIGN KEY([addressID])
REFERENCES [dbo].[userAddresses] ([addressID])
GO
ALTER TABLE [dbo].[userProperties] CHECK CONSTRAINT [FK_userProperties_userAddresses]
GO
ALTER TABLE [dbo].[userProperties]  WITH CHECK ADD  CONSTRAINT [FK_userProperties_userCompanies] FOREIGN KEY([companyID])
REFERENCES [dbo].[userCompanies] ([companyID])
GO
ALTER TABLE [dbo].[userProperties] CHECK CONSTRAINT [FK_userProperties_userCompanies]
GO
ALTER TABLE [dbo].[userReferences]  WITH CHECK ADD  CONSTRAINT [FK_references_applicationID] FOREIGN KEY([applicationID])
REFERENCES [dbo].[userApplications] ([applicationID])
GO
ALTER TABLE [dbo].[userReferences] CHECK CONSTRAINT [FK_references_applicationID]
GO
ALTER TABLE [dbo].[userReferences]  WITH CHECK ADD  CONSTRAINT [FK_references_personID] FOREIGN KEY([personID])
REFERENCES [dbo].[userPeople] ([personID])
GO
ALTER TABLE [dbo].[userReferences] CHECK CONSTRAINT [FK_references_personID]
GO
ALTER TABLE [dbo].[userSessions]  WITH CHECK ADD  CONSTRAINT [FK_userSessions_userAccounts] FOREIGN KEY([userID])
REFERENCES [dbo].[userAccounts] ([userID])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[userSessions] CHECK CONSTRAINT [FK_userSessions_userAccounts]
GO
ALTER TABLE [dbo].[userVehicles]  WITH CHECK ADD  CONSTRAINT [FK_applicationID] FOREIGN KEY([applicationID])
REFERENCES [dbo].[userApplications] ([applicationID])
GO
ALTER TABLE [dbo].[userVehicles] CHECK CONSTRAINT [FK_applicationID]
GO
USE [master]
GO
ALTER DATABASE [userData] SET  READ_WRITE 
GO
