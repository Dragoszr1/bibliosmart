<template>
  <div id="app" class="min-h-screen bg-gradient-to-b from-white to-gray-200">
    <!-- Bare de navigare globală -->
    <Navbar />

    <!-- Vizualizare rutieră -->
    <router-view />

    <!-- Subsol -->
    <footer class="bg-dark border-t-2 border-secondary/40 mt-16 py-8">
      <div class="max-w-7xl mx-auto px-4 text-center">
        <p class="text-cream/70 text-sm mb-1">© 2026 Sistemul de Gestiune a Bibliotecii Școlii</p>
        <p class="text-cream/50 text-xs">Construind o comunitate de cititori și învățători</p>
      </div>
    </footer>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'

export default {
  name: 'App',
  components: {
    Navbar
  }
}
</script>

<style scoped>
</style>
