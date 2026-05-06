<template>
  <nav class="bg-dark/95 backdrop-blur-md border-b border-white/5 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-3 group">
          <img src="/logo.webp" alt="Biblioteca" class="h-9 w-9 rounded-lg transition-transform duration-200 group-hover:scale-105">
          <div class="hidden sm:block">
            <h1 class="text-lg font-bold text-white leading-tight">Biblioteca</h1>
            <p class="text-[11px] text-white/40 font-medium -mt-0.5">Sistem Școlar</p>
          </div>
        </router-link>

        <!-- Desktop Nav -->
        <div class="hidden md:flex items-center gap-1">
          <router-link 
            to="/" 
            class="px-4 py-2 text-sm font-medium text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-all duration-150"
            active-class="!text-white bg-white/10"
            exact
          >
            Principală
          </router-link>
          <router-link 
            to="/books" 
            class="px-4 py-2 text-sm font-medium text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-all duration-150"
            active-class="!text-white bg-white/10"
          >
            Cărți
          </router-link>
          <router-link 
            v-if="isLoggedIn" 
            to="/profile" 
            class="px-4 py-2 text-sm font-medium text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-all duration-150"
            active-class="!text-white bg-white/10"
          >
            Profil
          </router-link>
          <router-link
            v-if="inClub"
            to="/club"
            class="px-4 py-2 text-sm font-medium text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-all duration-150"
            active-class="!text-white bg-white/10"
          >
            Club
          </router-link>

          <div class="w-px h-6 bg-white/10 mx-2"></div>

          <button 
            @click="handleAuthClick"
            :class="[
              'px-5 py-2 rounded-lg text-sm font-semibold transition-all duration-200',
              isLoggedIn 
                ? 'text-white/70 hover:text-white hover:bg-white/5' 
                : 'bg-secondary hover:bg-secondary/90 text-white shadow-soft'
            ]"
          >
            {{ isLoggedIn ? 'Deconectare' : 'Conectare' }}
          </button>
        </div>

        <!-- Mobile toggle -->
        <button 
          @click="mobileMenuOpen = !mobileMenuOpen"
          class="md:hidden p-2 text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-colors"
        >
          <i :class="mobileMenuOpen ? 'pi pi-times' : 'pi pi-bars'" class="text-lg"></i>
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <transition name="slide">
      <div v-if="mobileMenuOpen" class="md:hidden bg-dark border-t border-white/5">
        <div class="px-4 py-3 space-y-1">
          <router-link to="/" @click="mobileMenuOpen = false" class="block px-4 py-2.5 text-sm font-medium text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-all">
            Principală
          </router-link>
          <router-link to="/books" @click="mobileMenuOpen = false" class="block px-4 py-2.5 text-sm font-medium text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-all">
            Cărți
          </router-link>
          <router-link v-if="isLoggedIn" to="/profile" @click="mobileMenuOpen = false" class="block px-4 py-2.5 text-sm font-medium text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-all">
            Profil
          </router-link>
          <router-link v-if="inClub" to="/club" @click="mobileMenuOpen = false" class="block px-4 py-2.5 text-sm font-medium text-white/70 hover:text-white rounded-lg hover:bg-white/5 transition-all">
            Club
          </router-link>
          <div class="pt-2 border-t border-white/5">
            <button 
              @click="handleAuthClick"
              :class="[
                'w-full text-left px-4 py-2.5 rounded-lg text-sm font-semibold transition-all',
                isLoggedIn 
                  ? 'text-white/70 hover:text-white hover:bg-white/5' 
                  : 'bg-secondary text-white'
              ]"
            >
              {{ isLoggedIn ? 'Deconectare' : 'Conectare' }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  data() {
    return {
      isLoggedIn: false,
      inClub: false,
      mobileMenuOpen: false
    }
  },
  mounted() {
    this.checkAuth()
  },
  watch: {
    '$route'() {
      this.checkAuth()
    }
  },
  methods: {
    async checkAuth() {
      try {
        const response = await fetch('/api/auth/me', { credentials: 'include' })
        if (response.ok) {
          const data = await response.json()
          this.isLoggedIn = true
          this.inClub = !!data.club
        } else {
          this.isLoggedIn = false
          this.inClub = false
        }
      } catch {
        this.isLoggedIn = false
        this.inClub = false
      }
    },
    async handleAuthClick() {
      if (this.isLoggedIn) {
        try {
          await fetch('/api/auth/logout', { method: 'POST', credentials: 'include' })
        } catch { /* ignore */ }
        this.isLoggedIn = false
        this.inClub = false
        this.mobileMenuOpen = false
        this.$router.push('/')
      } else {
        this.mobileMenuOpen = false
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style scoped>
.slide-enter-active, .slide-leave-active {
  transition: all 0.2s ease;
}
.slide-enter-from, .slide-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
