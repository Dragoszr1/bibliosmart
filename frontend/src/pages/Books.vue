<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="bg-dark py-16 sm:py-24 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-secondary/20 via-transparent to-accent/10"></div>
      <div class="max-w-3xl mx-auto px-6 text-center relative z-10">
        <h2 class="text-3xl sm:text-5xl font-bold text-white mb-3 tracking-tight">Explorează Cărțile</h2>
        <p class="text-white/50 text-sm sm:text-lg font-normal">Descoperă cărți din colecția noastră</p>
      </div>
    </section>

    <!-- Main Content -->
    <main class="max-w-6xl mx-auto px-4 sm:px-6 py-10 sm:py-14">
      <!-- Search Bar -->
      <div class="mb-10">
        <div class="flex items-center gap-3 bg-white rounded-xl shadow-card border border-gray-100 px-5 py-3">
          <i class="pi pi-search text-gray-400"></i>
          <input
            v-model="searchQuery"
            @input="filterBooks"
            type="text"
            placeholder="Caută după titlu, autor sau gen..."
            class="flex-1 bg-transparent text-dark placeholder-gray-400 focus:outline-none text-sm sm:text-base"
          >
          <span v-if="searchQuery" @click="searchQuery = ''; filterBooks()" class="text-gray-400 hover:text-gray-600 cursor-pointer">
            <i class="pi pi-times text-sm"></i>
          </span>
        </div>
      </div>

      <!-- Results Info & Sort -->
      <div class="mb-6 flex items-center justify-between">
        <p class="text-gray-500 text-sm">
          <span class="text-dark font-semibold">{{ filteredBooks.length }}</span> cărți găsite
        </p>
        <div class="flex gap-1.5">
          <button 
            v-for="s in [{ key: 'title', label: 'A-Z' }, { key: 'available', icon: 'pi-check-circle' }, { key: 'newest', icon: 'pi-clock' }]"
            :key="s.key"
            @click="sortBy(s.key)"
            :class="[
              'px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-150',
              sortType === s.key 
                ? 'bg-secondary text-white' 
                : 'bg-white text-gray-500 border border-gray-200 hover:border-secondary/30 hover:text-secondary'
            ]"
          >
            <i v-if="s.icon" :class="'pi ' + s.icon"></i>
            <span v-else>{{ s.label }}</span>
          </button>
        </div>
      </div>

      <!-- Books Grid -->
      <div v-if="filteredBooks.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
        <div 
          v-for="book in filteredBooks"
          :key="book.id"
          @click="openBookDetail(book)"
          class="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden hover:shadow-elevated transition-all duration-200 cursor-pointer group"
        >
          <!-- Book Cover -->
          <div class="relative h-48 bg-cream flex items-center justify-center">
            <i class="pi pi-book text-5xl text-secondary/20 group-hover:text-secondary/30 transition-colors"></i>
            <!-- Availability Badge -->
            <span 
              :class="[
                'absolute top-3 right-3 text-xs px-2.5 py-1 rounded-full font-medium',
                book.available ? 'bg-green-50 text-green-700' : 'bg-red-50 text-accent'
              ]"
            >
              {{ book.available ? 'Disponibil' : 'Indisponibil' }}
            </span>
            <!-- Stock Badge -->
            <span class="absolute top-3 left-3 bg-dark/80 text-white text-xs px-2.5 py-1 rounded-full font-medium">
              {{ book.stoc_disponibil }}/{{ book.stoc_total }}
            </span>
          </div>

          <!-- Book Info -->
          <div class="p-4">
            <h3 class="text-sm font-semibold text-dark mb-1 line-clamp-2 group-hover:text-secondary transition-colors">
              {{ book.title }}
            </h3>
            <p class="text-gray-400 text-xs mb-3">{{ book.author }}</p>
            <span class="inline-block text-xs bg-cream text-secondary/80 px-2 py-0.5 rounded-md font-medium">
              {{ book.genre }}
            </span>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-20">
        <div class="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-4">
          <i class="pi pi-book text-2xl text-gray-300"></i>
        </div>
        <h3 class="text-lg font-semibold text-dark mb-2">Nicio carte găsită</h3>
        <p class="text-gray-500 text-sm mb-6">Modifică filtrele sau caută cu alt cuvânt cheie</p>
        <button 
          @click="clearFilters"
          class="btn-secondary text-sm"
        >
          Șterge Filtre
        </button>
      </div>
    </main>

    <!-- Book Detail Modal -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="showModal = false">
      <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showModal = false"></div>
      
      <div class="relative bg-white rounded-2xl shadow-modal w-full max-w-lg max-h-[85vh] overflow-y-auto z-10">
        <!-- Header -->
        <div class="sticky top-0 bg-dark px-6 py-5 rounded-t-2xl">
          <button @click="showModal = false" class="absolute top-4 right-4 text-white/40 hover:text-white transition-colors">
            <i class="pi pi-times"></i>
          </button>
          <h3 class="text-lg font-bold text-white pr-8">{{ selectedBook?.title }}</h3>
          <p class="text-white/40 text-sm mt-1">de {{ selectedBook?.author }}</p>
        </div>

        <!-- Book Info -->
        <div class="px-6 py-4 border-b border-gray-100">
          <div class="flex flex-wrap gap-2 mb-3">
            <span class="text-xs bg-cream text-secondary/80 px-2.5 py-1 rounded-md font-medium">{{ selectedBook?.genre }}</span>
            <span class="text-xs bg-gray-100 text-gray-500 px-2.5 py-1 rounded-md font-medium">ISBN: {{ selectedBook?.ISBN }}</span>
          </div>
          <div class="flex items-center gap-4 text-sm text-gray-500">
            <span><strong class="text-dark">{{ selectedBook?.stoc_disponibil }}</strong> disponibil</span>
            <span><strong class="text-dark">{{ selectedBook?.stoc_total }}</strong> total</span>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="px-6 py-4 border-b border-gray-100 flex gap-3">
          <button
            @click="requestFizic"
            :disabled="requestingFizic || !selectedBook?.available"
            :class="[
              'flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-150',
              selectedBook?.available
                ? 'bg-secondary text-white hover:bg-secondary/90 active:scale-[0.98]'
                : 'bg-gray-100 text-gray-400 cursor-not-allowed'
            ]"
          >
            <i :class="requestingFizic ? 'pi pi-spin pi-spinner' : 'pi pi-book'" class="text-sm"></i>
            {{ requestingFizic ? 'Se trimite...' : 'Împrumută Fizic' }}
          </button>
          <button
            disabled
            class="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold bg-gray-100 text-gray-400 cursor-not-allowed"
            title="Disponibil în curând"
          >
            <i class="pi pi-file-pdf text-sm"></i>
            PDF (în curând)
          </button>
        </div>

        <!-- Request feedback toast -->
        <div v-if="requestMessage" :class="[
          'mx-6 mt-4 px-4 py-2.5 rounded-xl text-sm font-medium transition-all',
          requestSuccess ? 'bg-green-50 text-green-700' : 'bg-red-50 text-accent'
        ]">
          {{ requestMessage }}
        </div>

        <!-- Rating -->
        <div class="px-6 py-4 border-b border-gray-100">
          <div class="flex items-center gap-3">
            <span class="text-3xl font-bold text-dark">{{ avgRating }}</span>
            <div>
              <div class="flex items-center gap-0.5">
                <span v-for="star in 5" :key="star" :class="star <= Math.round(avgRating) ? 'text-amber-400' : 'text-gray-200'" class="text-lg">★</span>
              </div>
              <p class="text-gray-400 text-xs mt-0.5">{{ totalReviews }} {{ totalReviews === 1 ? 'recenzie' : 'recenzii' }}</p>
            </div>
          </div>
        </div>

        <!-- Reviews -->
        <div class="px-6 py-5">
          <h4 class="font-semibold text-dark mb-4 text-sm">Recenzii</h4>

          <div v-if="loadingReviews" class="text-center py-8">
            <i class="pi pi-spin pi-spinner text-xl text-secondary"></i>
          </div>

          <div v-else-if="reviews.length === 0" class="text-center py-8">
            <p class="text-gray-400 text-sm">Nicio recenzie încă</p>
          </div>

          <div v-else class="space-y-3">
            <div v-for="review in reviews" :key="review.id" class="bg-cream rounded-xl p-4">
              <div class="flex items-center justify-between mb-2">
                <span class="font-medium text-dark text-sm">{{ review.username }}</span>
                <div class="flex items-center gap-0.5">
                  <span v-for="star in 5" :key="star" :class="star <= review.nota ? 'text-amber-400' : 'text-gray-200'" class="text-xs">★</span>
                </div>
              </div>
              <p class="text-gray-600 text-sm">{{ review.comentariu }}</p>
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
      sortType: 'newest',
      allBooks: [],
      filteredBooks: [],
      showModal: false,
      selectedBook: null,
      reviews: [],
      avgRating: 0,
      totalReviews: 0,
      loadingReviews: false,
      requestingFizic: false,
      requestMessage: '',
      requestSuccess: false
    }
  },
  methods: {
    async fetchBooks() {
      try {
        const response = await fetch('/api/books');
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
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(book =>
          book.title.toLowerCase().includes(query) ||
          book.author.toLowerCase().includes(query) ||
          book.genre.toLowerCase().includes(query)
        );
      }
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
      this.sortType = 'newest';
      this.filterBooks();
    },
    async openBookDetail(book) {
      this.selectedBook = book;
      this.reviews = [];
      this.avgRating = 0;
      this.totalReviews = 0;
      this.loadingReviews = true;
      this.requestMessage = '';
      this.requestSuccess = false;
      this.requestingFizic = false;
      this.showModal = true;
      try {
        const response = await fetch(`/api/reviews?carte_id=${book.id}`);
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
    },
    async requestFizic() {
      if (!this.selectedBook || this.requestingFizic) return;
      this.requestingFizic = true;
      this.requestMessage = '';
      try {
        const response = await fetch(`/api/books/${this.selectedBook.id}/request-fizic`, {
          method: 'POST',
          credentials: 'include'
        });
        const data = await response.json();
        this.requestSuccess = data.success;
        this.requestMessage = data.message || (data.success ? 'Cerere trimisă!' : 'Eroare la trimitere');
      } catch (error) {
        this.requestSuccess = false;
        this.requestMessage = 'Eroare de rețea';
      } finally {
        this.requestingFizic = false;
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
