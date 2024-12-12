@extends('layouts.main')
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">

@section('container')
    <div id="popup-container">
        <div id="popup-handle"></div>
        <div class="row p-2">
            <div class="col-lg-12">
                <div class="row mb-3">
                    <div class="col-6 lock-icon" onclick="toggleLock()">
                        <div id="lock-icon"><i class="fa-solid fa-unlock"></i></div>
                    </div>
                    <div class="col-6 text-end close-icon" onclick="closePopup()">
                        <i class="fa-solid fa-square-xmark"></i>
                    </div>
                </div>
                <div class="row text-center">
                    <div class="col-12">
                        <img src="assets/6.png" alt="Logo" style="width: 80px;">
                    </div>
                </div>
            </div>
        </div>
    </div>

    @if ($posts->count())
        <div class="container">
            <form action="{{ route('home') }}" method="GET">
                @csrf
                <div class="row justify-content-center">
                    <div class="col-lg-6">
                        <div class="input-group mb-3">
                            <input type="text" class="form-control" placeholder="Search.." name="search" value="{{ request('search') }}">
                            <button class="btn btn-outline-secondary" type="submit"><i class="fa-solid fa-magnifying-glass"></i></button>
                        </div>
                    </div>
                </div>
            </form>    

            <div class="tab-container mb-5">
                <div class="tab-bar ms-4">
                    @foreach($categories as $category)
                        <div class="tab @if(request('category') == $category->slug) active @endif" data-category="{{ $category->name }}">
                            <a href="/?category={{ $category->slug }}" style="color: inherit; text-decoration: none;">{{ $category->name }}</a>
                        </div>
                    @endforeach
                </div>
            </div>

            <div class="row justify-content-center mt-4">
                @foreach ($posts as $post)
                    <div class="col-lg-3 col-6 mb-4">
                        <div class="row mb-2">
                            <div class="col-12">
                                @if ($post->image)
                                    <img class="img-fluid rounded-3" style="height: auto; max-height: 140px; width: 100%;" src="{{ asset('storage/' . $post->image) }}" alt="image">
                                @else
                                    <img class="img-fluid rounded-3" src="https:/source.unsplash.com/1280x720/?{{ $post->category->name }}" alt="image">
                                @endif
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-12">
                                <h5 class="mb-2">
                                    <a href="/post/{{ $post->slug }}" style="color: inherit; text-decoration: none;">
                                        {{ $post->title }}
                                    </a>
                                </h5>
                            </div>
                        </div>
                    </div>
                @endforeach 
            </div>

            <!-- Menambahkan Livewire Komentar untuk Post Pertama -->
            <livewire:comments :model="$posts->first()"/>

        </div>
    @else
        <p class="fw-bold text-center">Page Not Found.</p>
    @endif

@endsection
