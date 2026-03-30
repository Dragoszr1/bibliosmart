<template>
  <div id="app" class="min-h-screen">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-secondary via-dark to-accent py-8 sm:py-16 shadow-elegant relative overflow-hidden">
      <div class="absolute inset-0 gradient-overlay opacity-30"></div>
      <div class="max-w-full mx-auto px-3 sm:px-4 text-center relative z-10">
        <h2 class="text-2xl sm:text-4xl font-bold text-gradient mb-2 sm:mb-4 glow-gold">Profilul Meu</h2>
        <p class="text-cream text-xs sm:text-lg mb-4 sm:mb-8 opacity-90">Bine ai revenit, {{ user.name }}</p>
      </div>
    </section>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-3 sm:px-4 py-8 sm:py-12">
      <!-- Profile Header Section -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8 mb-8 sm:mb-12">
        <!-- Profile Card -->
        <div class="md:col-span-1">
          <div class="bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 p-4 sm:p-8 card-hover text-center">
            <!-- Profile Picture -->
            <div class="mb-4 sm:mb-6 relative group">
              <div class="w-24 sm:w-32 h-24 sm:h-32 mx-auto rounded-full bg-cream-dark shadow-elegant border-4 border-secondary/40 overflow-hidden">
                <img 
                  :src="user.profilePicture" 
                  :alt="user.name"
                  class="w-full h-full object-cover"
                  @error="user.profilePicture = 'https://api.dicebear.com/7.x/avataaars/svg?seed=Profile'"
                >
              </div>
              <!-- Upload overlay -->
              <div 
                @click="triggerFileInput"
                class="absolute inset-0 flex items-center justify-center cursor-pointer"
              >
                <div class="w-24 sm:w-32 h-24 sm:h-32 mx-auto rounded-full bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center">
                  <i class="pi pi-camera text-white text-xl sm:text-2xl"></i>
                </div>
              </div>
              <input 
                ref="fileInput"
                type="file"
                accept="image/png,image/jpeg,image/jpg,image/gif,image/webp"
                class="hidden"
                @change="uploadProfilePicture"
              >
            </div>

            <!-- User Info -->
            <h1 class="text-xl sm:text-3xl font-bold text-secondary mb-1 sm:mb-2">{{ user.name }}</h1>
            <p class="text-gray-500 mb-3 sm:mb-4 text-xs sm:text-sm font-semibold">Membru din {{ user.joinDate }}</p>
            
            <!-- Description -->
            <p v-if="user.description" class="text-gray-700 mb-4 sm:mb-6 text-xs sm:text-sm leading-relaxed">
              {{ user.description }}
            </p>

            <!-- Stats Row -->
            <div class="grid grid-cols-2 gap-2 sm:gap-4 mb-3 sm:mb-4">
              <div class="bg-cream-dark rounded-lg p-2 sm:p-4 border-l-4 border-secondary">
                <p class="text-2xl sm:text-3xl font-bold text-secondary">{{ user.totalBooksRead }}</p>
                <p class="text-gray-500 text-xs mt-1">Cărți</p>
              </div>
              <div class="bg-cream-dark rounded-lg p-2 sm:p-4 border-l-4 border-secondary">
                <p class="text-2xl sm:text-3xl font-bold text-secondary">{{ user.averageRating }}</p>
                <p class="text-gray-500 text-xs mt-1">Evaluare</p>
              </div>
            </div>

            <button @click="openEditModal" class="w-full mt-4 sm:mt-6 bg-gradient-to-r from-secondary to-accent hover:shadow-lg text-white font-bold py-2 px-3 sm:px-4 rounded-lg text-xs sm:text-base transition-all duration-300 transform hover:scale-105">
              Editează Profil
            </button>
          </div>
        </div>

        <!-- Quick Stats -->
        <div class="md:col-span-2 space-y-4 sm:space-y-6">
          <!-- Favorite Genre -->
          <div class="bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 p-4 sm:p-8 card-hover">
            <h3 class="text-lg sm:text-2xl font-bold text-secondary mb-3 sm:mb-4 flex items-center gap-2">
              <span class="text-2xl sm:text-3xl">🎯</span> Gen Preferat
            </h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
              <div v-for="(genre, index) in user.favoriteGenres" :key="index" class="bg-cream-dark rounded-lg p-3 sm:p-4 border-l-4 border-secondary shadow-sm card-hover">
                <h4 class="text-base sm:text-lg font-bold text-dark mb-2">{{ genre.name }}</h4>
                <p class="text-gray-700 text-xs sm:text-sm mb-2">Cărți: <span class="font-semibold">{{ genre.count }}</span></p>
                <div class="w-full bg-cream rounded-full h-2 overflow-hidden border border-secondary/20">
                  <div class="bg-secondary h-full rounded-full" :style="{ width: genre.percentage + '%' }"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Member Stats -->
          <div class="bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 p-4 sm:p-8 card-hover">
            <h3 class="text-lg sm:text-2xl font-bold text-secondary mb-3 sm:mb-4 flex items-center gap-2">
              <span class="text-2xl sm:text-3xl">📊</span> Statistici
            </h3>
            <div class="grid grid-cols-3 gap-2 sm:gap-4">
              <div class="text-center p-2 sm:p-4 bg-cream-dark rounded-lg border-l-4 border-secondary shadow-sm text-xs sm:text-base">
                <p class="text-2xl sm:text-3xl font-bold text-secondary">{{ user.currentlyReading }}</p>
                <p class="text-gray-500 text-xs mt-1">Citesc</p>
              </div>
              <div class="text-center p-2 sm:p-4 bg-cream-dark rounded-lg border-l-4 border-secondary shadow-sm text-xs sm:text-base">
                <p class="text-2xl sm:text-3xl font-bold text-secondary">{{ user.wantToRead }}</p>
                <p class="text-gray-500 text-xs mt-1">Vreau</p>
              </div>
              <div class="text-center p-2 sm:p-4 bg-cream-dark rounded-lg border-l-4 border-secondary shadow-sm text-xs sm:text-base">
                <p class="text-2xl sm:text-3xl font-bold text-secondary">{{ user.yearsActive }}</p>
                <p class="text-gray-500 text-xs mt-1">Ani</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Books Read Section -->
      <div class="mb-8 sm:mb-12">
        <h2 class="text-xl sm:text-3xl font-bold text-secondary mb-4 sm:mb-6 flex items-center gap-2">
          <i class="pi pi-book text-2xl sm:text-4xl"></i> Cărțile Citite
        </h2>

        <!-- Empty state -->
        <div v-if="user.booksRead.length === 0" class="bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 p-8 sm:p-12 text-center">
          <i class="pi pi-book text-4xl sm:text-5xl text-secondary mb-4"></i>
          <p class="text-gray-600 text-sm sm:text-lg">Nici o carte citită</p>
        </div>

        <!-- Books grid -->
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          <div 
            v-for="(book, index) in user.booksRead" 
            :key="index"
            class="bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 p-3 sm:p-6 card-hover text-center"
          >
            <!-- Book Icon -->
            <div class="mb-3 sm:mb-4 h-32 sm:h-40 rounded-lg bg-cream-dark border border-secondary/20 flex items-center justify-center">
              <i class="pi pi-book text-5xl sm:text-6xl text-secondary"></i>
            </div>
            
            <!-- Book Info -->
            <h3 class="text-sm sm:text-lg font-bold text-dark mb-1">{{ book.titlu }}</h3>
            <p class="text-gray-500 text-xs sm:text-sm mb-1">{{ book.autor }}</p>
            <p class="text-gray-600 text-xs">ISBN: {{ book.ISBN }}</p>
          </div>
        </div>
      </div>

      <!-- Ratings Given Section -->
      <div class="mb-12">
        <h2 class="text-xl sm:text-3xl font-bold text-secondary mb-4 sm:mb-6 flex items-center gap-2">
          <i class="pi pi-star text-2xl sm:text-4xl"></i> Evalurile Mele
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
          <div 
            v-for="(rating, index) in user.ratingsGiven" 
            :key="index"
            class="bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 p-4 sm:p-6 card-hover"
          >
            <!-- Rating Header -->
            <div class="flex items-start justify-between mb-3 sm:mb-4 gap-2">
              <div class="min-w-0">
                <h3 class="text-base sm:text-xl font-bold text-dark break-words">{{ rating.book }}</h3>
                <p class="text-gray-500 text-xs sm:text-sm">de {{ rating.author }}</p>
              </div>
              <div class="bg-secondary text-white rounded-full w-10 h-10 sm:w-12 sm:h-12 flex items-center justify-center font-bold text-sm sm:text-lg flex-shrink-0">
                {{ rating.score }}
              </div>
            </div>

            <!-- Rating Stars -->
            <div class="flex items-center gap-1 mb-3 sm:mb-4">
              <span 
                v-for="star in 5" 
                :key="star"
                :class="['text-lg sm:text-2xl', star <= Math.floor(rating.score) ? 'text-accent' : 'text-gray-300']"
              >
                ★
              </span>
            </div>

            <!-- Review Comment -->
            <p class="text-gray-700 text-xs sm:text-sm leading-relaxed mb-3">
              {{ rating.comment }}
            </p>

            <!-- Rating Date -->
            <p class="text-gray-500 text-xs">Evaluat: {{ rating.date }}</p>
          </div>
        </div>
      </div>
    </main>

    <!-- Edit Profile Modal -->
    <div v-if="editModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4" @click.self="closeEditModal">
      <div class="w-full max-w-lg bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 p-6 sm:p-8">
        <!-- Modal Header -->
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl sm:text-2xl font-bold text-secondary">Editează Profil</h2>
          <button @click="closeEditModal" class="text-gray-500 hover:text-secondary text-2xl font-bold transition-colors duration-200">&times;</button>
        </div>

        <!-- Description Label -->
        <label class="block text-dark font-semibold mb-2 text-sm sm:text-base">Descriere</label>

        <!-- Description Textarea -->
        <textarea
          v-model="editDescription"
          rows="5"
          maxlength="255"
          placeholder="Scrie ceva despre tine..."
          class="w-full px-3 sm:px-4 py-2 sm:py-3 rounded-lg bg-cream-dark border-2 border-secondary/30 text-dark placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary/50 transition-all duration-200 text-xs sm:text-base resize-none"
        ></textarea>
        <p class="text-gray-500 text-xs mt-1 text-right">{{ editDescription.length }} / 255</p>

        <!-- Messages -->
        <div v-if="editErrorMessage" class="mt-3 bg-accent/10 border-l-4 border-accent rounded-lg p-3">
          <p class="text-accent text-xs sm:text-sm">{{ editErrorMessage }}</p>
        </div>
        <div v-if="editSuccessMessage" class="mt-3 bg-green-50 border-l-4 border-green-500 rounded-lg p-3">
          <p class="text-green-700 text-xs sm:text-sm">{{ editSuccessMessage }}</p>
        </div>

        <!-- Buttons -->
        <div class="mt-6 flex flex-col sm:flex-row gap-3">
          <button
            @click="saveDescription"
            :disabled="savingDescription"
            class="flex-1 bg-gradient-to-r from-secondary to-accent hover:shadow-lg text-white font-bold py-2 sm:py-3 px-4 rounded-lg text-sm sm:text-base transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ savingDescription ? 'Se salvează...' : 'Modifică' }}
          </button>
          <button
            @click="closeEditModal"
            class="flex-1 border-2 border-secondary text-secondary hover:bg-secondary hover:text-white font-bold py-2 sm:py-3 px-4 rounded-lg text-sm sm:text-base transition-all duration-300"
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
        booksRead: [],
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
    triggerFileInput() {
      this.$refs.fileInput.click()
    },
    async uploadProfilePicture(event) {
      const file = event.target.files[0]
      if (!file) return

      const email = localStorage.getItem('userEmail')
      if (!email) return

      const formData = new FormData()
      formData.append('file', file)
      formData.append('email', email)

      try {
        const response = await fetch('/api/auth/profile-picture', {
          method: 'POST',
          body: formData
        })
        const data = await response.json()

        if (response.ok) {
          // Reload profile picture with cache bust
          this.loadProfilePicture(this.user.name)
        } else {
          console.error('Upload failed:', data.message)
        }
      } catch (error) {
        console.error('Upload error:', error)
      }

      // Reset file input so the same file can be selected again
      this.$refs.fileInput.value = ''
    },
    loadProfilePicture(username) {
      if (!username) return
      // Add timestamp to bust cache after upload
      this.user.profilePicture = `/api/auth/profile-picture/${encodeURIComponent(username)}?t=${Date.now()}`
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

        // Load profile picture from backend
        this.loadProfilePicture(data.username)

        // Fetch books read by this user
        if (data.user_id) {
          this.loadBooksRead(data.user_id)
        }
      } catch (error) {
        console.error('Profile fetch error:', error)
        this.$router.push('/login')
      }
    },
    async loadBooksRead(userId) {
      try {
        const response = await fetch(`/api/auth/books-read?user_id=${userId}`)
        const data = await response.json()
        if (response.ok && data.books) {
          this.user.booksRead = data.books
          this.user.totalBooksRead = data.books.length
        }
      } catch (error) {
        console.error('Books read fetch error:', error)
      }
    }
  }
}
</script>

<style scoped>
</style>
