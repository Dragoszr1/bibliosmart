<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="bg-dark py-16 sm:py-24 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-secondary/20 via-transparent to-accent/10"></div>
      <div class="max-w-3xl mx-auto px-6 text-center relative z-10">
        <h2 class="text-3xl sm:text-5xl font-bold text-white mb-3 tracking-tight">Creare Cont</h2>
        <p class="text-white/50 text-sm sm:text-lg font-normal">Alătură-te Bibliotecii astăzi</p>
      </div>
    </section>

    <!-- Signup Form -->
    <main class="max-w-md mx-auto px-4 sm:px-6 -mt-8 relative z-10 pb-16">
      <div class="bg-white rounded-2xl shadow-elevated p-6 sm:p-8">
        <!-- Logo -->
        <div class="text-center mb-8">
          <img src="/logo.webp" alt="Biblioteca" class="h-14 w-14 mx-auto mb-3 rounded-xl">
          <h1 class="text-xl font-bold text-dark">Biblioteca</h1>
        </div>

        <!-- STEP 1: credentials -->
        <form v-if="step === 'credentials'" @submit.prevent="handleSignup" class="space-y-5">
          <div>
            <label for="fullName" class="block text-sm font-medium text-gray-600 mb-1.5">Nume Complet</label>
            <input
              id="fullName"
              v-model="form.fullName"
              type="text"
              placeholder="Introdu numele"
              class="input-field"
              required
            >
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-600 mb-1.5">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              placeholder="Introdu email"
              class="input-field"
              required
            >
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-600 mb-1.5">Parolă</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              placeholder="Min 8 caractere"
              class="input-field"
              required
            >
          </div>

          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-600 mb-1.5">Confirmă Parola</label>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              type="password"
              placeholder="Confirmă parola"
              class="input-field"
              required
            >
          </div>

          <label class="flex items-start gap-2 cursor-pointer">
            <input v-model="form.agreeToTerms" type="checkbox" class="w-4 h-4 rounded border-gray-300 text-secondary focus:ring-secondary mt-0.5" required>
            <span class="text-gray-500 text-sm">Accept <a href="#" class="text-secondary hover:underline">Termenii</a> și <a href="#" class="text-secondary hover:underline">Politica</a></span>
          </label>

          <!-- Error -->
          <div v-if="errorMessage" class="bg-red-50 border-l-4 border-accent rounded-lg p-3">
            <p class="text-accent text-sm">{{ errorMessage }}</p>
          </div>

          <!-- Success -->
          <div v-if="successMessage" class="bg-green-50 border-l-4 border-green-500 rounded-lg p-3">
            <p class="text-green-700 text-sm">{{ successMessage }}</p>
          </div>

          <button type="submit" :disabled="loading" class="btn-primary w-full flex items-center justify-center gap-2">
            <i v-if="loading" class="pi pi-spin pi-spinner text-sm"></i>
            {{ loading ? 'Se procesează...' : 'Creare Cont' }}
          </button>
        </form>

        <!-- STEP 2: 2FA code -->
        <form v-else @submit.prevent="handleVerifyCode" class="space-y-5">
          <div class="text-center mb-2">
            <div class="w-12 h-12 rounded-full bg-secondary/10 flex items-center justify-center mx-auto mb-3">
              <i class="pi pi-envelope text-secondary text-xl"></i>
            </div>
            <p class="text-sm text-gray-600">Am trimis un cod de 6 cifre la</p>
            <p class="text-sm font-semibold text-dark">{{ form.email }}</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-600 mb-1.5">Cod de verificare</label>
            <input
              v-model="code"
              type="text"
              inputmode="numeric"
              maxlength="6"
              placeholder="000000"
              class="input-field text-center text-2xl font-mono tracking-[0.5em]"
              autocomplete="one-time-code"
              required
              autofocus
            >
          </div>

          <p class="text-xs text-gray-400 text-center">Codul expiră în 10 minute. Verifică și folderul spam.</p>

          <div v-if="errorMessage" class="bg-red-50 border-l-4 border-accent rounded-lg p-3">
            <p class="text-accent text-sm">{{ errorMessage }}</p>
          </div>
          
          <div v-if="successMessage" class="bg-green-50 border-l-4 border-green-500 rounded-lg p-3">
            <p class="text-green-700 text-sm">{{ successMessage }}</p>
          </div>

          <button type="submit" :disabled="loading || code.length !== 6" class="btn-primary w-full flex items-center justify-center gap-2">
            <i v-if="loading" class="pi pi-spin pi-spinner text-sm"></i>
            {{ loading ? 'Se verifică...' : 'Verifică codul' }}
          </button>

          <button type="button" @click="resetToCredentials" class="w-full text-sm text-gray-400 hover:text-secondary text-center transition-colors">
            Înapoi
          </button>
        </form>

        <p v-if="step === 'credentials'" class="mt-6 text-center text-gray-500 text-sm">
          Ai deja un cont?
          <router-link to="/login" class="text-secondary hover:text-secondary/80 font-semibold">Conectare</router-link>
        </p>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'Signup',
  data() {
    return {
      step: 'credentials',
      form: {
        fullName: '',
        email: '',
        password: '',
        confirmPassword: '',
        agreeToTerms: false
      },
      code: '',
      tempToken: '',
      errorMessage: '',
      successMessage: '',
      loading: false
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

      this.loading = true
      try {
        const response = await fetch('/api/auth/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify({
            user: this.form.fullName,
            email: this.form.email,
            password: this.form.password
          })
        })

        const data = await response.json()
        if (response.ok && data.step === 'verify') {
          this.tempToken = data.temp_token
          this.step = 'verify'
          this.successMessage = data.message || 'Cod trimis.'
        } else {
          this.errorMessage = data.message || 'Eroare la înregistrare'
        }
      } catch (error) {
        this.errorMessage = 'Eroare de rețea. Încearcă din nou.'
      } finally {
        this.loading = false
      }
    },
    async handleVerifyCode() {
      this.errorMessage = ''
      this.successMessage = ''
      this.loading = true
      try {
        const res = await fetch('/api/auth/verify-register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({ temp_token: this.tempToken, code: this.code })
        })
        const data = await res.json()
        if (res.ok) {
          this.successMessage = 'Cont creat cu succes! Te redirecționăm la autentificare...'
          setTimeout(() => {
            this.$router.push('/login')
          }, 2000)
        } else {
          this.errorMessage = data.message || 'Cod incorect'
          this.code = ''
        }
      } catch {
        this.errorMessage = 'Eroare de rețea. Încearcă din nou.'
      } finally {
        this.loading = false
      }
    },
    resetToCredentials() {
      this.step = 'credentials'
      this.code = ''
      this.tempToken = ''
      this.errorMessage = ''
      this.successMessage = ''
    }
  }
}
</script>

<style scoped>
</style>
