<template>
  <div class="min-h-screen bg-gradient-to-b from-white to-gray-200">
    <!-- Hero Section -->
    <section class="bg-gradient-to-b from-secondary to-dark py-8 sm:py-16 shadow-gold">
      <div class="max-w-full mx-auto px-4 text-center">
        <h2 class="text-2xl sm:text-4xl font-bold text-gold mb-2 sm:mb-4 glow-gold">Explorez Cărțile</h2>
        <p class="text-primary text-sm sm:text-lg mb-4 sm:mb-8">Descoperiți cărți magice din colecția noastră vastă</p>
      </div>
    </section>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-3 sm:px-4 py-8 sm:py-12">
      <!-- Fancy Search Bar -->
      <div class="mb-8 sm:mb-12">
        <div class="relative">
          <div class="bg-gradient-to-r from-secondary to-dark rounded-lg sm:rounded-2xl shadow-dark-lg border-2 border-gold p-4 sm:p-8 card-hover">
            <div class="flex flex-col sm:flex-row items-center gap-3 sm:gap-4">
              <i class="pi pi-search hidden sm:block text-5xl text-gold"></i>
              <div class="flex-1 w-full sm:w-auto">
                <input
                  v-model="searchQuery"
                  @input="filterBooks"
                  type="text"
                  placeholder="Caută după titlu, autor..."
                  class="w-full px-4 sm:px-6 py-3 sm:py-4 rounded-lg sm:rounded-xl bg-dark border-2 border-gold text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gold transition-all duration-200 text-sm sm:text-lg"
                >
                <p class="text-primary text-xs sm:text-sm mt-2 sm:mt-3 hidden sm:block">💡 Sugestie: Caută după titlu, autor sau gen</p>
              </div>
              <button class="w-full sm:w-auto bg-gradient-to-r from-gold to-primary hover:shadow-gold text-dark font-bold py-3 sm:py-4 px-6 sm:px-8 rounded-lg sm:rounded-xl transition-all duration-300 transform hover:scale-105 btn-glow text-sm sm:text-base">
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
            class="lg:hidden w-full mb-4 bg-gradient-to-r from-gold to-primary hover:shadow-gold text-dark font-bold py-3 px-4 rounded-lg transition-all duration-300 flex items-center justify-between text-sm sm:text-base"
          >
            <span class="flex items-center gap-2">
              <span>🎯</span>
              <span>{{ filtersOpen ? 'Ascunde' : 'Afișează' }} Filtre</span>
            </span>
            <span class="text-lg">{{ filtersOpen ? '▲' : '▼' }}</span>
          </button>
          
          <!-- Filter Sidebar -->
          <div v-show="filtersOpen" class="lg:block bg-gradient-to-b from-secondary to-dark rounded-lg shadow-dark-lg border-2 border-gold sticky top-24 p-4 sm:p-6 card-hover">
            <h3 class="text-lg sm:text-2xl font-bold text-gold mb-4 sm:mb-6 hidden lg:flex items-center gap-2 glow-gold">
              <span class="text-3xl">🎯</span> Filtre
            </h3>

            <!-- Genre Filter -->
            <div class="mb-6 sm:mb-8">
              <h4 class="text-base sm:text-lg font-bold text-gold mb-3 sm:mb-4">Gen</h4>
              <div class="space-y-2 sm:space-y-3">
                <label 
                  v-for="genre in genres"
                  :key="genre"
                  class="flex items-center gap-3 cursor-pointer group text-sm sm:text-base"
                >
                  <input
                    type="checkbox"
                    :value="genre"
                    v-model="selectedGenres"
                    @change="filterBooks"
                    class="w-5 h-5 rounded border-gold text-gold focus:ring-gold cursor-pointer"
                  >
                  <span class="text-white group-hover:text-gold transition-colors duration-200">{{ genre }}</span>
                </label>
              </div>
            </div>

            <!-- Rating Filter -->
            <div class="mb-6 sm:mb-8">
              <h4 class="text-base sm:text-lg font-bold text-gold mb-3 sm:mb-4">Evaluare Minimă</h4>
              <div class="space-y-2 sm:space-y-3">
                <label 
                  v-for="rating in [5, 4, 3, 2]"
                  :key="rating"
                  class="flex items-center gap-3 cursor-pointer group text-sm sm:text-base"
                >
                  <input
                    type="radio"
                    :value="rating"
                    v-model="minRating"
                    @change="filterBooks"
                    class="w-5 h-5 rounded-full border-gold text-gold focus:ring-gold cursor-pointer"
                  >
                  <div class="flex items-center gap-1">
                    <span v-for="star in rating" :key="star" class="text-gold">★</span>
                    <span class="text-white group-hover:text-gold transition-colors duration-200 ml-2">{{ rating }}+</span>
                  </div>
                </label>
              </div>
              <label class="flex items-center gap-3 cursor-pointer group mt-3 text-sm sm:text-base">
                <input
                  type="radio"
                  :value="0"
                  v-model="minRating"
                  @change="filterBooks"
                  class="w-5 h-5 rounded-full border-gold text-gold focus:ring-gold cursor-pointer"
                >
                <span class="text-white group-hover:text-gold transition-colors duration-200">Toate</span>
              </label>
            </div>

            <!-- Availability Filter -->
            <div class="mb-6 sm:mb-8">
              <h4 class="text-base sm:text-lg font-bold text-gold mb-3 sm:mb-4">Disponibilitate</h4>
              <div class="space-y-2 sm:space-y-3">
                <label class="flex items-center gap-3 cursor-pointer group text-sm sm:text-base">
                  <input
                    type="checkbox"
                    v-model="showAvailableOnly"
                    @change="filterBooks"
                    class="w-5 h-5 rounded border-gold text-gold focus:ring-gold cursor-pointer"
                  >
                  <span class="text-white group-hover:text-gold transition-colors duration-200">Doar disponibile</span>
                </label>
              </div>
            </div>

            <!-- Clear Filters -->
            <button 
              @click="clearFilters"
              class="w-full bg-gradient-to-r from-gold to-primary hover:shadow-gold text-dark font-bold py-2 sm:py-3 px-4 rounded-lg transition-all duration-300 transform hover:scale-105 btn-glow text-sm sm:text-base"
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
              S-au găsit <span class="text-gold text-lg sm:text-xl">{{ filteredBooks.length }}</span> cărți
            </p>
            <div class="flex gap-2 flex-wrap sm:flex-nowrap">
              <button 
                @click="sortBy('title')"
                :class="['px-3 sm:px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm transition-all duration-300', sortType === 'title' ? 'bg-gold text-dark shadow-gold' : 'bg-secondary text-gold border-2 border-gold hover:bg-gold hover:text-dark']"
              >
                A-Z
              </button>
              <button 
                @click="sortBy('rating')"
                :class="['px-3 sm:px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm transition-all duration-300', sortType === 'rating' ? 'bg-gold text-dark shadow-gold' : 'bg-secondary text-gold border-2 border-gold hover:bg-gold hover:text-dark']"
              >
                <i class="pi pi-star"></i>
              </button>
              <button 
                @click="sortBy('newest')"
                :class="['px-3 sm:px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm transition-all duration-300', sortType === 'newest' ? 'bg-gold text-dark shadow-gold' : 'bg-secondary text-gold border-2 border-gold hover:bg-gold hover:text-dark']"
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
              class="bg-gradient-to-b from-secondary to-dark rounded-lg shadow-dark-lg border-2 border-gold overflow-hidden card-hover hover:shadow-gold transition-all duration-300 group cursor-pointer flex flex-col"
            >
              <!-- Book Cover -->
              <div class="relative overflow-hidden h-48 sm:h-56 md:h-64 bg-gold">
                <img 
                  :src="book.cover" 
                  :alt="book.title"
                  class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                >
                <!-- Availability Badge -->
                <div 
                  :class="[
                    'absolute top-2 right-2 text-xs sm:text-sm px-2 sm:px-3 py-1 rounded-full font-bold shadow-gold',
                    book.available ? 'bg-primary text-white' : 'bg-accent text-white'
                  ]"
                >
                  <i :class="book.available ? 'pi pi-check-circle' : 'pi pi-times-circle'"></i>
                </div>
                <!-- Rating Badge -->
                <div class="absolute top-2 left-2 bg-gold text-dark text-xs sm:text-sm px-2 sm:px-3 py-1 rounded-full font-bold shadow-gold">
                  <i class="pi pi-star"></i> {{ book.rating }}
                </div>
              </div>

              <!-- Book Info -->
              <div class="p-3 sm:p-4 md:p-6 flex-1 flex flex-col">
                <!-- Title -->
                <h3 class="text-sm sm:text-base md:text-lg font-bold text-gold mb-1 line-clamp-2 group-hover:text-primary transition-colors duration-200">
                  {{ book.title }}
                </h3>

                <!-- Author -->
                <p class="text-primary text-xs sm:text-sm mb-2">de {{ book.author }}</p>

                <!-- Genre Badge -->
                <div class="mb-2 sm:mb-3 flex flex-wrap gap-1">
                  <span class="text-xs bg-secondary text-gold px-2 py-1 rounded-full border-l-2 border-gold">
                    {{ book.genre }}
                  </span>
                </div>

                <!-- Description -->
                <p class="text-white text-xs sm:text-sm mb-3 line-clamp-2">
                  {{ book.description }}
                </p>

                <!-- Stats -->
                <div class="grid grid-cols-2 gap-2 my-2 sm:my-3">
                  <div class="text-center p-1 sm:p-2 bg-dark rounded-lg border-l-2 border-gold text-xs">
                    <p class="text-gold font-bold">{{ book.pages }}</p>
                    <p class="text-primary text-xs" style="font-size: 0.65rem;">Pag</p>
                  </div>
                  <div class="text-center p-1 sm:p-2 bg-dark rounded-lg border-l-2 border-gold text-xs">
                    <p class="text-gold font-bold">{{ book.year }}</p>
                    <p class="text-primary text-xs" style="font-size: 0.65rem;">An</p>
                  </div>
                </div>

                <!-- Action Buttons -->
                <div class="flex gap-2">
                  <button 
                    :disabled="!book.available"
                    :class="[
                      'flex-1 font-bold py-2 px-2 sm:px-3 rounded-lg text-xs sm:text-sm transition-all duration-300 transform hover:scale-105',
                      book.available 
                        ? 'bg-gradient-to-r from-gold to-primary hover:shadow-gold text-dark btn-glow' 
                        : 'bg-gray-500 text-white cursor-not-allowed'
                    ]"
                  >
                    {{ book.available ? '📥' : '❌' }}
                  </button>
                  <button class="flex-1 bg-secondary hover:bg-dark border-2 border-gold text-gold font-bold py-2 px-2 sm:px-3 rounded-lg text-xs sm:text-sm transition-all duration-300 transform hover:scale-105">
                    <i class="pi pi-info-circle"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else class="bg-gradient-to-b from-secondary to-dark rounded-lg shadow-dark-lg border-2 border-gold p-8 sm:p-12 text-center">
            <i class="pi pi-book text-4xl mb-4 text-gold"></i>
            <h3 class="text-xl sm:text-2xl font-bold text-gold mb-3">Nicio carte găsită</h3>
            <p class="text-white mb-6 text-sm sm:text-base">Încearcă să modifici filtrele sau cauta cu alt cuvânt cheie</p>
            <button 
              @click="clearFilters"
              class="bg-gradient-to-r from-gold to-primary hover:shadow-gold text-dark font-bold py-2 sm:py-3 px-6 sm:px-8 rounded-lg text-sm sm:text-base transition-all duration-300 transform hover:scale-105 btn-glow"
            >
              Șterge Filtre
            </button>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'Books',
  data() {
    return {
      searchQuery: '',
      selectedGenres: [],
      minRating: 0,
      showAvailableOnly: false,
      sortType: 'newest',
      filtersOpen: false,
      genres: ['Ficțiune Științifică', 'Fantezie', 'Mister', 'Romantism', 'Biografie', 'Istorie', 'Tehnologie', 'Dezvoltare Personală'],
      allBooks: [
        {
          title: 'The Midnight Library',
          author: 'Matt Haig',
          genre: 'Ficțiune Științifică',
          rating: 5,
          pages: 288,
          year: 2020,
          cover: 'https://images.unsplash.com/photo-1507842217343-583f20270319?w=300&h=400&fit=crop',
          available: true,
          description: 'O poveste profundă despre vieți netrăite și alegeri care ne definesc.'
        },
        {
          title: 'Dune',
          author: 'Frank Herbert',
          genre: 'Ficțiune Științifică',
          rating: 5,
          pages: 688,
          year: 1965,
          cover: 'https://images.unsplash.com/photo-1535274335684-82a01c61f026?w=300&h=400&fit=crop',
          available: true,
          description: 'O epopee cosmică despre putere, religie și politică în viitorul îndepărtat.'
        },
        {
          title: 'Project Hail Mary',
          author: 'Andy Weir',
          genre: 'Ficțiune Științifică',
          rating: 4,
          pages: 476,
          year: 2021,
          cover: 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=300&h=400&fit=crop',
          available: false,
          description: 'Un om trebuie să salveze omenirea cu ajutorul unui extraterestru prietenos.'
        },
        {
          title: 'The Silent Patient',
          author: 'Alex Michaelides',
          genre: 'Mister',
          rating: 4,
          pages: 336,
          year: 2019,
          cover: 'https://images.unsplash.com/photo-1569495253292-c5e36ba2904f?w=300&h=400&fit=crop',
          available: true,
          description: 'Un thriller psihologic cu un tărâm șocant și periculos.'
        },
        {
          title: 'Educated',
          author: 'Tara Westover',
          genre: 'Biografie',
          rating: 4,
          pages: 352,
          year: 2018,
          cover: 'https://images.unsplash.com/photo-1543002588-d4d8c2dfee02?w=300&h=400&fit=crop',
          available: true,
          description: 'Descopă cum educația i-a transformat viața unei femei extraordinare.'
        },
        {
          title: 'The Name of the Wind',
          author: 'Patrick Rothfuss',
          genre: 'Fantezie',
          rating: 5,
          pages: 662,
          year: 2007,
          cover: 'https://images.unsplash.com/photo-1546960072-91f25e37b725?w=300&h=400&fit=crop',
          available: true,
          description: 'Povestea unui magician legendariu, spusă de el însuși.'
        },
        {
          title: 'A Brief History of Time',
          author: 'Stephen Hawking',
          genre: 'Tehnologie',
          rating: 4,
          pages: 256,
          year: 1988,
          cover: 'https://images.unsplash.com/photo-1507842217343-583f20270319?w=300&h=400&fit=crop',
          available: true,
          description: 'Explorează misterele universului și ale timpului.'
        },
        {
          title: 'The Ambition',
          author: 'John Doe',
          genre: 'Dezvoltare Personală',
          rating: 4,
          pages: 320,
          year: 2022,
          cover: 'https://images.unsplash.com/photo-1544716278-ca5e3af4abd8?w=300&h=400&fit=crop',
          available: true,
          description: 'Ghid practic pentru a-ți atinge visurile și să devii cea mai bună versiune a ta.'
        },
        {
          title: 'The Murder Mystery',
          author: 'Jane Smith',
          genre: 'Mister',
          rating: 4,
          pages: 384,
          year: 2021,
          cover: 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=300&h=400&fit=crop',
          available: false,
          description: 'Un caz confuz care va tine în suspans până la final uimitor.'
        },
        {
          title: 'The Sword of Kalevala',
          author: 'Sarah Connor',
          genre: 'Fantezie',
          rating: 5,
          pages: 512,
          year: 2020,
          cover: 'https://images.unsplash.com/photo-1507842217343-583f20270319?w=300&h=400&fit=crop',
          available: true,
          description: 'Într-o lume magică, o erou trebuie să salveze regnul de la distrugere.'
        },
        {
          title: 'Digital Transformation',
          author: 'Thomas Anderson',
          genre: 'Tehnologie',
          rating: 4,
          pages: 424,
          year: 2023,
          cover: 'https://images.unsplash.com/photo-1495446815901-a7297e3ffe02?w=300&h=400&fit=crop',
          available: true,
          description: 'Cum să transformi o afacere pentru era digitală.'
        },
        {
          title: 'Love in Paris',
          author: 'Emma Louise',
          genre: 'Romantism',
          rating: 3,
          pages: 298,
          year: 2022,
          cover: 'https://images.unsplash.com/photo-1507842217343-583f20270319?w=300&h=400&fit=crop',
          available: true,
          description: 'O poveste de dragoste in inima Parisului care va face inima ta sa bată mai repede.'
        }
      ],
      filteredBooks: []
    }
  },
  methods: {
    filterBooks() {
      let result = this.allBooks;

      // Filtru de căutare
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(book =>
          book.title.toLowerCase().includes(query) ||
          book.author.toLowerCase().includes(query) ||
          book.genre.toLowerCase().includes(query) ||
          book.description.toLowerCase().includes(query)
        );
      }

      // Filtru de gen
      if (this.selectedGenres.length > 0) {
        result = result.filter(book =>
          this.selectedGenres.includes(book.genre)
        );
      }

      // Filtru de evaluare
      if (this.minRating > 0) {
        result = result.filter(book => book.rating >= this.minRating);
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
        case 'rating':
          books.sort((a, b) => b.rating - a.rating);
          break;
        case 'newest':
          books.sort((a, b) => b.year - a.year);
          break;
      }
    },
    sortBy(type) {
      this.sortType = type;
      this.filterBooks();
    },
    clearFilters() {
      this.searchQuery = '';
      this.selectedGenres = [];
      this.minRating = 0;
      this.showAvailableOnly = false;
      this.sortType = 'newest';
      this.filterBooks();
    }
  },
  mounted() {
    // Inițializează listele filtrelor
    this.filterBooks();
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
