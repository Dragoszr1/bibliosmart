<template>
  <div class="font-sans text-[#2a1410] bg-cream">
    <!-- Hero Section -->
    <section class="relative overflow-hidden border-b border-[#ede0cc] min-h-[520px] flex items-center">
      <img
        src="https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=1600&h=900&fit=crop&auto=format"
        alt="Library bookshelves"
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

      <div class="max-w-7xl mx-auto px-6 py-20 md:py-28 relative w-full">
        <div class="max-w-2xl text-center sm:text-left flex flex-col items-center sm:items-start mx-auto sm:mx-0">
          <img src="/logo.webp" alt="Biblioteca Logo" class="h-28 w-28 sm:h-32 sm:w-32 rounded-2xl shadow-xl mb-6 border-2 border-white/10 hover:scale-105 transition-transform duration-300" />
          
          <h2 class="text-5xl sm:text-7xl font-black text-white mb-4 tracking-tight drop-shadow font-display">
            Bine ai venit la Bibliotecă!
          </h2>
          <p class="text-white/95 text-xl sm:text-2xl font-medium mb-6 tracking-wide drop-shadow-sm">
            Colegiul Național de Informatică „Spiru Haret" Suceava
          
          </p>
          
          <div class="flex items-center justify-center sm:justify-start gap-4 mb-10 w-full opacity-90">
             <div class="h-px flex-1 max-w-[50px] sm:hidden bg-gradient-to-l from-[#c9a84c] to-transparent"></div>
             <p class="text-[#c9a84c] text-sm sm:text-base italic font-serif tracking-widest shrink-0">„Locul unde cunoașterea prinde viață"</p>
             <div class="h-px flex-1 max-w-[100px] bg-gradient-to-r from-[#c9a84c] to-transparent"></div>
          </div>
          
          <div class="flex flex-col sm:flex-row gap-3">
            <button
              @click="$router.push('/books')"
              class="flex items-center justify-center gap-2 px-6 py-3 text-sm font-mono tracking-wider uppercase transition-opacity hover:opacity-90 rounded-sm text-dark bg-[#c9a84c]"
            >
              Răsfoiește Catalogul <i class="pi pi-arrow-right text-[10px]"></i>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Search & Catalog -->
    <section class="bg-cream border-b border-cream-dark">
      <div class="max-w-7xl mx-auto px-6 py-16">
        <div class="flex flex-col md:flex-row md:items-end gap-6 mb-10">
          <div class="flex-1">
            <h2
              class="text-4xl font-black tracking-tight font-display text-[#2a1410]"
            >
              TITLURI NOI
            </h2>
          </div>
        </div>

        <div v-if="loadingCarti" class="flex justify-center py-8">
          <i class="pi pi-spin pi-spinner text-3xl text-secondary"></i>
        </div>
        <div v-else-if="cartiRecente.length === 0" class="text-center py-8 text-[#7a5a55] font-medium font-sans">
          Nu am găsit cărți.
        </div>
        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-5">
          <div
            v-for="carte in cartiRecente"
            :key="carte.carte_id"
            @click="$router.push('/books')"
            class="group rounded-sm overflow-hidden cursor-pointer transition-all bg-white border border-[#2a1410]/10 shadow-[0_1px_4px_rgba(42,20,16,0.06)] hover:shadow-[0_4px_16px_rgba(155,27,48,0.12)]"
          >
            <div class="relative overflow-hidden h-44 bg-cream-dark">
              <img
                :src="`/api/books/image/${carte.carte_id}`"
                @error="$event.target.src='https://placehold.co/200x280/e2e8f0/64748b?text=Carte'"
                :alt="`Coperta ${carte.titlu}`"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <div class="absolute top-2 right-2">
                <span
                  v-if="carte.stoc_disponibil > 0"
                  class="font-mono text-[10px] tracking-widest uppercase px-2 py-0.5 rounded-sm bg-[#2a5c3a]/60 text-[#6fcf97] border border-[#6fcf97]/30"
                >
                  Disponibil
                </span>
                <span
                  v-else
                  class="font-mono text-[10px] tracking-widest uppercase px-2 py-0.5 rounded-sm bg-[#ff3d5a]/10 text-[#ff3d5a] border border-[#ff3d5a]/30"
                >
                  Indisponibil
                </span>
              </div>
            </div>
            <div class="p-3">
              <p class="font-mono text-[10px] uppercase tracking-wider mb-1 text-[#7a5a55] truncate">
                {{ carte.gen || 'General' }}
              </p>
              <h3 class="text-sm font-semibold leading-tight mb-1 line-clamp-2 text-[#2a1410]">
                {{ carte.titlu }}
              </h3>
              <p class="text-xs text-[#7a5a55] truncate">{{ carte.autor }}</p>
              <p v-if="carte.stoc_disponibil > 0" class="font-mono text-[10px] mt-2 text-secondary">
                {{ carte.stoc_disponibil }} exemplare
              </p>
            </div>
          </div>
        </div>

        <div class="mt-8 text-center">
          <button
            @click="$router.push('/books')"
            class="font-mono text-xs uppercase tracking-widest hover:underline flex items-center gap-1 mx-auto text-secondary"
          >
            Vezi Catalogul Complet <i class="pi pi-chevron-right text-[10px]"></i>
          </button>
        </div>
      </div>
    </section>

    <!-- Main Content (Announcements + Side widgets) -->
    <section class="bg-cream">
      <div class="max-w-7xl mx-auto px-6 py-16 flex flex-col xl:grid xl:grid-cols-3 gap-10">
        
        <!-- Announcements (Col 1-2) -->
        <div class="xl:col-span-2 space-y-4">
          <div class="flex items-center gap-3 mb-8">
             <h2 class="text-3xl font-black text-[#2a1410] font-display uppercase tracking-tight">Anunțuri</h2>
             <div class="flex-1 h-px bg-[#2a1410]/20"></div>
          </div>

          <div v-if="loadingAnunturi" class="text-center py-16">
            <i class="pi pi-spin pi-spinner text-3xl text-secondary"></i>
          </div>
          <div v-else-if="anunturi.length === 0" class="text-center py-16">
            <div class="w-16 h-16 rounded-full bg-cream-dark flex items-center justify-center mx-auto mb-4">
              <i class="pi pi-megaphone text-2xl text-[#2a1410]/30"></i>
            </div>
            <p class="text-[#7a5a55]">Nu sunt anunțuri deocamdată.</p>
          </div>
          <div v-else class="space-y-4">
            <DecoratedBox 
              v-for="a in anunturi" 
              :key="a.anunt_id"
            >
              <template #heading>
                <div class="flex items-start justify-between gap-4 text-left">
                  <span class="text-xl font-bold">{{ a.titlu }}</span>
                  <time class="text-xs text-secondary whitespace-nowrap mt-1 font-sans font-medium">{{ a.data_publicare.substring(0, 10) }}</time>
                </div>
              </template>
              <p class="text-[#3b2b18] text-sm leading-relaxed whitespace-pre-line mb-4 font-sans">{{ a.anunt }}</p>
              <button 
                @click="toggleLike(a)"
                :class="[
                  'inline-flex items-center gap-1.5 text-sm font-medium px-3 py-1.5 rounded-sm transition-all duration-150 font-sans',
                  a.liked 
                    ? 'bg-[#c9a84c]/20 text-[#8a6a20] border border-[#c9a84c]/30' 
                    : 'text-[#7a5a55] hover:text-secondary hover:bg-secondary/5 border border-transparent'
                ]"
              >
                <i :class="a.liked ? 'pi pi-heart-fill' : 'pi pi-heart'" class="text-xs"></i>
                <span>{{ a.aprecieri }} Aprecieri</span>
              </button>
            </DecoratedBox>
          </div>
        </div>

        <!-- Sidebar (Col 3) -->
        <div class="space-y-6">
          <!-- Hours -->
          <div class="rounded-sm p-6 bg-white border border-[#2a1410]/10">
            <div class="flex items-center gap-2 mb-5">
              <i class="pi pi-clock text-secondary text-sm"></i>
              <p class="font-mono text-xs tracking-widest uppercase text-secondary">
                Program de Lucru
              </p>
            </div>
            <div class="flex flex-col gap-3">
              <div class="flex justify-between items-center pb-3 border-b border-[#2a1410]/10">
                <span class="font-mono text-xs uppercase tracking-wide text-[#7a5a55]">Luni – Vineri</span>
                <span class="font-mono text-xs font-medium text-[#2a1410]">08:00 – 16:00</span>
              </div>
              <div class="flex justify-between items-center pb-3 border-b border-[#2a1410]/10">
                <span class="font-mono text-xs uppercase tracking-wide text-[#7a5a55]">Sâmbătă - Duminică</span>
                <span class="font-mono text-xs font-medium text-[#c0392b]">Închis</span>
              </div>
            </div>
            <div
              class="mt-5 flex items-center gap-2 rounded-sm px-3 py-2 bg-[rgba(201,168,76,0.18)] border border-[rgba(201,168,76,0.35)]"
            >
              <div class="w-1.5 h-1.5 rounded-full animate-pulse bg-[#c9a84c]"></div>
              <span class="font-mono text-xs tracking-wider text-[#8a6a20]">
                Deschis în zilele lucrătoare
              </span>
            </div>
          </div>

          <!-- Quick links -->
          <div class="rounded-sm p-6 bg-white border border-[#2a1410]/10">
            <p class="font-mono text-xs tracking-widest uppercase mb-4 text-[#7a5a55]">
              Linkuri Rapide
            </p>
            <a
              @click="$router.push('/books')"
              class="flex items-center justify-between py-2.5 text-xs transition-colors group cursor-pointer border-b border-[#2a1410]/10 text-[#2a1410] hover:text-secondary"
            >
              <span class="flex items-center gap-2"><i class="pi pi-book"></i> Caută o carte</span>
              <i class="pi pi-chevron-right text-[10px] text-[#2a1410]/30 group-hover:text-secondary"></i>
            </a>
            <a
              @click="$router.push(isLoggedIn ? '/profile' : '/login')"
              class="flex items-center justify-between py-2.5 text-xs transition-colors group cursor-pointer border-b border-[#2a1410]/10 text-[#2a1410] hover:text-secondary"
            >
              <span class="flex items-center gap-2"><i class="pi pi-user"></i> Contul Meu</span>
              <i class="pi pi-chevron-right text-[10px] text-[#2a1410]/30 group-hover:text-secondary"></i>
            </a>

            <a
              href="mailto:contact@cni-sv.ro"
              class="flex items-center justify-between py-2.5 text-xs transition-colors group cursor-pointer border-b border-[#2a1410]/10 text-[#2a1410] hover:text-secondary"
            >
              <span class="flex items-center gap-2"><i class="pi pi-envelope"></i> Contact Bibliotecar</span>
              <i class="pi pi-chevron-right text-[10px] text-[#2a1410]/30 group-hover:text-secondary"></i>
            </a>
          </div>
        </div>
      </div>
    </section>
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
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(42, 20, 16, 0.2);
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(42, 20, 16, 0.4);
}
</style>
