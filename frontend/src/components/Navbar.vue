<template>
  <nav class="bg-dark shadow-elegant border-b border-secondary/40 sticky top-0 z-50">
    <div class="max-w-full mx-auto px-3 sm:px-4 py-3 sm:py-4 flex justify-between items-center">
      <!-- Logo Section -->
      <div class="flex items-center gap-2 sm:gap-3 group cursor-pointer transition-all duration-300">
        <div class="relative">
          <img src="/logo.webp" alt="Biblioteca Logo" class="h-9 sm:h-12 w-9 sm:w-12 transition-transform duration-300 group-">
          <div class="absolute inset-0 bg-cream rounded-full opacity-0 group-hover:opacity-20 blur-lg transition-opacity duration-300"></div>
        </div>
        <div class="hidden sm:block">
          <h1 class="text-xl sm:text-2xl font-bold text-cream">Biblioteca</h1>
          <p class="text-xs text-cream/70">Sistemul Bibliotecii Școlii</p>
        </div>
      </div>
      
      <!-- Desktop Menu -->
      <div class="hidden md:flex gap-4 lg:gap-8 items-center">
        <router-link to="/" class="text-cream/80 hover:text-cream transition-all duration-200 font-medium relative group text-sm lg:text-base">
          Principală
          <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-cream transition-all duration-300 group-hover:w-full"></span>
        </router-link>
        <router-link to="/books" class="text-cream/80 hover:text-cream transition-all duration-200 font-medium relative group text-sm lg:text-base">
          Cărți
          <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-cream transition-all duration-300 group-hover:w-full"></span>
        </router-link>
        <router-link v-if="isLoggedIn" to="/profile" class="text-cream/80 hover:text-cream transition-all duration-200 font-medium relative group text-sm lg:text-base">
          Profil
          <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-cream transition-all duration-300 group-hover:w-full"></span>
        </router-link>
        <a href="#" class="text-cream/80 hover:text-cream transition-all duration-200 font-medium relative group text-sm lg:text-base">
          Despre
          <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-cream transition-all duration-300 group-hover:w-full"></span>
        </a>
        
        <!-- Buton Conectare/Deconectare -->
        <button 
          @click="handleAuthClick"
          :class="[
            'px-4 lg:px-6 py-2 rounded-lg font-bold transition-all duration-300  text-sm lg:text-base',
            isLoggedIn 
              ? 'bg-gradient-to-r from-accent to-red-700 hover:shadow-lg text-white' 
              : 'bg-gradient-to-r from-secondary to-accent hover:shadow-lg text-white'
          ]"
        >
          {{ isLoggedIn ? 'Deconectare' : 'Conectare' }}
        </button>
      </div>
      
      <!-- Mobile Menu Button -->
      <button 
        @click="mobileMenuOpen = !mobileMenuOpen"
        class="md:hidden text-cream text-2xl font-bold h-10 w-10 flex items-center justify-center"
      >
        <i :class="mobileMenuOpen ? 'pi pi-times' : 'pi pi-bars'"></i>
      </button>
    </div>
    
    <!-- Mobile Menu -->
    <div v-if="mobileMenuOpen" class="md:hidden bg-dark border-t border-secondary/30">
      <div class="px-3 sm:px-4 py-3 flex flex-col gap-2">
        <router-link to="/" @click="mobileMenuOpen = false" class="text-cream/80 hover:text-cream transition-all duration-200 font-medium py-2 px-3 rounded hover:bg-secondary/20 text-sm">
          Principală
        </router-link>
        <router-link to="/books" @click="mobileMenuOpen = false" class="text-cream/80 hover:text-cream transition-all duration-200 font-medium py-2 px-3 rounded hover:bg-secondary/20 text-sm">
          Cărți
        </router-link>
        <router-link v-if="isLoggedIn" to="/profile" @click="mobileMenuOpen = false" class="text-cream/80 hover:text-cream transition-all duration-200 font-medium py-2 px-3 rounded hover:bg-secondary/20 text-sm">
          Profil
        </router-link>
        <a href="#" class="text-cream/80 hover:text-cream transition-all duration-200 font-medium py-2 px-3 rounded hover:bg-secondary/20 text-sm">
          Despre
        </a>
        <button 
          @click="handleAuthClick"
          :class="[
            'w-full px-4 py-2 rounded-lg font-bold transition-all duration-300  text-sm',
            isLoggedIn 
              ? 'bg-gradient-to-r from-accent to-red-700 hover:shadow-lg text-white' 
              : 'bg-gradient-to-r from-secondary to-accent hover:shadow-lg text-white'
          ]"
        >
          {{ isLoggedIn ? 'Deconectare' : 'Conectare' }}
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  data() {
    return {
      isLoggedIn: false,
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
        this.isLoggedIn = response.ok
      } catch {
        this.isLoggedIn = false
      }
    },
    async handleAuthClick() {
      if (this.isLoggedIn) {
        // Deconectare — call backend to clear the cookie
        try {
          await fetch('/api/auth/logout', { method: 'POST', credentials: 'include' })
        } catch { /* ignore */ }
        this.isLoggedIn = false
        this.mobileMenuOpen = false
        this.$router.push('/')
      } else {
        // Navighează la pagina de conectare
        this.mobileMenuOpen = false
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style scoped>
</style>
