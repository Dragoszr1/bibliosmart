<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-dark py-16 sm:py-24 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-secondary/20 via-transparent to-accent/10"></div>
      <div class="max-w-3xl mx-auto px-6 text-center relative z-10">
        <h2 class="text-3xl sm:text-5xl font-bold text-white mb-3 tracking-tight">Bine ai venit la Biblioteca</h2>
        <p class="text-white/80 text-sm sm:text-base font-medium mb-2">Colegiului Național de Informatică „Spiru-Haret"</p>
        <p class="text-white/45 text-sm sm:text-base italic">„Locul unde cunoașterea prinde viață"</p>
      </div>
    </section>

    <!-- Main Content -->
    <main class="w-full max-w-[1440px] mx-auto px-4 sm:px-6 py-10 sm:py-14 flex flex-col xl:grid xl:grid-cols-[1fr_auto_1fr] gap-6 xl:gap-8">
      
      <!-- Left Spacer for centering -->
      <div class="hidden xl:block"></div>

      <!-- Center Column: Announcements & Features -->
      <div class="w-full max-w-3xl mx-auto space-y-16">
        
        <!-- Announcements -->
        <section>
          <div class="flex items-center gap-3 mb-8">
            <h2 class="text-2xl font-bold text-dark">Anunțuri</h2>
            <div class="flex-1 h-px bg-gray-200"></div>
          </div>

          <!-- Loading -->
          <div v-if="loadingAnunturi" class="text-center py-16">
            <i class="pi pi-spin pi-spinner text-2xl text-secondary"></i>
          </div>

          <!-- Announcements List -->
          <div v-else class="space-y-4">
            <article 
              v-for="a in anunturi" 
              :key="a.anunt_id"
              class="bg-white rounded-xl p-5 sm:p-6 shadow-card border border-gray-100 hover:shadow-elevated transition-shadow duration-200"
            >
              <div class="flex items-start justify-between gap-4 mb-3">
                <h3 class="text-lg font-semibold text-dark">{{ a.titlu }}</h3>
                <time class="text-xs text-gray-400 whitespace-nowrap mt-1">{{ a.data_publicare }}</time>
              </div>
              <p class="text-gray-600 text-sm leading-relaxed whitespace-pre-line mb-4">{{ a.anunt }}</p>
              <button 
                @click="toggleLike(a)"
                :class="[
                  'inline-flex items-center gap-1.5 text-sm font-medium px-3 py-1.5 rounded-full transition-all duration-150',
                  a.liked 
                    ? 'bg-secondary/10 text-secondary' 
                    : 'text-gray-400 hover:text-secondary hover:bg-secondary/5'
                ]"
              >
                <i :class="a.liked ? 'pi pi-thumbs-up-fill' : 'pi pi-thumbs-up'" class="text-xs"></i>
                <span>{{ a.aprecieri }}</span>
              </button>
            </article>

            <!-- Empty State -->
            <div v-if="anunturi.length === 0" class="text-center py-16">
              <div class="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-4">
                <i class="pi pi-megaphone text-2xl text-gray-300"></i>
              </div>
              <p class="text-gray-500">Nu sunt anunțuri deocamdată.</p>
            </div>
          </div>
        </section>

        <!-- Features Section -->
        <section>
          <div class="flex items-center gap-3 mb-8">
            <h2 class="text-2xl font-bold text-dark">Facilități</h2>
            <div class="flex-1 h-px bg-gray-200"></div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="flex gap-4 p-5 rounded-xl bg-white shadow-card border border-gray-100">
              <div class="w-10 h-10 rounded-lg bg-secondary/10 flex items-center justify-center flex-shrink-0">
                <i class="pi pi-book text-secondary text-lg"></i>
              </div>
              <div>
                <h4 class="font-semibold text-dark mb-1 text-sm">Colecție Vastă</h4>
                <p class="text-gray-500 text-sm">Mii de cărți în toate genurile</p>
              </div>
            </div>
            <div class="flex gap-4 p-5 rounded-xl bg-white shadow-card border border-gray-100">
              <div class="w-10 h-10 rounded-lg bg-accent/10 flex items-center justify-center flex-shrink-0">
                <i class="pi pi-compass text-accent text-lg"></i>
              </div>
              <div>
                <h4 class="font-semibold text-dark mb-1 text-sm">Ușor de Utilizat</h4>
                <p class="text-gray-500 text-sm">Navigare simplă și intuitivă pe platformă</p>
              </div>
            </div>
            <div class="flex gap-4 p-5 rounded-xl bg-white shadow-card border border-gray-100">
              <div class="w-10 h-10 rounded-lg bg-secondary/10 flex items-center justify-center flex-shrink-0">
                <i class="pi pi-sync text-secondary text-lg"></i>
              </div>
              <div>
                <h4 class="font-semibold text-dark mb-1 text-sm">Împrumut Ușor</h4>
                <p class="text-gray-500 text-sm">Proces simplu de împrumut</p>
              </div>
            </div>
            <div class="flex gap-4 p-5 rounded-xl bg-white shadow-card border border-gray-100">
              <div class="w-10 h-10 rounded-lg bg-accent/10 flex items-center justify-center flex-shrink-0">
                <i class="pi pi-tablet text-accent text-lg"></i>
              </div>
              <div>
                <h4 class="font-semibold text-dark mb-1 text-sm">Acces Digital</h4>
                <p class="text-gray-500 text-sm">Cărți electronice și resurse</p>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- Right Column: Recent Books Widget -->
      <div class="w-full max-w-sm mx-auto xl:mx-0">
        <aside class="bg-white rounded-xl shadow-card border border-gray-100 p-5 sm:p-6 sticky top-24">
          <div class="flex items-center gap-3 mb-6">
            <h3 class="text-xl font-bold text-dark">Cărți Noi</h3>
            <div class="flex-1 h-px bg-gray-200"></div>
          </div>
          
          <!-- Loading state -->
          <div v-if="loadingCarti" class="flex justify-center py-8">
            <i class="pi pi-spin pi-spinner text-2xl text-secondary"></i>
          </div>
          
          <div v-else-if="cartiRecente.length === 0" class="text-center py-8">
            <p class="text-sm text-gray-500">Nu am găsit cărți.</p>
          </div>
          
          <div v-else class="space-y-5">
            <div 
              v-for="carte in cartiRecente" 
              :key="carte.carte_id"
              class="flex gap-4 items-center group cursor-pointer"
              @click="$router.push('/books')"
            >
              <div class="w-16 h-24 bg-gray-200 rounded-md overflow-hidden flex-shrink-0 relative shadow-sm group-hover:shadow-md transition-shadow">
                <img :src="`/api/books/image/${carte.carte_id}`" @error="$event.target.src='https://placehold.co/100x150/e2e8f0/64748b?text=Carte'" alt="Book Cover" class="w-full h-full object-cover" />
              </div>
              <div class="flex-1">
                <h4 class="text-sm font-semibold text-dark group-hover:text-secondary transition-colors line-clamp-2">{{ carte.titlu }}</h4>
                <p class="text-xs text-gray-500 mt-1">{{ carte.autor }}</p>
                <div class="mt-2 flex items-center gap-2">
                  <span class="text-[10px] font-bold px-2 py-0.5 bg-secondary/10 text-secondary rounded-full truncate max-w-[120px]">{{ carte.gen || 'General' }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <button @click="$router.push('/books')" class="w-full mt-6 py-2.5 rounded-lg border border-gray-200 text-sm font-semibold text-dark hover:bg-gray-50 transition-colors flex items-center justify-center gap-2">
            <span>Vezi colecția completă</span>
            <i class="pi pi-arrow-right text-xs"></i>
          </button>
        </aside>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      anunturi: [],
      loadingAnunturi: false,
      isLoggedIn: false,
      cartiRecente: [],
      loadingCarti: false
    }
  },
  mounted() {
    this.fetchAnunturi()
    this.checkAuth()
    this.fetchCartiRecente()
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
    async fetchCartiRecente() {
      this.loadingCarti = true
      try {
        const res = await fetch('/api/books/recent')
        const data = await res.json()
        if (data.success) {
          this.cartiRecente = data.books
        }
      } catch (error) {
        console.error('Error fetching recent books:', error)
      } finally {
        this.loadingCarti = false
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
