// src/utils/importCsv.ts

interface CsvRow {
    [key: string]: string;
}

export function importCsv(file: File): Promise<CsvRow[]> {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = (event) => {
            const content = event.target?.result as string;
            const rows = content.split('\n').map((row) => row.split(','));

            // Assuming the first row is the header
            const header = rows[0];

            // Process the data (excluding the header)
            const data: CsvRow[] = rows
                .slice(1)
                .map((row) => {
                    const entry: CsvRow = {};
                    header.forEach((col, index) => {
                        entry[col.trim()] = row[index].trim();
                    });
                    return entry;
                });

            resolve(data);
        };

        reader.onerror = (error) => {
            reject(error);
        };

        reader.readAsText(file);
    });
}
