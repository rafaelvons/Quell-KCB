<!DOCTYPE html>
<html lang="id"> <!-- Mengubah bahasa ke 'id' untuk Bahasa Indonesia -->
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rekomendasi Laptop</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            padding: 20px;
        }
        table {
            width: 100%;
            margin-top: 20px;
            background-color: #fff;
        }
        th, td {
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #007bff;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Rekomendasi Laptop</h1>
    @if($laptops && count($laptops) > 0)
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Produk</th>
                    <th>Processor</th>
                    <th>Graphic Card</th>
                    <th>RAM</th>
                    <th>OS</th>
                    <th>Harga (IDR)</th>
                    <th>Inches</th>
                    <th>Resolusi Layar</th>
                    <th>Berat (Kg)</th>
                </tr>
            </thead>
            <tbody>
                @foreach($laptops as $laptop)
                    <tr>
                        <td>{{ $laptop['Product'] }}</td>
                        <td>{{ $laptop['Cpu'] }}</td>
                        <td>{{ $laptop['Gpu'] }}</td>
                        <td>{{ $laptop['Ram'] }}</td>
                        <td>{{ $laptop['OpSys'] }}</td>
                        <td>Rp {{ number_format($laptop['Price_in_IDR'], 0, ',', '.') }}</td>
                        <td>{{ $laptop['Inches'] }} inch</td>
                        <td>{{ $laptop['ScreenResolution'] }}</td>
                        <td>{{ $laptop['Weight'] }}</td>
                    </tr>
                @endforeach
            </tbody>
        </table>
    @else
        <p>Maaf, tidak ditemukan laptop yang sesuai dengan deskripsi Anda.</p>
    @endif
</body>
</html>
