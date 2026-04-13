<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-secondary via-dark to-accent py-8 sm:py-16 shadow-elegant relative overflow-hidden">
      <div class="absolute inset-0 gradient-overlay opacity-30"></div>
      <div class="max-w-full mx-auto px-3 sm:px-4 text-center relative z-10">
        <h2 class="text-2xl sm:text-4xl font-bold text-white mb-2 sm:mb-4 glow-white tracking-tight">Bine ai venit la Biblioteca</h2>
        <p class="text-cream/80 text-xs sm:text-lg mb-4 sm:mb-8 font-light">Locul unde cunoașterea prinde viață</p>
      </div>
    </section>

    <!-- Main Content -->
    <main class="max-w-full mx-auto px-3 sm:px-4 py-8 sm:py-12">
      <div class="flex flex-col lg:flex-row gap-6 lg:gap-8">
        <!-- Left Sidebar - Top Readers (Hidden on mobile) -->
        <aside class="hidden lg:block w-full lg:w-72 lg:flex-shrink-0">
          <div class="bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 card-hover p-4 sm:p-6 sticky top-24">
            <h3 class="text-lg sm:text-2xl font-bold text-secondary mb-4 sm:mb-6 flex items-center gap-2">
              <i class="pi pi-trophy text-2xl sm:text-3xl text-secondary"></i>
              Top Cititori
            </h3>
            <div class="space-y-3 sm:space-y-4">
              <div
                v-for="(reader, index) in topReaders"
                :key="index"
                class="bg-cream-dark rounded-lg p-3 sm:p-4 border border-secondary/20 card-hover shadow-sm text-sm"
              >
                <div class="flex items-center justify-between mb-2">
                  <h4 class="text-dark font-bold">{{ reader.name }}</h4>
                  <span class="text-white text-xs font-semibold bg-secondary rounded-full px-2 py-1">{{ reader.rank }}</span>
                </div>
                <p class="text-gray-700 text-xs">
                  <i class="pi pi-book text-secondary mr-1"></i>
                  {{ reader.booksRead }} cărți
                </p>
                <div class="mt-2 bg-cream rounded-full h-2 overflow-hidden border border-secondary/20">
                  <div 
                    class="bg-secondary h-full rounded-full transition-all duration-500" 
                    :style="{ width: reader.progress + '%' }"
                  ></div>
                </div>
              </div>
            </div>
            <button class="w-full mt-4 sm:mt-6 bg-gradient-to-r from-secondary to-accent hover:shadow-lg text-white font-bold py-2 sm:py-3 px-4 rounded-lg text-xs sm:text-base transition-all duration-300 ">
              Toți Cititorii
            </button>
          </div>
        </aside>

        <!-- Main Content - Announcements -->
        <section class="flex-1 min-w-0">
          <!-- Announcements Section -->
          <div class="bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 card-hover p-4 sm:p-8">
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 sm:mb-8 gap-3">
              <h2 class="text-xl sm:text-3xl font-bold text-secondary flex items-center gap-2 sm:gap-3">
                <i class="pi pi-megaphone text-2xl sm:text-4xl text-accent"></i>
                Anunțuri
              </h2>
            </div>

            <!-- Loading -->
            <div v-if="loadingAnunturi" class="text-center py-12">
              <i class="pi pi-spin pi-spinner text-3xl text-secondary"></i>
            </div>

            <!-- Announcements List -->
            <div v-else class="space-y-4 sm:space-y-6">
              <div 
                v-for="a in anunturi" 
                :key="a.anunt_id"
                class="bg-cream-dark rounded-lg p-4 sm:p-6 border border-secondary/20 shadow-sm card-hover"
              >
                <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between mb-2 sm:mb-3 gap-2">
                  <div>
                    <h3 class="text-base sm:text-xl font-bold text-dark">{{ a.titlu }}</h3>
                    <p class="text-gray-500 text-xs sm:text-sm mt-1">
                      <i class="pi pi-calendar mr-1"></i>{{ a.data_publicare }}
                    </p>
                  </div>
                </div>
                <p class="text-gray-700 mb-3 sm:mb-4 text-xs sm:text-base whitespace-pre-line">{{ a.anunt }}</p>
                <div class="flex items-center gap-4 text-xs sm:text-sm">
                  <button 
                    @click="toggleLike(a)"
                    :class="[
                      'flex items-center gap-1.5 font-medium transition-all duration-200 px-3 py-1.5 rounded-full border',
                      a.liked 
                        ? 'bg-secondary/10 text-secondary border-secondary/40' 
                        : 'text-gray-500 hover:text-secondary border-transparent hover:border-secondary/30'
                    ]"
                  >
                    <i :class="a.liked ? 'pi pi-thumbs-up-fill' : 'pi pi-thumbs-up'"></i>
                    <span>{{ a.aprecieri }}</span>
                  </button>
                </div>
              </div>

              <!-- Empty State -->
              <div v-if="anunturi.length === 0" class="text-center py-8 sm:py-12">
                <i class="pi pi-megaphone text-4xl text-gray-300 mb-3"></i>
                <p class="text-gray-600 text-xs sm:text-lg">Nu sunt anunțuri deocamdată. Revino în curând!</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Right Sidebar - Reserved for Future Use (Hidden on mobile) -->
        <aside class="hidden lg:block w-full lg:w-72 lg:flex-shrink-0">
          <div class="bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 card-hover p-4 sm:p-6 sticky top-24">
            <h3 class="text-lg sm:text-2xl font-bold text-secondary mb-4">Curand</h3>
            <p class="text-gray-600 text-center py-6 sm:py-12 text-xs sm:text-base">
              Noi caracteristici și conțut vor fi adăugate aici curând!
            </p>
          </div>
        </aside>
      </div>

      <!-- Features Section -->
      <section class="bg-cream rounded-lg shadow-elegant p-4 sm:p-8 border-2 border-secondary/60 card-hover mt-8 sm:mt-12">
        <h2 class="text-xl sm:text-3xl font-bold text-secondary mb-4 sm:mb-6">De ce să Alegi Biblioteca?</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
          <div class="flex gap-3 sm:gap-4 p-3 sm:p-4 rounded-lg bg-cream-dark border border-secondary/20 shadow-sm card-hover">
            <i class="pi pi-check text-accent text-xl sm:text-2xl flex-shrink-0"></i>
            <div class="text-xs sm:text-base">
              <h4 class="font-bold text-dark mb-1">Colecție Vastă</h4>
              <p class="text-gray-700">Mii de cărți în toate genurile</p>
            </div>
          </div>
          <div class="flex gap-3 sm:gap-4 p-3 sm:p-4 rounded-lg bg-cream-dark border border-secondary/20 shadow-sm card-hover">
            <i class="pi pi-check text-accent text-xl sm:text-2xl flex-shrink-0"></i>
            <div class="text-xs sm:text-base">
              <h4 class="font-bold text-dark mb-1">Ghidare Expert</h4>
              <p class="text-gray-700">Bibliotecari gata să te ajute</p>
            </div>
          </div>
          <div class="flex gap-3 sm:gap-4 p-3 sm:p-4 rounded-lg bg-cream-dark border border-secondary/20 shadow-sm card-hover">
            <i class="pi pi-check text-accent text-xl sm:text-2xl flex-shrink-0"></i>
            <div class="text-xs sm:text-base">
              <h4 class="font-bold text-dark mb-1">Împrumut Ușor</h4>
              <p class="text-gray-700">Proces simplu de împrumut</p>
            </div>
          </div>
          <div class="flex gap-3 sm:gap-4 p-3 sm:p-4 rounded-lg bg-cream-dark border border-secondary/20 shadow-sm card-hover">
            <i class="pi pi-check text-accent text-xl sm:text-2xl flex-shrink-0"></i>
            <div class="text-xs sm:text-base">
              <h4 class="font-bold text-dark mb-1">Acces Digital</h4>
              <p class="text-gray-700">Cărți electronice și resurse</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>

export default {
  name: 'Home',
  data() {
    return {
      topReaders: [
        {
          name: 'Sarah Johnson',
          rank: '#1',
          booksRead: 24,
          progress: 95
        },
        {
          name: 'Michael Chen',
          rank: '#2',
          booksRead: 21,
          progress: 85
        },
        {
          name: 'Emma Wilson',
          rank: '#3',
          booksRead: 18,
          progress: 72
        },
        {
          name: 'David Martinez',
          rank: '#4',
          booksRead: 16,
          progress: 65
        },
        {
          name: 'Lisa Anderson',
          rank: '#5',
          booksRead: 14,
          progress: 58
        }
      ],
      anunturi: [],
      loadingAnunturi: false,
      isLoggedIn: false
    }
  },
  mounted() {
    this.fetchAnunturi()
    this.checkAuth()
  },
  methods: {
    async checkAuth() {
      try {
        const res = await fetch('/api/auth/me', { credentials: 'include' })
        this.isLoggedIn = res.ok
      } catch {
        this.isLoggedIn = false
      }
    },
    async fetchAnunturi() {
      this.loadingAnunturi = true
      try {
        const res = await fetch('/api/anunturi', { credentials: 'include' })
        const data = await res.json()
        if (data.success) {
          this.anunturi = data.anunturi
        }
      } catch (error) {
        console.error('Error fetching announcements:', error)
      } finally {
        this.loadingAnunturi = false
      }
    },
    async toggleLike(a) {
      if (!this.isLoggedIn) {
        this.$router.push('/login')
        return
      }
      try {
        const res = await fetch(`/api/anunturi/${a.anunt_id}/like`, {
          method: 'POST',
          credentials: 'include'
        })
        const data = await res.json()
        if (data.success) {
          a.liked = data.liked
          a.aprecieri = data.aprecieri
        }
      } catch (error) {
        console.error('Like error:', error)
      }
    }
  }
}
</script>

<style scoped>
</style>
