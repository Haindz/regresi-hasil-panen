document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('csvFileInput');
    const submitBtn = document.getElementById('submitBtn');
    const equationEl = document.getElementById('equation');
    const statusEl = document.getElementById('status');
    let myChart;

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
            const response = await fetch('http://127.0.0.1:5000/regresi', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();

            if (!response.ok) {
                // Tangani error dari server Flask
                throw new Error(result.error || 'Terjadi kesalahan di server.');
            }
            
            // Karena API hanya mengembalikan koefisien, kita perlu membaca file CSV
            // secara lokal untuk bisa menampilkan scatter plot data aslinya.
            const dataPoints = await parseCSV(file);
            
            // Ekstrak koefisien dari respons API
            const beta = result.koefisien_regresi;
            const intercept = beta[0][0];
            const slope = beta[1][0];

            // Tampilkan hasil
            equationEl.textContent = `Persamaan Regresi: y = ${slope.toFixed(4)}x + ${intercept.toFixed(4)}`;
            statusEl.textContent = 'Analisis berhasil diterima dari server!';
            
            // Render grafik
            renderChart(dataPoints, slope, intercept);

        } catch (error) {
            console.error('Error:', error);
            equationEl.textContent = `Error: ${error.message}`;
            statusEl.textContent = 'Gagal melakukan analisis.';
        }
    });

    function renderChart(data, slope, intercept) {
        const ctx = document.getElementById('regressionChart').getContext('2d');
        if (myChart) myChart.destroy();

        const xValues = data.map(p => p.x);
        const minX = Math.min(...xValues);
        const maxX = Math.max(...xValues);
        const regressionLine = [
            { x: minX, y: slope * minX + intercept },
            { x: maxX, y: slope * maxX + intercept }
        ];

        myChart = new Chart(ctx, { /* ... (konfigurasi chart sama seperti sebelumnya) ... */ });
    }

    // Fungsi helper untuk membaca CSV di sisi klien (untuk scatter plot)
    function parseCSV(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = e => {
                const text = e.target.result;
                const lines = text.trim().split('\n').slice(1);
                const points = lines.map(line => {
                    const [x, y] = line.split(',').map(parseFloat);
                    return { x, y };
                });
                resolve(points);
            };
            reader.onerror = reject;
            reader.readAsText(file);
        });
    }
});

// Sisipkan konfigurasi Chart.js yang lengkap di dalam fungsi renderChart
// (Sama seperti kode sebelumnya, sengaja dipersingkat di sini agar fokus pada perubahan)
function renderChart(data, slope, intercept) {
    const ctx = document.getElementById('regressionChart').getContext('2d');
    if (window.myChart) window.myChart.destroy();
    
    const xValues = data.map(p => p.x);
    const minX = Math.min(...xValues);
    const maxX = Math.max(...xValues);
    const regressionLine = [{ x: minX, y: slope * minX + intercept }, { x: maxX, y: slope * maxX + intercept }];
    
    window.myChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Data Asli',
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.6)'
            }, {
                label: 'Garis Regresi dari API',
                data: regressionLine,
                type: 'line',
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'transparent',
                borderWidth: 2,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { type: 'linear', position: 'bottom', title: { display: true, text: 'Variabel X' } },
                y: { title: { display: true, text: 'Variabel Y' } }
            }
        }
    });
}
