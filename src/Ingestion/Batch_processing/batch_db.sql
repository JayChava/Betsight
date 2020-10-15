CREATE SCHEMA public
    AUTHORIZATION postgres;

COMMENT ON SCHEMA public
    IS 'standard public schema';

GRANT ALL ON SCHEMA public TO PUBLIC;

GRANT ALL ON SCHEMA public TO postgres;



CREATE TABLE "Game" (
  "GameID" INT PRIMARY KEY NOT NULL,
  "Season" VARCHAR(255) NOT NULL,
  "Country_name" VARCHAR(255) NOT NULL,
  "GameweekID" VARCHAR(255) NOT NULL,
  "Hometeam" VARCHAR(255) NOT NULL,
  "Awayteam" VARCHAR(255) NOT NULL,
  "FTHG" INT,
  "FTAG" INT,
  PRIMARY KEY ("GameID"),
  CONSTRAINT fk_Gameweek
   FOREIGN KEY(GameweekID) 
      REFERENCES Gameweek(GameweekID)
);

CREATE TABLE "Gameweek" (
  "GameweekID" INT GENERATED ALWAYS AS IDENTITY,
  "GameweekID" INT,
  "Gameweek" VARCHAR(255) NOT NULL,
  "year" INT,
  "week" INT,
  "Date" VARCHAR(255) NOT NULL,
  PRIMARY KEY ("GameweekID")
);

CREATE TABLE "Bets" (
  "BetID" INT GENERATED ALWAYS AS IDENTITY,
  "BetID" INT,
  "SessionID"VARCHAR(255) NOT NULL,
  "GameID" INT,
  "Bet_company" VARCHAR(255) NOT NULL,
  "bet_type" VARCHAR(255) NOT NULL,
  "Odds" INT,
  "Amount" INT,
  PRIMARY KEY ("BetID"),
  CONSTRAINT fk_Game
    FOREIGN KEY(GameID) 
        REFERENCES Game(GameID),
  CONSTRAINT fk_session
    FOREIGN KEY(SessionID) 
        REFERENCES Session(SessionID)
);

CREATE TABLE "Users" (
  "UserID" INT GENERATED ALWAYS AS IDENTITY,
  "UserID" INT,
  "Name" VARCHAR(255) NOT NULL,
  PRIMARY KEY ("UserID")
);

CREATE TABLE "Session " (
  "SessionID" INT,
  "UserID" INT,
  "Number_of_clicks" INT,
  "Time_spent" INT,
  PRIMARY KEY ("SessionID"),
  CONSTRAINT fk_User
    FOREIGN KEY(UserID) 
        REFERENCES Users(UserID)
);

