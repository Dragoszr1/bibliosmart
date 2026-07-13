<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-dark py-20 sm:py-32 relative overflow-hidden flex items-center min-h-[400px]">
      <div class="absolute inset-0 z-0">
        <img src="/hero-bg.jpg" alt="Library Background" class="w-full h-full object-cover opacity-60" />
        <div class="absolute inset-0 bg-gradient-to-r from-dark/90 via-dark/50 to-transparent"></div>
      </div>
      <div class="w-full max-w-[1440px] mx-auto px-6 relative z-10">
        <div class="max-w-2xl text-center sm:text-left flex flex-col items-center sm:items-start mx-auto sm:mx-0">
          <!-- Decoration -->
          <img src="/logo.webp" alt="Biblioteca Logo" class="h-24 w-24 sm:h-28 sm:w-28 rounded-2xl shadow-2xl mb-6 border-2 border-white/10 hover:scale-105 transition-transform duration-300" />
          
          <h2 class="text-4xl sm:text-6xl font-extrabold text-white mb-4 tracking-tight drop-shadow-lg font-display">Bine ai venit la Biblioteca</h2>
          <p class="text-white/90 text-lg sm:text-xl font-medium mb-3 tracking-wide drop-shadow-md">Colegiului Național de Informatică „Spiru-Haret"</p>
          
          <div class="flex items-center justify-center sm:justify-start gap-4 mt-6 w-full">
             <div class="h-px flex-1 max-w-[50px] sm:hidden bg-gradient-to-l from-accent to-transparent"></div>
             <p class="text-accent/90 text-sm sm:text-base italic font-serif tracking-widest shrink-0">„Locul unde cunoașterea prinde viață"</p>
             <div class="h-px flex-1 max-w-[100px] bg-gradient-to-r from-accent to-transparent"></div>
          </div>
        </div>
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
            <DecoratedBox 
              v-for="a in anunturi" 
              :key="a.anunt_id"
            >
              <template #heading>
                <div class="flex items-start justify-between gap-4 text-left">
                  <span class="text-xl font-bold">{{ a.titlu }}</span>
                  <time class="text-xs text-[#8b4513]/70 whitespace-nowrap mt-1 font-sans">{{ a.data_publicare }}</time>
                </div>
              </template>
              <p class="text-[#3b2b18] text-sm leading-relaxed whitespace-pre-line mb-4 font-sans">{{ a.anunt }}</p>
              <button 
                @click="toggleLike(a)"
                :class="[
                  'inline-flex items-center gap-1.5 text-sm font-medium px-3 py-1.5 rounded-full transition-all duration-150 font-sans',
                  a.liked 
                    ? 'bg-[#8b4513]/10 text-[#8b4513]' 
                    : 'text-[#8b4513]/50 hover:text-[#8b4513] hover:bg-[#8b4513]/5'
                ]"
              >
                <i :class="a.liked ? 'pi pi-thumbs-up-fill' : 'pi pi-thumbs-up'" class="text-xs"></i>
                <span>{{ a.aprecieri }}</span>
              </button>
            </DecoratedBox>

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
            <div class="flex-1 h-px bg-[#8b4513]/20"></div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="flex gap-4 p-5 rounded-xl bg-papyrus-light shadow-card border border-[#8b4513]/10">
              <div class="w-10 h-10 rounded-lg bg-[#8b4513]/10 flex items-center justify-center flex-shrink-0">
                <i class="pi pi-book text-[#8b4513] text-lg"></i>
              </div>
              <div>
                <h4 class="font-semibold text-dark mb-1 text-sm">Colecție Vastă</h4>
                <p class="text-[#8b4513]/70 text-sm">Mii de cărți în toate genurile</p>
              </div>
            </div>
            <div class="flex gap-4 p-5 rounded-xl bg-papyrus-light shadow-card border border-[#8b4513]/10">
              <div class="w-10 h-10 rounded-lg bg-[#8b4513]/10 flex items-center justify-center flex-shrink-0">
                <i class="pi pi-compass text-[#8b4513] text-lg"></i>
              </div>
              <div>
                <h4 class="font-semibold text-dark mb-1 text-sm">Ușor de Utilizat</h4>
                <p class="text-[#8b4513]/70 text-sm">Navigare simplă și intuitivă pe platformă</p>
              </div>
            </div>
            <div class="flex gap-4 p-5 rounded-xl bg-papyrus-light shadow-card border border-[#8b4513]/10">
              <div class="w-10 h-10 rounded-lg bg-[#8b4513]/10 flex items-center justify-center flex-shrink-0">
                <i class="pi pi-sync text-[#8b4513] text-lg"></i>
              </div>
              <div>
                <h4 class="font-semibold text-dark mb-1 text-sm">Împrumut Ușor</h4>
                <p class="text-[#8b4513]/70 text-sm">Proces simplu de împrumut</p>
              </div>
            </div>
            <div class="flex gap-4 p-5 rounded-xl bg-papyrus-light shadow-card border border-[#8b4513]/10">
              <div class="w-10 h-10 rounded-lg bg-[#8b4513]/10 flex items-center justify-center flex-shrink-0">
                <i class="pi pi-tablet text-[#8b4513] text-lg"></i>
              </div>
              <div>
                <h4 class="font-semibold text-dark mb-1 text-sm">Acces Digital</h4>
                <p class="text-[#8b4513]/70 text-sm">Cărți electronice și resurse</p>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- Right Column: Recent Books Widget -->
      <div class="w-full max-w-sm mx-auto xl:mx-0">
        <ScrollWidget class="sticky top-24">
          <template #title>Cărți Noi</template>
          
          <!-- Loading state -->
          <div v-if="loadingCarti" class="flex justify-center py-8">
            <i class="pi pi-spin pi-spinner text-2xl text-[#8b4513]"></i>
          </div>
          
          <div v-else-if="cartiRecente.length === 0" class="text-center py-8 text-[#856b50] font-medium">
            Nu am găsit cărți.
          </div>
          
          <div v-else class="space-y-5">
            <div 
              v-for="carte in cartiRecente" 
              :key="carte.carte_id"
              class="flex gap-4 items-center group cursor-pointer"
              @click="$router.push('/books')"
            >
              <div class="w-16 h-24 bg-[#cca36b]/20 rounded-md overflow-hidden flex-shrink-0 relative shadow-sm group-hover:shadow-md transition-shadow border border-[#cca36b]/30">
                <img :src="`/api/books/image/${carte.carte_id}`" @error="$event.target.src='https://placehold.co/100x150/e2e8f0/64748b?text=Carte'" alt="Book Cover" class="w-full h-full object-cover" />
              </div>
              <div class="flex-1">
                <h4 class="text-sm font-semibold text-[#4a2e15] group-hover:text-[#b88034] transition-colors line-clamp-2">{{ carte.titlu }}</h4>
                <p class="text-xs text-[#856b50] mt-1">{{ carte.autor }}</p>
                <div class="mt-2 flex items-center gap-2">
                  <span class="text-[10px] font-bold px-2 py-0.5 bg-[#8b4513]/10 text-[#8b4513] rounded-full truncate max-w-[120px]">{{ carte.gen || 'General' }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <template #footer>
            <button @click="$router.push('/books')" class="w-full flex items-center justify-center gap-2 border-2 border-[#cca36b] text-[#6b421c] py-2.5 rounded-lg hover:bg-[#f6e5c8] hover:border-[#b88034] transition-all duration-300 group">
              <span class="font-semibold">Vezi colecția completă</span>
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                class="h-5 w-5 transform group-hover:translate-x-1 transition-transform duration-300" 
                viewBox="0 0 20 20" 
                fill="currentColor"
              >
                <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </template>
        </ScrollWidget>
      </div>
    </main>
  </div>
</template>

<script>
import DecoratedBox from '../components/DecoratedBox.vue'
import ScrollWidget from '../components/ScrollWidget.vue'

export default {
  name: 'Home',
  components: { DecoratedBox, ScrollWidget },
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
