-- Logic-corrected version of the uploaded schema
-- Main changes:
-- 1) Added NOT NULL and CHECK constraints for key business fields.
-- 2) Replaced PromotionCampaigns.ValidPeriod with StartDate and EndDate.
-- 3) Removed ambiguous DigitalOrders.OrderChannel; channel is represented by ChannelId -> DigitalChannels.
-- 4) Renamed delivery fee fields to distinguish actual order fee from partner standard fee.
-- 5) Added MemberId to OrderCampaigns so campaign usage can be tied to both the order and the member's received campaign.
-- 6) Split RecipeMaterials.Dosage into numeric amount and unit.
-- 7) Added recipe effective dates to support recipe versioning.

PRAGMA foreign_keys = ON;

CREATE TABLE Customers (
    CustomerId INT PRIMARY KEY,
    Segment VARCHAR(50) NOT NULL,
    City VARCHAR(50) NOT NULL,
    AgeBand VARCHAR(20),
    CHECK (AgeBand IS NULL OR AgeBand IN ('Under 18', '18-24', '25-34', '35-44', '45-54', '55+'))
);

CREATE TABLE MembershipAccounts (
    MemberId INT PRIMARY KEY,
    CustomerId INT NOT NULL UNIQUE,
    PointsBalance INT NOT NULL DEFAULT 0,
    CouponValue DECIMAL(10,2) NOT NULL DEFAULT 0,
    MemberTier VARCHAR(20) NOT NULL DEFAULT 'Regular',
    ActivityStatus VARCHAR(20) NOT NULL DEFAULT 'Active',
    FOREIGN KEY (CustomerId) REFERENCES Customers(CustomerId),
    CHECK (PointsBalance >= 0),
    CHECK (CouponValue >= 0),
    CHECK (MemberTier IN ('Regular', 'Silver', 'Gold', 'Platinum', 'Black')),
    CHECK (ActivityStatus IN ('Active', 'Inactive', 'Suspended', 'Closed'))
);

CREATE TABLE DigitalChannels (
    ChannelId INT PRIMARY KEY,
    ChannelType VARCHAR(50) NOT NULL,
    AccessDevice VARCHAR(50),
    AppVersion VARCHAR(20),
    CHECK (ChannelType IN ('App', 'Mini Program', 'Website', 'POS', 'Third-party Platform'))
);

CREATE TABLE PromotionCampaigns (
    CampaignId INT PRIMARY KEY,
    CampaignType VARCHAR(50) NOT NULL,
    TargetSegment VARCHAR(50),
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    SubsidyAmount DECIMAL(10,2) NOT NULL DEFAULT 0,
    CHECK (StartDate <= EndDate),
    CHECK (SubsidyAmount >= 0)
);

CREATE TABLE MemberCampaigns (
    MemberId INT NOT NULL,
    CampaignId INT NOT NULL,
    ReceivedDate DATE NOT NULL,
    UsedStatus VARCHAR(20) NOT NULL DEFAULT 'Received',
    PRIMARY KEY (MemberId, CampaignId),
    FOREIGN KEY (MemberId) REFERENCES MembershipAccounts(MemberId),
    FOREIGN KEY (CampaignId) REFERENCES PromotionCampaigns(CampaignId),
    CHECK (UsedStatus IN ('Received', 'Used', 'Expired', 'Cancelled'))
);

CREATE TABLE DigitalOrders (
    OrderId INT PRIMARY KEY,
    MemberId INT NOT NULL,
    ChannelId INT NOT NULL,
    PaymentMethod VARCHAR(50) NOT NULL,
    QueueStatus VARCHAR(20) NOT NULL DEFAULT 'Pending',
    GrossOrderAmount DECIMAL(10,2) NOT NULL,
    CampaignDiscountAmount DECIMAL(10,2) NOT NULL DEFAULT 0,
    ItemDiscountAmount DECIMAL(10,2) NOT NULL DEFAULT 0,
    ActualDeliveryFee DECIMAL(10,2) NOT NULL DEFAULT 0,
    NetPayableAmount DECIMAL(10,2) NOT NULL,
    OrderDate DATE NOT NULL,
    OrderTime TIME NOT NULL,
    UNIQUE (OrderId, MemberId),
    FOREIGN KEY (MemberId) REFERENCES MembershipAccounts(MemberId),
    FOREIGN KEY (ChannelId) REFERENCES DigitalChannels(ChannelId),
    CHECK (PaymentMethod IN ('Cash', 'Card', 'Wallet', 'Bank Transfer', 'Third-party Pay')),
    CHECK (QueueStatus IN ('Pending', 'Queued', 'Preparing', 'Ready', 'Completed', 'Cancelled')),
    CHECK (GrossOrderAmount >= 0),
    CHECK (CampaignDiscountAmount >= 0),
    CHECK (ItemDiscountAmount >= 0),
    CHECK (ActualDeliveryFee >= 0),
    CHECK (NetPayableAmount >= 0),
    CHECK (NetPayableAmount = GrossOrderAmount - CampaignDiscountAmount - ItemDiscountAmount + ActualDeliveryFee)
);

CREATE TABLE OrderCampaigns (
    OrderId INT NOT NULL,
    MemberId INT NOT NULL,
    CampaignId INT NOT NULL,
    AppliedAmount DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (OrderId, CampaignId),
    FOREIGN KEY (OrderId, MemberId) REFERENCES DigitalOrders(OrderId, MemberId),
    FOREIGN KEY (MemberId, CampaignId) REFERENCES MemberCampaigns(MemberId, CampaignId),
    FOREIGN KEY (CampaignId) REFERENCES PromotionCampaigns(CampaignId),
    CHECK (AppliedAmount >= 0)
);

CREATE TABLE Products (
    ProductId INT PRIMARY KEY,
    ProductName VARCHAR(100) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    Season VARCHAR(50),
    GrossMargin DECIMAL(5,2),
    CurrentStandardCost DECIMAL(10,2),
    CHECK (GrossMargin IS NULL OR GrossMargin BETWEEN 0 AND 100),
    CHECK (CurrentStandardCost IS NULL OR CurrentStandardCost >= 0)
);

CREATE TABLE OrderItems (
    OrderId INT NOT NULL,
    ItemNr INT NOT NULL,
    ProductId INT NOT NULL,
    Quantity INT NOT NULL,
    Customization VARCHAR(100),
    LineDiscountAmount DECIMAL(10,2) NOT NULL DEFAULT 0,
    UnitItemPrice DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (OrderId, ItemNr),
    FOREIGN KEY (OrderId) REFERENCES DigitalOrders(OrderId),
    FOREIGN KEY (ProductId) REFERENCES Products(ProductId),
    CHECK (ItemNr > 0),
    CHECK (Quantity > 0),
    CHECK (LineDiscountAmount >= 0),
    CHECK (UnitItemPrice >= 0),
    CHECK (LineDiscountAmount <= Quantity * UnitItemPrice)
);

CREATE TABLE DeliveryPartners (
    PartnerId INT PRIMARY KEY,
    PartnerName VARCHAR(100) NOT NULL,
    PartnerType VARCHAR(50) NOT NULL,
    ServiceArea VARCHAR(100),
    StandardDeliveryFee DECIMAL(10,2) NOT NULL DEFAULT 0,
    ComplaintRate DECIMAL(5,2),
    CHECK (StandardDeliveryFee >= 0),
    CHECK (ComplaintRate IS NULL OR ComplaintRate BETWEEN 0 AND 100)
);

CREATE TABLE Stores (
    StoreId INT PRIMARY KEY,
    StoreName VARCHAR(100) NOT NULL,
    OwnershipType VARCHAR(50) NOT NULL,
    CityTier VARCHAR(20),
    LocationType VARCHAR(50),
    Revenue DECIMAL(15,2) NOT NULL DEFAULT 0,
    LaborCost DECIMAL(15,2) NOT NULL DEFAULT 0,
    CHECK (OwnershipType IN ('Self-operated', 'Franchise', 'Joint Venture')),
    CHECK (Revenue >= 0),
    CHECK (LaborCost >= 0)
);

CREATE TABLE FulfilmentTasks (
    TaskId INT PRIMARY KEY,
    OrderId INT NOT NULL,
    StoreId INT NOT NULL,
    PartnerId INT,
    TaskType VARCHAR(50) NOT NULL,
    PrepTime INT,
    WaitingTime INT,
    CompletionRate DECIMAL(5,2),
    Status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (OrderId) REFERENCES DigitalOrders(OrderId),
    FOREIGN KEY (StoreId) REFERENCES Stores(StoreId),
    FOREIGN KEY (PartnerId) REFERENCES DeliveryPartners(PartnerId),
    CHECK (TaskType IN ('Pickup', 'Delivery', 'Dine-in', 'Takeaway')),
    CHECK (PrepTime IS NULL OR PrepTime >= 0),
    CHECK (WaitingTime IS NULL OR WaitingTime >= 0),
    CHECK (CompletionRate IS NULL OR CompletionRate BETWEEN 0 AND 100),
    CHECK (Status IN ('Pending', 'In Progress', 'Completed', 'Cancelled', 'Failed'))
);

CREATE TABLE StoreStaff (
    StaffId INT PRIMARY KEY,
    StoreId INT NOT NULL,
    StaffName VARCHAR(100) NOT NULL,
    StaffRole VARCHAR(50) NOT NULL,
    TrainingStatus VARCHAR(50) NOT NULL DEFAULT 'Not Started',
    WorkingHours INT NOT NULL DEFAULT 0,
    LaborCost DECIMAL(10,2) NOT NULL DEFAULT 0,
    Productivity DECIMAL(5,2),
    FOREIGN KEY (StoreId) REFERENCES Stores(StoreId),
    CHECK (TrainingStatus IN ('Not Started', 'In Progress', 'Certified', 'Expired')),
    CHECK (WorkingHours >= 0),
    CHECK (LaborCost >= 0),
    CHECK (Productivity IS NULL OR Productivity >= 0)
);

CREATE TABLE Suppliers (
    SupplierId INT PRIMARY KEY,
    SupplierName VARCHAR(100) NOT NULL,
    SupplierType VARCHAR(50),
    LeadTime INT,
    CHECK (LeadTime IS NULL OR LeadTime >= 0)
);

CREATE TABLE RawMaterials (
    MaterialId INT PRIMARY KEY,
    SupplierId INT NOT NULL,
    MaterialName VARCHAR(100) NOT NULL,
    MaterialType VARCHAR(50) NOT NULL,
    Origin VARCHAR(50),
    BatchStatus VARCHAR(20) NOT NULL DEFAULT 'Available',
    InventoryValue DECIMAL(15,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (SupplierId) REFERENCES Suppliers(SupplierId),
    CHECK (BatchStatus IN ('Available', 'Quarantined', 'Rejected', 'Expired', 'Consumed')),
    CHECK (InventoryValue >= 0)
);

CREATE TABLE StoreMaterials (
    StoreId INT NOT NULL,
    MaterialId INT NOT NULL,
    StockLevel INT NOT NULL DEFAULT 0,
    StockoutRate DECIMAL(5,2),
    PRIMARY KEY (StoreId, MaterialId),
    FOREIGN KEY (StoreId) REFERENCES Stores(StoreId),
    FOREIGN KEY (MaterialId) REFERENCES RawMaterials(MaterialId),
    CHECK (StockLevel >= 0),
    CHECK (StockoutRate IS NULL OR StockoutRate BETWEEN 0 AND 100)
);

CREATE TABLE RecipeStandards (
    RecipeId INT PRIMARY KEY,
    ProductId INT NOT NULL,
    RecipeVersion VARCHAR(20) NOT NULL,
    SopStatus VARCHAR(20) NOT NULL DEFAULT 'Draft',
    RecipeStandardCost DECIMAL(10,2) NOT NULL DEFAULT 0,
    DefectRate DECIMAL(5,2),
    EffectiveFrom DATE NOT NULL,
    EffectiveTo DATE,
    FOREIGN KEY (ProductId) REFERENCES Products(ProductId),
    UNIQUE (ProductId, RecipeVersion),
    CHECK (SopStatus IN ('Draft', 'Active', 'Inactive', 'Archived')),
    CHECK (RecipeStandardCost >= 0),
    CHECK (DefectRate IS NULL OR DefectRate BETWEEN 0 AND 100),
    CHECK (EffectiveTo IS NULL OR EffectiveFrom <= EffectiveTo)
);

CREATE TABLE RecipeMaterials (
    RecipeId INT NOT NULL,
    MaterialId INT NOT NULL,
    DosageAmount DECIMAL(10,3) NOT NULL,
    DosageUnit VARCHAR(20) NOT NULL,
    PRIMARY KEY (RecipeId, MaterialId),
    FOREIGN KEY (RecipeId) REFERENCES RecipeStandards(RecipeId),
    FOREIGN KEY (MaterialId) REFERENCES RawMaterials(MaterialId),
    CHECK (DosageAmount > 0)
);

-- Business consistency triggers.
-- These constraints involve multiple tables, so they cannot be expressed with simple CHECK constraints.

CREATE TRIGGER trg_order_campaign_before_insert
BEFORE INSERT ON OrderCampaigns
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NOT EXISTS (
            SELECT 1
            FROM DigitalOrders o
            JOIN PromotionCampaigns c ON c.CampaignId = NEW.CampaignId
            WHERE o.OrderId = NEW.OrderId
              AND o.MemberId = NEW.MemberId
              AND o.OrderDate BETWEEN c.StartDate AND c.EndDate
        )
        THEN RAISE(ABORT, 'Campaign is not valid for the order date or member')
    END;

    SELECT CASE
        WHEN NEW.AppliedAmount > (
            SELECT SubsidyAmount
            FROM PromotionCampaigns
            WHERE CampaignId = NEW.CampaignId
        )
        THEN RAISE(ABORT, 'Applied campaign amount exceeds campaign subsidy amount')
    END;

    SELECT CASE
        WHEN NEW.AppliedAmount > (
            SELECT GrossOrderAmount
            FROM DigitalOrders
            WHERE OrderId = NEW.OrderId
        )
        THEN RAISE(ABORT, 'Applied campaign amount exceeds gross order amount')
    END;
END;

CREATE TRIGGER trg_order_campaign_before_update
BEFORE UPDATE ON OrderCampaigns
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NOT EXISTS (
            SELECT 1
            FROM DigitalOrders o
            JOIN PromotionCampaigns c ON c.CampaignId = NEW.CampaignId
            WHERE o.OrderId = NEW.OrderId
              AND o.MemberId = NEW.MemberId
              AND o.OrderDate BETWEEN c.StartDate AND c.EndDate
        )
        THEN RAISE(ABORT, 'Campaign is not valid for the order date or member')
    END;

    SELECT CASE
        WHEN NEW.AppliedAmount > (
            SELECT SubsidyAmount
            FROM PromotionCampaigns
            WHERE CampaignId = NEW.CampaignId
        )
        THEN RAISE(ABORT, 'Applied campaign amount exceeds campaign subsidy amount')
    END;

    SELECT CASE
        WHEN NEW.AppliedAmount > (
            SELECT GrossOrderAmount
            FROM DigitalOrders
            WHERE OrderId = NEW.OrderId
        )
        THEN RAISE(ABORT, 'Applied campaign amount exceeds gross order amount')
    END;
END;
