<template>
  <div class="min-h-screen bg-base relative">
    
    <!-- Toast Notification -->
    <transition name="toast-slide">
      <div v-if="toastMsg" class="fixed top-24 left-0 right-0 z-[100] flex justify-center pointer-events-none">
        <div class="bg-white px-6 py-4 rounded-2xl shadow-xl border-b-4 border-green-500 flex items-center gap-3">
          <i class="pi pi-check-circle text-green-500 text-xl"></i>
          <span class="text-sm font-bold text-dark">{{ toastMsg }}</span>
        </div>
      </div>
    </transition>
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">

      <!-- Header -->
      <div class="mb-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <button @click="$router.push('/club')" class="text-sm text-gray-500 hover:text-secondary mb-2 flex items-center gap-1 transition-colors">
            <i class="pi pi-arrow-left text-xs"></i> Înapoi la Club
          </button>
          <h1 class="text-2xl sm:text-3xl font-bold text-dark flex items-center gap-2">
            <i class="pi pi-comments text-secondary"></i> Toate Discuțiile
          </h1>
          <p class="text-gray-500 text-sm mt-1">Participă la discuțiile comunității sau propune un subiect nou</p>
        </div>
        <div class="flex self-start">
          <button
            @click="openAddThreadModal"
            class="px-5 py-2.5 bg-secondary hover:bg-secondary/90 text-white font-semibold rounded-xl text-sm transition-all flex items-center gap-2 shadow-sm"
          >
            <i class="pi pi-plus text-xs"></i> Propune Discuție
          </button>
        </div>
      </div>

      <!-- Loading / Error -->
      <div v-if="loading" class="text-center py-20 text-gray-400">
        <i class="pi pi-spin pi-spinner text-3xl mb-3 block"></i>
        <p class="text-sm">Se încarcă discuțiile...</p>
      </div>
      <div v-else-if="loadError" class="bg-accent/10 border-l-4 border-accent rounded-xl p-4 text-accent text-sm mb-6">
        {{ loadError }}
      </div>

      <!-- Threads Feed -->
      <div v-else class="space-y-6">
        <div v-if="threads.length === 0" class="text-center py-20 text-gray-400">
          <p class="text-sm">Nicio discuție creată încă.</p>
        </div>
        <div
          v-for="thread in threads"
          :key="thread.thread_id"
          class="bg-white rounded-2xl shadow-card border border-gray-100 p-5 sm:p-6"
        >
          <!-- Thread Header -->
          <div class="flex items-start justify-between gap-3">
            <div class="flex-1 min-w-0">
              <div class="flex flex-wrap items-center gap-2 mb-2">
                <span class="text-xs text-gray-400 flex items-center gap-1">
                  <i class="pi pi-clock text-[10px]"></i> {{ formatDate(thread.creat_la) }}
                </span>
              </div>
              <h3 class="text-lg sm:text-xl font-bold text-dark leading-snug cursor-pointer hover:text-secondary transition-colors" @click="openThreadModal(thread)">
                {{ thread.titlu }}
              </h3>
              <p class="text-sm text-gray-600 mt-2 whitespace-pre-line leading-relaxed line-clamp-3">
                {{ thread.continut }}
              </p>
            </div>
            <button
              v-if="canDeleteThread(thread)"
              @click="deleteThread(thread.thread_id)"
              class="text-gray-300 hover:text-accent text-lg leading-none flex-shrink-0 transition-colors"
              title="Șterge discuția"
            >
              <i class="pi pi-trash"></i>
            </button>
          </div>

          <!-- Thread Footer (Author & Action) -->
          <div class="mt-5 flex items-center justify-between border-t border-gray-50 pt-4">
            <div class="flex items-center gap-2 cursor-pointer group">
              <div class="w-8 h-8 rounded-full bg-secondary/10 flex items-center justify-center text-secondary text-xs font-bold uppercase group-hover:bg-secondary group-hover:text-white transition-colors">
                {{ thread.autor ? thread.autor.charAt(0) : 'U' }}
              </div>
              <div>
                <p class="text-sm font-semibold text-dark group-hover:text-secondary transition-colors">{{ thread.autor }}</p>
                <p class="text-[10px] text-gray-400">Membru Club</p>
              </div>
            </div>
            
            <button
              @click="openThreadModal(thread)"
              class="px-4 py-2 bg-gray-50 hover:bg-gray-100 text-dark font-semibold rounded-lg text-sm transition-colors flex items-center gap-2"
            >
              <i class="pi pi-comments text-secondary text-xs"></i>
              <span>Vezi discuția</span>
            </button>
          </div>
        </div>
      </div>

    </div>

    <!-- Thread Details & Comments Modal -->
    <div v-if="selectedThread" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 sm:p-6" @click.self="selectedThread = null">
      <div class="w-full max-w-3xl max-h-[90vh] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden">
        
        <!-- Modal Header -->
        <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between bg-gray-50">
          <h2 class="text-lg font-bold text-dark truncate pr-4">{{ selectedThread.titlu }}</h2>
          <button @click="selectedThread = null" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-200 text-gray-500 transition-colors">
            <i class="pi pi-times"></i>
          </button>
        </div>

        <!-- Modal Scrollable Content -->
        <div class="flex-1 overflow-y-auto p-6 custom-scrollbar">
          <!-- Main Thread Content inside modal -->
          <div class="mb-8 pb-6 border-b border-gray-100">
            <div class="flex items-center gap-3 mb-4">
               <div class="w-10 h-10 rounded-full bg-secondary/10 flex items-center justify-center text-secondary text-sm font-bold uppercase">
                {{ selectedThread.autor ? selectedThread.autor.charAt(0) : 'U' }}
              </div>
              <div>
                <p class="font-bold text-dark">{{ selectedThread.autor }}</p>
                <p class="text-xs text-gray-500">{{ formatDate(selectedThread.creat_la) }}</p>
              </div>
            </div>
            <p class="text-gray-800 whitespace-pre-line text-sm sm:text-base leading-relaxed">{{ selectedThread.continut }}</p>
          </div>

          <!-- Comments Section -->
          <h3 class="font-bold text-dark mb-5 text-lg flex items-center gap-2">
            <i class="pi pi-comments text-secondary"></i> Comentarii ({{ comments.length }})
          </h3>

          <div v-if="loadingComments" class="text-center py-4 text-gray-400">
            <i class="pi pi-spin pi-spinner text-2xl"></i>
          </div>

          <div v-else class="space-y-6">
            <div v-if="comments.length === 0" class="text-xs text-gray-400 text-center py-2">
              Niciun comentariu încă. Fii primul care adaugă unul!
            </div>
            
            <!-- Parent Comment -->
            <div v-for="comment in comments" :key="comment.comentariu_id" class="flex gap-3 sm:gap-4">
              <div class="flex-shrink-0 w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 text-xs font-bold uppercase">
                {{ comment.autor ? comment.autor.charAt(0) : 'U' }}
              </div>
              <div class="flex-1 min-w-0">
                <div class="bg-gray-50 p-3 sm:p-4 rounded-2xl rounded-tl-none border border-gray-100 group relative">
                  <button
                    v-if="canDeleteComment(comment)"
                    @click="deleteComment(comment.comentariu_id)"
                    class="absolute top-2 right-2 text-gray-300 hover:text-accent text-sm transition-colors opacity-0 group-hover:opacity-100"
                    title="Șterge comentariul"
                  >
                    <i class="pi pi-trash"></i>
                  </button>
                  <div class="flex items-center justify-between gap-2 mb-1 pr-6">
                    <span class="text-sm font-bold text-dark">{{ comment.autor }}</span>
                    <span class="text-[10px] text-gray-400">{{ formatDate(comment.creat_la) }}</span>
                  </div>
                  <p class="text-sm text-gray-700 whitespace-pre-line">{{ comment.continut }}</p>
                </div>
                
                <!-- Comment Actions -->
                <div class="flex items-center gap-4 mt-1.5 ml-2">
                  <button @click="replyTo = replyTo === comment.comentariu_id ? null : comment.comentariu_id" class="text-xs font-semibold text-gray-500 hover:text-secondary transition-colors">Răspunde</button>
                  <button class="text-xs font-semibold text-gray-500 hover:text-red-500 transition-colors flex items-center gap-1"><i class="pi pi-heart text-[10px]"></i> {{ comment.likes }}</button>
                </div>
                
                <!-- Reply Box -->
                <div v-if="replyTo === comment.comentariu_id" class="mt-3 flex gap-2 ml-4">
                  <input
                    v-model="newSubcommentText"
                    @keydown.enter.exact.prevent="submitSubcomment(comment.comentariu_id)"
                    type="text"
                    placeholder="Scrie un răspuns..."
                    class="flex-1 text-xs border border-gray-200 rounded-xl px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-secondary/40"
                  />
                  <button
                    @click="submitSubcomment(comment.comentariu_id)"
                    :disabled="!newSubcommentText.trim()"
                    class="px-3 py-1.5 bg-secondary hover:bg-secondary/90 disabled:opacity-40 text-white rounded-xl text-xs font-semibold transition-all"
                  >
                    Trimite
                  </button>
                </div>

                <!-- Sub-comments (Replies) -->
                <div v-if="comment.subcomments && comment.subcomments.length > 0" class="mt-4 space-y-4 relative before:absolute before:left-[-17px] sm:before:left-[-25px] before:top-0 before:bottom-0 before:w-px before:bg-gray-200 ml-4 sm:ml-6">
                  <div v-for="reply in comment.subcomments" :key="reply.subcomentariu_id" class="flex gap-3 relative before:absolute before:left-[-17px] sm:before:left-[-25px] before:top-4 before:w-3 sm:before:w-5 before:h-px before:bg-gray-200">
                    <div class="flex-shrink-0 w-6 h-6 rounded-full bg-amber-100 flex items-center justify-center text-amber-700 text-[10px] font-bold uppercase">
                      {{ reply.autor ? reply.autor.charAt(0) : 'U' }}
                    </div>
                    <div class="flex-1 min-w-0">
                      <div class="bg-gray-50 p-2.5 sm:p-3 rounded-2xl rounded-tl-none border border-gray-100 group relative">
                        <button
                          v-if="canDeleteSubcomment(reply)"
                          @click="deleteSubcomment(comment.comentariu_id, reply.subcomentariu_id)"
                          class="absolute top-2 right-2 text-gray-300 hover:text-accent text-xs transition-colors opacity-0 group-hover:opacity-100"
                          title="Șterge răspunsul"
                        >
                          <i class="pi pi-trash"></i>
                        </button>
                        <div class="flex items-center justify-between gap-2 mb-1 pr-6">
                          <span class="text-xs font-bold text-dark">{{ reply.autor }}</span>
                          <span class="text-[10px] text-gray-400">{{ formatDate(reply.creat_la) }}</span>
                        </div>
                        <p class="text-xs text-gray-700 whitespace-pre-line"><span class="text-secondary font-semibold">@{{ comment.autor }}</span> {{ reply.continut }}</p>
                      </div>
                      <div class="flex items-center gap-4 mt-1 ml-2">
                        <button class="text-[11px] font-semibold text-gray-500 hover:text-red-500 transition-colors flex items-center gap-1"><i class="pi pi-heart text-[9px]"></i> {{ reply.likes }}</button>
                      </div>
                    </div>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </div>

        <!-- Add Comment Footer -->
        <div class="p-4 sm:p-6 border-t border-gray-100 bg-white">
          <div class="flex gap-3">
            <div class="w-8 h-8 rounded-full bg-gray-200 flex-shrink-0 flex items-center justify-center">
              <i class="pi pi-user text-gray-400 text-xs"></i>
            </div>
            <div class="flex-1 flex flex-col gap-2">
              <textarea 
                v-model="newCommentText"
                rows="2" 
                placeholder="Adaugă un comentariu la discuție..." 
                class="w-full text-sm border border-gray-200 rounded-xl px-3 py-2 bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-secondary/40 resize-none custom-scrollbar"
              ></textarea>
              <div class="flex justify-between items-center">
                <p v-if="commentError" class="text-xs text-accent">{{ commentError }}</p>
                <div v-else></div>
                <button 
                  @click="submitComment"
                  :disabled="!newCommentText.trim() || commentLoading"
                  class="px-5 py-2 bg-secondary hover:bg-secondary/90 disabled:opacity-50 text-white font-semibold rounded-lg text-sm transition-all flex items-center gap-2"
                >
                  <i :class="commentLoading ? 'pi pi-spin pi-spinner' : 'pi pi-send'" class="text-xs"></i> Postează
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Request Thread Modal -->
    <div v-if="addModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm px-4" @click.self="addModalOpen = false">
      <div class="w-full max-w-lg bg-white rounded-2xl shadow-modal p-6">
         <div class="flex items-center justify-between mb-5">
          <h2 class="text-lg font-bold text-dark flex items-center gap-2">
            <i class="pi pi-plus-circle text-secondary"></i> Adaugă o Discuție
          </h2>
          <button @click="addModalOpen = false" class="text-gray-400 hover:text-secondary text-2xl font-bold leading-none">&times;</button>
        </div>
        
        <div class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-gray-600 mb-1">Titlul discuției *</label>
            <input v-model="addForm.titlu" type="text" placeholder="Ex: Teorii despre finalul..." class="w-full text-sm border border-gray-200 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-secondary/40" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-600 mb-1">Conținut / Prima postare *</label>
            <textarea v-model="addForm.continut" rows="4" placeholder="Dezvoltă ideea aici..." class="w-full text-sm border border-gray-200 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-secondary/40 resize-none"></textarea>
          </div>
        </div>

        <p v-if="addError" class="mt-3 text-xs text-accent">{{ addError }}</p>

        <div class="flex gap-3 mt-6">
          <button @click="addModalOpen = false" class="flex-1 px-4 py-2.5 border border-gray-200 text-gray-600 font-semibold rounded-xl text-sm hover:bg-gray-50 transition-colors">Anulează</button>
          <button 
            @click="submitThread" 
            :disabled="!addForm.titlu.trim() || !addForm.continut.trim() || addLoading"
            class="flex-1 px-4 py-2.5 bg-secondary hover:bg-secondary/90 disabled:opacity-50 text-white font-semibold rounded-xl text-sm transition-colors flex items-center justify-center gap-2"
          >
            <i :class="addLoading ? 'pi pi-spin pi-spinner' : 'pi pi-check'" class="text-xs"></i> Postează
          </button>
        </div>
      </div>
    </div>

    <!-- Custom Delete Modal -->
    <div v-if="deleteModal.open" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 backdrop-blur-sm px-4" @click.self="deleteModal.open = false">
      <div class="w-full max-w-sm bg-white rounded-2xl shadow-modal p-6 text-center border border-gray-100">
        <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <i class="pi pi-exclamation-triangle text-red-500 text-3xl"></i>
        </div>
        <h3 class="text-lg font-bold text-dark mb-2">Ești sigur că vrei să ștergi?</h3>
        <p class="text-sm text-gray-500 mb-6">Această acțiune este ireversibilă.</p>
        <div class="flex gap-3">
          <button @click="deleteModal.open = false" class="flex-1 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-dark font-semibold rounded-xl text-sm transition-colors">Nu, anulează</button>
          <button @click="confirmDelete" class="flex-1 px-4 py-2 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-xl text-sm transition-colors">Da, șterge</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'ClubThreads',
  data() {
    return {
      currentUser: null,
      loading: true,
      loadError: '',
      threads: [],
      
      addModalOpen: false,
      addForm: { titlu: '', continut: '' },
      addError: '',
      addLoading: false,
      toastMsg: '',

      selectedThread: null,
      comments: [],
      loadingComments: false,
      
      newCommentText: '',
      commentLoading: false,
      commentError: '',
      
      replyTo: null,
      newSubcommentText: '',
      
      deleteModal: {
        open: false,
        type: null, // 'thread', 'comment', 'subcomment'
        id: null,
        parentId: null
      }
    }
  },
  async mounted() {
    await this.fetchMe()
    await this.fetchThreads()
  },
  methods: {
    async fetchMe() {
      try {
        const res = await fetch('/api/auth/me', { credentials: 'include' })
        if (res.ok) this.currentUser = await res.json()
      } catch { /* ignore */ }
    },
    async fetchThreads() {
      this.loading = true
      this.loadError = ''
      try {
        const res = await fetch('/api/club/threads', { credentials: 'include' })
        if (res.status === 403) {
          this.$router.push('/')
          return
        }
        const data = await res.json()
        if (!res.ok) {
          this.loadError = data.error || 'Eroare la încărcarea discuțiilor.'
        } else {
          this.threads = data.threads || []
          
          if (this.$route.query.id) {
            const targetId = parseInt(this.$route.query.id, 10)
            const targetThread = this.threads.find(t => t.thread_id === targetId)
            if (targetThread) {
              this.openThreadModal(targetThread)
            }
            this.$router.replace({ query: {} })
          }
        }
      } catch (err) {
        this.loadError = 'Eroare de rețea.'
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const d = new Date(dateString)
      return d.toLocaleDateString('ro-RO', { hour: '2-digit', minute: '2-digit', day: '2-digit', month: 'short' })
    },
    openAddThreadModal() {
      this.addForm = { titlu: '', continut: '' }
      this.addError = ''
      this.addModalOpen = true
    },
    async submitThread() {
      this.addError = ''
      this.addLoading = true
      try {
        const res = await fetch('/api/club/threads', {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.addForm)
        })
        const data = await res.json()
        if (!res.ok) {
          this.addError = data.error || 'Eroare la crearea discuției.'
        } else {
          this.addModalOpen = false
          this.toastMsg = data.message
          setTimeout(() => {
            this.toastMsg = ''
          }, 4000)
          await this.fetchThreads()
        }
      } catch (err) {
        this.addError = 'Eroare de rețea.'
      } finally {
        this.addLoading = false
      }
    },
    canDeleteThread(thread) {
      if (!this.currentUser) return false
      return this.currentUser.rol === 'bibliotecar'
    },
    deleteThread(threadId) {
      this.deleteModal = { open: true, type: 'thread', id: threadId, parentId: null }
    },
    async openThreadModal(thread) {
      this.selectedThread = thread
      document.body.style.overflow = 'hidden'
      await this.fetchComments(thread.thread_id)
    },
    async fetchComments(threadId) {
      this.loadingComments = true
      this.comments = []
      try {
        const res = await fetch(`/api/club/threads/${threadId}`, { credentials: 'include' })
        const data = await res.json()
        if (res.ok && data.thread) {
          this.comments = data.thread.comments || []
        }
      } catch (err) { /* ignore */ } finally {
        this.loadingComments = false
      }
    },
    async submitComment() {
      if (!this.newCommentText.trim() || !this.selectedThread) return
      this.commentError = ''
      this.commentLoading = true
      try {
        const res = await fetch(`/api/club/threads/${this.selectedThread.thread_id}/comments`, {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ continut: this.newCommentText })
        })
        const data = await res.json()
        if (!res.ok) {
          this.commentError = data.error || 'Eroare la postare.'
        } else {
          this.newCommentText = ''
          await this.fetchComments(this.selectedThread.thread_id)
        }
      } catch (err) {
        this.commentError = 'Eroare de rețea.'
      } finally {
        this.commentLoading = false
      }
    },
    canDeleteComment(comment) {
      if (!this.currentUser) return false
      return this.currentUser.rol === 'bibliotecar'
    },
    deleteComment(commentId) {
      this.deleteModal = { open: true, type: 'comment', id: commentId, parentId: null }
    },
    async submitSubcomment(commentId) {
      if (!this.newSubcommentText.trim()) return
      try {
        const res = await fetch(`/api/club/threads/comments/${commentId}/subcomments`, {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ continut: this.newSubcommentText })
        })
        if (res.ok) {
          this.replyTo = null
          this.newSubcommentText = ''
          await this.fetchComments(this.selectedThread.thread_id)
        }
      } catch (err) { /* ignore */ }
    },
    canDeleteSubcomment(subcomment) {
      if (!this.currentUser) return false
      return this.currentUser.rol === 'bibliotecar'
    },
    deleteSubcomment(commentId, subcommentId) {
      this.deleteModal = { open: true, type: 'subcomment', id: subcommentId, parentId: commentId }
    },
    async confirmDelete() {
      const { type, id, parentId } = this.deleteModal
      this.deleteModal.open = false
      
      try {
        if (type === 'thread') {
          const res = await fetch(`/api/club/threads/${id}`, { method: 'DELETE', credentials: 'include' })
          if (res.ok) this.threads = this.threads.filter(t => t.thread_id !== id)
        } else if (type === 'comment') {
          const res = await fetch(`/api/club/threads/comments/${id}`, { method: 'DELETE', credentials: 'include' })
          if (res.ok) this.comments = this.comments.filter(c => c.comentariu_id !== id)
        } else if (type === 'subcomment') {
          const res = await fetch(`/api/club/threads/subcomments/${id}`, { method: 'DELETE', credentials: 'include' })
          if (res.ok) {
            const c = this.comments.find(x => x.comentariu_id === parentId)
            if (c) c.subcomments = c.subcomments.filter(s => s.subcomentariu_id !== id)
          }
        }
      } catch (err) { /* ignore */ }
    }
  },
  watch: {
    selectedThread(newVal) {
      if (!newVal) {
        document.body.style.overflow = 'auto'
      }
    }
  }
}
</script>

<style scoped>
.toast-slide-enter-active, .toast-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.toast-slide-enter-from, .toast-slide-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 8px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 8px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
