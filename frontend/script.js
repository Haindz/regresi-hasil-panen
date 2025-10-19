document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('csvFileInput');
    const submitBtn = document.getElementById('submitBtn');
    const equationEl = document.getElementById('equation');
    const statusEl = document.getElementById('status');
    const featureSelect = document.getElementById('featureSelect');
    let myChart;
    let chartInstance;
    let parsedData = [];
    let headers = [];

    submitBtn.addEventListener('click', async () => {
        const file = fileInput.files[0];
        if (!file) {
            alert('Silakan pilih file CSV terlebih dahulu!');
            return;
        }

        // Siapkan data untuk dikirim ke API
        const formData = new FormData();
        formData.append('file', file);

        statusEl.textContent = 'Mengirim data ke server dan menunggu perhitungan...';
        equationEl.textContent = '';

        try {
            // Lakukan request POST ke API Flask Anda
            const response = await fetch('http://localhost:5000/predict', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Terjadi kesalahan di server.');
            }

            headers = result.header;
            parsedData = await parseCSV(file);

            const betas = result.koefisien.map(row => row[0]);
            const equation = headers.slice(0, -1)
                .map((h, i) => `${betas[i+1].toFixed(3)}×${h}`)
                .join(' + ');
            equationEl.textContent = `y = ${betas[0].toFixed(3)} + ${equation}`;
            statusEl.textContent = 'Analisis berhasil diterima!';

            // Buat dropdown fitur
            featureSelect.innerHTML = '';
            headers.slice(0, -1).forEach((h, i) => {
                const opt = document.createElement('option');
                opt.value = i;
                opt.textContent = h;
                featureSelect.appendChild(opt);
            });

            // Render plot pertama
            renderScatter(headers[0], betas, parsedData);

            // Update plot saat ganti fitur
            featureSelect.addEventListener('change', e => {
                const index = parseInt(e.target.value);
                renderScatter(headers[index], betas, parsedData, index);
            });

        } catch (error) {
            console.error(error);
            equationEl.textContent = `Error: ${error.message}`;
            statusEl.textContent = 'Gagal melakukan analisis.';
        }
    });

    async function parseCSV(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = e => {
                const text = e.target.result.trim();
                const [headerLine, ...lines] = text.split('\n');
                const header = headerLine.split(',');
                const rows = lines.map(line => line.split(',').map(parseFloat));
                resolve({ header, rows });
            };
            reader.onerror = reject;
            reader.readAsText(file);
        });
    }

    function renderScatter(selectedFeature, betas, dataObj, featureIndex = 0) {
        const ctx = document.getElementById('regressionChart').getContext('2d');
        const xIndex = featureIndex;
        const yIndex = dataObj.header.length - 1;
        const dataPoints = dataObj.rows.map(row => ({
            x: row[xIndex],
            y: row[yIndex]
        }));

        // Hitung prediksi untuk garis regresi
        const minX = Math.min(...dataPoints.map(p => p.x));
        const maxX = Math.max(...dataPoints.map(p => p.x));
        const predict = x => {
            let y = betas[0];
            dataObj.header.slice(0, -1).forEach((_, i) => {
                y += betas[i + 1] * (i === xIndex ? x : 0);
            });
            return y;
        };
        const lineData = [
            { x: minX, y: predict(minX) },
            { x: maxX, y: predict(maxX) }
        ];

        if (chartInstance) chartInstance.destroy();

        chartInstance = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [
                    {
                        label: 'Data Asli',
                        data: dataPoints,
                        backgroundColor: 'rgba(75, 192, 192, 0.6)'
                    },
                    {
                        label: `Garis Regresi (${selectedFeature})`,
                        data: lineData,
                        type: 'line',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 2,
                        pointRadius: 0
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: { display: true, text: selectedFeature }
                    },
                    y: {
                        title: { display: true, text: 'Hasil_Panen' }
                    }
                }
            }
        });
    }
});
