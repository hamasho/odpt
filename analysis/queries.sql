SELECT
    s1.name AS name1
    , s2.name AS name2
FROM node n
LEFT JOIN station s1 ON n.st1_id = s1.id
LEFT JOIN station s2 on n.st2_id = s2.id
LIMIT 40
