<template>
  <div>
    <!-- Floating Button -->
    <button
      @click="open = !open"
      class="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-secondary shadow-elevated flex items-center justify-center hover:bg-secondary/90 transition-all duration-200 hover:scale-110"
      title="Asistent AI"
    >
      <i :class="open ? 'pi pi-times' : 'pi pi-comments'" class="text-white text-xl"></i>
    </button>

    <!-- Chat Window -->
    <transition name="chat-slide">
      <div
        v-if="open"
        class="fixed bottom-24 right-6 z-50 w-[340px] sm:w-[380px] bg-white rounded-2xl shadow-modal border border-gray-100 flex flex-col"
        style="max-height: 520px;"
      >
        <!-- Header -->
        <div class="bg-dark rounded-t-2xl px-4 py-3 flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-secondary/20 flex items-center justify-center flex-shrink-0">
            <i class="pi pi-star text-secondary text-sm"></i>
          </div>
          <div>
            <p class="text-white text-sm font-semibold leading-tight">Asistent Bibliotecă</p>
            <p class="text-white/40 text-xs">Alimentat de Gemini AI</p>
          </div>
        </div>

        <!-- Messages -->
        <div ref="msgContainer" class="flex-1 overflow-y-auto p-4 space-y-3" style="min-height:200px;">
          <!-- Welcome message -->
          <div class="flex gap-2">
            <div class="w-7 h-7 rounded-full bg-secondary/10 flex items-center justify-center flex-shrink-0 mt-0.5">
              <i class="pi pi-star text-secondary text-xs"></i>
            </div>
            <div class="bg-cream rounded-2xl rounded-tl-none px-3 py-2 max-w-[85%]">
              <p class="text-dark text-xs leading-relaxed">Salut! Sunt asistentul bibliotecii. Te pot ajuta să găsești cărți, să afli disponibilitatea lor sau orice altceva legat de bibliotecă. 📚</p>
            </div>
          </div>

          <!-- Chat history -->
          <div v-for="(msg, i) in messages" :key="i">
            <!-- User message -->
            <div v-if="msg.role === 'user'" class="flex justify-end">
              <div class="bg-secondary text-white rounded-2xl rounded-tr-none px-3 py-2 max-w-[85%]">
                <p class="text-xs leading-relaxed">{{ msg.text }}</p>
              </div>
            </div>
            <!-- AI message -->
            <div v-else class="flex gap-2">
              <div class="w-7 h-7 rounded-full bg-secondary/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                <i class="pi pi-star text-secondary text-xs"></i>
              </div>
              <div class="bg-cream rounded-2xl rounded-tl-none px-3 py-2 max-w-[85%]">
                <p class="text-dark text-xs leading-relaxed whitespace-pre-line">{{ msg.text }}</p>
              </div>
            </div>
          </div>

          <!-- Typing indicator -->
          <div v-if="loading" class="flex gap-2">
            <div class="w-7 h-7 rounded-full bg-secondary/10 flex items-center justify-center flex-shrink-0">
              <i class="pi pi-star text-secondary text-xs"></i>
            </div>
            <div class="bg-cream rounded-2xl rounded-tl-none px-3 py-2">
              <div class="flex gap-1 items-center h-4">
                <span class="w-1.5 h-1.5 bg-secondary/50 rounded-full animate-bounce" style="animation-delay:0ms"></span>
                <span class="w-1.5 h-1.5 bg-secondary/50 rounded-full animate-bounce" style="animation-delay:150ms"></span>
                <span class="w-1.5 h-1.5 bg-secondary/50 rounded-full animate-bounce" style="animation-delay:300ms"></span>
              </div>
            </div>
          </div>
        </div>

        <!-- Input -->
        <div class="p-3 border-t border-gray-100">
          <form @submit.prevent="sendMessage" class="flex gap-2">
            <input
              v-model="input"
              :disabled="loading"
              type="text"
              placeholder="Scrie un mesaj..."
              class="flex-1 text-xs px-3 py-2 rounded-xl border border-gray-200 focus:outline-none focus:border-secondary/50 bg-cream placeholder-gray-400 disabled:opacity-50"
            >
            <button
              type="submit"
              :disabled="loading || !input.trim()"
              class="w-9 h-9 rounded-xl bg-secondary hover:bg-secondary/90 flex items-center justify-center flex-shrink-0 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              <i class="pi pi-send text-white text-xs"></i>
            </button>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'AiChat',
  data() {
    return {
      open: false,
      input: '',
      loading: false,
      messages: []
    }
  },
  watch: {
    messages() {
      this.$nextTick(() => {
        const c = this.$refs.msgContainer
        if (c) c.scrollTop = c.scrollHeight
      })
    }
  },
  methods: {
    async sendMessage() {
      const text = this.input.trim()
      if (!text || this.loading) return
      this.input = ''
      this.messages.push({ role: 'user', text })
      this.loading = true
      try {
        const res = await fetch('/api/ai/chat', {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text })
        })
        const data = await res.json()
        this.messages.push({ role: 'ai', text: data.reply || 'Îmi pare rău, nu am putut răspunde.' })
      } catch {
        this.messages.push({ role: 'ai', text: 'Eroare de rețea. Încearcă din nou.' })
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.chat-slide-enter-active,
.chat-slide-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.chat-slide-enter-from,
.chat-slide-leave-to {
  opacity: 0;
  transform: translateY(12px) scale(0.97);
}
</style>
