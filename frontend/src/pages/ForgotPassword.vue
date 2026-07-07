<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="bg-dark py-16 sm:py-24 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-secondary/20 via-transparent to-accent/10"></div>
      <div class="max-w-3xl mx-auto px-6 text-center relative z-10">
        <h2 class="text-3xl sm:text-5xl font-bold text-white mb-3 tracking-tight">Resetare Parolă</h2>
        <p class="text-white/50 text-sm sm:text-lg font-normal">Recuperează accesul la contul tău</p>
      </div>
    </section>

    <main class="max-w-md mx-auto px-4 sm:px-6 -mt-8 relative z-10 pb-16">
      <div class="bg-white rounded-2xl shadow-elevated p-6 sm:p-8">

        <!-- Logo -->
        <div class="text-center mb-8">
          <img src="/logo.webp" alt="Biblioteca" class="h-14 w-14 mx-auto mb-3 rounded-xl">
          <h1 class="text-xl font-bold text-dark">Biblioteca</h1>
        </div>

        <div v-if="successMessage" class="bg-green-50 border-l-4 border-green-500 rounded-lg p-4 mb-6">
          <p class="text-green-700 text-sm font-medium">{{ successMessage }}</p>
          <router-link to="/login" class="inline-block mt-3 text-sm font-semibold text-green-700 hover:text-green-800">Înapoi la conectare</router-link>
        </div>

        <form v-else @submit.prevent="handleSubmit" class="space-y-5">
          <p class="text-gray-600 text-sm mb-4">
            Introdu adresa de email asociată contului tău și îți vom trimite un link pentru resetarea parolei.
          </p>
          
          <div>
            <label class="block text-sm font-medium text-gray-600 mb-1.5">Email</label>
            <input
              v-model="email"
              type="email"
              placeholder="Introdu email-ul tău"
              class="input-field"
              required
            >
          </div>

          <div v-if="errorMessage" class="bg-red-50 border-l-4 border-accent rounded-lg p-3">
            <p class="text-accent text-sm">{{ errorMessage }}</p>
          </div>

          <button type="submit" :disabled="loading" class="btn-primary w-full flex items-center justify-center gap-2">
            <i v-if="loading" class="pi pi-spin pi-spinner text-sm"></i>
            {{ loading ? 'Se trimite...' : 'Trimite link-ul' }}
          </button>
        </form>

        <p v-if="!successMessage" class="mt-6 text-center text-gray-500 text-sm">
          Ți-ai amintit parola?
          <router-link to="/login" class="text-secondary hover:text-secondary/80 font-semibold">Conectare</router-link>
        </p>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'ForgotPassword',
  data() {
    return {
      email: '',
      loading: false,
      errorMessage: '',
      successMessage: ''
    }
  },
  methods: {
    async handleSubmit() {
      this.errorMessage = ''
      this.successMessage = ''
      
      if (!this.email) {
        this.errorMessage = 'Introdu adresa de email.'
        return
      }

      this.loading = true
      try {
        const res = await fetch('/api/auth/forgot-password', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: this.email })
        })
        const data = await res.json()
        
        if (res.ok) {
          this.successMessage = data.message || 'Dacă email-ul există în sistem, vei primi un link pentru resetarea parolei.'
        } else {
          this.errorMessage = data.message || 'A apărut o eroare. Încearcă din nou.'
        }
      } catch (err) {
        this.errorMessage = 'Eroare de rețea. Te rugăm să încerci din nou mai târziu.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
