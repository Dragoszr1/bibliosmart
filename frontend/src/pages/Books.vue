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
      <div class="mb-6">
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

      <!-- Filters Panel -->
      <div class="bg-white rounded-xl shadow-card border border-gray-100 p-4 mb-6">
        <div class="flex flex-wrap gap-4 items-end">

          <!-- Gen -->
          <div class="flex flex-col gap-1 min-w-[160px]">
            <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Gen</label>
            <select v-model="filterGen" @change="filterBooks" class="text-sm border border-gray-200 rounded-lg px-3 py-2 bg-cream focus:outline-none focus:border-secondary/50 text-dark">
              <option value="">Toate genurile</option>
              <option v-for="g in allGenres" :key="g" :value="g">{{ g }}</option>
            </select>
          </div>

          <!-- Autor -->
          <div class="flex flex-col gap-1 min-w-[180px]">
            <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Autor</label>
            <select v-model="filterAutor" @change="filterBooks" class="text-sm border border-gray-200 rounded-lg px-3 py-2 bg-cream focus:outline-none focus:border-secondary/50 text-dark">
              <option value="">Toți autorii</option>
              <option v-for="a in allAuthors" :key="a" :value="a">{{ a }}</option>
            </select>
          </div>

          <!-- Disponibilitate -->
          <div class="flex flex-col gap-1 min-w-[170px]">
            <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Disponibilitate</label>
            <select v-model="filterAvailability" @change="filterBooks" class="text-sm border border-gray-200 rounded-lg px-3 py-2 bg-cream focus:outline-none focus:border-secondary/50 text-dark">
              <option value="">Toate</option>
              <option value="available">Disponibile</option>
              <option value="unavailable">Indisponibile</option>
            </select>
          </div>

          <!-- Sortare -->
          <div class="flex flex-col gap-1 min-w-[200px]">
            <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Sortare</label>
            <select v-model="sortType" @change="filterBooks" class="text-sm border border-gray-200 rounded-lg px-3 py-2 bg-cream focus:outline-none focus:border-secondary/50 text-dark">
              <option value="newest">Cele mai noi</option>
              <option value="title_asc">Titlu A → Z</option>
              <option value="title_desc">Titlu Z → A</option>
              <option value="author_asc">Autor A → Z</option>
              <option value="author_desc">Autor Z → A</option>
              <option value="stock_desc">Stoc disponibil ↓</option>
              <option value="stock_asc">Stoc disponibil ↑</option>
              <option value="stock_total_desc">Stoc total ↓</option>
              <option value="stock_total_asc">Stoc total ↑</option>
            </select>
          </div>

          <!-- Reset -->
          <button
            v-if="hasActiveFilters"
            @click="clearFilters"
            class="flex items-center gap-1.5 px-4 py-2 text-xs font-semibold text-accent border border-accent/30 rounded-lg hover:bg-accent/5 transition-colors"
          >
            <i class="pi pi-filter-slash"></i> Resetează
          </button>
        </div>
      </div>

      <!-- Results Info -->
      <div class="mb-5">
        <p class="text-gray-500 text-sm">
          <span class="text-dark font-semibold">{{ filteredBooks.length }}</span> cărți găsite
          <span v-if="hasActiveFilters" class="ml-2 text-secondary text-xs">(filtrate din {{ allBooks.length }} total)</span>
        </p>
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
          <div class="relative h-48 bg-cream flex items-center justify-center overflow-hidden">
            <img
              :src="`/api/books/image/${book.id}`"
              :alt="book.title"
              class="absolute inset-0 w-full h-full object-cover"
              @error="$event.target.style.display='none'"
            >
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
        <div class="sticky top-0 bg-dark px-6 py-5 rounded-t-2xl flex items-center gap-4">
          <img
            v-if="selectedBook"
            :src="`/api/books/image/${selectedBook.id}`"
            :alt="selectedBook.title"
            class="w-14 h-20 object-cover rounded-md flex-shrink-0 shadow"
            @error="$event.target.style.display='none'"
          >
          <div class="flex-1 min-w-0 pr-8">
            <h3 class="text-lg font-bold text-white">{{ selectedBook?.title }}</h3>
            <p class="text-white/40 text-sm mt-1">de {{ selectedBook?.author }}</p>
          </div>
          <button @click="showModal = false" class="absolute top-4 right-4 text-white/40 hover:text-white transition-colors">
            <i class="pi pi-times"></i>
          </button>
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
          <div v-if="selectedBook?.pozitie" class="flex items-center gap-1.5 mt-2 text-sm text-gray-500">
            <i class="pi pi-map-marker text-secondary text-xs"></i>
            <span>Poziție: <strong class="text-dark">{{ selectedBook.pozitie }}</strong></span>
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
          <a
            v-if="selectedBook?.has_pdf"
            :href="`/api/books/pdf/${selectedBook.id}`"
            target="_blank"
            class="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold bg-red-600 hover:bg-red-700 text-white transition-all duration-150"
          >
            <i class="pi pi-file-pdf text-sm"></i>
            Citește PDF
          </a>
          <button
            v-else
            disabled
            class="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold bg-gray-100 text-gray-400 cursor-not-allowed"
          >
            <i class="pi pi-file-pdf text-sm"></i>
            PDF indisponibil
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

        <!-- AI Reviews Summary -->
        <div v-if="reviews.length > 0" class="px-6 py-4 border-b border-gray-100">
          <div class="flex items-center justify-between mb-3">
            <h4 class="font-semibold text-dark text-sm flex items-center gap-2">
              <i class="pi pi-sparkles text-secondary text-xs"></i> Rezumat AI
            </h4>
            <button
              @click="loadAiSummary"
              :disabled="loadingAiSummary"
              class="text-xs text-secondary hover:underline disabled:opacity-50 flex items-center gap-1"
            >
              <i :class="loadingAiSummary ? 'pi pi-spin pi-spinner' : 'pi pi-refresh'" class="text-xs"></i>
              {{ aiSummary ? 'Reîmprospătează' : 'Generează' }}
            </button>
          </div>
          <div v-if="loadingAiSummary" class="text-center py-3">
            <i class="pi pi-spin pi-spinner text-secondary text-sm"></i>
          </div>
          <div v-if="aiSummary" class="bg-cream rounded-xl p-3 text-xs text-dark leading-relaxed">
            {{ aiSummary }}
          </div>
        </div>

        <!-- Submit Review -->
        <div v-if="isLoggedIn" class="px-6 py-5">
          <h4 class="font-semibold text-dark mb-4 text-sm">Scrie o Recenzie</h4>
          <!-- Star picker -->
          <div class="flex gap-1 mb-3">
            <button
              v-for="s in 5" :key="s"
              @click="reviewNota = s"
              :class="s <= reviewNota ? 'text-amber-400' : 'text-gray-300'"
              class="text-2xl leading-none hover:scale-110 transition-transform"
            >★</button>
          </div>
          <textarea
            v-model="reviewText"
            rows="3"
            placeholder="Scrie părerea ta despre carte..."
            class="w-full text-sm px-3 py-2 rounded-xl border border-gray-200 focus:outline-none focus:border-secondary/50 resize-none bg-cream placeholder-gray-400"
          ></textarea>

          <!-- AI assist -->
          <div class="flex items-center gap-2 mt-2 mb-3">
            <button
              @click="aiAssistReview"
              :disabled="loadingAiReview || !reviewText.trim()"
              class="text-xs text-secondary hover:underline disabled:opacity-50 flex items-center gap-1"
            >
              <i :class="loadingAiReview ? 'pi pi-spin pi-spinner' : 'pi pi-sparkles'" class="text-xs"></i>
              {{ loadingAiReview ? 'Se îmbunătățește...' : 'Îmbunătățește cu AI' }}
            </button>
            <span v-if="aiReviewError" class="text-xs text-red-500">{{ aiReviewError }}</span>
          </div>

          <div class="flex items-center gap-2">
            <button
              @click="submitReview"
              :disabled="submittingReview || !reviewText.trim() || reviewNota === 0"
              class="px-4 py-2 bg-secondary hover:bg-secondary/90 text-white text-xs font-semibold rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
            >
              <i :class="submittingReview ? 'pi pi-spin pi-spinner' : 'pi pi-send'" class="text-xs"></i>
              Trimite Recenzia
            </button>
            <span v-if="reviewMessage" :class="reviewSuccess ? 'text-green-600' : 'text-red-500'" class="text-xs">{{ reviewMessage }}</span>
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
      filterGen: '',
      filterAutor: '',
      filterAvailability: '',
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
      requestSuccess: false,
      // AI (inteligență artificială)
      aiSummary: '',
      loadingAiSummary: false,
      // Formular recenzie
      reviewNota: 0,
      reviewText: '',
      submittingReview: false,
      reviewMessage: '',
      reviewSuccess: false,
      loadingAiReview: false,
      aiReviewError: '',
      // Autentificare
      isLoggedIn: false
    }
  },
  computed: {
    allGenres() {
      return [...new Set(this.allBooks.map(b => b.genre).filter(Boolean))].sort((a, b) => a.localeCompare(b, 'ro'))
    },
    allAuthors() {
      return [...new Set(this.allBooks.map(b => b.author).filter(Boolean))].sort((a, b) => a.localeCompare(b, 'ro'))
    },
    hasActiveFilters() {
      return this.searchQuery.trim() || this.filterGen || this.filterAutor || this.filterAvailability || this.sortType !== 'newest'
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
            imprumutat: book.imprumutat,
            pozitie: book.pozitie || null,
            has_pdf: book.has_pdf || false
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
      if (this.filterGen) {
        result = result.filter(b => b.genre === this.filterGen);
      }
      if (this.filterAutor) {
        result = result.filter(b => b.author === this.filterAutor);
      }
      if (this.filterAvailability === 'available') {
        result = result.filter(b => b.available);
      } else if (this.filterAvailability === 'unavailable') {
        result = result.filter(b => !b.available);
      }
      result = [...result];
      this.sortBooks(result);
      this.filteredBooks = result;
    },
    sortBooks(books) {
      switch (this.sortType) {
        case 'title_asc':
          books.sort((a, b) => a.title.localeCompare(b.title, 'ro'));
          break;
        case 'title_desc':
          books.sort((a, b) => b.title.localeCompare(a.title, 'ro'));
          break;
        case 'author_asc':
          books.sort((a, b) => a.author.localeCompare(b.author, 'ro'));
          break;
        case 'author_desc':
          books.sort((a, b) => b.author.localeCompare(a.author, 'ro'));
          break;
        case 'stock_desc':
          books.sort((a, b) => b.stoc_disponibil - a.stoc_disponibil);
          break;
        case 'stock_asc':
          books.sort((a, b) => a.stoc_disponibil - b.stoc_disponibil);
          break;
        case 'stock_total_desc':
          books.sort((a, b) => b.stoc_total - a.stoc_total);
          break;
        case 'stock_total_asc':
          books.sort((a, b) => a.stoc_total - b.stoc_total);
          break;
        default: // newest
          books.sort((a, b) => b.id - a.id);
      }
    },
    sortBy(type) {
      this.sortType = type;
      this.filterBooks();
    },
    clearFilters() {
      this.searchQuery = '';
      this.sortType = 'newest';
      this.filterGen = '';
      this.filterAutor = '';
      this.filterAvailability = '';
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
      this.aiSummary = '';
      this.reviewNota = 0;
      this.reviewText = '';
      this.reviewMessage = '';
      this.reviewSuccess = false;
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
    },
    async loadAiSummary() {
      if (!this.selectedBook) return;
      this.loadingAiSummary = true;
      this.aiSummary = '';
      try {
        const res = await fetch(`/api/ai/book-summary/${this.selectedBook.id}`, {
          credentials: 'include'
        });
        const data = await res.json();
        if (data.success) {
          this.aiSummary = data.no_reviews ? 'Nicio recenzie disponibilă pentru a genera un rezumat.' : data.summary;
        }
      } catch { /* silent */ }
      finally { this.loadingAiSummary = false; }
    },
    async aiAssistReview() {
      if (!this.reviewText.trim() || !this.selectedBook) return;
      this.loadingAiReview = true;
      this.aiReviewError = '';
      try {
        const res = await fetch('/api/ai/review-assist', {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ draft: this.reviewText, titlu: this.selectedBook.title })
        });
        const data = await res.json();
        if (data.success) {
          this.reviewText = data.review;
        } else {
          this.aiReviewError = data.message || 'Eroare AI';
        }
      } catch { this.aiReviewError = 'Eroare de rețea'; }
      finally { this.loadingAiReview = false; }
    },
    async submitReview() {
      if (!this.reviewText.trim() || this.reviewNota === 0 || !this.selectedBook) return;
      this.submittingReview = true;
      this.reviewMessage = '';
      try {
        const res = await fetch('/api/reviews', {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ carte_id: this.selectedBook.id, nota: this.reviewNota, comentariu: this.reviewText })
        });
        const data = await res.json();
        this.reviewSuccess = data.success;
        this.reviewMessage = data.message || (data.success ? 'Recenzie trimisă!' : 'Eroare');
        if (data.success) {
          this.reviewText = '';
          this.reviewNota = 0;
          // Reîncărcăm recenziile
          const r2 = await fetch(`/api/reviews?carte_id=${this.selectedBook.id}`);
          const d2 = await r2.json();
          if (d2.success) { this.reviews = d2.reviews; this.avgRating = d2.avg_rating; this.totalReviews = d2.total_reviews; }
        }
      } catch {
        this.reviewSuccess = false;
        this.reviewMessage = 'Eroare de rețea';
      } finally { this.submittingReview = false; }
    }
  },
  async mounted() {
    this.fetchBooks();
    try {
      const res = await fetch('/api/auth/me', { credentials: 'include' });
      const data = await res.json();
      this.isLoggedIn = data.success === true;
    } catch { this.isLoggedIn = false; }
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
