<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http; // Menggunakan Laravel HTTP Client
use Illuminate\Support\Facades\Log;

class LaptopController extends Controller
{
    public function recommend(Request $request)
    {
        try {
            // Validasi input
            $validated = $request->validate([
                'description' => 'required|string',
            
            ]);

            // Mendapatkan data dari request
            $description = $validated['description'];
            $brand = $validated['brand'] ?? '';
            $storage = $validated['storage'] ?? '';

            // Log permintaan untuk debugging
            Log::info('Mengirim permintaan ke Flask Backend', [
                'description' => $description,
                
            ]);

            // Kirim permintaan ke Flask backend
            $response = Http::post('http://127.0.0.1:5000/recommend', [
                'description' => $description,
                
            ]);

            // Periksa apakah respons berhasil
            if ($response->successful()) {
                // Mengembalikan data dari Flask ke frontend
                return response()->json($response->json(), 200);
            } else {
                // Menangani error dari Flask
                Log::error('Flask Backend Error', [
                    'status' => $response->status(),
                    'body' => $response->body(),
                ]);

                return response()->json([
                    'error' => 'Terjadi kesalahan pada server rekomendasi.'
                ], $response->status());
            }
        } catch (\Exception $e) {
            // Menangani exception
            Log::error('Exception di LaptopController@recommend', [
                'message' => $e->getMessage(),
            ]);

            return response()->json([
                'error' => 'Terjadi kesalahan saat memproses permintaan.'
            ], 500);
        }
    }
}
