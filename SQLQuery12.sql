BULK INSERT JobPostings
FROM 'C:\Users\pc\Desktop\job_execl.csv'
WITH (
    FIELDTERMINATOR = ';',  -- D�limiteur de colonnes
    ROWTERMINATOR = '\n',   -- D�limiteur de lignes
    FIRSTROW = 2,           -- Ignorer la ligne d'en-t�te
    CODEPAGE = '65001',     -- UTF-8
    FORMAT = 'CSV'
);
