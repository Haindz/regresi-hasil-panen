document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('csvFileInput');
    const submitBtn = document.getElementById('submitBtn');
    const equationEl = document.getElementById('equation');
    const statusEl = document.getElementById('status');
    const featureSelect = document.getElementById('featureSelect');
    let chartInstance;
    let headers = [];
    let parsedData = [];
    let visualCoeffs = {}; // Untuk menyimpan koefisien visual

    submitBtn.addEventListener('click', async () => {
        const file = fileInput.files[0];
        if (!file) {
            alert('Silakan pilih file CSV terlebih dahulu!');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        statusEl.textContent = 'Mengirim data ke server dan menunggu perhitungan...';
        equationEl.textContent = '';
        featureSelect.innerHTML = '<option value="">(Menunggu data)</option>';
        if (chartInstance) chartInstance.destroy();

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

            // --- PERBAIKAN DI SINI ---
            // 1. Ambil data langsung dari backend, tidak perlu parseCSV lagi
            headers = result.header;
            parsedData = result.original_data; // Data mentah dari backend
            
            // 2. Ambil koefisien MULTIVARIATE untuk teks hasil
            // Pastikan backend mengirim 'koefisien_multivariate'
            const multi_betas = result.koefisien_multivariate.map(row => row[0]);

            // 3. Ambil koefisien VISUAL untuk grafik
            // Pastikan backend mengirim 'koefisien_visual'
            visualCoeffs = result.koefisien_visual;
            // --- AKHIR PERBAIKAN ---

            // Buat teks persamaan regresi (menggunakan koefisien multivariate)
            const equation = headers.slice(0, -1)
                .map((h, i) => `${multi_betas[i + 1].toFixed(3)}×${h}`)
                .join(' + ');
            equationEl.textContent = `y = ${multi_betas[0].toFixed(3)} + ${equation}`;
            statusEl.textContent = 'Analisis berhasil diterima!';

            // Buat dropdown fitur
            featureSelect.innerHTML = '';
            const featureHeaders = headers.slice(0, -1);
            featureHeaders.forEach((h, i) => {
                const opt = document.createElement('option');
                opt.value = i; // 'i' adalah indeks kolom fitur
                opt.textContent = h; // 'h' adalah nama fitur
                featureSelect.appendChild(opt);
            });

            // Render plot pertama (fitur pertama, indeks 0)
            renderScatter(0); // Kirim indeks fitur

            // Update plot saat ganti fitur
            featureSelect.addEventListener('change', e => {
                const selectedFeatureIndex = parseInt(e.target.value);
                renderScatter(selectedFeatureIndex);
            });

        } catch (error) {
            console.error('Error saat fetch:', error);
            equationEl.textContent = `Error: ${error.message}`;
            statusEl.textContent = 'Gagal melakukan analisis.';
        }
    });

    // Fungsi renderScatter di-refactor agar lebih sederhana
    function renderScatter(featureIndex) {
        if (!parsedData.length) return;

        const ctx = document.getElementById('regressionChart').getContext('2d');
        const yIndex = headers.length - 1; // Indeks kolom Target (Y)
        const selectedFeatureName = headers[featureIndex];
        const targetName = headers[yIndex];

        // Ambil data mentah untuk plot (X dan Y)
        const dataPoints = parsedData.map(row => ({
            x: row[featureIndex], // Data X dari fitur yang dipilih
            y: row[yIndex]      // Data Y dari kolom target
        }));

        // --- PERBAIKAN LOGIKA GRAFIK ---
        // Ambil koefisien regresi SEDERHANA yang benar untuk fitur ini
        // dari data 'visualCoeffs' yang dikirim backend
        const simple_beta = visualCoeffs[selectedFeatureName];
        const intercept = simple_beta[0][0]; // beta_0 (intercept)
        const slope = simple_beta[1][0];     // beta_1 (slope)
        
        // Buat fungsi prediksi 2D sederhana
        const predict = x => intercept + slope * x;
        // --- AKHIR PERBAIKAN LOGIKA GRAFIK ---

        // Hitung titik awal dan akhir untuk garis regresi
        const minX = Math.min(...dataPoints.map(p => p.x));
        const maxX = Math.max(...dataPoints.map(p => p.x));
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
                        label: `Garis Regresi (${selectedFeatureName})`,
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
                        title: { display: true, text: selectedFeatureName }
                    },
                    y: {
                        title: { display: true, text: targetName }
                    }
                }
            }
        });
    }
});
