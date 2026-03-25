<template>
  <nav class="bg-dark shadow-dark-lg border-b-4 border-gold sticky top-0 z-50">
    <div class="max-w-full mx-auto px-3 sm:px-4 py-3 sm:py-4 flex justify-between items-center">
      <!-- Logo Section -->
      <div class="flex items-center gap-2 sm:gap-3 group cursor-pointer transition-all duration-300">
        <div class="relative">
          <img src="/logo.webp" alt="Biblioteca Logo" class="h-9 sm:h-12 w-9 sm:w-12 transition-transform duration-300 group-hover:scale-110">
          <div class="absolute inset-0 bg-gold rounded-full opacity-0 group-hover:opacity-20 blur-lg transition-opacity duration-300"></div>
        </div>
        <div class="hidden sm:block">
          <h1 class="text-xl sm:text-2xl font-bold text-gold glow-gold">Biblioteca</h1>
          <p class="text-xs text-primary">Sistemul Bibliotecii Școlii</p>
        </div>
      </div>
      
      <!-- Desktop Menu -->
      <div class="hidden md:flex gap-4 lg:gap-8 items-center">
        <router-link to="/" class="text-white hover:text-gold transition-all duration-200 font-medium relative group text-sm lg:text-base">
          Principală
          <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-gold transition-all duration-300 group-hover:w-full"></span>
        </router-link>
        <router-link to="/books" class="text-white hover:text-gold transition-all duration-200 font-medium relative group text-sm lg:text-base">
          Cărți
          <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-gold transition-all duration-300 group-hover:w-full"></span>
        </router-link>
        <router-link to="/profile" class="text-white hover:text-gold transition-all duration-200 font-medium relative group text-sm lg:text-base">
          Profil
          <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-gold transition-all duration-300 group-hover:w-full"></span>
        </router-link>
        <a href="#" class="text-white hover:text-gold transition-all duration-200 font-medium relative group text-sm lg:text-base">
          Despre
          <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-gold transition-all duration-300 group-hover:w-full"></span>
        </a>
        
        <!-- Buton Conectare/Deconectare -->
        <button 
          @click="handleAuthClick"
          :class="[
            'px-4 lg:px-6 py-2 rounded-lg font-bold transition-all duration-300 transform hover:scale-105 btn-glow text-sm lg:text-base',
            isLoggedIn 
              ? 'bg-gradient-to-r from-accent to-red-700 hover:shadow-gold text-white' 
              : 'bg-gradient-to-r from-gold to-primary hover:shadow-gold text-dark'
          ]"
        >
          {{ isLoggedIn ? 'Deconectare' : 'Conectare' }}
        </button>
      </div>
      
      <!-- Mobile Menu Button -->
      <button 
        @click="mobileMenuOpen = !mobileMenuOpen"
        class="md:hidden text-gold text-2xl font-bold h-10 w-10 flex items-center justify-center"
      >
        {{ mobileMenuOpen ? '✕' : '≡' }}
      </button>
    </div>
    
    <!-- Mobile Menu -->
    <div v-if="mobileMenuOpen" class="md:hidden bg-gradient-to-b from-secondary to-dark border-t-2 border-gold">
      <div class="px-3 sm:px-4 py-3 flex flex-col gap-2">
        <router-link to="/" @click="mobileMenuOpen = false" class="text-white hover:text-gold transition-all duration-200 font-medium py-2 px-3 rounded hover:bg-dark text-sm">
          Principală
        </router-link>
        <router-link to="/books" @click="mobileMenuOpen = false" class="text-white hover:text-gold transition-all duration-200 font-medium py-2 px-3 rounded hover:bg-dark text-sm">
          Cărți
        </router-link>
        <router-link to="/profile" @click="mobileMenuOpen = false" class="text-white hover:text-gold transition-all duration-200 font-medium py-2 px-3 rounded hover:bg-dark text-sm">
          Profil
        </router-link>
        <a href="#" class="text-white hover:text-gold transition-all duration-200 font-medium py-2 px-3 rounded hover:bg-dark text-sm">
          Despre
        </a>
        <button 
          @click="handleAuthClick"
          :class="[
            'w-full px-4 py-2 rounded-lg font-bold transition-all duration-300 transform hover:scale-105 btn-glow text-sm',
            isLoggedIn 
              ? 'bg-gradient-to-r from-accent to-red-700 hover:shadow-gold text-white' 
              : 'bg-gradient-to-r from-gold to-primary hover:shadow-gold text-dark'
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
  methods: {
    handleAuthClick() {
      if (this.isLoggedIn) {
        // Deconectare
        this.isLoggedIn = false
        console.log('Utilizatorul s-a deconectat')
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
