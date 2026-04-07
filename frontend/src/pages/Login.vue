<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-secondary via-dark to-accent py-8 sm:py-16 shadow-elegant relative overflow-hidden">
      <div class="absolute inset-0 gradient-overlay opacity-30"></div>
      <div class="max-w-full mx-auto px-3 sm:px-4 text-center relative z-10">
        <h2 class="text-2xl sm:text-4xl font-bold text-white mb-2 sm:mb-4 glow-white tracking-tight">Conectare</h2>
        <p class="text-cream/80 text-xs sm:text-lg mb-4 sm:mb-8 font-light">Bine ai revenit la Biblioteca</p>
      </div>
    </section>

    <!-- Login Form Section -->
    <main class="max-w-full mx-auto px-3 sm:px-4 py-8 sm:py-12">
      <div class="flex justify-center">
        <div class="w-full max-w-md">
          <!-- Login Card -->
          <div class="bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 p-4 sm:p-8 card-hover">
            <!-- Logo Section -->
            <div class="text-center mb-6 sm:mb-8">
              <img src="/logo.webp" alt="Biblioteca Logo" class="h-16 sm:h-20 w-16 sm:w-20 mx-auto mb-3 sm:mb-4">
              <h1 class="text-2xl sm:text-3xl font-bold text-secondary">Biblioteca</h1>
              <p class="text-gray-500 text-xs sm:text-sm mt-2">Sistem de Gestiune a Bibliotecii</p>
            </div>

            <!-- Login Form -->
            <form @submit.prevent="handleLogin" class="space-y-4 sm:space-y-6">
              <!-- Email Field -->
              <div>
                <label for="email" class="block text-dark font-semibold mb-2 text-sm sm:text-base">
                  Email
                </label>
                <input
                  id="email"
                  v-model="form.email"
                  type="email"
                  placeholder="Introdu email"
                  class="w-full px-3 sm:px-4 py-2 sm:py-3 rounded-lg bg-cream-dark border-2 border-secondary/30 text-dark placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary/50 transition-all duration-200 text-xs sm:text-base"
                  required
                >
              </div>

              <!-- Password Field -->
              <div>
                <label for="password" class="block text-dark font-semibold mb-2 text-sm sm:text-base">
                  Parolă
                </label>
                <input
                  id="password"
                  v-model="form.password"
                  type="password"
                  placeholder="Introdu parola"
                  class="w-full px-3 sm:px-4 py-2 sm:py-3 rounded-lg bg-cream-dark border-2 border-secondary/30 text-dark placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary/50 transition-all duration-200 text-xs sm:text-base"
                  required
                >
              </div>

              <!-- Remember Me & Forgot Password -->
              <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                <label class="flex items-center gap-2 cursor-pointer">
                  <input
                    v-model="form.rememberMe"
                    type="checkbox"
                    class="w-4 h-4 rounded border-secondary text-secondary focus:ring-secondary"
                  >
                  <span class="text-gray-700 text-xs sm:text-sm">Ține-mă minte</span>
                </label>
                <a href="#" class="text-secondary hover:text-accent text-xs sm:text-sm font-medium transition-colors duration-200">
                  Ai uitat parola?
                </a>
              </div>

              <!-- Error Message -->
              <div v-if="errorMessage" class="bg-accent/10 border-l-4 border-accent rounded-lg p-3 sm:p-4">
                <p class="text-accent text-xs sm:text-sm">{{ errorMessage }}</p>
              </div>

              <!-- Success Message -->
              <div v-if="successMessage" class="bg-green-50 border-l-4 border-green-500 rounded-lg p-3 sm:p-4">
                <p class="text-green-700 text-xs sm:text-sm">{{ successMessage }}</p>
              </div>

              <!-- Login Button -->
              <button
                type="submit"
                class="w-full bg-gradient-to-r from-secondary to-accent hover:shadow-lg text-white font-bold py-2 sm:py-3 px-4 rounded-lg text-sm sm:text-base transition-all duration-300 "
              >
                Conectare
              </button>
            </form>

            <!-- Divider -->
            <div class="relative my-6 sm:my-8">
              <div class="absolute inset-0 flex items-center">
                <div class="w-full border-t border-secondary/30"></div>
              </div>
              <div class="relative flex justify-center text-xs sm:text-sm">
                <span class="px-2 bg-cream text-gray-500">SAU</span>
              </div>
            </div>

            <!-- Social Login Options -->
            <div class="space-y-2 sm:space-y-3">
              <button class="w-full bg-cream-dark hover:bg-cream border-2 border-secondary/30 text-dark font-semibold py-2 sm:py-3 px-4 text-sm sm:text-base rounded-lg transition-all duration-300 flex items-center justify-center gap-2 hover:shadow-sm">
                <i class="pi pi-user"></i> Oaspete
              </button>
            </div>

            <!-- Sign Up Link -->
            <div class="mt-6 sm:mt-8 text-center">
              <p class="text-gray-600 text-xs sm:text-base">
                Nu ai cont?
                <router-link to="/signup" class="text-secondary hover:text-accent font-bold transition-colors duration-200">
                  Înregistrare
                </router-link>
              </p>
            </div>

            <!-- Additional Info -->
            <div class="mt-6 sm:mt-8 p-3 sm:p-4 bg-cream-dark rounded-lg border-l-4 border-secondary text-xs">
              <p class="text-gray-700 leading-relaxed">
                <strong class="text-dark">Demo:</strong><br>
                Email: student@library.com<br>
                Parolă: demo123
              </p>
            </div>
          </div>

          <!-- Features Section -->
          <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 p-6 text-center card-hover">
              <i class="pi pi-book text-4xl mb-3 text-secondary"></i>
              <h3 class="text-dark font-bold mb-2">Răsfoi Cărți</h3>
              <p class="text-gray-600 text-sm">Explorează colecția noastră vastă de cărți și resurse</p>
            </div>
            <div class="bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 p-6 text-center card-hover">
              <i class="pi pi-star text-4xl mb-3 text-accent"></i>
              <h3 class="text-dark font-bold mb-2">Evaluează și Recenzionează</h3>
              <p class="text-gray-600 text-sm">Partajează gândurile tale și ajută-i pe alții să descopere cărți grozave</p>
            </div>
            <div class="bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 p-6 text-center card-hover">
              <i class="pi pi-users text-4xl mb-3 text-secondary"></i>
              <h3 class="text-dark font-bold mb-2">Alătură-te Comunității</h3>
              <p class="text-gray-600 text-sm">Conectează-te cu alți cititori și pasionați de cărți</p>
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

      try {
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify({
            email: this.form.email,
            password: this.form.password
          })
        })

        const data = await response.json()
        if (response.ok) {
          this.successMessage = 'Conectare reușită! Se redirecționează...'
          setTimeout(() => {
            this.$router.push('/')
          }, 1500)
        } else {
          this.errorMessage = data.message || 'Email sau parolă invalidă'
        }
      } catch (error) {
        this.errorMessage = 'Eroare de rețea. Încearcă din nou.'
      }
    }
  }
}
</script>

<style scoped>
input:focus {
  border-color: #9B1B30 !important;
}

input::placeholder {
  color: rgba(0, 0, 0, 0.35);
}
</style>
