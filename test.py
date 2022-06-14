SELECT code FROM courses_cpy WHERE usrid=self.ids AND code NOT IN ('LUNCH','MEET','FREE') AND hours>0 ORDER BY random() LIMIT 1

SELECT code FROM courses_cpy WHERE hours>0

UPDATE jobs
SET code = (SELECT co FROM comp(0,0) WHERE co NOT IN ('LUNCH','MEET','FREE'))
WHERE code IS NULL AND usrid=0 AND hour IN (11,21,31,41,51)

UPDATE jobs
SET code = (SELECT code FROM courses_cpy WHERE usrid=0 AND code NOT IN ('LUNCH','MEET','FREE') AND hours>0 ORDER BY random()+dest_col LIMIT 1)
WHERE code IS NULL AND usrid=0 AND hour IN (11,21,31,41,51)


CREATE OR REPLACE FUNCTION comp (i NUMERIC(12),imp NUMERIC(2))
    RETURNS TABLE (
        co VARCHAR(8),
        hrs INTEGER,
        ids NUMERIC (12)
)
AS $$
BEGIN
    RETURN QUERY SELECT * FROM courses_cpy WHERE usrid=i AND hours>0 ORDER BY random() LIMIT 1;
END; $$

LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION first (i NUMERIC(12),imp NUMERIC(2))
RETURNS INTEGER
AS
$$
BEGIN
    UPDATE jobs
    SET code = (SELECT co FROM comp(i,imp) WHERE co NOT IN ('LUNCH','MEET','FREE'))
    WHERE code IS NULL AND usrid=i AND hour IN (11,21,31,41,51);
    RETURN 0;
END;
$$
LANGUAGE 'plpgsql';

PERFORM first(0,0);

SELECT hour FROM jobs WHERE code IS NULL AND usrid=self.ids AND hour IN (11,21,31,41,51);
