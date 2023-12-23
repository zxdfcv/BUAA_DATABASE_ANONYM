// exportCsv.js
export function exportCsv(data, fileName) {
    const bom = '\uFEFF';
    const header = Object.keys(data[0]).join(',') + '\n';
    const rows = data.map(entry => {
        const values = Object.values(entry).map(value => {
            // 如果值是字符串并且包含逗号，使用双引号括起来
            if (Array.isArray(value) || typeof value === 'string' && value.includes(',')) {

                return `"${value}"`.replace(/,/g, ' ');
            }
            return value;
        });
        return values.join(',');
    }).join('\n');

    const csvContent = bom + header + rows;

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.href = url;
    link.setAttribute('download', fileName || 'exported_data.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
