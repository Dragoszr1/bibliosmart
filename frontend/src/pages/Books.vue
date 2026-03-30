<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-secondary via-dark to-accent py-8 sm:py-16 shadow-elegant relative overflow-hidden">
      <div class="absolute inset-0 gradient-overlay opacity-30"></div>
      <div class="max-w-full mx-auto px-4 text-center relative z-10">
        <h2 class="text-2xl sm:text-4xl font-bold text-white mb-2 sm:mb-4 glow-white tracking-tight">Explorează Cărțile</h2>
        <p class="text-cream/80 text-sm sm:text-lg mb-4 sm:mb-8 font-light">Descoperă cărți din colecția noastră</p>
      </div>
    </section>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-3 sm:px-4 py-8 sm:py-12">
      <!-- Fancy Search Bar -->
      <div class="mb-8 sm:mb-12">
        <div class="relative">
          <div class="bg-cream rounded-lg sm:rounded-2xl shadow-elegant border-2 border-secondary/60 p-4 sm:p-8 card-hover">
            <div class="flex flex-col sm:flex-row items-center gap-3 sm:gap-4">
              <i class="pi pi-search hidden sm:block text-5xl text-secondary"></i>
              <div class="flex-1 w-full sm:w-auto">
                <input
                  v-model="searchQuery"
                  @input="filterBooks"
                  type="text"
                  placeholder="Caută după titlu, autor..."
                  class="w-full px-4 sm:px-6 py-3 sm:py-4 rounded-lg sm:rounded-xl bg-cream-dark border-2 border-secondary/30 text-dark placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary/50 transition-all duration-200 text-sm sm:text-lg"
                >
                <p class="text-gray-500 text-xs sm:text-sm mt-2 sm:mt-3 hidden sm:block">💡 Sugestie: Caută după titlu, autor sau gen</p>
              </div>
              <button class="w-full sm:w-auto bg-gradient-to-r from-secondary to-accent hover:shadow-lg text-white font-bold py-3 sm:py-4 px-6 sm:px-8 rounded-lg sm:rounded-xl transition-all duration-300  text-sm sm:text-base">
                Caută
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Content Layout -->
      <div class="flex flex-col lg:flex-row gap-6 lg:gap-8">
        <!-- Sidebar - Filters (Collapsible on mobile) -->
        <aside class="w-full lg:w-72 lg:flex-shrink-0">
          <!-- Mobile Filter Toggle Button -->
          <button 
            @click="filtersOpen = !filtersOpen"
            class="lg:hidden w-full mb-4 bg-gradient-to-r from-secondary to-accent hover:shadow-lg text-white font-bold py-3 px-4 rounded-lg transition-all duration-300 flex items-center justify-between text-sm sm:text-base"
          >
            <span class="flex items-center gap-2">
              <span>🎯</span>
              <span>{{ filtersOpen ? 'Ascunde' : 'Afișează' }} Filtre</span>
            </span>
            <span class="text-lg">{{ filtersOpen ? '▲' : '▼' }}</span>
          </button>
          
          <!-- Filter Sidebar -->
          <div v-show="filtersOpen" class="lg:block bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 sticky top-24 p-4 sm:p-6 card-hover">
            <h3 class="text-lg sm:text-2xl font-bold text-secondary mb-4 sm:mb-6 hidden lg:flex items-center gap-2">
              <span class="text-3xl">🎯</span> Filtre
            </h3>

            <!-- Availability Filter -->
            <div class="mb-6 sm:mb-8">
              <h4 class="text-base sm:text-lg font-bold text-dark mb-3 sm:mb-4">Disponibilitate</h4>
              <div class="space-y-2 sm:space-y-3">
                <label class="flex items-center gap-3 cursor-pointer group text-sm sm:text-base">
                  <input
                    type="checkbox"
                    v-model="showAvailableOnly"
                    @change="filterBooks"
                    class="w-5 h-5 rounded border-secondary text-secondary focus:ring-secondary cursor-pointer"
                  >
                  <span class="text-gray-700 group-hover:text-secondary transition-colors duration-200">Doar disponibile</span>
                </label>
              </div>
            </div>

            <!-- Clear Filters -->
            <button 
              @click="clearFilters"
              class="w-full bg-gradient-to-r from-secondary to-accent hover:shadow-lg text-white font-bold py-2 sm:py-3 px-4 rounded-lg transition-all duration-300  text-sm sm:text-base"
            >
              Șterge Filtre
            </button>
          </div>
        </aside>

        <!-- Main Content - Books Grid -->
        <section class="flex-1 min-w-0">
          <!-- Results Info -->
          <div class="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <p class="text-dark font-semibold text-sm sm:text-base">
              S-au găsit <span class="text-secondary text-lg sm:text-xl">{{ filteredBooks.length }}</span> cărți
            </p>
            <div class="flex gap-2 flex-wrap sm:flex-nowrap">
              <button 
                @click="sortBy('title')"
                :class="['px-3 sm:px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm transition-all duration-300', sortType === 'title' ? 'bg-secondary text-white shadow-sm' : 'bg-cream text-secondary border-2 border-secondary/40 hover:bg-secondary hover:text-white']"
              >
                A-Z
              </button>
              <button 
                @click="sortBy('available')"
                :class="['px-3 sm:px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm transition-all duration-300', sortType === 'available' ? 'bg-secondary text-white shadow-sm' : 'bg-cream text-secondary border-2 border-secondary/40 hover:bg-secondary hover:text-white']"
              >
                <i class="pi pi-check-circle"></i>
              </button>
              <button 
                @click="sortBy('newest')"
                :class="['px-3 sm:px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm transition-all duration-300', sortType === 'newest' ? 'bg-secondary text-white shadow-sm' : 'bg-cream text-secondary border-2 border-secondary/40 hover:bg-secondary hover:text-white']"
              >
                <i class="pi pi-clock"></i>
              </button>
            </div>
          </div>

          <!-- Books Grid -->
          <div v-if="filteredBooks.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            <div 
              v-for="(book, index) in filteredBooks"
              :key="index"
              class="bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 overflow-hidden card-hover transition-all duration-300 group cursor-pointer flex flex-col"
            >
              <!-- Book Cover -->
              <div class="relative overflow-hidden h-48 sm:h-56 md:h-64 bg-cream-dark flex items-center justify-center">
                <i class="pi pi-book text-6xl text-secondary/30"></i>
                <!-- Availability Badge -->
                <div 
                  :class="[
                    'absolute top-2 right-2 text-xs sm:text-sm px-2 sm:px-3 py-1 rounded-full font-bold shadow-sm',
                    book.available ? 'bg-green-600 text-white' : 'bg-accent text-white'
                  ]"
                >
                  <i :class="book.available ? 'pi pi-check-circle' : 'pi pi-times-circle'"></i>
                </div>
                <!-- Stock Badge -->
                <div class="absolute top-2 left-2 bg-secondary text-white text-xs sm:text-sm px-2 sm:px-3 py-1 rounded-full font-bold shadow-sm">
                  {{ book.stoc_disponibil }}/{{ book.stoc_total }}
                </div>
              </div>

              <!-- Book Info -->
              <div class="p-3 sm:p-4 md:p-6 flex-1 flex flex-col">
                <!-- Title -->
                <h3 class="text-sm sm:text-base md:text-lg font-bold text-dark mb-1 line-clamp-2 group-hover:text-secondary transition-colors duration-200">
                  {{ book.title }}
                </h3>

                <!-- Author -->
                <p class="text-gray-500 text-xs sm:text-sm mb-2">de {{ book.author }}</p>

                <!-- Genre Badge -->
                <div class="mb-2 sm:mb-3 flex flex-wrap gap-1">
                  <span class="text-xs bg-cream-dark text-secondary px-2 py-1 rounded-full border-l-2 border-secondary">
                    {{ book.genre }}
                  </span>
                </div>

                <!-- Stats -->
                <div class="grid grid-cols-2 gap-2 my-2 sm:my-3">
                  <div class="text-center p-1 sm:p-2 bg-cream-dark rounded-lg border-l-2 border-secondary text-xs">
                    <p class="text-secondary font-bold">{{ book.stoc_disponibil }}</p>
                    <p class="text-gray-500 text-xs" style="font-size: 0.65rem;">Disponibil</p>
                  </div>
                  <div class="text-center p-1 sm:p-2 bg-cream-dark rounded-lg border-l-2 border-secondary text-xs">
                    <p class="text-secondary font-bold">{{ book.imprumutat }}</p>
                    <p class="text-gray-500 text-xs" style="font-size: 0.65rem;">Împrumutat</p>
                  </div>
                </div>

                <!-- Action Buttons -->
                <div class="flex gap-2">
                  <button 
                    :disabled="!book.available"
                    :class="[
                      'flex-1 font-bold py-2 px-2 sm:px-3 rounded-lg text-xs sm:text-sm transition-all duration-300 ',
                      book.available 
                        ? 'bg-gradient-to-r from-secondary to-accent hover:shadow-lg text-white' 
                        : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    ]"
                  >
                    {{ book.available ? '📥' : '❌' }}
                  </button>
                  <button @click="openBookDetail(book)" class="flex-1 bg-cream-dark hover:bg-cream border-2 border-secondary/30 text-secondary font-bold py-2 px-2 sm:px-3 rounded-lg text-xs sm:text-sm transition-all duration-300 ">
                    <i class="pi pi-info-circle"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else class="bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 p-8 sm:p-12 text-center">
            <i class="pi pi-book text-4xl mb-4 text-secondary"></i>
            <h3 class="text-xl sm:text-2xl font-bold text-dark mb-3">Nicio carte găsită</h3>
            <p class="text-gray-600 mb-6 text-sm sm:text-base">Încearcă să modifici filtrele sau cauta cu alt cuvânt cheie</p>
            <button 
              @click="clearFilters"
              class="bg-gradient-to-r from-secondary to-accent hover:shadow-lg text-white font-bold py-2 sm:py-3 px-6 sm:px-8 rounded-lg text-sm sm:text-base transition-all duration-300 "
            >
              Șterge Filtre
            </button>
          </div>
        </section>
      </div>
    </main>

    <!-- Book Detail Modal -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="showModal = false">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="showModal = false"></div>
      
      <!-- Modal Content -->
      <div class="relative bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 w-full max-w-lg max-h-[85vh] overflow-y-auto z-10">
        <!-- Header -->
        <div class="sticky top-0 bg-dark p-4 sm:p-6 rounded-t-lg border-b border-secondary/30">
          <button @click="showModal = false" class="absolute top-3 right-3 text-cream/60 hover:text-white transition-colors">
            <i class="pi pi-times text-xl"></i>
          </button>
          <h3 class="text-lg sm:text-xl font-bold text-white pr-8">{{ selectedBook?.title }}</h3>
          <p class="text-cream/60 text-sm mt-1">de {{ selectedBook?.author }}</p>
        </div>

        <!-- Book Info -->
        <div class="p-4 sm:p-6 border-b border-secondary/20">
          <div class="flex flex-wrap gap-2 mb-3">
            <span class="text-xs bg-cream-dark text-secondary px-2 py-1 rounded-full border-l-2 border-secondary">
              {{ selectedBook?.genre }}
            </span>
            <span class="text-xs bg-cream-dark text-secondary px-2 py-1 rounded-full border-l-2 border-secondary">
              ISBN: {{ selectedBook?.ISBN }}
            </span>
          </div>
          <div class="flex items-center gap-4 text-sm">
            <div class="flex items-center gap-1">
              <span class="text-secondary font-bold">{{ selectedBook?.stoc_disponibil }}</span>
              <span class="text-gray-500">disponibil</span>
            </div>
            <div class="flex items-center gap-1">
              <span class="text-secondary font-bold">{{ selectedBook?.stoc_total }}</span>
              <span class="text-gray-500">total</span>
            </div>
          </div>
        </div>

        <!-- Rating Summary -->
        <div class="p-4 sm:p-6 border-b border-secondary/20">
          <div class="flex items-center gap-3">
            <div class="text-3xl font-bold text-secondary">{{ avgRating }}</div>
            <div>
              <div class="flex items-center gap-0.5">
                <span v-for="star in 5" :key="star" :class="star <= Math.round(avgRating) ? 'text-accent' : 'text-gray-300'" class="text-lg">★</span>
              </div>
              <p class="text-gray-500 text-xs mt-0.5">{{ totalReviews }} {{ totalReviews === 1 ? 'recenzie' : 'recenzii' }}</p>
            </div>
          </div>
        </div>

        <!-- Reviews List -->
        <div class="p-4 sm:p-6">
          <h4 class="font-bold text-dark mb-4">Recenzii</h4>

          <div v-if="loadingReviews" class="text-center py-8">
            <i class="pi pi-spin pi-spinner text-2xl text-secondary"></i>
          </div>

          <div v-else-if="reviews.length === 0" class="text-center py-8">
            <i class="pi pi-comments text-3xl text-gray-300 mb-2"></i>
            <p class="text-gray-500 text-sm">Nicio recenzie încă</p>
          </div>

          <div v-else class="space-y-4">
            <div v-for="review in reviews" :key="review.id" class="bg-cream-dark rounded-lg p-3 sm:p-4 border border-secondary/15">
              <div class="flex items-center justify-between mb-2">
                <span class="font-semibold text-dark text-sm">{{ review.username }}</span>
                <div class="flex items-center gap-0.5">
                  <span v-for="star in 5" :key="star" :class="star <= review.nota ? 'text-accent' : 'text-gray-300'" class="text-sm">★</span>
                </div>
              </div>
              <p class="text-gray-700 text-sm">{{ review.comentariu }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Books',
  data() {
    return {
      searchQuery: '',
      showAvailableOnly: false,
      sortType: 'newest',
      filtersOpen: false,
      allBooks: [],
      filteredBooks: [],
      showModal: false,
      selectedBook: null,
      reviews: [],
      avgRating: 0,
      totalReviews: 0,
      loadingReviews: false
    }
  },
  methods: {
    async fetchBooks() {
      try {
        const response = await fetch('http://localhost:5000/api/books');
        const data = await response.json();
        if (data.books) {
          this.allBooks = data.books.map(book => ({
            id: book.carte_id,
            title: book.titlu,
            author: book.autor,
            ISBN: book.ISBN,
            genre: book.gen,
            stoc_total: book.stoc_total,
            available: book.stoc_disponibil > 0,
            stoc_disponibil: book.stoc_disponibil,
            imprumutat: book.imprumutat
          }));
          this.filterBooks();
        }
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    },
    filterBooks() {
      let result = this.allBooks;

      // Filtru de căutare
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(book =>
          book.title.toLowerCase().includes(query) ||
          book.author.toLowerCase().includes(query) ||
          book.genre.toLowerCase().includes(query)
        );
      }

      // Filtru de disponibilitate
      if (this.showAvailableOnly) {
        result = result.filter(book => book.available);
      }

      // Sortare
      this.sortBooks(result);
      this.filteredBooks = result;
    },
    sortBooks(books) {
      switch (this.sortType) {
        case 'title':
          books.sort((a, b) => a.title.localeCompare(b.title));
          break;
        case 'available':
          books.sort((a, b) => b.stoc_disponibil - a.stoc_disponibil);
          break;
        case 'newest':
          books.sort((a, b) => b.id - a.id);
          break;
      }
    },
    sortBy(type) {
      this.sortType = type;
      this.filterBooks();
    },
    clearFilters() {
      this.searchQuery = '';
      this.showAvailableOnly = false;
      this.sortType = 'newest';
      this.filterBooks();
    },
    async openBookDetail(book) {
      this.selectedBook = book;
      this.reviews = [];
      this.avgRating = 0;
      this.totalReviews = 0;
      this.loadingReviews = true;
      this.showModal = true;

      try {
        const response = await fetch(`http://localhost:5000/api/reviews?carte_id=${book.id}`);
        const data = await response.json();
        if (data.success) {
          this.reviews = data.reviews;
          this.avgRating = data.avg_rating;
          this.totalReviews = data.total_reviews;
        }
      } catch (error) {
        console.error('Error fetching reviews:', error);
      } finally {
        this.loadingReviews = false;
      }
    }
  },
  mounted() {
    this.fetchBooks();
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
