// src/utils/importCsv.ts

interface CsvRow {
    [key: string]: string | string[];
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
                        console.log(row[index])
                        if (row[0] == '') { return null; }
                        let value = row[index].trim();
                        console.log(value)
                        // Check if the value is enclosed in quotes and contains commas
                        if (value.startsWith('"') && value.endsWith('"')) {
                            // Remove quotes and split the value by commas
                            value = value.slice(1, -1);
                            const arrayValues = value.split(' ').map((v) => v.trim());
                            console.log(arrayValues)
                            entry[col.trim()] = arrayValues;
                        } else {
                            entry[col.trim()] = value;
                        }
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
