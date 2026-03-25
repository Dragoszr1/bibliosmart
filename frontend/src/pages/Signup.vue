<template>
  <div class="min-h-screen bg-white">
    <!-- Hero Section -->
    <section class="bg-gradient-to-b from-secondary to-dark py-8 sm:py-16 shadow-gold">
      <div class="max-w-full mx-auto px-3 sm:px-4 text-center">
        <h2 class="text-2xl sm:text-4xl font-bold text-gold mb-2 sm:mb-4 glow-gold">Creare Cont</h2>
        <p class="text-primary text-xs sm:text-lg mb-4 sm:mb-8">Alătură-te Bibliotecii astazi</p>
      </div>
    </section>

    <!-- Signup Form Section -->
    <main class="max-w-full mx-auto px-3 sm:px-4 py-8 sm:py-12">
      <div class="flex justify-center">
        <div class="w-full max-w-md">
          <!-- Signup Card -->
          <div class="bg-gradient-to-b from-secondary to-dark rounded-lg shadow-dark-lg border-2 border-gold p-4 sm:p-8 card-hover">
            <!-- Logo Section -->
            <div class="text-center mb-6 sm:mb-8">
              <img src="/logo.webp" alt="Biblioteca Logo" class="h-16 sm:h-20 w-16 sm:w-20 mx-auto mb-3 sm:mb-4">
              <h1 class="text-2xl sm:text-3xl font-bold text-gold glow-gold">Biblioteca</h1>
              <p class="text-primary text-xs sm:text-sm mt-2">Sistem de Gestiune a Bibliotecii</p>
            </div>

            <!-- Signup Form -->
            <form @submit.prevent="handleSignup" class="space-y-4 sm:space-y-5">
              <!-- Full Name Field -->
              <div>
                <label for="fullName" class="block text-gold font-semibold mb-2 text-sm sm:text-base">
                  Nume Complet
                </label>
                <input
                  id="fullName"
                  v-model="form.fullName"
                  type="text"
                  placeholder="Introdu numele"
                  class="w-full px-3 sm:px-4 py-2 sm:py-3 rounded-lg bg-dark border-2 border-gold text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gold transition-all duration-200 text-xs sm:text-base"
                  required
                >
              </div>

              <!-- Email Field -->
              <div>
                <label for="email" class="block text-gold font-semibold mb-2 text-sm sm:text-base">
                  Email
                </label>
                <input
                  id="email"
                  v-model="form.email"
                  type="email"
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
                  placeholder="Creia o parolă puternică"
                  class="w-full px-3 sm:px-4 py-2 sm:py-3 rounded-lg bg-dark border-2 border-gold text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gold transition-all duration-200 text-xs sm:text-base"
                  required
                >
                <p class="text-xs text-primary mt-1 sm:mt-2">Min 8 caractere</p>
              </div>

              <!-- Confirm Password Field -->
              <div>
                <label for="confirmPassword" class="block text-gold font-semibold mb-2 text-sm sm:text-base">
                  Confirmă Parola
                </label>
                <input
                  id="confirmPassword"
                  v-model="form.confirmPassword"
                  type="password"
                  placeholder="Confirmă parola"
                  class="w-full px-3 sm:px-4 py-2 sm:py-3 rounded-lg bg-dark border-2 border-gold text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gold transition-all duration-200 text-xs sm:text-base"
                  required
                >
              </div>

              <!-- Terms & Conditions -->
              <div class="flex items-start gap-2">
                <input
                  id="terms"
                  v-model="form.agreeToTerms"
                  type="checkbox"
                  class="w-4 h-4 rounded border-gold text-gold focus:ring-gold mt-1"
                  required
                >
                <label for="terms" class="text-white text-xs sm:text-sm">
                  Accept
                  <a href="#" class="text-gold hover:text-primary">Termenii</a>
                  și
                  <a href="#" class="text-gold hover:text-primary">Politica</a>
                </label>
              </div>

              <!-- Error Message -->
              <div v-if="errorMessage" class="bg-accent bg-opacity-20 border-l-4 border-accent rounded-lg p-3 sm:p-4">
                <p class="text-accent text-xs sm:text-sm">{{ errorMessage }}</p>
              </div>

              <!-- Success Message -->
              <div v-if="successMessage" class="bg-primary bg-opacity-20 border-l-4 border-primary rounded-lg p-3 sm:p-4">
                <p class="text-primary text-xs sm:text-sm">{{ successMessage }}</p>
              </div>

              <!-- Signup Button -->
              <button
                type="submit"
                class="w-full bg-gradient-to-r from-gold to-primary hover:shadow-gold text-dark font-bold py-3 px-4 rounded-lg transition-all duration-300 transform hover:scale-105 btn-glow"
              >
                Creare Cont
              </button>
            </form>

            <!-- Sign In Link -->
            <div class="mt-8 text-center">
              <p class="text-white">
                Ai deja un cont?
                <router-link to="/login" class="text-gold hover:text-primary font-bold transition-colors duration-200">
                  Conectare
                </router-link>
              </p>
            </div>
          </div>

          <!-- Security Info -->
          <div class="mt-8 bg-dark rounded-lg shadow-dark-lg border-2 border-gold p-6">
            <h3 class="text-gold font-bold mb-4 flex items-center gap-2">
              <i class="pi pi-shield"></i> Datele Tale sunt în Siguranță
            </h3>
            <ul class="space-y-2 text-white text-sm">
              <li class="flex items-start gap-2">
                <i class="pi pi-check text-gold"></i>
                <span>Parola ta este criptată și niciodală partajată</span>
              </li>
              <li class="flex items-start gap-2">
                <i class="pi pi-check text-gold"></i>
                <span>Respectăm reglementatiile de protecție a datelor</span>
              </li>
              <li class="flex items-start gap-2">
                <i class="pi pi-check text-gold"></i>
                <span>Autentificare cu doi factori disponibilă</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'Signup',
  data() {
    return {
      form: {
        fullName: '',
        email: '',
        password: '',
        confirmPassword: '',
        agreeToTerms: false
      },
      errorMessage: '',
      successMessage: ''
    }
  },
  methods: {
    async handleSignup() {
      // Resetează mesajele
      this.errorMessage = ''
      this.successMessage = ''

      // Validare
      if (!this.form.fullName || !this.form.email || !this.form.password || !this.form.confirmPassword) {
        this.errorMessage = 'Te rog completează toate câmpurile'
        return
      }

      if (this.form.password !== this.form.confirmPassword) {
        this.errorMessage = 'Parolele nu se potrivesc'
        return
      }

      if (this.form.password.length < 8) {
        this.errorMessage = 'Parola trebuie să aibă cel puțin 8 caractere'
        return
      }

      if (!this.form.agreeToTerms) {
        this.errorMessage = 'Trebuie să accepți termenii și condițiile'
        return
      }

      // Simulează înregistrare
      this.successMessage = 'Cont creat cu succes! Se redirecționează la conectare...'
      
      setTimeout(() => {
        this.$router.push('/login')
      }, 2000)
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
