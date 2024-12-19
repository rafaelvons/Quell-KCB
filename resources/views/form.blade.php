<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot Rekomendasi Laptop</title>
    <meta name="csrf-token" content="{{ csrf_token() }}">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">

    <!-- Custom CSS -->
    <style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .chatbox {
            display: flex;
            flex-direction: column;
            height: 100vh;
            max-width: 100%;
            background: #ffffff;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        .chat-header {
            background-color: #007bff;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 1.5rem;
        }
        .chat-body {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background-color: #f9f9f9;
        }
        .message {
            display: flex;
            margin-bottom: 20px;
        }
        .message.user {
            justify-content: flex-end;
        }
        .message.bot {
            justify-content: flex-start;
        }
        .message .avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .message.user .avatar {
            margin-right: 0;
            margin-left: 10px;
        }
        .message .bubble {
            max-width: 70%;
            padding: 15px 20px;
            border-radius: 20px;
            position: relative;
            word-wrap: break-word;
            font-size: 1rem;
            line-height: 1.4;
        }
        .message.user .bubble {
            background-color: #007bff;
            color: white;
            border-bottom-right-radius: 0;
        }
        .message.bot .bubble {
            background-color: #e4e6eb;
            color: #333;
            border-bottom-left-radius: 0;
        }
        .chat-footer {
            padding: 20px;
            background-color: #ffffff;
            border-top: 1px solid #ddd;
            position: relative;
            display: flex;
            align-items: center;
        }
        .chat-footer textarea {
            resize: none;
            width: calc(100% - 70px);
            height: 50px;
            border-radius: 25px;
            border: 1px solid #ccc;
            padding: 10px 15px;
            font-size: 1rem;
            outline: none;
        }
        .chat-footer button {
            background-color: #007bff;
            border: none;
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            font-size: 1.25rem;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-left: 10px;
        }
        /* Typing Indicator Styling */
        .typing-indicator {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        .typing-indicator .dot {
            height: 8px;
            width: 8px;
            margin: 0 2px;
            background-color: #333;
            border-radius: 50%;
            display: inline-block;
            animation: typing 1.4s infinite;
        }
        .typing-indicator .dot:nth-child(2) {
            animation-delay: -0.32s;
        }
        .typing-indicator .dot:nth-child(3) {
            animation-delay: -0.16s;
        }
        @keyframes typing {
            0% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
            100% { transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="chatbox">
        <div class="chat-header">
            Chatbot Rekomendasi Laptop
        </div>
        <div class="chat-body" id="chat-container">
            <!-- Pesan akan ditambahkan secara dinamis di sini -->
            <div class="message bot">
            <img src="{{ asset('assets/robot.png') }}" alt="Bot" class="avatar">
                <div class="bubble">
                    <strong>Bot:</strong> Halo! Saya LaptopBot. Bagaimana saya bisa membantu Anda hari ini?
                </div>
            </div>
        </div>
        <div class="chat-footer">
            <form id="chat-form" style="width: 100%; display: flex;">
                <textarea class="form-control" id="description" name="description" placeholder="Ketik pesan Anda..." required></textarea>
                <button type="submit" title="Kirim"><i class="fas fa-paper-plane"></i></button>
            </form>
        </div>
    </div>

    <!-- jQuery dan Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <!-- Custom JavaScript -->
    <script>
        $(document).ready(function() {
            $('#chat-form').on('submit', function(e) {
                e.preventDefault();
                var description = $('#description').val().trim();

                if (description === '') {
                    return;
                }

                // Mendapatkan CSRF token dari meta tag
                var csrfToken = $('meta[name="csrf-token"]').attr('content');

                // Buat pesan pengguna
                appendMessage(`<strong>You:</strong> ${description}`, 'user');

                // Tampilkan typing indicator
                showTypingIndicator();

                // Kirim permintaan ke Flask backend
                $.ajax({
                    url: 'http://127.0.0.1:5000/recommend',  // Ganti dengan URL Flask Anda
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    data: JSON.stringify({ description: description }),
                    success: function(response) {
                        hideTypingIndicator();

                        if (Array.isArray(response) && response.length > 0) {
                            response.forEach(function(laptop) {
                                var laptopInfo = `
                                    <strong>Nama Laptop:</strong> ${laptop['Product']}<br>
                                    <strong>Brand:</strong> ${laptop['Company']}<br>
                                    <strong>Processor:</strong> ${laptop['Cpu']}<br>
                                    <strong>Graphic Card:</strong> ${laptop['Gpu']}<br>
                                    <strong>RAM:</strong> ${laptop['Ram']}<br>
                                    <strong>Penyimpanan:</strong> ${laptop['Memory']}<br>
                                    <strong>OS:</strong> ${laptop['OpSys']}<br>
                                    <strong>Harga:</strong> Rp ${parseInt(laptop['Price_in_IDR']).toLocaleString()}<br>
                                    <strong>Inches:</strong> ${laptop['Inches']} inch<br>
                                    <strong>Resolusi Layar:</strong> ${laptop['ScreenResolution']}<br>
                                    <strong>Berat:</strong> ${laptop['Weight']} 
                                `;
                                appendMessage(laptopInfo, 'bot');
                            });
                        } else {
                            appendMessage('Tidak ada rekomendasi yang ditemukan.', 'bot');
                        }
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        console.log('AJAX Error:', textStatus, errorThrown);
                        hideTypingIndicator();
                        appendMessage('Terjadi kesalahan saat mendapatkan rekomendasi.', 'bot');
                    }
                });

                // Reset textarea
                $('#description').val('');
            });

            function appendMessage(message, type) {
                var avatarPath = (type === 'user') ? '{{ asset("assets/user.png") }}' : '{{ asset("assets/robot.png") }}';
                var messageClass = (type === 'user') ? 'user' : 'bot';
                var senderLabel = (type === 'user') ? '<strong></strong> ' : '<strong>Bot:</strong> ';
                var messageElement = `
                    <div class="message ${messageClass}">
                        ${type === 'bot' ? `<img src="${avatarPath}" alt="Bot" class="avatar">` : ''}
                        <div class="bubble">
                            ${senderLabel}${message}
                        </div>
                        ${type === 'user' ? `<img src="${avatarPath}" alt="User" class="avatar">` : ''}
                    </div>
                `;
                $('#chat-container').append(messageElement);
                $('#chat-container').scrollTop($('#chat-container')[0].scrollHeight);
            }

            function showTypingIndicator() {
                var typingElement = `
                    <div class="message bot typing-indicator">
                        <img src="{{ asset('assets/robot.png') }}" alt="Bot" class="avatar">
                        <div class="bubble">
                            <em>Bot sedang mengetik...</em>
                            <div class="dot"></div>
                            <div class="dot"></div>
                            <div class="dot"></div>
                        </div>
                    </div>
                `;
                $('#chat-container').append(typingElement);
                $('#chat-container').scrollTop($('#chat-container')[0].scrollHeight);
            }

            function hideTypingIndicator() {
                $('.typing-indicator').remove();
            }
        });
    </script>
</body>
</html>
