<template>
  <div class="min-h-screen bg-base">
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
            <i class="pi pi-plus text-xs"></i> Propune Thread
          </button>
        </div>
      </div>

      <!-- Threads Feed -->
      <div class="space-y-6">
        <div
          v-for="thread in dummyThreads"
          :key="thread.id"
          class="bg-white rounded-2xl shadow-card border border-gray-100 p-5 sm:p-6"
        >
          <!-- Thread Header -->
          <div class="flex items-start justify-between gap-3">
            <div class="flex-1 min-w-0">
              <div class="flex flex-wrap items-center gap-2 mb-2">
                <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-gray-100 text-gray-600">
                  <i class="pi pi-tag text-[9px]"></i> {{ thread.tag }}
                </span>
                <span class="text-xs text-gray-400 flex items-center gap-1">
                  <i class="pi pi-clock text-[10px]"></i> {{ thread.timeAgo }}
                </span>
              </div>
              <h3 class="text-lg sm:text-xl font-bold text-dark leading-snug cursor-pointer hover:text-secondary transition-colors" @click="openThreadModal(thread)">
                {{ thread.title }}
              </h3>
              <p class="text-sm text-gray-600 mt-2 whitespace-pre-line leading-relaxed line-clamp-3">
                {{ thread.content }}
              </p>
            </div>
          </div>

          <!-- Thread Footer (Author & Action) -->
          <div class="mt-5 flex items-center justify-between border-t border-gray-50 pt-4">
            <div class="flex items-center gap-2 cursor-pointer group">
              <div class="w-8 h-8 rounded-full bg-secondary/10 flex items-center justify-center text-secondary text-xs font-bold uppercase group-hover:bg-secondary group-hover:text-white transition-colors">
                {{ thread.author.charAt(0) }}
              </div>
              <div>
                <p class="text-sm font-semibold text-dark group-hover:text-secondary transition-colors">{{ thread.author }}</p>
                <p class="text-[10px] text-gray-400">Membru Club</p>
              </div>
            </div>
            
            <button
              @click="openThreadModal(thread)"
              class="px-4 py-2 bg-gray-50 hover:bg-gray-100 text-dark font-semibold rounded-lg text-sm transition-colors flex items-center gap-2"
            >
              <i class="pi pi-comments text-secondary text-xs"></i>
              <span>{{ thread.commentsCount }} comentarii</span>
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
          <h2 class="text-lg font-bold text-dark truncate pr-4">{{ selectedThread.title }}</h2>
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
                {{ selectedThread.author.charAt(0) }}
              </div>
              <div>
                <p class="font-bold text-dark">{{ selectedThread.author }}</p>
                <p class="text-xs text-gray-500">{{ selectedThread.timeAgo }} • <span class="bg-gray-100 px-1.5 py-0.5 rounded text-[10px]">{{ selectedThread.tag }}</span></p>
              </div>
            </div>
            <p class="text-gray-800 whitespace-pre-line text-sm sm:text-base leading-relaxed">{{ selectedThread.content }}</p>
          </div>

          <!-- Comments Section -->
          <h3 class="font-bold text-dark mb-5 text-lg flex items-center gap-2">
            <i class="pi pi-comments text-secondary"></i> Comentarii ({{ selectedThread.commentsCount }})
          </h3>

          <div class="space-y-6">
            <!-- Parent Comment -->
            <div v-for="comment in dummyComments" :key="comment.id" class="flex gap-3 sm:gap-4">
              <div class="flex-shrink-0 w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 text-xs font-bold">
                {{ comment.author.charAt(0) }}
              </div>
              <div class="flex-1 min-w-0">
                <div class="bg-gray-50 p-3 sm:p-4 rounded-2xl rounded-tl-none border border-gray-100">
                  <div class="flex items-center justify-between gap-2 mb-1">
                    <span class="text-sm font-bold text-dark">{{ comment.author }}</span>
                    <span class="text-[10px] text-gray-400">{{ comment.timeAgo }}</span>
                  </div>
                  <p class="text-sm text-gray-700">{{ comment.content }}</p>
                </div>
                
                <!-- Comment Actions -->
                <div class="flex items-center gap-4 mt-1.5 ml-2">
                  <button class="text-xs font-semibold text-gray-500 hover:text-secondary transition-colors">Răspunde</button>
                  <button class="text-xs font-semibold text-gray-500 hover:text-red-500 transition-colors flex items-center gap-1"><i class="pi pi-heart text-[10px]"></i> {{ comment.likes }}</button>
                </div>

                <!-- Sub-comments (Replies) -->
                <div v-if="comment.replies && comment.replies.length > 0" class="mt-4 space-y-4 relative before:absolute before:left-[-17px] sm:before:left-[-25px] before:top-0 before:bottom-0 before:w-px before:bg-gray-200 ml-4 sm:ml-6">
                  <div v-for="reply in comment.replies" :key="reply.id" class="flex gap-3 relative before:absolute before:left-[-17px] sm:before:left-[-25px] before:top-4 before:w-3 sm:before:w-5 before:h-px before:bg-gray-200">
                    <div class="flex-shrink-0 w-6 h-6 rounded-full bg-amber-100 flex items-center justify-center text-amber-700 text-[10px] font-bold">
                      {{ reply.author.charAt(0) }}
                    </div>
                    <div class="flex-1 min-w-0">
                      <div class="bg-gray-50 p-2.5 sm:p-3 rounded-2xl rounded-tl-none border border-gray-100">
                        <div class="flex items-center justify-between gap-2 mb-1">
                          <span class="text-xs font-bold text-dark">{{ reply.author }}</span>
                          <span class="text-[10px] text-gray-400">{{ reply.timeAgo }}</span>
                        </div>
                        <p class="text-xs text-gray-700"><span class="text-secondary font-semibold">@{{ comment.author }}</span> {{ reply.content }}</p>
                      </div>
                      <div class="flex items-center gap-4 mt-1 ml-2">
                        <button class="text-[11px] font-semibold text-gray-500 hover:text-secondary transition-colors">Răspunde</button>
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
                rows="2" 
                placeholder="Adaugă un comentariu la discuție..." 
                class="w-full text-sm border border-gray-200 rounded-xl px-3 py-2 bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-secondary/40 resize-none custom-scrollbar"
              ></textarea>
              <div class="flex justify-end">
                <button class="px-5 py-2 bg-secondary hover:bg-secondary/90 text-white font-semibold rounded-lg text-sm transition-all flex items-center gap-2">
                  <i class="pi pi-send text-xs"></i> Postează
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Request Thread Modal (Placeholder) -->
    <div v-if="addModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm px-4" @click.self="addModalOpen = false">
      <div class="w-full max-w-lg bg-white rounded-2xl shadow-modal p-6">
         <div class="flex items-center justify-between mb-5">
          <h2 class="text-lg font-bold text-dark flex items-center gap-2">
            <i class="pi pi-plus-circle text-secondary"></i> Propune un Thread
          </h2>
          <button @click="addModalOpen = false" class="text-gray-400 hover:text-secondary text-2xl font-bold leading-none">&times;</button>
        </div>
        <p class="text-sm text-gray-500 mb-5">Thread-ul tău va fi trimis spre moderare. După aprobare de către un bibliotecar, acesta va deveni public.</p>
        
        <div class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-gray-600 mb-1">Titlul discuției</label>
            <input type="text" placeholder="Ex: Teorii despre finalul..." class="w-full text-sm border border-gray-200 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-secondary/40" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-600 mb-1">Conținut / Prima postare</label>
            <textarea rows="4" placeholder="Dezvoltă ideea aici..." class="w-full text-sm border border-gray-200 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-secondary/40 resize-none"></textarea>
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-600 mb-1">Tag (Opțional)</label>
            <input type="text" placeholder="Ex: SF, Harry Potter, Spoiler" class="w-full text-sm border border-gray-200 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-secondary/40" />
          </div>
        </div>

        <div class="flex gap-3 mt-6">
          <button @click="addModalOpen = false" class="flex-1 px-4 py-2.5 border border-gray-200 text-gray-600 font-semibold rounded-xl text-sm hover:bg-gray-50">Anulează</button>
          <button class="flex-1 px-4 py-2.5 bg-secondary hover:bg-secondary/90 text-white font-semibold rounded-xl text-sm">Trimite spre aprobare</button>
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
      addModalOpen: false,
      selectedThread: null,
      
      // Dummy data for skeleton
      dummyThreads: [
        {
          id: 1,
          title: 'Teorii despre finalul romanului Dune',
          content: 'Am terminat de citit prima carte din seria Dune și finalul m-a lăsat cu foarte multe semne de întrebare. Ce credeți că se va întâmpla cu Paul Atreides și cu Fremenii? Vi se pare că transformarea lui a fost prea bruscă?\n\nAș vrea să discutăm despre implicațiile politice din universul creat de Frank Herbert. (Vă rog fără spoilere din Mântuitorul Dunei!)',
          author: 'Alex Popescu',
          timeAgo: 'Acum 2 ore',
          tag: 'Science Fiction',
          commentsCount: 14
        },
        {
          id: 2,
          title: 'Care este personajul vostru preferat din seria Harry Potter?',
          content: 'Facem un scurt sondaj informal. Fiecare să spună personajul preferat și un motiv clar. Incep eu: Severus Snape, pentru că are cel mai complex arc de redempțiune din toată literatura young adult contemporană.',
          author: 'Maria C.',
          timeAgo: 'Acum 1 zi',
          tag: 'Fantasy',
          commentsCount: 32
        },
        {
          id: 3,
          title: 'Recomandări de cărți SF pentru începători',
          content: 'Salutare club! Nu am citit niciodată literatură SF hardcore dar aș vrea să încep. Îmi plac filmele precum Interstellar sau Arrival. Ce cărți, de preferat nu foarte groase, mi-ați recomanda pentru a intra în acest univers?',
          author: 'Vlad M.',
          timeAgo: 'Acum 3 zile',
          tag: 'Recomandări',
          commentsCount: 8
        }
      ],
      
      // Dummy comments for the opened thread
      dummyComments: [
        {
          id: 101,
          author: 'Cristi Dan',
          content: 'Cred că transformarea lui Paul a fost inevitabilă având în vedere expunerea la mirodenie și presiunea pe care o avea pe umeri.',
          timeAgo: 'Acum 1 oră',
          likes: 5,
          replies: [
            {
              id: 201,
              author: 'Alex Popescu',
              content: 'Exact! Deși pe alocuri pare că și-a pierdut umanitatea în favoarea "scopului măreț".',
              timeAgo: 'Acum 45 minute',
              likes: 2
            },
            {
              id: 202,
              author: 'Diana R.',
              content: 'Subscriu la faza cu pierderea umanității. Herbert a descris perfect povara puterii absolute.',
              timeAgo: 'Acum 30 minute',
              likes: 4
            }
          ]
        },
        {
          id: 102,
          author: 'Andrei T.',
          content: 'Eu zic să citești Mântuitorul Dunei, îți va răspunde la jumătate din întrebările astea, iar pentru restul îți va genera altele noi =)))',
          timeAgo: 'Acum 10 minute',
          likes: 8,
          replies: []
        }
      ]
    }
  },
  methods: {
    openAddThreadModal() {
      this.addModalOpen = true
    },
    openThreadModal(thread) {
      this.selectedThread = thread
      // In viitor, aici vom face un fetch call ca sa incarcam comentariile in functie de thread.id
      document.body.style.overflow = 'hidden' // prevent body scrolling
    }
  },
  watch: {
    selectedThread(newVal) {
      if (!newVal) {
        document.body.style.overflow = 'auto' // restore body scrolling
      }
    }
  }
}
</script>

<style scoped>
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
