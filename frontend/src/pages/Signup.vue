<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-secondary via-dark to-accent py-8 sm:py-16 shadow-elegant relative overflow-hidden">
      <div class="absolute inset-0 gradient-overlay opacity-30"></div>
      <div class="max-w-full mx-auto px-3 sm:px-4 text-center relative z-10">
        <h2 class="text-2xl sm:text-4xl font-bold text-gradient mb-2 sm:mb-4 glow-gold">Creare Cont</h2>
        <p class="text-cream text-xs sm:text-lg mb-4 sm:mb-8 opacity-90">Alătură-te Bibliotecii astazi</p>
      </div>
    </section>

    <!-- Signup Form Section -->
    <main class="max-w-full mx-auto px-3 sm:px-4 py-8 sm:py-12">
      <div class="flex justify-center">
        <div class="w-full max-w-md">
          <!-- Signup Card -->
          <div class="bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 p-4 sm:p-8 card-hover">
            <!-- Logo Section -->
            <div class="text-center mb-6 sm:mb-8">
              <img src="/logo.webp" alt="Biblioteca Logo" class="h-16 sm:h-20 w-16 sm:w-20 mx-auto mb-3 sm:mb-4">
              <h1 class="text-2xl sm:text-3xl font-bold text-secondary">Biblioteca</h1>
              <p class="text-gray-500 text-xs sm:text-sm mt-2">Sistem de Gestiune a Bibliotecii</p>
            </div>

            <!-- Signup Form -->
            <form @submit.prevent="handleSignup" class="space-y-4 sm:space-y-5">
              <!-- Full Name Field -->
              <div>
                <label for="fullName" class="block text-dark font-semibold mb-2 text-sm sm:text-base">
                  Nume Complet
                </label>
                <input
                  id="fullName"
                  v-model="form.fullName"
                  type="text"
                  placeholder="Introdu numele"
                  class="w-full px-3 sm:px-4 py-2 sm:py-3 rounded-lg bg-cream-dark border-2 border-secondary/30 text-dark placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary/50 transition-all duration-200 text-xs sm:text-base"
                  required
                >
              </div>

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
                  placeholder="Creia o parolă puternică"
                  class="w-full px-3 sm:px-4 py-2 sm:py-3 rounded-lg bg-cream-dark border-2 border-secondary/30 text-dark placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary/50 transition-all duration-200 text-xs sm:text-base"
                  required
                >
                <p class="text-xs text-gray-500 mt-1 sm:mt-2">Min 8 caractere</p>
              </div>

              <!-- Confirm Password Field -->
              <div>
                <label for="confirmPassword" class="block text-dark font-semibold mb-2 text-sm sm:text-base">
                  Confirmă Parola
                </label>
                <input
                  id="confirmPassword"
                  v-model="form.confirmPassword"
                  type="password"
                  placeholder="Confirmă parola"
                  class="w-full px-3 sm:px-4 py-2 sm:py-3 rounded-lg bg-cream-dark border-2 border-secondary/30 text-dark placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-secondary/50 transition-all duration-200 text-xs sm:text-base"
                  required
                >
              </div>

              <!-- Terms & Conditions -->
              <div class="flex items-start gap-2">
                <input
                  id="terms"
                  v-model="form.agreeToTerms"
                  type="checkbox"
                  class="w-4 h-4 rounded border-secondary text-secondary focus:ring-secondary mt-1"
                  required
                >
                <label for="terms" class="text-gray-700 text-xs sm:text-sm">
                  Accept
                  <a href="#" class="text-secondary hover:text-accent">Termenii</a>
                  și
                  <a href="#" class="text-secondary hover:text-accent">Politica</a>
                </label>
              </div>

              <!-- Error Message -->
              <div v-if="errorMessage" class="bg-accent/10 border-l-4 border-accent rounded-lg p-3 sm:p-4">
                <p class="text-accent text-xs sm:text-sm">{{ errorMessage }}</p>
              </div>

              <!-- Success Message -->
              <div v-if="successMessage" class="bg-green-50 border-l-4 border-green-500 rounded-lg p-3 sm:p-4">
                <p class="text-green-700 text-xs sm:text-sm">{{ successMessage }}</p>
              </div>

              <!-- Signup Button -->
              <button
                type="submit"
                class="w-full bg-gradient-to-r from-secondary to-accent hover:shadow-lg text-white font-bold py-3 px-4 rounded-lg transition-all duration-300 transform hover:scale-105"
              >
                Creare Cont
              </button>
            </form>

            <!-- Sign In Link -->
            <div class="mt-8 text-center">
              <p class="text-gray-600">
                Ai deja un cont?
                <router-link to="/login" class="text-secondary hover:text-accent font-bold transition-colors duration-200">
                  Conectare
                </router-link>
              </p>
            </div>
          </div>

          <!-- Security Info -->
          <div class="mt-8 bg-cream rounded-lg shadow-elegant border-2 border-secondary/60 p-6">
            <h3 class="text-dark font-bold mb-4 flex items-center gap-2">
              <i class="pi pi-shield text-secondary"></i> Datele Tale sunt în Siguranță
            </h3>
            <ul class="space-y-2 text-gray-700 text-sm">
              <li class="flex items-start gap-2">
                <i class="pi pi-check text-accent"></i>
                <span>Parola ta este criptată și niciodală partajată</span>
              </li>
              <li class="flex items-start gap-2">
                <i class="pi pi-check text-accent"></i>
                <span>Respectăm reglementatiile de protecție a datelor</span>
              </li>
              <li class="flex items-start gap-2">
                <i class="pi pi-check text-accent"></i>
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

      try {
        const response = await fetch('/api/auth/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user: this.form.fullName,
            email: this.form.email,
            password: this.form.password
          })
        })

        const data = await response.json()
        if (response.ok) {
          this.successMessage = 'Cont creat cu succes! Se redirecționează la conectare...'
          setTimeout(() => {
            this.$router.push('/login')
          }, 2000)
        } else {
          this.errorMessage = data.message || 'Eroare la înregistrare'
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
