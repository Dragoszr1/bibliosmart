<template>
  <div id="app" class="min-h-screen bg-cream flex flex-col">
    <Navbar />
    <div class="flex-1">
      <router-view />
    </div>
    <footer class="bg-dark border-t border-white/5 py-8 mt-auto">
      <div class="max-w-7xl mx-auto px-6 text-center">
        <p class="text-white/40 text-sm">© 2026 Biblioteca — Sistem Școlar</p>
      </div>
    </footer>
    <AiChat />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import AiChat from './components/AiChat.vue'

export default {
  name: 'App',
  components: {
    Navbar,
    AiChat
  }
}
</script>

<style scoped>
</style>
