
''' Creating tables to handle streaming data, some of these are testing tables '''

CREATE TABLE "gameweek_count" (
  "ID" INT GENERATED ALWAYS AS IDENTITY,
  "Gameweek_id" VARCHAR(255),
  "count" INT,
  "timestamp" TIMESTAMP,
    PRIMARY KEY ("ID")
);


CREATE TABLE "gameweek_profit" (
  "ID" INT GENERATED ALWAYS AS IDENTITY,
  "Gameweek_id" VARCHAR(255),
  "profit" INT,
  "timestamp" TIMESTAMP,
    PRIMARY KEY ("ID")
);

CREATE TABLE "gameweek_clicks" (
  "ID" INT GENERATED ALWAYS AS IDENTITY,
  "Gameweek_id" VARCHAR(255),
  "avg_clicks" INT,
  "timestamp" TIMESTAMP,
    PRIMARY KEY ("ID")
);


CREATE TABLE "gameweek_amount" (
  "ID" INT GENERATED ALWAYS AS IDENTITY,
  "Gameweek_id" VARCHAR(255),
  "total_amount" INT,
  "timestamp" TIMESTAMP,
    PRIMARY KEY ("ID")
);


CREATE TABLE "company_gameweek" (
  "ID" INT GENERATED ALWAYS AS IDENTITY,
  "Gameweek_id" VARCHAR(255),
  "Bet_company" VARCHAR(255),
  "profit" INT,
  PRIMARY KEY ("ID")
);

CREATE TABLE "clickstream" (
  "ID" INT GENERATED ALWAYS AS IDENTITY,
  "dataid" VARCHAR(255),
  "timestamp" TIMESTAMP,
  "AwayTeam" VARCHAR(255),
  "winnings" INT,
  "FTAG" INT,
  "FTHG" INT,
  "Gameweek_id" VARCHAR(255),
  "HomeTeam" VARCHAR(255),
  "amount" INT,
  "bet_company" VARCHAR(255),
  "bet_type"  VARCHAR(255),
  "country" VARCHAR(255),
  "game_id" INT,
  "name" VARCHAR(255),
  "number_clicks" INT,
  "odds" INT,
  "season" VARCHAR(255),
  "session" VARCHAR(255),
  "Time_spent" INT,
  "week" INT,
  "year" INT,
  "Date" VARCHAR(255),
  PRIMARY KEY("ID"));
