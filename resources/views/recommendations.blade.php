<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recommended Laptops</title>
</head>
<body>
    <h1>Recommended Laptops</h1>
    {% if laptops %}
        <table border="1">
            <thead>
                <tr>
                    <th>Nama Laptop</th>
                    <th>Processor</th>
                    <th>Graphic Card</th>
                    <th>RAM</th>
                    <th>OS</th>
                    <th>Harga</th>
                    <th>Panel Layar</th>
                    <th>Refresh Rate</th>
                    <th>Berat</th>
                </tr>
            </thead>
            <tbody>
                {% for laptop in laptops %}
                    <tr>
                        <td>{{ laptop['Nama Laptop'] }}</td>
                        <td>{{ laptop['Processor'] }}</td>
                        <td>{{ laptop['Gpu'] }}</td>
                        <td>{{ laptop['Ram'] }} GB</td>
                        <td>{{ laptop['OS'] }}</td>
                        <td>{{ laptop['Price_IDR'] | format_price }}</td>
                        <td>{{ laptop['ScreenResolution'] }}</td>
                        <td>{{ laptop['RefreshRate'] }}</td>
                        <td>{{ laptop['Weight'] }} kg</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>Maaf, tidak ditemukan laptop yang sesuai dengan deskripsi Anda.</p>
    {% endif %}
</body>
</html>
