CREATE TABLE Users (
    UserId SERIAL PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Password VARCHAR(255) NOT NULL
);

CREATE TABLE Stocks (
    StockId SERIAL PRIMARY KEY,
    Symbol VARCHAR(32) NOT NULL,
    ShortName VARCHAR(255),
    LongName VARCHAR(255),
    Sector VARCHAR(255),
    Industry VARCHAR(255)
);

CREATE TABLE Preferences (
    PreferenceId SERIAL PRIMARY KEY,
    UserId INT NOT NULL,
    StockId INT NOT NULL,
    PreferencesList TEXT NOT NULL,
    FOREIGN KEY (UserId) REFERENCES Users(UserId) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (StockId) REFERENCES Stocks(StockId) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_preferences_userid ON Preferences(UserId);
