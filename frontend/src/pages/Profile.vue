<template>
  <div id="app" class="min-h-screen bg-white">
    <!-- Hero Section -->
    <section class="bg-gradient-to-b from-secondary to-dark py-8 sm:py-16 shadow-gold">
      <div class="max-w-full mx-auto px-3 sm:px-4 text-center">
        <h2 class="text-2xl sm:text-4xl font-bold text-gold mb-2 sm:mb-4 glow-gold">Profilul Meu</h2>
        <p class="text-primary text-xs sm:text-lg mb-4 sm:mb-8">Bine ai revenit, {{ user.name }}</p>
      </div>
    </section>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-3 sm:px-4 py-8 sm:py-12">
      <!-- Profile Header Section -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8 mb-8 sm:mb-12">
        <!-- Profile Card -->
        <div class="md:col-span-1">
          <div class="bg-gradient-to-b from-secondary to-dark rounded-lg shadow-dark-lg border-2 border-gold p-4 sm:p-8 card-hover text-center">
            <!-- Profile Picture -->
            <div class="mb-4 sm:mb-6">
              <div class="w-24 sm:w-32 h-24 sm:h-32 mx-auto rounded-full bg-gold shadow-dark-lg border-4 border-gold overflow-hidden">
                <img 
                  :src="user.profilePicture" 
                  :alt="user.name"
                  class="w-full h-full object-cover"
                >
              </div>
            </div>

            <!-- User Info -->
            <h1 class="text-xl sm:text-3xl font-bold text-gold mb-1 sm:mb-2 glow-gold">{{ user.name }}</h1>
            <p class="text-primary mb-3 sm:mb-4 text-xs sm:text-sm font-semibold">Membru din {{ user.joinDate }}</p>
            
            <!-- Description -->
            <p v-if="user.description" class="text-white mb-4 sm:mb-6 text-xs sm:text-sm leading-relaxed">
              {{ user.description }}
            </p>

            <!-- Stats Row -->
            <div class="grid grid-cols-2 gap-2 sm:gap-4 mb-3 sm:mb-4">
              <div class="bg-dark rounded-lg p-2 sm:p-4 border-l-4 border-gold">
                <p class="text-2xl sm:text-3xl font-bold text-gold">{{ user.totalBooksRead }}</p>
                <p class="text-primary text-xs mt-1">Cărți</p>
              </div>
              <div class="bg-dark rounded-lg p-2 sm:p-4 border-l-4 border-gold">
                <p class="text-2xl sm:text-3xl font-bold text-gold">{{ user.averageRating }}</p>
                <p class="text-primary text-xs mt-1">Evaluare</p>
              </div>
            </div>

            <button @click="openEditModal" class="w-full mt-4 sm:mt-6 bg-gradient-to-r from-gold to-primary hover:shadow-gold text-dark font-bold py-2 px-3 sm:px-4 rounded-lg text-xs sm:text-base transition-all duration-300 transform hover:scale-105 btn-glow">
              Editează Profil
            </button>
          </div>
        </div>

        <!-- Quick Stats -->
        <div class="md:col-span-2 space-y-4 sm:space-y-6">
          <!-- Favorite Genre -->
          <div class="bg-dark rounded-lg shadow-dark-lg border-2 border-gold p-4 sm:p-8 card-hover">
            <h3 class="text-lg sm:text-2xl font-bold text-gold mb-3 sm:mb-4 flex items-center gap-2 glow-gold">
              <span class="text-2xl sm:text-3xl">🎯</span> Gen Preferat
            </h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
              <div v-for="(genre, index) in user.favoriteGenres" :key="index" class="bg-gradient-to-b from-secondary to-dark rounded-lg p-3 sm:p-4 border-l-4 border-gold shadow-gold card-hover">
                <h4 class="text-base sm:text-lg font-bold text-gold mb-2">{{ genre.name }}</h4>
                <p class="text-white text-xs sm:text-sm mb-2">Cărți: <span class="font-semibold">{{ genre.count }}</span></p>
                <div class="w-full bg-gold rounded-full h-2 overflow-hidden">
                  <div class="bg-primary h-full rounded-full" :style="{ width: genre.percentage + '%' }"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Member Stats -->
          <div class="bg-dark rounded-lg shadow-dark-lg border-2 border-gold p-4 sm:p-8 card-hover">
            <h3 class="text-lg sm:text-2xl font-bold text-gold mb-3 sm:mb-4 flex items-center gap-2 glow-gold">
              <span class="text-2xl sm:text-3xl">📊</span> Statistici
            </h3>
            <div class="grid grid-cols-3 gap-2 sm:gap-4">
              <div class="text-center p-2 sm:p-4 bg-gradient-to-b from-secondary to-dark rounded-lg border-l-4 border-gold shadow-gold text-xs sm:text-base">
                <p class="text-2xl sm:text-3xl font-bold text-gold">{{ user.currentlyReading }}</p>
                <p class="text-primary text-xs mt-1">Citesc</p>
              </div>
              <div class="text-center p-2 sm:p-4 bg-gradient-to-b from-secondary to-dark rounded-lg border-l-4 border-gold shadow-gold text-xs sm:text-base">
                <p class="text-2xl sm:text-3xl font-bold text-gold">{{ user.wantToRead }}</p>
                <p class="text-primary text-xs mt-1">Vreau</p>
              </div>
              <div class="text-center p-2 sm:p-4 bg-gradient-to-b from-secondary to-dark rounded-lg border-l-4 border-gold shadow-gold text-xs sm:text-base">
                <p class="text-2xl sm:text-3xl font-bold text-gold">{{ user.yearsActive }}</p>
                <p class="text-primary text-xs mt-1">Ani</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Books Read Section -->
      <div class="mb-8 sm:mb-12">
        <h2 class="text-xl sm:text-3xl font-bold text-gold mb-4 sm:mb-6 flex items-center gap-2 glow-gold">
          <i class="pi pi-book text-2xl sm:text-4xl"></i> Cărțile Citite
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          <div 
            v-for="(book, index) in user.booksRead" 
            :key="index"
            class="bg-gradient-to-b from-secondary to-dark rounded-lg shadow-dark-lg border-2 border-gold p-3 sm:p-6 card-hover text-center"
          >
            <!-- Book Cover -->
            <div class="mb-3 sm:mb-4 h-32 sm:h-40 rounded-lg bg-gold shadow-dark-lg overflow-hidden">
              <img 
                :src="book.cover" 
                :alt="book.title"
                class="w-full h-full object-cover"
              >
            </div>
            
            <!-- Book Info -->
            <h3 class="text-sm sm:text-lg font-bold text-gold mb-1">{{ book.title }}</h3>
            <p class="text-primary text-xs sm:text-sm mb-2">{{ book.author }}</p>
            
            <!-- Rating -->
            <div class="flex justify-center items-center gap-1 mb-2 sm:mb-3">
              <span 
                v-for="star in 5" 
                :key="star"
                :class="['text-lg sm:text-2xl', star <= book.rating ? 'text-gold' : 'text-gray-600']"
              >
                ★
              </span>
            </div>
            
            <!-- Read Date -->
            <p class="text-white text-xs">Citit: {{ book.readDate }}</p>
          </div>
        </div>
      </div>

      <!-- Ratings Given Section -->
      <div class="mb-12">
        <h2 class="text-xl sm:text-3xl font-bold text-gold mb-4 sm:mb-6 flex items-center gap-2 glow-gold">
          <i class="pi pi-star text-2xl sm:text-4xl"></i> Evalurile Mele
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
          <div 
            v-for="(rating, index) in user.ratingsGiven" 
            :key="index"
            class="bg-gradient-to-b from-secondary to-dark rounded-lg shadow-dark-lg border-2 border-gold p-4 sm:p-6 card-hover"
          >
            <!-- Rating Header -->
            <div class="flex items-start justify-between mb-3 sm:mb-4 gap-2">
              <div class="min-w-0">
                <h3 class="text-base sm:text-xl font-bold text-gold break-words">{{ rating.book }}</h3>
                <p class="text-primary text-xs sm:text-sm">de {{ rating.author }}</p>
              </div>
              <div class="bg-gold text-dark rounded-full w-10 h-10 sm:w-12 sm:h-12 flex items-center justify-center font-bold text-sm sm:text-lg flex-shrink-0">
                {{ rating.score }}
              </div>
            </div>

            <!-- Rating Stars -->
            <div class="flex items-center gap-1 mb-3 sm:mb-4">
              <span 
                v-for="star in 5" 
                :key="star"
                :class="['text-lg sm:text-2xl', star <= Math.floor(rating.score) ? 'text-gold' : 'text-gray-600']"
              >
                ★
              </span>
            </div>

            <!-- Review Comment -->
            <p class="text-white text-xs sm:text-sm leading-relaxed mb-3">
              {{ rating.comment }}
            </p>

            <!-- Rating Date -->
            <p class="text-primary text-xs">Evaluat: {{ rating.date }}</p>
          </div>
        </div>
      </div>
    </main>

    <!-- Edit Profile Modal -->
    <div v-if="editModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4" @click.self="closeEditModal">
      <div class="w-full max-w-lg bg-gradient-to-b from-secondary to-dark rounded-lg shadow-dark-lg border-2 border-gold p-6 sm:p-8">
        <!-- Modal Header -->
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl sm:text-2xl font-bold text-gold glow-gold">Editează Profil</h2>
          <button @click="closeEditModal" class="text-white hover:text-gold text-2xl font-bold transition-colors duration-200">&times;</button>
        </div>

        <!-- Description Label -->
        <label class="block text-gold font-semibold mb-2 text-sm sm:text-base">Descriere</label>

        <!-- Description Textarea -->
        <textarea
          v-model="editDescription"
          rows="5"
          maxlength="255"
          placeholder="Scrie ceva despre tine..."
          class="w-full px-3 sm:px-4 py-2 sm:py-3 rounded-lg bg-dark border-2 border-gold text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gold transition-all duration-200 text-xs sm:text-base resize-none"
        ></textarea>
        <p class="text-primary text-xs mt-1 text-right">{{ editDescription.length }} / 255</p>

        <!-- Messages -->
        <div v-if="editErrorMessage" class="mt-3 bg-accent bg-opacity-20 border-l-4 border-accent rounded-lg p-3">
          <p class="text-accent text-xs sm:text-sm">{{ editErrorMessage }}</p>
        </div>
        <div v-if="editSuccessMessage" class="mt-3 bg-primary bg-opacity-20 border-l-4 border-primary rounded-lg p-3">
          <p class="text-primary text-xs sm:text-sm">{{ editSuccessMessage }}</p>
        </div>

        <!-- Buttons -->
        <div class="mt-6 flex flex-col sm:flex-row gap-3">
          <button
            @click="saveDescription"
            :disabled="savingDescription"
            class="flex-1 bg-gradient-to-r from-gold to-primary hover:shadow-gold text-dark font-bold py-2 sm:py-3 px-4 rounded-lg text-sm sm:text-base transition-all duration-300 transform hover:scale-105 btn-glow disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ savingDescription ? 'Se salvează...' : 'Modifică' }}
          </button>
          <button
            @click="closeEditModal"
            class="flex-1 border-2 border-gold text-gold hover:bg-gold hover:text-dark font-bold py-2 sm:py-3 px-4 rounded-lg text-sm sm:text-base transition-all duration-300"
          >
            Anulează
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  data() {
    return {
      user: {
        name: '',
        profilePicture: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Profile',
        joinDate: 'Ianuarie 2023',
        description: null,
        totalBooksRead: 24,
        averageRating: 4.2,
        currentlyReading: 3,
        wantToRead: 12,
        yearsActive: 2,
        favoriteGenres: [
          { name: 'Ficțiune Știintifică', count: 8, percentage: 80 },
          { name: 'Fantezie', count: 7, percentage: 70 }
        ],
        booksRead: [
          {
            title: 'The Midnight Library',
            author: 'Matt Haig',
            rating: 5,
            readDate: 'mar 2026',
            cover: 'https://images.unsplash.com/photo-1507842217343-583f20270319?w=200&h=300&fit=crop'
          },
          {
            title: 'Dune',
            author: 'Frank Herbert',
            rating: 5,
            readDate: 'feb 2026',
            cover: 'https://images.unsplash.com/photo-1535274335684-82a01c61f026?w=200&h=300&fit=crop'
          },
          {
            title: 'Project Hail Mary',
            author: 'Andy Weir',
            rating: 4,
            readDate: 'ian 2026',
            cover: 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=200&h=300&fit=crop'
          },
          {
            title: 'The Silent Patient',
            author: 'Alex Michaelides',
            rating: 4,
            readDate: 'dec 2025',
            cover: 'https://images.unsplash.com/photo-1569495253292-c5e36ba2904f?w=200&h=300&fit=crop'
          }
        ],
        ratingsGiven: [
          {
            book: 'The Midnight Library',
            author: 'Matt Haig',
            score: 5,
            comment: 'O carte absolut minunată! Conceptul de a explora ale‛y de viață diferite este att filosofic cât și profund emotionant. Foarte recomandă pentru oricine caută inspirație.',
            date: 'mar 2026'
          },
          {
            book: 'Dune',
            author: 'Frank Herbert',
            score: 5,
            comment: 'O capodoperă epicală a ficțiunii știintifice. Construcția lumii este extraordinară, iar intriga politică m-a menținut angrenat pe toată durata. O carte obligatorie pentru toți fănii sci-fi.',
            date: 'feb 2026'
          },
          {
            book: 'Ínvățământ',
            author: 'Tara Westover',
            score: 4,
            comment: 'O biografie puternică și revelatoră. Desăvrșit intensă la momente, ea oferă o perspectivă fascinantă asupra familiei, educației și creșterii personale.',
            date: 'ian 2026'
          }
        ]
      },
      editModalOpen: false,
      editDescription: '',
      editErrorMessage: '',
      editSuccessMessage: '',
      savingDescription: false
    }
  },
  mounted() {
    this.loadProfile()
  },
  methods: {
    openEditModal() {
      this.editDescription = this.user.description || ''
      this.editErrorMessage = ''
      this.editSuccessMessage = ''
      this.editModalOpen = true
    },
    closeEditModal() {
      this.editModalOpen = false
    },
    async saveDescription() {
      const email = localStorage.getItem('userEmail')
      if (!email) {
        this.editErrorMessage = 'Utilizatorul nu este autentificat.'
        return
      }
      this.savingDescription = true
      this.editErrorMessage = ''
      this.editSuccessMessage = ''

      try {
        const response = await fetch('/api/auth/profile', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, description: this.editDescription })
        })
        const data = await response.json()

        if (!response.ok) {
          this.editErrorMessage = data.message || 'Nu s-a putut actualiza descrierea.'
          return
        }

        this.user.description = this.editDescription || null
        this.editSuccessMessage = 'Descriere actualizată cu succes!'
        setTimeout(() => {
          this.editModalOpen = false
        }, 1200)
      } catch (error) {
        this.editErrorMessage = 'Eroare de rețea. Încearcă din nou.'
      } finally {
        this.savingDescription = false
      }
    },
    async loadProfile() {
      const email = localStorage.getItem('userEmail')
      if (!email) {
        this.$router.push('/login')
        return
      }

      try {
        const response = await fetch(`/api/auth/profile?email=${encodeURIComponent(email)}`)
        const data = await response.json()

        if (!response.ok) {
          console.error('Profile load failed:', data.message)
          this.$router.push('/login')
          return
        }

        this.user.name = data.username || ''
        this.user.description = data.description || null
      } catch (error) {
        console.error('Profile fetch error:', error)
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style scoped>
</style>
