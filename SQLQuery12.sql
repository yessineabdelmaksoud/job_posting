BULK INSERT JobPostings
FROM 'C:\Users\pc\Desktop\job_execl.csv'
WITH (
    FIELDTERMINATOR = ';',  -- Délimiteur de colonnes
    ROWTERMINATOR = '\n',   -- Délimiteur de lignes
    FIRSTROW = 2,           -- Ignorer la ligne d'en-tête
    CODEPAGE = '65001',     -- UTF-8
    FORMAT = 'CSV'
);
