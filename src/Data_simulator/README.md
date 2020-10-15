The Data simulator runs on an AWS EMR cluster, that is spun up and shut down as soon as the job is finished. The `create-emr-cluster.sh` starts the cluster from the command line, it takes in a `bootstrap.sh` file which helps it set up the required packages and environment. The instance used is a [C5instance](https://aws.amazon.com/ec2/instance-types/c5/) for fast compute capability.  

# The Data


## Odds Data Dump

All data is in csv format

Key to results data:

```
Div = League Division
Date = Match Date (dd/mm/yy)
HomeTeam = Home Team
AwayTeam = Away Team
FTHG = Full Time Home Team Goals
FTAG = Full Time Away Team Goals
FTR = Full Time Result (H=Home Win, D=Draw, A=Away Win)
HTHG = Half Time Home Team Goals
HTAG = Half Time Away Team Goals
HTR = Half Time Result (H=Home Win, D=Draw, A=Away Win)

Match Statistics (where available)
Attendance = Crowd Attendance
Referee = Match Referee
HS = Home Team Shots
AS = Away Team Shots
HST = Home Team Shots on Target
AST = Away Team Shots on Target
HHW = Home Team Hit Woodwork
AHW = Away Team Hit Woodwork
HC = Home Team Corners
AC = Away Team Corners
HF = Home Team Fouls Committed
AF = Away Team Fouls Committed
HO = Home Team Offsides
AO = Away Team Offsides
HY = Home Team Yellow Cards
AY = Away Team Yellow Cards
HR = Home Team Red Cards
AR = Away Team Red Cards
HBP = Home Team Bookings Points (10 = yellow, 25 = red)
ABP = Away Team Bookings Points (10 = yellow, 25 = red)

Key to 1X2 (match) betting odds data:

B365H = Bet365 home win odds
B365D = Bet365 draw odds
B365A = Bet365 away win odds

BWH = Bet&Win home win odds
BWD = Bet&Win draw odds
BWA = Bet&Win away win odds

IWH = Interwetten home win odds
IWD = Interwetten draw odds
IWA = Interwetten away win odds

PSH = Pinnacle Sports home win odds
PSD = Pinnacle Sports draw odds
PSA = Pinnacle Sports away win odds

VCH = VC Bet home win odds
VCD = VC Bet draw odds
VCA = VC Bet away win odds

WHH = William Hill home win odds
WHD = William Hill draw odds
WHA = William Hill away win odds
```

I would like to acknowledge the following sources which have been utilised in the compilation of results and odds files.

Historical results: (might need a vpn to access some of these sites)\
[International Soccer Server](http://sunsite.tut.fi/rec/riku/soccer.html)\
[European Football](http://www.eurofootball.be/)\
[RSSSF Archive](http://www.rsssf.com/)

Current results (full time, half time)\
[TBWSport](http://www.tbwsport.com)\
[Livescore](http://www.livescore.com)

------------------------------------------------------------------------------------------------------

## Simulated Clickstream Data 

Clickstream data is propreitary for internet companies, their key business descions are made using insights from them, I simulated my clickstream data from the clickstream data schema of an ecommerce website.


 - User data
    * SessionID
    * UserID
    * Time_spent
    * Clicks

 - Odds Purchase data
    * SessionID
    * GameID
    * Bet_company
    * Bet_type
    * Amount

