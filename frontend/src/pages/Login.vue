<template>
  <div class="min-h-screen bg-white">
    <!-- Hero Section -->
    <section class="bg-gradient-to-b from-secondary to-dark py-8 sm:py-16 shadow-gold">
      <div class="max-w-full mx-auto px-3 sm:px-4 text-center">
        <h2 class="text-2xl sm:text-4xl font-bold text-gold mb-2 sm:mb-4 glow-gold">Conectare</h2>
        <p class="text-primary text-xs sm:text-lg mb-4 sm:mb-8">Bine ai revenit la Biblioteca</p>
      </div>
    </section>

    <!-- Login Form Section -->
    <main class="max-w-full mx-auto px-3 sm:px-4 py-8 sm:py-12">
      <div class="flex justify-center">
        <div class="w-full max-w-md">
          <!-- Login Card -->
          <div class="bg-gradient-to-b from-secondary to-dark rounded-lg shadow-dark-lg border-2 border-gold p-4 sm:p-8 card-hover">
            <!-- Logo Section -->
            <div class="text-center mb-6 sm:mb-8">
              <img src="/logo.webp" alt="Biblioteca Logo" class="h-16 sm:h-20 w-16 sm:w-20 mx-auto mb-3 sm:mb-4">
              <h1 class="text-2xl sm:text-3xl font-bold text-gold glow-gold">Biblioteca</h1>
              <p class="text-primary text-xs sm:text-sm mt-2">Sistem de Gestiune a Bibliotecii</p>
            </div>

            <!-- Login Form -->
            <form @submit.prevent="handleLogin" class="space-y-4 sm:space-y-6">
              <!-- Email/Username Field -->
              <div>
                <label for="email" class="block text-gold font-semibold mb-2 text-sm sm:text-base">
                  Email sau Utilizator
                </label>
                <input
                  id="email"
                  v-model="form.email"
                  type="text"
                  placeholder="Introdu email"
                  class="w-full px-3 sm:px-4 py-2 sm:py-3 rounded-lg bg-dark border-2 border-gold text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gold transition-all duration-200 text-xs sm:text-base"
                  required
                >
              </div>

              <!-- Password Field -->
              <div>
                <label for="password" class="block text-gold font-semibold mb-2 text-sm sm:text-base">
                  Parolă
                </label>
                <input
                  id="password"
                  v-model="form.password"
                  type="password"
                  placeholder="Introdu parola"
                  class="w-full px-3 sm:px-4 py-2 sm:py-3 rounded-lg bg-dark border-2 border-gold text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gold transition-all duration-200 text-xs sm:text-base"
                  required
                >
              </div>

              <!-- Remember Me & Forgot Password -->
              <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                <label class="flex items-center gap-2 cursor-pointer">
                  <input
                    v-model="form.rememberMe"
                    type="checkbox"
                    class="w-4 h-4 rounded border-gold text-gold focus:ring-gold"
                  >
                  <span class="text-white text-xs sm:text-sm">Ține-mă minte</span>
                </label>
                <a href="#" class="text-gold hover:text-primary text-xs sm:text-sm font-medium transition-colors duration-200">
                  Ai uitat parola?
                </a>
              </div>

              <!-- Error Message -->
              <div v-if="errorMessage" class="bg-accent bg-opacity-20 border-l-4 border-accent rounded-lg p-3 sm:p-4">
                <p class="text-accent text-xs sm:text-sm">{{ errorMessage }}</p>
              </div>

              <!-- Success Message -->
              <div v-if="successMessage" class="bg-primary bg-opacity-20 border-l-4 border-primary rounded-lg p-3 sm:p-4">
                <p class="text-primary text-xs sm:text-sm">{{ successMessage }}</p>
              </div>

              <!-- Login Button -->
              <button
                type="submit"
                class="w-full bg-gradient-to-r from-gold to-primary hover:shadow-gold text-dark font-bold py-2 sm:py-3 px-4 rounded-lg text-sm sm:text-base transition-all duration-300 transform hover:scale-105 btn-glow"
              >
                Conectare
              </button>
            </form>

            <!-- Divider -->
            <div class="relative my-6 sm:my-8">
              <div class="absolute inset-0 flex items-center">
                <div class="w-full border-t border-gold"></div>
              </div>
              <div class="relative flex justify-center text-xs sm:text-sm">
                <span class="px-2 bg-gradient-to-b from-secondary to-dark text-gold">SAU</span>
              </div>
            </div>

            <!-- Social Login Options -->
            <div class="space-y-2 sm:space-y-3">
              <button class="w-full bg-dark hover:bg-secondary border-2 border-gold text-gold font-semibold py-2 sm:py-3 px-4 text-sm sm:text-base rounded-lg transition-all duration-300 flex items-center justify-center gap-2 hover:shadow-gold">
                <i class="pi pi-user"></i> Oaspete
              </button>
            </div>

            <!-- Sign Up Link -->
            <div class="mt-6 sm:mt-8 text-center">
              <p class="text-white text-xs sm:text-base">
                Nu ai cont?
                <router-link to="/signup" class="text-gold hover:text-primary font-bold transition-colors duration-200">
                  Înregistrare
                </router-link>
              </p>
            </div>

            <!-- Additional Info -->
            <div class="mt-6 sm:mt-8 p-3 sm:p-4 bg-dark rounded-lg border-l-4 border-gold text-xs">
              <p class="text-white leading-relaxed">
                <strong class="text-gold">Demo:</strong><br>
                Email: student@library.com<br>
                Parolă: demo123
              </p>
            </div>
          </div>

          <!-- Features Section -->
          <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-dark rounded-lg shadow-dark-lg border-2 border-gold p-6 text-center card-hover">
              <i class="pi pi-book text-4xl mb-3 text-gold"></i>
              <h3 class="text-gold font-bold mb-2">Răsfoi Cărți</h3>
              <p class="text-white text-sm">Explorează colecția noastră vastă de cărți și resurse</p>
            </div>
            <div class="bg-dark rounded-lg shadow-dark-lg border-2 border-gold p-6 text-center card-hover">
              <i class="pi pi-star text-4xl mb-3 text-gold"></i>
              <h3 class="text-gold font-bold mb-2">Evaluează și Recenzionează</h3>
              <p class="text-white text-sm">Partajează gândurile tale și ajută-i pe alții să descopere cărți grozave</p>
            </div>
            <div class="bg-dark rounded-lg shadow-dark-lg border-2 border-gold p-6 text-center card-hover">
              <i class="pi pi-users text-4xl mb-3 text-gold"></i>
              <h3 class="text-gold font-bold mb-2">Alătură-te Comunității</h3>
              <p class="text-white text-sm">Conectează-te cu alți cititori și pasionați de cărți</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      form: {
        email: '',
        password: '',
        rememberMe: false
      },
      errorMessage: '',
      successMessage: ''
    }
  },
  methods: {
    async handleLogin() {
      // Resetează mesajele
      this.errorMessage = ''
      this.successMessage = ''

      // Validare de bază
      if (!this.form.email || !this.form.password) {
        this.errorMessage = 'Te rog completează toate câmpurile'
        return
      }

      // Simulează login cu acreditări demo
      if (this.form.email === 'student@library.com' && this.form.password === 'demo123') {
        this.successMessage = 'Conectare reușită! Se redirecționează...'
        
        // Simulează apel API
        setTimeout(() => {
          this.$router.push('/')
        }, 1500)
      } else {
        this.errorMessage = 'Email sau parolă invalidă. Încearcă: student@library.com / demo123'
      }
    }
  }
}
</script>

<style scoped>
input:focus {
  border-color: #FFD700 !important;
}

input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}
</style>
