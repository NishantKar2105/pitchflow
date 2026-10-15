-- Drop table if resetting the raw staging environment
DROP TABLE IF EXISTS raw_player_gw;

CREATE TABLE raw_player_gw (
    -- Season Context (added to partition or track seasons easily)
    season VARCHAR(10),

    -- Player Info
    name VARCHAR(100),
    position VARCHAR(20),
    team VARCHAR(50),
    element INT,

    -- Match Context
    fixture INT,
    round INT,                 -- Gameweek number
    opponent_team INT,
    was_home BOOLEAN,
    kickoff_time VARCHAR(20),    -- Converted from ISO string for time-based queries
    team_h_score INT,
    team_a_score INT,

    -- Performance
    total_points INT,
    minutes INT,
    starts INT,
    goals_scored INT,
    assists INT,
    clean_sheets INT,
    goals_conceded INT,
    own_goals INT,
    penalties_saved INT,
    penalties_missed INT,
    saves INT,
    yellow_cards INT,
    red_cards INT,
    bonus INT,
    bps INT,

    -- ICT & Expected Stats (Stored as NUMERIC for clean mathematical aggregations)
    ict_index NUMERIC,
    influence NUMERIC,
    creativity NUMERIC,
    threat NUMERIC,
    expected_goals NUMERIC,
    expected_assists NUMERIC,
    expected_goal_involvements NUMERIC,
    expected_goals_conceded NUMERIC,

    -- Additional GW Stats
    "xP" NUMERIC,                -- Expected points (noting the post-match timing caveat)
    value INT,                 -- Player price in £0.1m
    selected INT,
    transfers_in INT,
    transfers_out INT,
    transfers_balance INT,
    modified BOOLEAN,

    -- Defensive Stats (when available)
    tackles INT,
    recoveries INT,
    clearances_blocks_interceptions INT,
    defensive_contributions NUMERIC
);

-- Drop table if resetting the raw staging environment
DROP TABLE IF EXISTS raw_fixtures;

CREATE TABLE raw_fixtures (
    -- Season Context
    season VARCHAR(10),

    -- Fixture Identification & Context
    id INT,
    event INT,                 -- Gameweek number (null if not yet scheduled)
    team_h INT,                -- Home team ID
    team_a INT,                -- Away team ID
    
    -- Scores & Timing
    team_h_score INT,          -- Home team score (null if not played)
    team_a_score INT,          -- Away team score (null if not played)
    kickoff_time TIMESTAMP,    -- Scheduled kickoff (converted from ISO format string)
    
    -- Match Status flags
    finished BOOLEAN,
    started BOOLEAN,
    finished_provisional BOOLEAN,
    minutes INT,
    
    -- Fixture Difficulty Ratings (FDR)
    team_h_difficulty INT,     -- Fixture difficulty for home team (1-5)
    team_a_difficulty INT      -- Fixture difficulty for away team (1-5)
);
