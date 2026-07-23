<template>
  <div class="font-sans text-[#2a1410] bg-cream min-h-screen pb-20">
    <!-- Hero Section -->
    <section class="relative overflow-hidden border-b border-[#ede0cc] min-h-[300px] flex items-center">
      <img
        src="https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1600&h=900&fit=crop&auto=format"
        alt="Library books"
        class="absolute inset-0 w-full h-full object-cover object-center"
      />
      <div
        class="absolute inset-0"
        style="background: linear-gradient(105deg, rgba(45,16,24,0.85) 0%, rgba(45,16,24,0.65) 45%, rgba(45,16,24,0.35) 70%, rgba(45,16,24,0.1) 100%)"
      ></div>
      <div
        class="absolute inset-0 opacity-[0.03]"
        style="background-image: repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(201,168,76,1) 39px, rgba(201,168,76,1) 40px), repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(201,168,76,1) 39px, rgba(201,168,76,1) 40px)"
      ></div>
      
      <div class="max-w-7xl mx-auto px-6 py-16 relative w-full text-center sm:text-left">
        <h2 class="text-4xl sm:text-6xl font-black text-white mb-3 tracking-tight drop-shadow font-display uppercase">
          Catalog Cărți
        </h2>
        <div class="flex items-center justify-center sm:justify-start gap-4 w-full opacity-90">
             <div class="h-px flex-1 max-w-[30px] sm:hidden bg-gradient-to-l from-[#c9a84c] to-transparent"></div>
             <p class="text-[#c9a84c] text-sm sm:text-base italic font-serif tracking-widest shrink-0">„Descoperă următoarea ta lectură"</p>
             <div class="h-px flex-1 max-w-[80px] bg-gradient-to-r from-[#c9a84c] to-transparent"></div>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-6 py-10">
      <!-- Search Bar -->
      <div class="mb-6">
        <div class="flex items-center gap-3 bg-white rounded-sm border border-[#2a1410]/10 px-5 py-4 shadow-[0_1px_4px_rgba(42,20,16,0.04)]">
          <i class="pi pi-search text-[#7a5a55]"></i>
          <input
            v-model="searchQuery"
            @input="filterBooks"
            type="text"
            placeholder="Caută după titlu, autor sau gen..."
            class="flex-1 bg-transparent text-[#2a1410] placeholder-[#7a5a55]/50 focus:outline-none text-sm sm:text-base font-medium"
          >
          <span v-if="searchQuery" @click="searchQuery = ''; filterBooks()" class="text-[#7a5a55] hover:text-[#2a1410] cursor-pointer">
            <i class="pi pi-times text-sm"></i>
          </span>
        </div>
      </div>

      <!-- Filters Panel -->
      <div class="bg-white rounded-sm border border-[#2a1410]/10 p-5 mb-8 shadow-[0_1px_4px_rgba(42,20,16,0.04)]">
        <div class="flex flex-wrap gap-5 items-end">
          <!-- Gen -->
          <div class="flex flex-col gap-2 min-w-[160px]">
            <label class="font-mono text-[10px] tracking-widest uppercase text-[#7a5a55]">Gen</label>
            <select v-model="filterGen" @change="filterBooks" class="text-sm font-medium border border-[#2a1410]/10 rounded-sm px-3 py-2 bg-cream-dark focus:outline-none focus:border-[#c9a84c] text-[#2a1410]">
              <option value="">Toate genurile</option>
              <option v-for="g in allGenres" :key="g" :value="g">{{ g }}</option>
            </select>
          </div>

          <!-- Autor -->
          <div class="flex flex-col gap-2 min-w-[180px]">
            <label class="font-mono text-[10px] tracking-widest uppercase text-[#7a5a55]">Autor</label>
            <select v-model="filterAutor" @change="filterBooks" class="text-sm font-medium border border-[#2a1410]/10 rounded-sm px-3 py-2 bg-cream-dark focus:outline-none focus:border-[#c9a84c] text-[#2a1410]">
              <option value="">Toți autorii</option>
              <option v-for="a in allAuthors" :key="a" :value="a">{{ a }}</option>
            </select>
          </div>

          <!-- Disponibilitate -->
          <div class="flex flex-col gap-2 min-w-[170px]">
            <label class="font-mono text-[10px] tracking-widest uppercase text-[#7a5a55]">Disponibilitate</label>
            <select v-model="filterAvailability" @change="filterBooks" class="text-sm font-medium border border-[#2a1410]/10 rounded-sm px-3 py-2 bg-cream-dark focus:outline-none focus:border-[#c9a84c] text-[#2a1410]">
              <option value="">Toate</option>
              <option value="available">Disponibile</option>
              <option value="unavailable">Indisponibile</option>
            </select>
          </div>

          <!-- Sortare -->
          <div class="flex flex-col gap-2 min-w-[200px]">
            <label class="font-mono text-[10px] tracking-widest uppercase text-[#7a5a55]">Sortare</label>
            <select v-model="sortType" @change="filterBooks" class="text-sm font-medium border border-[#2a1410]/10 rounded-sm px-3 py-2 bg-cream-dark focus:outline-none focus:border-[#c9a84c] text-[#2a1410]">
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
            class="flex items-center gap-1.5 px-4 py-2.5 text-[10px] font-mono tracking-widest uppercase font-bold text-secondary border border-secondary/30 rounded-sm hover:bg-secondary/5 transition-colors"
          >
            <i class="pi pi-filter-slash"></i> Resetează
          </button>
        </div>
      </div>

      <!-- Results Info -->
      <div class="mb-5 flex items-center justify-between">
        <p class="font-mono text-xs tracking-wider text-[#7a5a55] uppercase">
          <span class="text-[#2a1410] font-bold">{{ filteredBooks.length }}</span> cărți găsite
          <span v-if="hasActiveFilters" class="ml-2 text-secondary/80">(filtrate din {{ allBooks.length }})</span>
        </p>
      </div>

      <!-- Books Grid -->
      <div v-if="filteredBooks.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-5">
        <div 
          v-for="book in paginatedBooks"
          :key="book.id"
          @click="openBookDetail(book)"
          class="group rounded-sm overflow-hidden cursor-pointer transition-all bg-white border border-[#2a1410]/10 shadow-[0_1px_4px_rgba(42,20,16,0.06)] hover:shadow-[0_4px_16px_rgba(155,27,48,0.12)] flex flex-col"
        >
          <!-- Book Cover -->
          <div class="relative overflow-hidden h-44 bg-cream-dark shrink-0">
            <img
              :src="`/api/books/image/${book.id}`"
              :alt="book.title"
              loading="lazy"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              @error="$event.target.style.display='none'"
            >
            <div class="absolute inset-0 flex items-center justify-center -z-10 bg-cream-dark">
                <i class="pi pi-book text-3xl text-secondary/20"></i>
            </div>
            <!-- Availability Badge -->
            <div class="absolute top-2 right-2 flex flex-col gap-1 items-end">
                <span
                  v-if="book.available"
                  class="font-mono text-[9px] tracking-widest uppercase px-1.5 py-0.5 rounded-sm bg-[#2a5c3a]/90 text-[#6fcf97] backdrop-blur-sm border border-[#6fcf97]/30"
                >
                  Disponibil
                </span>
                <span
                  v-else
                  class="font-mono text-[9px] tracking-widest uppercase px-1.5 py-0.5 rounded-sm bg-[#ff3d5a]/90 text-white backdrop-blur-sm border border-white/30"
                >
                  Indisponibil
                </span>
            </div>
            <!-- Stock Badge -->
            <div class="absolute bottom-2 right-2">
                <span class="font-mono text-[9px] bg-dark/80 backdrop-blur-sm text-white px-1.5 py-0.5 rounded-sm border border-white/20">
                  {{ book.stoc_disponibil }}/{{ book.stoc_total }}
                </span>
            </div>
          </div>

          <!-- Book Info -->
          <div class="p-3 flex-1 flex flex-col">
            <p class="font-mono text-[10px] uppercase tracking-wider mb-1 text-[#7a5a55] truncate">
              {{ book.genre || 'General' }}
            </p>
            <h3 class="text-sm font-semibold leading-tight mb-1 line-clamp-2 text-[#2a1410]">
              {{ book.title }}
            </h3>
            <p class="text-xs text-[#7a5a55] truncate mt-auto">{{ book.author }}</p>
          </div>
        </div>
      </div>

      <!-- Pagination Controls -->
      <div v-if="totalPages > 1" class="flex justify-center items-center gap-4 mt-12">
        <button 
          @click="currentPage > 1 ? currentPage-- : null"
          :disabled="currentPage === 1"
          class="px-4 py-2 rounded-sm font-mono text-xs uppercase tracking-wider transition-colors border"
          :class="currentPage === 1 ? 'border-[#2a1410]/10 text-[#7a5a55]/50 bg-cream-dark cursor-not-allowed' : 'border-[#2a1410]/20 text-[#2a1410] hover:bg-[#c9a84c] hover:border-[#c9a84c]'"
        >
          <i class="pi pi-chevron-left mr-1 text-[10px]"></i> Înapoi
        </button>
        
        <span class="font-mono text-xs uppercase tracking-wider text-[#7a5a55]">
          Pagina <span class="text-[#2a1410] font-bold">{{ currentPage }}</span> din <span class="text-[#2a1410] font-bold">{{ totalPages }}</span>
        </span>

        <button 
          @click="currentPage < totalPages ? currentPage++ : null"
          :disabled="currentPage === totalPages"
          class="px-4 py-2 rounded-sm font-mono text-xs uppercase tracking-wider transition-colors border"
          :class="currentPage === totalPages ? 'border-[#2a1410]/10 text-[#7a5a55]/50 bg-cream-dark cursor-not-allowed' : 'border-[#2a1410]/20 text-[#2a1410] hover:bg-[#c9a84c] hover:border-[#c9a84c]'"
        >
          Înainte <i class="pi pi-chevron-right ml-1 text-[10px]"></i>
        </button>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-20 bg-white border border-[#2a1410]/10 rounded-sm">
        <div class="w-16 h-16 rounded-full bg-cream-dark flex items-center justify-center mx-auto mb-4">
          <i class="pi pi-book text-2xl text-[#2a1410]/30"></i>
        </div>
        <h3 class="text-lg font-bold font-display uppercase tracking-tight text-[#2a1410] mb-2">Nicio carte găsită</h3>
        <p class="text-[#7a5a55] text-sm mb-6">Modifică filtrele sau caută cu alt cuvânt cheie</p>
        <button 
          @click="clearFilters"
          class="px-5 py-2.5 rounded-sm font-mono text-xs uppercase tracking-wider transition-colors bg-[#c9a84c] text-dark hover:opacity-90"
        >
          Șterge Filtre
        </button>
      </div>
    </main>

    <!-- Book Detail Modal -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="showModal = false">
      <div class="absolute inset-0 bg-dark/80 backdrop-blur-sm" @click="showModal = false"></div>
      
      <div class="relative bg-cream rounded-sm shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto z-10 border border-[#c9a84c]/20 custom-scrollbar">
        <!-- Header -->
        <div class="sticky top-0 bg-dark px-6 py-5 border-b border-white/10 flex items-start gap-5 z-20">
          <img
            v-if="selectedBook"
            :src="`/api/books/image/${selectedBook.id}`"
            :alt="selectedBook.title"
            class="w-20 h-28 object-cover rounded-sm flex-shrink-0 shadow-lg border border-white/10"
            @error="$event.target.style.display='none'"
          >
          <div class="flex-1 min-w-0 pr-8">
            <span class="inline-block text-[10px] font-mono tracking-widest uppercase text-[#c9a84c] mb-1">
              {{ selectedBook?.genre || 'General' }}
            </span>
            <h3 class="text-xl sm:text-2xl font-black font-display tracking-tight text-white leading-tight mb-1">{{ selectedBook?.title }}</h3>
            <p class="text-white/70 text-sm font-medium">de {{ selectedBook?.author }}</p>
          </div>
          <button @click="showModal = false" class="absolute top-4 right-4 text-white/40 hover:text-white transition-colors bg-white/5 hover:bg-white/10 p-2 rounded-sm">
            <i class="pi pi-times"></i>
          </button>
        </div>

        <!-- Book Info & Action Buttons -->
        <div class="px-6 py-5 bg-white border-b border-[#2a1410]/10 flex flex-col md:flex-row md:items-center justify-between gap-6">
           <div class="flex gap-8 text-sm">
             <div>
               <p class="font-mono text-[10px] tracking-widest uppercase text-[#7a5a55] mb-0.5">Stoc Disponibil</p>
               <p class="font-bold text-[#2a1410] text-lg">{{ selectedBook?.stoc_disponibil }} <span class="text-sm font-normal text-[#7a5a55]">/ {{ selectedBook?.stoc_total }}</span></p>
             </div>
             <div v-if="selectedBook?.pozitie">
               <p class="font-mono text-[10px] tracking-widest uppercase text-[#7a5a55] mb-0.5">Poziție</p>
               <p class="font-bold text-[#2a1410] mt-1">{{ selectedBook.pozitie }}</p>
             </div>
             <div>
               <p class="font-mono text-[10px] tracking-widest uppercase text-[#7a5a55] mb-0.5">ISBN</p>
               <p class="font-mono text-xs text-[#2a1410] mt-1.5">{{ selectedBook?.ISBN || 'N/A' }}</p>
             </div>
           </div>

           <div class="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
              <button
                @click="requestFizic"
                :disabled="requestingFizic || !selectedBook?.available"
                :class="[
                  'flex items-center justify-center gap-2 px-5 py-2.5 rounded-sm text-xs font-mono tracking-wider uppercase transition-all whitespace-nowrap',
                  selectedBook?.available
                    ? 'bg-[#c9a84c] text-dark hover:opacity-90'
                    : 'bg-[#2a1410]/5 text-[#7a5a55] cursor-not-allowed border border-[#2a1410]/10'
                ]"
              >
                <i :class="requestingFizic ? 'pi pi-spin pi-spinner' : 'pi pi-book'" class="text-sm"></i>
                {{ requestingFizic ? 'Se trimite...' : 'Împrumută Fizic' }}
              </button>
              <a
                v-if="selectedBook?.has_pdf"
                :href="`/api/books/pdf/${selectedBook.id}`"
                target="_blank"
                class="flex items-center justify-center gap-2 px-5 py-2.5 rounded-sm text-xs font-mono tracking-wider uppercase transition-all bg-secondary text-white hover:bg-secondary/90 whitespace-nowrap"
              >
                <i class="pi pi-file-pdf text-sm"></i> Citește PDF
              </a>
           </div>
        </div>

        <div v-if="requestMessage" :class="[
          'mx-6 mt-4 px-4 py-3 border rounded-sm text-sm font-medium transition-all',
          requestSuccess ? 'bg-[#2a5c3a]/10 border-[#2a5c3a]/20 text-[#2a5c3a]' : 'bg-[#9b1b30]/10 border-[#9b1b30]/20 text-[#9b1b30]'
        ]">
          {{ requestMessage }}
        </div>

        <!-- Rating & AI Summary -->
        <div class="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-[#2a1410]/10 bg-cream border-b border-[#2a1410]/10">
           <div class="p-6">
              <div class="flex items-center gap-5">
                <div class="text-5xl font-black font-display text-[#2a1410]">{{ avgRating }}</div>
                <div>
                  <div class="flex items-center gap-1 text-lg">
                    <span v-for="star in 5" :key="star" :class="star <= Math.round(avgRating) ? 'text-[#c9a84c]' : 'text-[#2a1410]/15'">★</span>
                  </div>
                  <p class="font-mono text-[10px] tracking-widest uppercase text-[#7a5a55] mt-1">{{ totalReviews }} RECENZII</p>
                </div>
              </div>
           </div>

           <div class="p-6 bg-white flex flex-col justify-center">
              <div class="flex items-center justify-between mb-2">
                <h4 class="font-mono text-[10px] tracking-widest uppercase text-[#7a5a55] flex items-center gap-1.5">
                  <i class="pi pi-sparkles text-[#c9a84c]"></i> Rezumat AI
                </h4>
                <button v-if="reviews.length > 0" @click="loadAiSummary" :disabled="loadingAiSummary" class="text-[10px] font-mono tracking-widest uppercase text-secondary hover:underline disabled:opacity-50 flex items-center gap-1">
                   <i :class="loadingAiSummary ? 'pi pi-spin pi-spinner' : 'pi pi-refresh'"></i> Generează
                </button>
              </div>
              <div v-if="loadingAiSummary" class="py-2 text-[#7a5a55] font-mono text-xs"><i class="pi pi-spin pi-spinner"></i> Generare în curs...</div>
              <div v-else-if="aiSummary" class="text-xs text-[#2a1410] leading-relaxed italic font-serif">{{ aiSummary }}</div>
              <div v-else class="text-xs text-[#7a5a55] italic font-serif">Apasă pe generează pentru a obține un rezumat bazat pe recenzii.</div>
           </div>
        </div>

        <!-- Write Review -->
        <div v-if="isLoggedIn" class="px-6 py-6 bg-white border-b border-[#2a1410]/10">
          <h4 class="font-bold text-[#2a1410] mb-4 text-sm font-display tracking-tight uppercase">Scrie o Recenzie</h4>
          <div class="flex gap-1 mb-3">
            <button
              v-for="s in 5" :key="s"
              @click="reviewNota = s"
              :class="s <= reviewNota ? 'text-[#c9a84c]' : 'text-[#2a1410]/10'"
              class="text-2xl leading-none hover:scale-110 transition-transform"
            >★</button>
          </div>
          <textarea
            v-model="reviewText"
            rows="3"
            placeholder="Scrie părerea ta despre carte..."
            class="w-full text-sm px-4 py-3 rounded-sm border border-[#2a1410]/10 focus:outline-none focus:border-[#c9a84c] resize-none bg-cream-dark placeholder-[#7a5a55]/50 text-[#2a1410]"
          ></textarea>

          <div class="flex flex-col sm:flex-row items-center justify-between mt-3 gap-4">
            <div class="flex items-center gap-3 w-full sm:w-auto">
              <button
                @click="aiAssistReview"
                :disabled="loadingAiReview || !reviewText.trim()"
                class="text-[10px] font-mono tracking-widest uppercase text-secondary hover:underline disabled:opacity-50 flex items-center gap-1.5"
              >
                <i :class="loadingAiReview ? 'pi pi-spin pi-spinner' : 'pi pi-sparkles'"></i>
                Îmbunătățește cu AI
              </button>
              <span v-if="aiReviewError" class="text-[10px] text-red-500 font-mono">{{ aiReviewError }}</span>
            </div>

            <div class="flex items-center gap-3 w-full sm:w-auto justify-end">
              <span v-if="reviewMessage" :class="reviewSuccess ? 'text-green-600' : 'text-red-500'" class="text-[10px] font-mono tracking-wider uppercase">{{ reviewMessage }}</span>
              <button
                @click="submitReview"
                :disabled="submittingReview || !reviewText.trim() || reviewNota === 0"
                class="px-5 py-2.5 bg-[#c9a84c] hover:opacity-90 text-dark text-[10px] font-mono tracking-widest uppercase font-bold rounded-sm disabled:opacity-50 transition-colors flex items-center gap-2 w-full sm:w-auto justify-center"
              >
                <i :class="submittingReview ? 'pi pi-spin pi-spinner' : 'pi pi-send'" class="text-[10px]"></i>
                Trimite
              </button>
            </div>
          </div>
        </div>

        <!-- Reviews List -->
        <div class="px-6 py-6 bg-cream">
          <h4 class="font-bold text-[#2a1410] mb-5 text-sm font-display tracking-tight uppercase">Recenzii ({{ reviews.length }})</h4>

          <div v-if="loadingReviews" class="text-center py-8">
            <i class="pi pi-spin pi-spinner text-xl text-secondary"></i>
          </div>
          <div v-else-if="reviews.length === 0" class="text-center py-8">
            <p class="text-[#7a5a55] font-serif italic text-sm">Nicio recenzie încă. Fii primul care își spune părerea!</p>
          </div>
          <div v-else class="space-y-4">
            <div v-for="review in reviews" :key="review.id" class="bg-white rounded-sm p-5 border border-[#2a1410]/5 shadow-[0_1px_3px_rgba(42,20,16,0.03)]">
              <div class="flex items-center justify-between mb-3">
                <span class="font-bold text-[#2a1410] text-sm">{{ review.username }}</span>
                <div class="flex items-center gap-1">
                  <span v-for="star in 5" :key="star" :class="star <= review.nota ? 'text-[#c9a84c]' : 'text-[#2a1410]/10'" class="text-[10px]">★</span>
                </div>
              </div>
              <p class="text-[#3b2b18] text-sm font-serif italic leading-relaxed">{{ review.comentariu }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import localforage from 'localforage';

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
      currentPage: 1,
      itemsPerPage: 12,
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
    paginatedBooks() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredBooks.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredBooks.length / this.itemsPerPage);
    },
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
        // Încercăm să luăm datele din cache (localforage/IndexedDB) mai întâi pentru afișare instantanee
        const cachedBooks = await localforage.getItem('cachedBookList');
        if (cachedBooks && cachedBooks.length > 0) {
          this.allBooks = cachedBooks;
          this.filterBooks();
        }

        // Preluăm datele proaspete din rețea
        const response = await fetch('/api/books');
        const data = await response.json();
        if (data.books) {
          const freshBooks = data.books.map(book => ({
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

          // Actualizăm UI-ul și cache-ul doar dacă datele s-au schimbat sau cache-ul era gol
          if (!cachedBooks || JSON.stringify(cachedBooks) !== JSON.stringify(freshBooks)) {
            this.allBooks = freshBooks;
            this.filterBooks();
            await localforage.setItem('cachedBookList', freshBooks);
          }
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
      this.currentPage = 1; // Resetează la pagina 1 la aplicarea filtrelor noi
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
